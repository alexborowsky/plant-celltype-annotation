#!/usr/bin/env python3
"""Score published per-cluster gene sets in the current clusters.

For published annotations that exist only per cluster (no per-cell labels): a table of
published cluster (or label) -> marker genes. Each published gene set is scored in each
current cluster as the mean z (z of the cluster mean across current clusters, per gene)
over the set's genes in the data, plus the mean fraction of cells detecting them.

Reported:
  - per published set (and per published label, pooling the sets that share a label):
    best current cluster, its score, the second best and the margin between them
  - per current cluster: best published set/label, second best and the margin
  - clusters whose median counts are > --high-counts x the median cell (default 1.5):
    every gene is detected more often in them, which inflates every set's score there.
    Doublet or large-cell clusters show up as "matching" many sets at once.
Small margins (< --margin, default 0.25 z) mean the match is ambiguous.

Gene resolution: a gene_id column whose values are in the data is used as is; otherwise
symbols (or IDs) are resolved through --gene-map / --marker-tables / --gene-annotation
exactly as in check_genes.py (all copies; nothing is guessed). Unresolved genes are listed.

Input --sets: TSV with a set column (--set-col; default the first of set_name, set,
published_cluster, cluster, label) and gene_id and/or symbol columns. Labels: --label-col
(a column of --sets, default label/published_label if present) or --labels FILE (TSV with
the set column and a label column, e.g. published_cluster -> published_label).

Output: markdown to stdout and <out>.md; TSVs <out>_scores.tsv (set x cluster),
<out>_best_per_set.tsv, <out>_best_per_cluster.tsv (and _by_label variants with labels).

Example (tea leaf, published cluster DEGs):
  python score_gene_sets.py --h5ad annotated.h5ad --cluster-key leiden_res0.5 \
      --sets truth/N4_tea_leaf_markers.tsv --set-col published_cluster \
      --labels truth/N4_tea_leaf_clusters.tsv --label-col published_sublabel \
      --gene-map gene_map.tsv --out published/pub_sets
"""

import argparse
import os
import sys
import warnings

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cluster_evidence import expression_source, gene_matrix, group_mean_frac, natural_key  # noqa: E402
from check_genes import GeneResolver, clean, find_ref_annotation  # noqa: E402

warnings.filterwarnings('ignore')

COUNT_COLS = ['total_counts', 'n_counts', 'nCount_RNA', 'total_UMIs']
GENE_COLS = ['n_genes_by_counts', 'n_genes', 'nFeature_RNA']


def first_col(cols, cands):
    for c in cands:
        if c in cols:
            return c
    return None


def cell_depth(adata, X):
    c = first_col(adata.obs.columns, COUNT_COLS)
    if c:
        return adata.obs[c].to_numpy(dtype=float), c
    c = first_col(adata.obs.columns, GENE_COLS)
    if c:
        return adata.obs[c].to_numpy(dtype=float), c
    from scipy import sparse
    nz = np.asarray((X > 0).sum(1)).ravel() if sparse.issparse(X) else (np.asarray(X) > 0).sum(1)
    return nz.astype(float), 'genes detected (computed)'


def best_two(s):
    """Series -> (best index, best value, second index, second value)."""
    s = s.dropna().sort_values(ascending=False)
    if s.empty:
        return '', np.nan, '', np.nan
    if len(s) == 1:
        return s.index[0], s.iloc[0], '', np.nan
    return s.index[0], s.iloc[0], s.index[1], s.iloc[1]


