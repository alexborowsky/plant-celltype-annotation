#!/usr/bin/env python3
"""Build a gene-activity AnnData from a single-nucleus ATAC object, for use with the skill's RNA scripts.

Each gene's window is its body plus --upstream bp before the TSS (and --downstream bp after the TES),
strand-aware. Two inputs:

  peaks (default)   sum each nucleus's region counts over the regions that overlap the window
                    (a region overlapping two windows counts for both). Fast; a gene with no overlapping
                    region cannot be measured (var['measurable'] = False), which is not the same as "off".
  --fragments       count Tn5 insertions (both fragment ends; --count insertions) or fragments
                    (--count fragments) inside the window, streamed from fragment files. Closer to Signac
                    GeneActivity / ArchR gene scores; every gene is measurable, but genes in closed
                    chromatin only collect background.

Output h5ad (obs_names, obs, obsm, obsp and uns copied from the input, so clusters and UMAP are identical):
  X = log1p(counts / total * 1e4)   layers['counts'] = raw counts (float32)
  var: chrom, start, end, strand (window, 0-based half-open), gene_name, n_regions (input regions overlapping
       the window), frac_detected, measurable
  obs: n_gene_activity_counts, n_genes_active
  uns['gene_activity']: parameters
Unmeasurable gene IDs are written to <out>.unmeasurable_genes.txt.

Region coordinates come from var chrom/start/end or from var_names like chr1:100-600 / chr1-100-600 /
chr1_100_600 (taken as 0-based half-open, BED-style). GFF3/GTF coordinates are 1-based inclusive.

Barcodes for --fragments: each file's barcodes are matched to obs as (sample, barcode) using obs
--barcode-column (default barcode_raw) and --sample-column (default sample); the sample of each file is
--fragment-samples, or the obs sample name found in the file name (longest match). Without those columns,
obs_names are built with --barcode-template (default "{sample}_{barcode}"). --barcode-map TSV (columns
barcode, obs_name and optionally sample) overrides both. A trailing "-1" is tolerated on either side.

Example:
  python gene_activity.py --h5ad atac.h5ad --gff genes.gff3.gz --out gene_activity.h5ad
  python gene_activity.py --h5ad atac.h5ad --gff genes.gff3.gz --out gene_activity.h5ad \
      --fragments frag/rep1_fragments.tsv.gz frag/rep2_fragments.tsv.gz
"""
import argparse
import gzip
import os
import re
import sys

import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp


def opener(path):
    return gzip.open(path, 'rt') if path.endswith('.gz') else open(path)


def read_genes(path, features, id_attr, up, down):
    rows = []
    fmt = None
    with opener(path) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            p = line.rstrip('\n').split('\t')
            if len(p) < 9 or p[2] not in features:
                continue
            if fmt is None:
                fmt = 'gtf' if re.search(r'\w+ "', p[8]) and '=' not in p[8].split(';')[0] else 'gff3'
            if fmt == 'gff3':
                attr = dict(kv.split('=', 1) for kv in p[8].strip().strip(';').split(';') if '=' in kv)
                gid = attr.get(id_attr or 'ID')
                name = attr.get('Name', attr.get('gene_name', ''))
            else:
                attr = dict(m.groups() for m in re.finditer(r'(\S+) "([^"]*)"', p[8]))
                gid = attr.get(id_attr or 'gene_id')
                name = attr.get('gene_name', '')
            if not gid:
                continue
            gid = re.sub(r'^gene[:-]', '', gid)
            s, e, strand = int(p[3]) - 1, int(p[4]), p[6]
            if strand == '-':
                s, e = max(0, s - down), e + up
            else:
                s, e = max(0, s - up), e + down
            rows.append((gid, p[0], s, e, strand, name))
    g = pd.DataFrame(rows, columns=['gene_id', 'chrom', 'start', 'end', 'strand', 'gene_name'])
    n = len(g)
    g = g.drop_duplicates('gene_id').reset_index(drop=True)
    if n > len(g):
        print(f'NOTE {n - len(g)} duplicate gene IDs in the annotation: kept the first')
    if g.empty:
        raise SystemExit(f'no {"/".join(features)} features with an ID in {path} (try --feature / --gene-id-attr)')
    print(f'{len(g):,} genes from {os.path.basename(path)} ({fmt}); window = body + {up} bp upstream'
          + (f' + {down} bp downstream' if down else ''))
    named = g['gene_name'].astype(str).str.len() > 0
    if id_attr is None and named.mean() > 0.9 and (g.loc[named, 'gene_name'] != g.loc[named, 'gene_id']).mean() > 0.9:
        print(f'NOTE gene IDs look like {g["gene_id"].iat[0]} and Names like {g["gene_name"].iat[0]}: the var names '
              'must match the protein FASTA / marker gene map IDs; use --gene-id-attr Name if those use the Name form')
    return g


