#!/usr/bin/env python3
"""Check named genes per cluster, with IDs resolved from tables, never typed from memory.

Give symbols (MC9, XCP1, SULTR2;1), reference IDs (AT5G04200) or target gene IDs; each
term is resolved to *every* target gene copy through the gene map(s), the mapped marker
tables and gene annotation tables, and each copy is reported per cluster: fraction of
cells expressing, mean log expression, z of the cluster mean across clusters, and the
cluster where it peaks.

Resolution (exact, case-insensitive matches only; nothing is guessed):
  1. a target gene ID present in the data (var_names, or obs '<gene>_expr')
  2. a symbol in --gene-annotation (target species: gene_id, symbol, description)
  3. a symbol in --marker-tables (target marker tables from map_markers.py)
  4. a reference gene ID, reference symbol, or one comma-separated name in the reference
     description of --gene-map (e.g. "metacaspase 9"), or a symbol in --ref-annotation
     (reference species: gene_id, symbol[, description]; aliases separated by , or |; a ; is part
     of a symbol, as in SULTR2;1);
     then every target gene whose hit to that reference gene has rank <= --max-rank
  "A/B" is tried as A and B (alternative names of one gene) when "A/B" itself does not resolve.
Terms that resolve to nothing are reported, with symbols that start with the same letters
as hints only. Terms with more than --many copies are flagged.

Output: compact markdown to stdout (and --out-md), long TSV to --out (one row per
term x copy x key x cluster).

Example:
  python check_genes.py --h5ad data.h5ad --cluster-key leiden_res1.5 \
      --genes MC9/MCP2f XCP1 XCP2 VND2 SND2 --gene-map gene_map.tsv --out checks/pcd.tsv
"""

import argparse
import glob
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cluster_evidence import expression_source, gene_matrix, group_mean_frac, natural_key  # noqa: E402

warnings.filterwarnings('ignore')

SKILL_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# Araport/TAIR export placeholders: treat as empty
PLACEHOLDERS = {'', 'nan', 'none', '-', 'na', 'n/a', 'no symbol available', 'no full name available',
                'no description available'}


def clean(s):
    """String or '' (NaN, None and Araport placeholders become '')."""
    if s is None:
        return ''
    if isinstance(s, float) and np.isnan(s):
        return ''
    s = str(s).strip()
    return '' if s.lower() in PLACEHOLDERS else s


def name_tokens(s, seps=r'[,|]'):
    return [t for t in (clean(x) for x in re.split(seps, clean(s))) if t]


def ref_key(g):
    """Reference gene key: upper case, transcript suffix (.1) removed."""
    return re.sub(r'\.\d+$', '', str(g).strip()).upper()


def load_gene_maps(paths):
    """All hits of one or more gene_map.tsv files (first file wins for a repeated query/ref pair)."""
    frames = []
    for i, p in enumerate(paths or []):
        gm = pd.read_csv(p, sep='\t', dtype={'query_gene': str, 'ref_gene': str})
        for c in ['ref_symbol', 'ref_description', 'pident', 'rbh', 'relationship']:
            if c not in gm.columns:
                gm[c] = np.nan if c == 'pident' else ''
        gm['ref_symbol'] = gm['ref_symbol'].map(clean)
        gm['ref_description'] = gm['ref_description'].map(clean)
        gm['rbh'] = gm['rbh'].map(clean)
        gm['relationship'] = gm['relationship'].map(clean)
        gm['pident'] = pd.to_numeric(gm['pident'], errors='coerce')
        gm['hit_rank'] = pd.to_numeric(gm['hit_rank'], errors='coerce').fillna(99).astype(int)
        gm['map_order'] = i
        gm['map_file'] = os.path.basename(p)
        frames.append(gm)
    if not frames:
        return None
    gm = pd.concat(frames, ignore_index=True)
    gm['ref_key'] = gm['ref_gene'].map(ref_key)
    gm = gm.sort_values(['map_order', 'query_gene', 'hit_rank'], kind='mergesort')
    return gm.drop_duplicates(['query_gene', 'ref_key']).reset_index(drop=True)


def rank1_map(gm):
    """query_gene -> rank-1 row from the primary map that has the gene (like load_gene_map)."""
    if gm is None:
        return None
    r1 = gm[gm['hit_rank'] == 1].sort_values(['map_order'], kind='mergesort')
    return r1.drop_duplicates('query_gene').set_index('query_gene')