def md_table(df, floatfmt='{:.2f}'):
    cols = list(df.columns)
    out = ['| ' + ' | '.join(map(str, cols)) + ' |', '|' + '---|' * len(cols)]
    for _, r in df.iterrows():
        vals = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating)):
                vals.append('' if np.isnan(v) else floatfmt.format(v))
            else:
                vals.append(str(v))
        out.append('| ' + ' | '.join(vals) + ' |')
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True)
    p.add_argument('--cluster-key', nargs='+', required=True)
    p.add_argument('--sets', required=True, help='TSV: set column + gene_id and/or symbol')
    p.add_argument('--set-col', default=None)
    p.add_argument('--gene-col', default=None, help='default: gene_id, then symbol (per row, whichever resolves)')
    p.add_argument('--label-col', default=None, help='label column (in --labels if given, else in --sets)')
    p.add_argument('--labels', default=None, help='TSV mapping the set column to labels')
    p.add_argument('--gene-map', nargs='+', default=None)
    p.add_argument('--marker-tables', nargs='+', default=None)
    p.add_argument('--gene-annotation', nargs='+', default=None)
    p.add_argument('--ref-annotation', nargs='+', default=None)
    p.add_argument('--max-rank', type=int, default=1,
                   help='gene-map hit rank for symbol -> copies (default 1: sets stay specific)')
    p.add_argument('--min-genes', type=int, default=2, help='sets with fewer genes in the data are flagged')
    p.add_argument('--min-frac', type=float, default=0.02,
                   help='a gene detected in fewer cells of a cluster cannot raise its z there (as cluster_evidence)')
    p.add_argument('--high-counts', type=float, default=1.5,
                   help='flag clusters whose median counts exceed this multiple of the median cell')
    p.add_argument('--margin', type=float, default=0.25, help='margins below this are called ambiguous')
    p.add_argument('--layer', default=None)
    p.add_argument('--use-raw', choices=['auto', 'yes', 'no'], default='auto')
    p.add_argument('--out', required=True, help='output prefix')
    args = p.parse_args()

    sets = pd.read_csv(args.sets, sep='\t', dtype=str).fillna('')
    set_col = args.set_col or first_col(sets.columns, ['set_name', 'set', 'published_cluster', 'cluster', 'label'])
    if not set_col or set_col not in sets.columns:
        sys.exit(f'set column not found; give --set-col (columns: {list(sets.columns)})')
    labels = None
    if args.labels:
        lt = pd.read_csv(args.labels, sep='\t', dtype=str).fillna('')
        lc = args.label_col or first_col(lt.columns, ['label', 'published_label', 'cell_type'])
        if set_col not in lt.columns or lc not in lt.columns:
            sys.exit(f'--labels needs columns {set_col} and a label column (got {list(lt.columns)})')
        labels = dict(zip(lt[set_col].str.strip(), lt[lc].str.strip()))
    else:
        lc = args.label_col or first_col(sets.columns, ['label', 'published_label'])
        if lc and lc != set_col and lc in sets.columns:
            labels = dict(zip(sets[set_col].str.strip(), sets[lc].str.strip()))
    sets[set_col] = sets[set_col].str.strip()

    ref_ann = args.ref_annotation
    if ref_ann is None:
        auto = find_ref_annotation()
        ref_ann = [auto] if auto else None

    import scanpy as sc
    adata = sc.read_h5ad(args.h5ad)
    for k in args.cluster_key:
        if k not in adata.obs.columns:
            sys.exit(f'{k} not in obs')
    X, var_names, src = expression_source(adata, args.layer, args.use_raw)
    res = GeneResolver(var_names, adata.obs.columns, args.gene_map, args.marker_tables,
                       args.gene_annotation, ref_ann, args.max_rank)

    # ---- resolve genes per set
    gene_cols = [args.gene_col] if args.gene_col else [c for c in ('gene_id', 'symbol') if c in sets.columns]
    if not gene_cols:
        sys.exit('--sets needs a gene_id or symbol column (or --gene-col)')
    members, unresolved, multi = {}, [], []
    for _, r in sets.iterrows():
        s = r[set_col]
        if not s:
            continue
        hit = []
        for c in gene_cols:
            term = clean(r[c])
            if not term:
                continue
            hit = [d['gene_id'] for d in res.resolve(term) if d['in_data']]
            if hit:
                break
        if not hit:
            unresolved.append(f"{s}:{'/'.join(clean(r[c]) for c in gene_cols if clean(r[c]))}")
            continue
        if len(hit) > 1:
            multi.append(f"{s}:{clean(r[gene_cols[-1]]) or hit[0]} -> {len(hit)} copies")
        members.setdefault(s, [])
        members[s] += [g for g in hit if g not in members[s]]
    all_sets = sorted(sets.loc[sets[set_col] != '', set_col].unique(), key=natural_key)
    empty = [s for s in all_sets if s not in members]
    genes = list(dict.fromkeys(g for v in members.values() for g in v))
    if not genes:
        sys.exit('no set gene found in the data')
    M, found = gene_matrix(adata, X, var_names, genes)
    col = {g: i for i, g in enumerate(found)}
    depth, depth_col = cell_depth(adata, X)
    med_all = float(np.nanmedian(depth))

    def name(s):
        return f'{s} ({labels[s]})' if labels and s in labels and labels[s] and labels[s] != s else str(s)

    md = [f'# Published gene sets scored in current clusters: {os.path.basename(args.h5ad)}', '',
          f'{adata.n_obs:,} cells; expression from {src}; sets from {os.path.basename(args.sets)} '
          f'(set column {set_col}); {len(members)}/{len(all_sets)} sets with genes in the data; '
          f'{len(genes)} genes. Score = mean z of the set genes across current clusters; '
          f'frac = mean fraction of cells detecting them. Depth: {depth_col}.', '']
    if unresolved:
        md += [f'Unresolved or absent genes ({len(unresolved)}): ' + ', '.join(unresolved[:40])
               + (' ...' if len(unresolved) > 40 else ''), '']
    if multi:
        md += [f'Genes resolved to several copies (all used): ' + ', '.join(multi[:20]), '']
    if empty:
        md += ['Sets with no gene in the data: ' + ', '.join(map(str, empty)), '']

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or '.', exist_ok=True)
    all_scores, all_bps, all_bpc = [], [], []
    for key in args.cluster_key:
        lab = adata.obs[key].astype(str).to_numpy()
        ok = ~pd.isna(adata.obs[key].to_numpy()) & (lab != 'nan') & (lab != '')
        groups, mean, frac = group_mean_frac(M[ok] if ok.sum() < len(ok) else M, lab[ok])
        sd = mean.std(0, ddof=0)
        z = (mean - mean.mean(0)) / np.where(sd > 0, sd, 1)
        z = np.where(frac >= args.min_frac, z, np.minimum(z, 0))
        sizes = pd.Series(lab[ok]).value_counts().reindex(groups)
        dmed = pd.Series(depth[ok]).groupby(lab[ok]).median().reindex(groups)
        ratio = dmed / med_all
        high = ratio > args.high_counts

        def score_sets(gsets):
            sc_, fr_, n_ = {}, {}, {}
            for s, gs in gsets.items():
                idx = [col[g] for g in gs if g in col]
                if not idx:
                    continue
                sc_[s] = z[:, idx].mean(1)
                fr_[s] = frac[:, idx].mean(1)
                n_[s] = len(idx)
            S = pd.DataFrame(sc_, index=groups)
            F = pd.DataFrame(fr_, index=groups)
            return S, F, n_

        variants = [('set', members)]
        if labels:
            by_lab = {}
            for s, gs in members.items():
                lb = labels.get(s, '') or s
                by_lab.setdefault(lb, [])
                by_lab[lb] += [g for g in gs if g not in by_lab[lb]]
            variants.append(('label', by_lab))
        md += [f'## {key} ({len(groups)} clusters)', '']
        hc = [f'{g} ({ratio[g]:.1f}x)' for g in groups if high[g]]
        md += [f'High-count clusters (median {depth_col} > {args.high_counts}x the median cell; scores inflated): '
               + (', '.join(hc) if hc else 'none'), '']
        for level, gsets in variants:
            S, F, n_ = score_sets(gsets)
            if S.empty:
                continue
            disp = (lambda s: name(s)) if level == 'set' else (lambda s: str(s))
            long = S.stack().rename('score').reset_index()
            long.columns = ['cluster', level, 'score']
            long['frac'] = [F.at[c, s] for c, s in zip(long['cluster'], long[level])]
            long['n_genes'] = long[level].map(n_)
            long['cluster_cells'] = long['cluster'].map(sizes).astype(int)
            long['depth_ratio'] = long['cluster'].map(ratio).round(2)
            long['high_counts'] = long['cluster'].map(high)
            long.insert(0, 'key', key)
            all_scores.append(long.assign(level=level))
            # per published set/label
            rows = []
            for s in sorted(S.columns, key=natural_key):
                b, bv, c2, v2 = best_two(S[s])
                rows.append({level: disp(s), 'n_genes': n_[s], 'best_cluster': b, 'score': bv,
                             'frac': F.at[b, s] if b != '' else np.nan, 'second': c2, 'second_score': v2,
                             'margin': bv - v2 if c2 != '' else np.nan,
                             'flags': '; '.join(x for x in (
                                 'few genes' if n_[s] < args.min_genes else '',
                                 'ambiguous' if c2 != '' and bv - v2 < args.margin else '',
                                 f'best is high-count ({ratio[b]:.1f}x)' if b != '' and high[b] else '') if x)})
            bps = pd.DataFrame(rows)
            all_bps.append(bps.assign(key=key, level=level))
            md += [f'### Best current cluster per published {level}', ''] + md_table(bps) + ['']
            # per current cluster
            rows = []
            for g in groups:
                b, bv, s2, v2 = best_two(S.loc[g])
                rows.append({'cluster': g, 'cells': int(sizes[g]), 'depth': f'{ratio[g]:.1f}x',
                             f'best_{level}': disp(b) if b != '' else '', 'score': bv,
                             'frac': F.at[g, b] if b != '' else np.nan,
                             f'second_{level}': disp(s2) if s2 != '' else '', 'second_score': v2,
                             'margin': bv - v2 if s2 != '' else np.nan,
                             'flags': '; '.join(x for x in (
                                 'high counts' if high[g] else '',
                                 'ambiguous' if s2 != '' and bv - v2 < args.margin else '',
                                 'no positive match' if not (bv > 0) else '') if x)})
            bpc = pd.DataFrame(rows)
            all_bpc.append(bpc.assign(key=key, level=level))
            md += [f'### Best published {level} per current cluster', ''] + md_table(bpc) + ['']

    def write(frames, suffix):
        if not frames:
            return
        df = pd.concat(frames, ignore_index=True)
        for level in df['level'].unique():
            sub = df[df['level'] == level].dropna(axis=1, how='all')
            path = f"{args.out}_{suffix}{'' if level == 'set' else '_by_label'}.tsv"
            sub.drop(columns='level').to_csv(path, sep='\t', index=False, float_format='%.4g')
            print(f'Wrote {path}')

    print('\n'.join(md))
    with open(f'{args.out}.md', 'w') as fh:
        fh.write('\n'.join(md) + '\n')
    print(f'Wrote {args.out}.md')
    write(all_scores, 'scores')
    write(all_bps, 'best_per_set')
    write(all_bpc, 'best_per_cluster')


if __name__ == '__main__':
    main()