def region_table(a):
    v = a.var
    if {'chrom', 'start', 'end'} <= set(v.columns):
        r = pd.DataFrame({'chrom': v['chrom'].astype(str).values, 'start': v['start'].astype(np.int64).values,
                          'end': v['end'].astype(np.int64).values})
    else:
        m = pd.Series(a.var_names).str.extract(r'^(.+?)[:_-](\d+)[-_](\d+)$')
        if m.isna().any(axis=None):
            bad = a.var_names[m.isna().any(axis=1).values][:3].tolist()
            raise SystemExit(f'var has no chrom/start/end and names like {bad} are not chr:start-end')
        r = pd.DataFrame({'chrom': m[0].values, 'start': m[1].astype(np.int64).values,
                          'end': m[2].astype(np.int64).values})
    return r


def harmonize_chroms(reg_chroms, genes):
    """Match the annotation's chromosome names to the data's (adds/strips chr/Chr prefixes if that helps)."""
    have = set(reg_chroms)
    ok = genes['chrom'].isin(have).mean()
    if ok >= 0.5:
        return genes
    best, best_ok = None, ok
    for f in (lambda c: re.sub(r'^(chr|Chr|CHR)', '', c), lambda c: 'chr' + c, lambda c: 'Chr' + c,
              lambda c: 'chr' + re.sub(r'^(chr|Chr|CHR)', '', c), lambda c: 'Chr' + re.sub(r'^(chr|Chr|CHR)', '', c)):
        cand = genes['chrom'].map(f)
        if cand.isin(have).mean() > best_ok:
            best, best_ok = cand, cand.isin(have).mean()
    if best is not None:
        print(f'NOTE renamed annotation chromosomes to match the data ({ok:.0%} -> {best_ok:.0%} of genes)')
        genes = genes.assign(chrom=best.values)
    return genes