def load_annotation_tables(paths):
    """gene_id<TAB>symbol<TAB>description[<TAB>aliases] (header optional; first file wins), placeholders cleaned."""
    frames = []
    for p in paths or []:
        t = pd.read_csv(p, sep='\t', header=None, dtype=str, comment=None).fillna('')
        t = t.iloc[:, :4]  # optional 4th column: aliases (e.g. CESA7 for IRX3, VND2 for NAC076)
        while t.shape[1] < 4:
            t[t.shape[1]] = ''
        t.columns = ['gene_id', 'symbol', 'description', 'aliases']
        if t.iloc[0, 0].strip().lower() in ('gene_id', 'gene', 'locus', 'id', 'locus_id', 'query_gene'):
            t = t.iloc[1:]
        t['gene_id'] = t['gene_id'].str.strip()
        t['symbol'] = t['symbol'].map(clean)
        t['description'] = t['description'].map(clean)
        frames.append(t)
    if not frames:
        return None
    t = pd.concat(frames, ignore_index=True)
    return t.drop_duplicates('gene_id').set_index('gene_id')


def find_ref_annotation():
    """A shipped Arabidopsis (Araport11) symbol table under references/, if one exists."""
    pats = ['references/**/araport11*symbol*.tsv*', 'references/**/araport11*gene*.tsv*',
            'references/**/araport11*annotation*.tsv*', 'references/**/arabidopsis*gene*annotation*.tsv*']
    for pat in pats:
        hits = sorted(glob.glob(os.path.join(SKILL_DIR, pat), recursive=True))
        if hits:
            return hits[0]
    return None