class Segments:
    """Per chromosome: elementary segments between window boundaries and the genes covering each (CSR)."""

    def __init__(self, genes):
        self.chrom = {}
        for chrom, d in genes.groupby('chrom'):
            b = np.unique(np.concatenate([d['start'].values, d['end'].values]))
            i0 = np.searchsorted(b, d['start'].values)
            i1 = np.searchsorted(b, d['end'].values)
            lens = i1 - i0
            seg = np.concatenate([np.arange(x, y) for x, y in zip(i0, i1)]) if len(d) else np.zeros(0, int)
            gid = np.repeat(d.index.values, lens)
            o = np.argsort(seg, kind='stable')
            seg, gid = seg[o], gid[o]
            indptr = np.searchsorted(seg, np.arange(len(b) + 1))
            self.chrom[chrom] = (b, indptr, gid)

    def lookup(self, chrom, pos):
        """For positions on one chromosome: (index of position, gene) pairs for every covering gene."""
        if chrom not in self.chrom:
            return np.zeros(0, np.int64), np.zeros(0, np.int64)
        b, indptr, gid = self.chrom[chrom]
        k = np.searchsorted(b, pos, side='right') - 1
        k = np.where((k >= 0) & (k < len(b) - 1), k, len(b) - 1)  # last boundary has no genes
        lo, hi = indptr[k], indptr[k + 1]
        n = hi - lo
        has = n > 0
        if not has.any():
            return np.zeros(0, np.int64), np.zeros(0, np.int64)
        idx = np.repeat(np.nonzero(has)[0], n[has])
        off = np.arange(len(idx)) - np.repeat(np.cumsum(n[has]) - n[has], n[has])
        return idx, gid[np.repeat(lo[has], n[has]) + off]

    def overlaps(self, chrom, start, end):
        """For intervals on one chromosome: (interval index, gene) pairs for every gene window overlapping it."""
        if chrom not in self.chrom:
            return np.zeros(0, np.int64), np.zeros(0, np.int64)
        b, indptr, gid = self.chrom[chrom]
        k0 = np.maximum(np.searchsorted(b, start, side='right') - 1, 0)
        k1 = np.searchsorted(b, end, side='left')  # segments k0..k1-1 intersect [start, end)
        k1 = np.minimum(k1, len(b) - 1)
        n = np.maximum(k1 - k0, 0)
        ii = np.repeat(np.arange(len(start)), n)
        kk = np.repeat(k0, n) + (np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n))
        lo, hi = indptr[kk], indptr[kk + 1]
        m = hi - lo
        i2 = np.repeat(ii, m)
        g2 = gid[np.repeat(lo, m) + (np.arange(m.sum()) - np.repeat(np.cumsum(m) - m, m))]
        pairs = np.unique(np.stack([i2, g2], 1), axis=0) if len(i2) else np.zeros((0, 2), np.int64)
        return pairs[:, 0], pairs[:, 1]


def overlap_matrix(reg, genes, segs):
    rows, cols = [], []
    for chrom, idx in reg.groupby('chrom').indices.items():
        i, g = segs.overlaps(chrom, reg['start'].values[idx], reg['end'].values[idx])
        rows.append(idx[i]); cols.append(g)
    r = np.concatenate(rows) if rows else np.zeros(0, int)
    c = np.concatenate(cols) if cols else np.zeros(0, int)
    return sp.csr_matrix((np.ones(len(r), np.float32), (r, c)), shape=(len(reg), len(genes)))


def strip1(x):
    return re.sub(r'-1$', '', str(x))


def barcode_index(a, args, files):
    """Per fragment file: dict barcode -> obs row."""
    n = a.n_obs
    obs_pos = pd.Series(np.arange(n), index=a.obs_names)
    samples = args.fragment_samples or [None] * len(files)
    if len(samples) != len(files):
        raise SystemExit('--fragment-samples must give one sample per fragment file')
    if args.barcode_map:
        m = pd.read_csv(args.barcode_map, sep='\t', dtype=str)
        if not {'barcode', 'obs_name'} <= set(m.columns):
            raise SystemExit('--barcode-map needs columns barcode, obs_name (and optionally sample)')
        m = m[m['obs_name'].isin(obs_pos.index)]
    have_cols = args.sample_column in a.obs and args.barcode_column in a.obs
    obs_samples = sorted(a.obs[args.sample_column].astype(str).unique(), key=len, reverse=True) \
        if args.sample_column in a.obs else []
    out = []
    for f, s in zip(files, samples):
        if s is None and obs_samples:
            base = os.path.basename(f)
            hit = [x for x in obs_samples if x in base]
            s = hit[0] if hit else None
        if args.barcode_map:
            mm = m if 'sample' not in m.columns or s is None else m[m['sample'].astype(str) == s]
            d = dict(zip(mm['barcode'].map(strip1), obs_pos[mm['obs_name']].values))
        elif have_cols:
            sel = np.ones(n, bool) if s is None else (a.obs[args.sample_column].astype(str).values == s)
            if s is None and len(files) > 1:
                print(f'WARN could not tell the sample of {f}: matching its barcodes against all nuclei')
            d = dict(zip(a.obs[args.barcode_column].astype(str).map(strip1).values[sel], np.nonzero(sel)[0]))
        else:
            if s is None and '{sample}' in args.barcode_template:
                raise SystemExit(f'cannot tell the sample of {f}: give --fragment-samples')
            pat = re.escape(args.barcode_template).replace(r'\{sample\}', re.escape(s or '')) \
                .replace(r'\{barcode\}', '(.+)')
            core = pd.Series(a.obs_names).str.extract('^' + pat + '$')[0]
            ok = core.notna().values
            d = dict(zip(core[ok].map(strip1), np.nonzero(ok)[0]))
        out.append((f, s, d))
    return out


def count_fragments(a, genes, segs, args):
    files = barcode_index(a, args, args.fragments)
    M = sp.csr_matrix((a.n_obs, len(genes)), dtype=np.float32)
    seen = np.zeros(a.n_obs, bool)
    for f, s, d in files:
        nfr = nkeep = 0
        bcs = None
        for ch in pd.read_csv(f, sep='\t', header=None, comment='#', usecols=[0, 1, 2, 3],
                              names=['chrom', 'start', 'end', 'bc'], chunksize=args.chunksize,
                              dtype={'chrom': str, 'start': np.int64, 'end': np.int64, 'bc': str}):
            nfr += len(ch)
            if bcs is None:
                bcs = ch['bc'].head(1000)
            ci = ch['bc'].map(strip1).map(d)
            ok = ci.notna().values
            ch = ch[ok]
            ci = ci[ok].astype(np.int64).values
            nkeep += len(ch)
            seen[ci] = True
            rows, cols = [], []
            for chrom, idx in ch.groupby('chrom').indices.items():
                st, en = ch['start'].values[idx], ch['end'].values[idx]
                if args.count == 'insertions':
                    for pos in (st, en - 1):
                        i, g = segs.lookup(chrom, pos)
                        rows.append(ci[idx][i]); cols.append(g)
                else:
                    i1, g1 = segs.lookup(chrom, st)
                    i2, g2 = segs.lookup(chrom, en - 1)
                    pr = np.unique(np.stack([np.concatenate([i1, i2]), np.concatenate([g1, g2])], 1), axis=0)
                    rows.append(ci[idx][pr[:, 0]]); cols.append(pr[:, 1])
            if rows:  # add per chunk: memory stays at one chunk plus the gene x nucleus matrix
                r, c = np.concatenate(rows), np.concatenate(cols)
                M = M + sp.csr_matrix((np.ones(len(r), np.float32), (r, c)), shape=M.shape)
        if nfr and nkeep == 0:
            ex = ', '.join(bcs.astype(str).head(3)) if bcs is not None else ''
            raise SystemExit(f'{f}: no barcode matched any nucleus (sample {s!r}; file barcodes like {ex}). '
                             'Fix --fragment-samples / --barcode-column / --barcode-template / --barcode-map')
        print(f'{os.path.basename(f)} (sample {s}): {nfr:,} fragments, {nkeep:,} from the object\'s nuclei')
    miss = (~seen).sum()
    if miss:
        print(f'WARN {miss:,} of {a.n_obs:,} nuclei have no fragments in the given files')
    M.sum_duplicates()
    return M


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True, help='ATAC object: nuclei x regions (peaks or tiles), raw counts')
    p.add_argument('--gff', required=True, help='GFF3 or GTF (.gz ok)')
    p.add_argument('--out', required=True)
    p.add_argument('--feature', nargs='+', default=['gene'], help='feature types to use (default gene)')
    p.add_argument('--gene-id-attr', default=None, help='default ID (GFF3) / gene_id (GTF); "gene:" prefixes are stripped')
    p.add_argument('--upstream', type=int, default=2000)
    p.add_argument('--downstream', type=int, default=0)
    p.add_argument('--counts-layer', default='counts', help='region counts layer (default counts, else X)')
    p.add_argument('--fragments', nargs='+', default=None, help='fragment files (chrom, start, end, barcode, ...)')
    p.add_argument('--count', choices=['insertions', 'fragments'], default='insertions')
    p.add_argument('--fragment-samples', nargs='+', default=None, help='sample of each fragment file, in order')
    p.add_argument('--sample-column', default='sample')
    p.add_argument('--barcode-column', default='barcode_raw')
    p.add_argument('--barcode-template', default='{sample}_{barcode}')
    p.add_argument('--barcode-map', default=None, help='TSV: barcode, obs_name[, sample]')
    p.add_argument('--chunksize', type=int, default=5_000_000)
    args = p.parse_args()

    a = ad.read_h5ad(args.h5ad)
    print(f'{args.h5ad}: {a.n_obs:,} nuclei x {a.n_vars:,} regions')
    genes = read_genes(args.gff, set(args.feature), args.gene_id_attr, args.upstream, args.downstream)
    reg = region_table(a)
    genes = harmonize_chroms(reg['chrom'].unique(), genes)
    on = reg['chrom'].isin(set(genes['chrom'])).mean()
    print(f'{on:.1%} of regions are on chromosomes that carry annotated genes')
    if on < 0.5:
        ex = ', '.join(reg['chrom'].unique()[:3])
        exg = ', '.join(genes['chrom'].unique()[:3])
        raise SystemExit(f'chromosome names do not match (data {ex}; annotation {exg})')
    segs = Segments(genes)
    O = overlap_matrix(reg, genes, segs)
    n_regions = np.asarray(O.sum(0)).ravel().astype(int)

    if args.fragments:
        M = count_fragments(a, genes, segs, args)
        mode = f'fragments ({args.count})'
    else:
        X = a.layers[args.counts_layer] if args.counts_layer in a.layers else a.X
        X = sp.csr_matrix(X, dtype=np.float32)
        if X.nnz and not np.allclose(X.data[:10000], np.round(X.data[:10000])):
            print('WARN region values are not integers: expected raw counts (use --counts-layer)')
        M = (X @ O).tocsr()
        mode = 'peaks'
    M.eliminate_zeros()
    tot = np.asarray(M.sum(1)).ravel()
    L = sp.diags(1e4 / np.maximum(tot, 1)) @ M
    L = sp.csr_matrix(L, dtype=np.float32)
    L.data = np.log1p(L.data)

    var = genes.set_index('gene_id')
    var.index.name = None
    var['n_regions'] = n_regions
    det = np.asarray((M > 0).sum(0)).ravel() / max(a.n_obs, 1)
    var['frac_detected'] = det.astype(np.float32)
    var['measurable'] = (n_regions > 0) if not args.fragments else (det >= 0.005)
    b = ad.AnnData(X=L, obs=a.obs.copy(), var=var, obsm=dict(a.obsm), obsp=dict(a.obsp), uns=dict(a.uns))
    b.layers['counts'] = M.astype(np.float32)
    b.obs['n_gene_activity_counts'] = tot
    b.obs['n_genes_active'] = np.asarray((M > 0).sum(1)).ravel()
    b.uns['gene_activity'] = {'source_h5ad': os.path.abspath(args.h5ad), 'gff': os.path.abspath(args.gff),
                              'mode': mode, 'upstream': args.upstream, 'downstream': args.downstream,
                              'fragments': [os.path.abspath(f) for f in (args.fragments or [])],
                              'X': 'log1p(counts / total * 1e4)'}
    b.write_h5ad(args.out, compression='gzip')
    un = b.var_names[~b.var['measurable'].values]
    with open(re.sub(r'\.h5ad$', '', args.out) + '.unmeasurable_genes.txt', 'w') as f:
        f.write('\n'.join(un) + ('\n' if len(un) else ''))
    print(f'mode {mode}: {b.var["measurable"].mean():.1%} of {b.n_vars:,} genes measurable '
          f'({len(un):,} unmeasurable: ' + ('no overlapping region' if not args.fragments else 'detected in <0.5% of nuclei')
          + '); median counts per nucleus %.0f, median active genes %.0f' % (np.median(tot), np.median(b.obs['n_genes_active'])))
    if (tot == 0).any():
        print(f'WARN {(tot == 0).sum():,} nuclei have no gene-activity counts')
    print(f'Wrote {args.out}')


if __name__ == '__main__':
    sys.exit(main())