class GeneResolver:
    """Resolve gene terms to target gene copies through tables only."""

    def __init__(self, var_names, obs_columns=(), gene_maps=None, marker_tables=None,
                 gene_annotations=None, ref_annotations=None, max_rank=2):
        self.var = pd.Index(var_names)
        self.var_upper = {}
        for g in self.var:
            self.var_upper.setdefault(str(g).upper(), g)
        for c in obs_columns:
            if str(c).endswith('_expr'):
                self.var_upper.setdefault(str(c)[:-5].upper(), str(c)[:-5])
        self.in_data = set(self.var) | {str(c)[:-5] for c in obs_columns if str(c).endswith('_expr')}
        self.max_rank = max_rank
        self.gm = load_gene_maps(gene_maps)
        self.r1 = rank1_map(self.gm)
        self.ann = load_annotation_tables(gene_annotations)
        self.ref_ann = load_annotation_tables(ref_annotations)
        self.markers = None
        if marker_tables:
            from cluster_evidence import load_markers
            mk = load_markers(marker_tables)
            for c in ['ref_gene', 'hit_rank', 'pident', 'rbh', 'via', 'relationship', 'ref_symbol']:
                if c not in mk.columns:
                    mk[c] = ''
            self.markers = mk
        self._build()

    def _build(self):
        self.ann_sym = {}
        if self.ann is not None:
            for g, s in zip(self.ann.index, self.ann['symbol']):
                for t in name_tokens(s):
                    self.ann_sym.setdefault(t.upper(), []).append(g)
        self.mk_sym = {}
        if self.markers is not None:
            for i, r in self.markers.iterrows():
                for s in {clean(r['symbol']), clean(r['ref_symbol'])}:
                    for t in name_tokens(s) + ([s] if s else []):
                        self.mk_sym.setdefault(t.upper(), set()).add(i)
        self.gm_by_ref, self.ref_sym, self.ref_desc = {}, {}, {}
        if self.gm is not None:
            for k, idx in self.gm.groupby('ref_key').indices.items():
                self.gm_by_ref[k] = idx
            refs = self.gm.drop_duplicates('ref_key')
            for k, s, d in zip(refs['ref_key'], refs['ref_symbol'], refs['ref_description']):
                for t in name_tokens(s):
                    self.ref_sym.setdefault(t.upper(), set()).add(k)
                for t in name_tokens(d):
                    self.ref_desc.setdefault(t.upper(), set()).add(k)
        self.refann_sym = {}
        if self.ref_ann is not None:
            for g, s, al in zip(self.ref_ann.index, self.ref_ann['symbol'], self.ref_ann['aliases']):
                for t in name_tokens(s) + ([clean(s)] if clean(s) else []) + name_tokens(al):
                    self.refann_sym.setdefault(t.upper(), set()).add(ref_key(g))

    # -- symbol / homolog helpers used by the report
    def symbol_of(self, gene):
        """Best display name for a target gene: own annotation symbol, else rank-1 reference symbol."""
        if self.ann is not None and gene in self.ann.index and self.ann.at[gene, 'symbol']:
            return name_tokens(self.ann.at[gene, 'symbol'])[0]
        if self.r1 is not None and gene in self.r1.index:
            s = name_tokens(self.r1.at[gene, 'ref_symbol'])
            return s[0] if s else str(self.r1.at[gene, 'ref_gene'])
        return gene

    def homolog_info(self, gene):
        if self.r1 is None or gene not in self.r1.index:
            return {}
        r = self.r1.loc[gene]
        return dict(ref_gene=r['ref_gene'], ref_symbol=(name_tokens(r['ref_symbol']) or [''])[0],
                    hit_rank=int(r['hit_rank']), pident=r['pident'], rbh=r['rbh'],
                    relationship=r['relationship'])

    def _copy(self, gene, route, **kw):
        d = dict(gene_id=gene, route=route, ref_gene='', ref_symbol='', hit_rank=np.nan,
                 pident=np.nan, rbh='', relationship='', in_data=gene in self.in_data)
        d.update({k: v for k, v in kw.items() if v is not None})
        return d

    def resolve(self, term):
        """-> list of copy dicts (gene_id, route, ref_gene, ref_symbol, hit_rank, pident, rbh, in_data)."""
        t = term.strip()
        T = t.upper()
        if not t:
            return []
        if T in self.var_upper:
            g = self.var_upper[T]
            return [self._copy(g, 'target gene ID', **self.homolog_info(g))]
        found = {}

        def add(d):
            g = d['gene_id']
            if g not in found:
                found[g] = d
                return
            old = found[g]
            if d['route'] not in old['route']:
                old['route'] += '; ' + d['route']
            if (not np.isnan(d['hit_rank'])) and (np.isnan(old['hit_rank']) or d['hit_rank'] < old['hit_rank']):
                for k in ('ref_gene', 'ref_symbol', 'hit_rank', 'pident', 'rbh', 'relationship'):
                    old[k] = d[k]

        for g in self.ann_sym.get(T, []):
            add(self._copy(g, 'target annotation symbol', **self.homolog_info(g)))
        for i in sorted(self.mk_sym.get(T, [])):
            r = self.markers.loc[i]
            rank = pd.to_numeric(r['hit_rank'], errors='coerce')
            same = clean(r['via']) == 'same_species'
            add(self._copy(r['gene_id'], f"marker table ({r['cell_type']})",
                           ref_gene='' if same else clean(r['ref_gene']),
                           ref_symbol=clean(r['ref_symbol']) or clean(r['symbol']),
                           hit_rank=np.nan if same else rank,
                           pident=np.nan if same else pd.to_numeric(r['pident'], errors='coerce'),
                           rbh=clean(r['rbh']), relationship=clean(r['relationship'])))
        refs = {}
        k = ref_key(t)
        if k in self.gm_by_ref:
            refs[k] = 'reference ID'
        for k in self.ref_sym.get(T, []):
            refs.setdefault(k, 'reference symbol')
        for k in self.refann_sym.get(T, []):
            refs.setdefault(k, 'reference annotation symbol')
        for k in self.ref_desc.get(T, []):
            refs.setdefault(k, 'reference description name')
        if self.gm is not None:
            for k, how in refs.items():
                for j in self.gm_by_ref.get(k, []):
                    r = self.gm.iloc[j]
                    if r['hit_rank'] > self.max_rank:
                        continue
                    add(self._copy(r['query_gene'], f"gene map {how} {r['ref_gene']}",
                                   ref_gene=r['ref_gene'], ref_symbol=(name_tokens(r['ref_symbol']) or [''])[0],
                                   hit_rank=int(r['hit_rank']), pident=r['pident'], rbh=r['rbh'],
                                   relationship=r['relationship']))
        if not found and '/' in t:
            for part in t.split('/'):
                for d in self.resolve(part):
                    add(d)
        out = list(found.values())
        out.sort(key=lambda d: (not d['in_data'], 99 if np.isnan(d['hit_rank']) else d['hit_rank'],
                                -(0 if np.isnan(d['pident']) else d['pident']), str(d['gene_id'])))
        return out

    def hints(self, term, n=8):
        """Names starting with the term's first 3 letters (hints only, never used for checks)."""
        T = term.strip().upper()
        if len(T) < 3:
            return []
        pre = T[:3]
        names = set(self.ann_sym) | set(self.mk_sym) | set(self.ref_sym) | set(self.refann_sym)
        return sorted(x for x in names if x.startswith(pre))[:n]


def parse_terms(genes, genes_file):
    terms = []
    for g in genes or []:
        terms += [x for x in re.split(r'[,\s]+', g) if x]
    if genes_file:
        with open(genes_file) as fh:
            for ln in fh:
                ln = ln.split('#')[0].strip()
                if ln:
                    terms += [x for x in re.split(r'[,\t]+', ln) if x.strip()][:1]
    return list(dict.fromkeys(t.strip() for t in terms))


def cluster_stats(adata, X, var_names, genes, key):
    """-> (groups, sizes, mean, frac, z) over clusters of key (cells with NaN key excluded)."""
    M, found = gene_matrix(adata, X, var_names, genes)
    lab = adata.obs[key].astype(str).to_numpy()
    ok = ~pd.isna(adata.obs[key].to_numpy()) & (lab != 'nan') & (lab != '')
    M = M[ok] if ok.sum() < len(ok) else M
    groups, mean, frac = group_mean_frac(M, lab[ok])
    sizes = pd.Series(lab[ok]).value_counts().reindex(groups).to_numpy()
    sd = mean.std(0, ddof=0)
    z = (mean - mean.mean(0)) / np.where(sd > 0, sd, 1)
    return found, groups, sizes, mean, frac, z


def fmt_pid(p):
    return '' if p is None or (isinstance(p, float) and np.isnan(p)) else f'{p:.0f}%'


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True)
    p.add_argument('--cluster-key', nargs='+', required=True, help='obs column(s) with cluster IDs')
    p.add_argument('--genes', nargs='*', default=[], help='symbols or IDs (comma or space separated)')
    p.add_argument('--genes-file', default=None, help='one term per line (first column; # comments)')
    p.add_argument('--gene-map', nargs='+', default=None, help='gene_map.tsv file(s) from map_markers.py; first is primary')
    p.add_argument('--marker-tables', nargs='+', default=None, help='target marker tables from map_markers.py')
    p.add_argument('--gene-annotation', nargs='+', default=None,
                   help='target-species gene_id, symbol, description table(s)')
    p.add_argument('--ref-annotation', nargs='+', default=None,
                   help='reference-species (e.g. Araport11) gene_id, symbol[, description] table(s) for symbol '
                        '-> reference ID (aliases separated by , or |). Default: a shipped Araport11 table if present')
    p.add_argument('--max-rank', type=int, default=2,
                   help='gene-map hits up to this rank count as copies of a reference gene (shown with rank)')
    p.add_argument('--many', type=int, default=6, help='warn when a term resolves to more copies than this')
    p.add_argument('--clusters', default=None,
                   help='comma-separated cluster IDs to show in the markdown in addition to the peak (e.g. 0,5)')
    p.add_argument('--wide', action='store_true', help='also print the fraction in every cluster')
    p.add_argument('--layer', default=None)
    p.add_argument('--use-raw', choices=['auto', 'yes', 'no'], default='auto')
    p.add_argument('--out', default=None, help='long TSV output')
    p.add_argument('--out-md', default=None, help='markdown output (also printed)')
    args = p.parse_args()

    terms = parse_terms(args.genes, args.genes_file)
    if not terms:
        sys.exit('no genes given (--genes or --genes-file)')
    if not (args.gene_map or args.marker_tables or args.gene_annotation):
        print('NOTE no --gene-map/--marker-tables/--gene-annotation: only target gene IDs can be resolved')
    ref_ann = args.ref_annotation
    if ref_ann is None:
        auto = find_ref_annotation()
        if auto:
            ref_ann = [auto]
            print(f'  reference symbols from {os.path.relpath(auto, SKILL_DIR)}')

    import scanpy as sc
    adata = sc.read_h5ad(args.h5ad)
    for k in args.cluster_key:
        if k not in adata.obs.columns:
            sys.exit(f'{k} not in obs (columns: {", ".join(map(str, adata.obs.columns[:40]))})')
    X, var_names, src = expression_source(adata, args.layer, args.use_raw)
    res = GeneResolver(var_names, adata.obs.columns, args.gene_map, args.marker_tables,
                       args.gene_annotation, ref_ann, args.max_rank)

    md = [f'# Gene check: {os.path.basename(args.h5ad)} ({adata.n_obs:,} cells; expression from {src})', '']
    copies, warns = [], []
    for t in terms:
        cs = res.resolve(t)
        if not cs:
            h = res.hints(t)
            warns.append(f'- **{t}**: resolves to nothing in the given tables; not checked (no guessing). '
                         'Give the reference ID (e.g. the AGI) or a --ref-annotation table with this symbol.'
                         + (f' Names with the same start (hints only): {", ".join(h)}' if h else ''))
            continue
        absent = [c['gene_id'] for c in cs if not c['in_data']]
        if absent:
            warns.append(f'- {t}: {len(absent)} cop{"y" if len(absent) == 1 else "ies"} not in the data '
                         f'(filtered or not expressed): {", ".join(absent[:10])}')
        if len(cs) > args.many:
            warns.append(f'- {t}: {len(cs)} copies (gene family?); check rank/identity before using all of them')
        for c in cs:
            copies.append(dict(term=t, **c))
    if warns:
        md += ['## Warnings', ''] + warns + ['']
    print('\n'.join(md))
    if not copies:
        sys.exit('nothing resolved')
    cdf = pd.DataFrame(copies)
    genes = list(dict.fromkeys(cdf.loc[cdf['in_data'], 'gene_id']))
    show = [x.strip() for x in args.clusters.split(',')] if args.clusters else []

    long = []
    md2 = []
    for key in args.cluster_key:
        found, groups, sizes, mean, frac, z = cluster_stats(adata, X, var_names, genes, key)
        col = {g: i for i, g in enumerate(found)}
        md2 += [f'## {key} ({len(groups)} clusters)', '']
        head = '| term | gene | homolog (rank, id, RBH) | peak cluster: frac, mean, z | 2nd |'
        extra = [c for c in show if c in groups]
        head += ''.join(f' cl {c}: frac, z |' for c in extra)
        md2 += [head, '|' + '---|' * (5 + len(extra))]
        for c in copies:
            g = c['gene_id']
            hom = ''
            if c['ref_gene']:
                rk = '' if np.isnan(c['hit_rank']) else f"r{int(c['hit_rank'])}"
                pid = fmt_pid(c['pident']) or (f"orthology {c['relationship']}" if c['relationship'] else '')
                hom = f"{c['ref_symbol'] or c['ref_gene']} ({c['ref_gene']}; {', '.join(x for x in (rk, pid) if x)}" \
                      + (', RBH' if c['rbh'] == 'yes' else '') + ')'
            if g not in col:
                md2.append(f"| {c['term']} | {g} | {hom} | not in data | |" + ' |' * len(extra))
                continue
            j = col[g]
            order = np.argsort(-mean[:, j])
            i1 = order[0]
            i2 = order[1] if len(order) > 1 else None
            pk = f'{groups[i1]}: {frac[i1, j]:.0%}, {mean[i1, j]:.2f}, {z[i1, j]:.1f}'
            nd = f'{groups[i2]}: {frac[i2, j]:.0%}, z {z[i2, j]:.1f}' if i2 is not None else ''
            gi = {gr: i for i, gr in enumerate(groups)}
            row = f"| {c['term']} | {g} | {hom} | {pk} | {nd} |" + ''.join(
                f' {frac[gi[x], j]:.0%}, {z[gi[x], j]:.1f} |' for x in extra)
            md2.append(row)
            for i, cl in enumerate(groups):
                long.append(dict(term=c['term'], gene_id=g, route=c['route'], ref_gene=c['ref_gene'],
                                 ref_symbol=c['ref_symbol'], hit_rank=c['hit_rank'], pident=c['pident'],
                                 rbh=c['rbh'], relationship=c['relationship'], key=key, cluster=cl,
                                 n_cells=int(sizes[i]), frac=round(float(frac[i, j]), 4),
                                 mean=round(float(mean[i, j]), 4), z=round(float(z[i, j]), 3),
                                 is_peak=bool(i == i1)))
        md2.append('')
        if args.wide and found:
            md2 += [f'Fraction expressing per cluster ({key}); * = z >= 2', '',
                    '| gene | ' + ' | '.join(groups) + ' |', '|---|' + '---|' * len(groups)]
            for g in found:
                j = col[g]
                md2.append(f'| {g} | ' + ' | '.join(f"{frac[i, j]:.0%}{'*' if z[i, j] >= 2 else ''}"
                                                    for i in range(len(groups))) + ' |')
            md2.append('')
    md2 += ['Routes (how each term was resolved):', '']
    for c in copies:
        md2.append(f"- {c['term']} -> {c['gene_id']}: {c['route']}")
    print('\n'.join(md2))
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        pd.DataFrame(long).to_csv(args.out, sep='\t', index=False)
        print(f'\nWrote {args.out}')
    if args.out_md:
        os.makedirs(os.path.dirname(os.path.abspath(args.out_md)), exist_ok=True)
        with open(args.out_md, 'w') as fh:
            fh.write('\n'.join(md + md2) + '\n')
        print(f'Wrote {args.out_md}')


if __name__ == '__main__':
    main()
