#!/usr/bin/env python3
"""Per-cluster evidence for cell-type annotation, across one or more clusterings.

For every cluster key (default: all obs columns starting with 'leiden'):
  de_<key>.csv                 top Wilcoxon genes per cluster (+ homolog annotation, pct in/out)
  marker_expression_<key>.tsv  per cluster x marker gene: mean, frac expressing, z across clusters
  marker_scores_<key>.tsv      per cluster x cell type: mean marker z, mean frac, n markers
  cluster_evidence_<key>.md    human/LLM-readable per-cluster summary
plus cluster_hierarchy.tsv (nesting across keys) and evidence_plots.pdf.

Expression is read from --layer, else adata.raw (if present), else adata.X, and
must be log-normalized (not scaled).
"""

import argparse
import os
import re
import warnings

import numpy as np
import pandas as pd
import scanpy as sc
from scipy import sparse

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# matplotlib < 3.7 writes raster images with <= 16 colors into PDFs as 1/2/4-bit
# palettes without BitsPerComponent in the PNG decode parameters, so PDF viewers
# decode them as horizontal stripes (rasterized UMAPs with one highlight color hit
# this). Write such images as RGB instead; newer matplotlib needs no change.
def _pdf_palette_workaround():
    major, minor = (int(x) for x in matplotlib.__version__.split('.')[:2])
    if (major, minor) >= (3, 7):
        return
    from matplotlib.backends import backend_pdf
    from PIL import Image
    write_img = backend_pdf.PdfFile._writeImg

    def _write_img_rgb(self, data, id, smask=None):
        getcolors = Image.Image.getcolors
        Image.Image.getcolors = lambda img, maxcolors=256: None
        try:
            return write_img(self, data, id, smask)
        finally:
            Image.Image.getcolors = getcolors

    backend_pdf.PdfFile._writeImg = _write_img_rgb


_pdf_palette_workaround()


warnings.filterwarnings('ignore')
sc.settings.verbosity = 1

QC_CANDIDATES = {
    'counts': ['total_counts', 'n_counts', 'nCount_RNA'],
    'genes': ['n_genes_by_counts', 'n_genes', 'nFeature_RNA'],
    'doublet': ['doublet_score', 'scrublet_score', 'scDblFinder.score'],
    'organellar': ['pct_organellar', 'pct_counts_organellar', 'pct_chloroplast',
                   'pct_counts_pt', 'pct_counts_mt', 'pct_mt'],
}


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def natural_key(x):
    s = str(x)
    return (0, int(s), '') if s.lstrip('-').isdigit() else (1, 0, s)


def resolution_of(key):
    m = re.search(r'(\d+(?:\.\d+)?)$', key)
    return float(m.group(1)) if m else np.inf


def expression_source(adata, layer, use_raw):
    if layer:
        return adata.layers[layer], pd.Index(adata.var_names), f'layers[{layer!r}]'
    if use_raw != 'no' and adata.raw is not None:
        return adata.raw.X, pd.Index(adata.raw.var_names), 'raw.X'
    if use_raw == 'yes':
        raise SystemExit('--use-raw yes but adata.raw is None')
    return adata.X, pd.Index(adata.var_names), 'X'


def gene_matrix(adata, X, var_names, genes):
    """cells x genes matrix (sparse if X is sparse), extracted in one pass.

    Genes absent from var_names fall back to obs['<gene>_expr'] (e.g. transgenes).
    """
    genes = list(dict.fromkeys(genes))
    idx = var_names.get_indexer(genes)
    in_var = [(g, i) for g, i in zip(genes, idx) if i >= 0]
    in_obs = [g for g, i in zip(genes, idx) if i < 0 and f'{g}_expr' in adata.obs.columns]
    parts, found = [], []
    if in_var:
        parts.append(X[:, [i for _, i in in_var]])
        found += [g for g, _ in in_var]
    if in_obs:
        parts.append(np.column_stack([adata.obs[f'{g}_expr'].to_numpy(dtype=np.float32)
                                      for g in in_obs]))
        found += in_obs
    if not parts:
        return np.zeros((adata.n_obs, 0), dtype=np.float32), []
    if any(sparse.issparse(p) for p in parts):
        M = sparse.hstack([sparse.csr_matrix(p) for p in parts], format='csr')
    else:
        M = np.hstack([np.asarray(p) for p in parts])
    return M.astype(np.float32), found


def group_mean_frac(M, labels):
    """M: cells x genes dense; labels: array-like. Returns (groups, mean, frac)."""
    codes, groups = pd.factorize(pd.Series(labels).astype(str), sort=False)
    k, n = len(groups), len(codes)
    ind = sparse.csr_matrix((np.ones(n, dtype=np.float32), (codes, np.arange(n))), shape=(k, n))
    counts = np.bincount(codes, minlength=k).astype(np.float64)[:, None]
    dense = lambda A: A.toarray() if sparse.issparse(A) else np.asarray(A)
    mean = dense(ind @ M) / counts
    frac = dense(ind @ (M > 0).astype(np.float32)) / counts
    order = sorted(range(k), key=lambda i: natural_key(groups[i]))
    return [str(groups[i]) for i in order], mean[order], frac[order]


def load_markers(paths):
    """One or more marker tables; the first file wins when a (gene, cell type) pair repeats."""
    alias = {'NbID': 'gene_id', 'GeneID': 'gene_id', 'Gene': 'symbol',
             'gene_name': 'symbol', 'CellType': 'cell_type'}
    frames = []
    for path in paths:
        df = pd.read_csv(path, sep='\t', dtype=str).fillna('')
        df = df.rename(columns={k: v for k, v in alias.items() if k in df.columns and v not in df.columns})
        if 'gene_id' not in df.columns or 'cell_type' not in df.columns:
            raise SystemExit(f'{path}: need gene_id and cell_type columns (got {list(df.columns)})')
        if 'symbol' not in df.columns:
            df['symbol'] = df['gene_id']
        if 'evidence' not in df.columns:
            df['evidence'] = ''
        frames.append(df)
    df = pd.concat(frames, ignore_index=True).fillna('')
    df['symbol'] = df['symbol'].where(~df['symbol'].str.strip().isin(['', '-']), df['gene_id'])
    # One symbol per gene: the species' own name (same-species or user-curated rows, which have no
    # homology `via`) beats a reference-homolog name (Sobic SWEET13, not Arabidopsis SWEET11).
    via = df['via'] if 'via' in df.columns else pd.Series('', index=df.index)
    own = via.isin(['', 'same_species']) & (df['symbol'] != df['gene_id'])
    pref = df[own].drop_duplicates('gene_id').set_index('gene_id')['symbol']
    df['ref_symbol'] = df['symbol']
    df['symbol'] = df['gene_id'].map(pref).fillna(df['symbol'])
    return df.drop_duplicates(['gene_id', 'cell_type'])


def load_stress_genes(path):
    with open(path) as fh:
        return {ln.strip().split('\t')[0].upper() for ln in fh if ln.strip() and not ln.startswith('#')}


def stress_fraction(genes, gm, stress):
    """Fraction of genes whose own ID or rank-1 reference homolog is in the stress list."""
    if not stress or not len(genes):
        return np.nan, 0
    hit = 0
    for g in genes:
        ids = {str(g).upper()}
        if gm is not None and g in gm.index:
            ids.add(str(gm.at[g, 'ref_gene']).upper())
        hit += bool(ids & stress)
    return hit / len(genes), hit


def load_gene_map(path):
    gm = pd.read_csv(path, sep='\t', dtype={'query_gene': str})
    gm = gm[gm['hit_rank'] == 1].drop_duplicates('query_gene').set_index('query_gene')
    return gm


def load_gene_annotation(path):
    """gene_id<TAB>symbol<TAB>description (header optional): names for same-species runs."""
    ann = pd.read_csv(path, sep='\t', header=None, dtype=str, usecols=[0, 1, 2],
                      names=['gene_id', 'symbol', 'description']).fillna('')
    if ann.iloc[0, 0].lower() in ('gene_id', 'gene', 'locus', 'id'):
        ann = ann.iloc[1:]
    return ann.drop_duplicates('gene_id').set_index('gene_id')


def homolog_str(gene, gm, max_desc=60, ann=None):
    if gm is None or gene not in gm.index:
        if ann is not None and gene in ann.index:
            r = ann.loc[gene]
            return ' '.join(x for x in (r['symbol'], r['description'][:max_desc]) if x)
        return ''
    r = gm.loc[gene]
    sym = r.get('ref_symbol', '')
    sym = '' if pd.isna(sym) else str(sym).split(',')[0]
    desc = r.get('ref_description', '')
    desc = '' if pd.isna(desc) else str(desc).split(',')[0][:max_desc]
    out = f"{sym} ({r['ref_gene']})" if sym else str(r['ref_gene'])
    if desc:
        out += f" {desc}"
    out += f" [{r['pident']:.0f}%"
    if str(r.get('rbh', '')) == 'yes':
        out += ', RBH'
    return out + ']'


def pick(obs, names):
    for n in names:
        if n in obs.columns:
            return n
    return None


# ----------------------------------------------------------------------------
# per-key analyses
# ----------------------------------------------------------------------------

def run_de(adata, key, n_top, max_cells, use_raw, layer, seed):
    labels = adata.obs[key].astype(str)
    rng = np.random.default_rng(seed)
    keep = []
    for g, idx in labels.groupby(labels).indices.items():
        if max_cells and len(idx) > max_cells:
            idx = rng.choice(idx, max_cells, replace=False)
        keep.append(idx)
    keep = np.sort(np.concatenate(keep))
    sub = adata[keep].copy() if len(keep) < adata.n_obs else adata
    sub.obs[key] = pd.Categorical(labels.iloc[keep].values)
    counts = sub.obs[key].value_counts()
    groups = [g for g in counts.index if counts[g] >= 3]
    if len(groups) < 2:
        return pd.DataFrame()
    kw = dict(method='wilcoxon', groups=groups, n_genes=n_top, key_added='rgg_ev')
    if layer:
        kw.update(layer=layer, use_raw=False)
    else:
        kw.update(use_raw=(sub.raw is not None and use_raw != 'no'))
    sc.tl.rank_genes_groups(sub, key, **kw)
    res = sub.uns['rgg_ev']
    rows = []
    for g in res['names'].dtype.names:
        for i in range(len(res['names'][g])):
            rows.append({'cluster': g, 'rank': i + 1, 'gene': res['names'][g][i],
                         'score': float(res['scores'][g][i]),
                         'logfc': float(res['logfoldchanges'][g][i]),
                         'pval_adj': float(res['pvals_adj'][g][i])})
    return pd.DataFrame(rows)


def add_pct(de, adata, X, var_names, key):
    """pct expressing inside the cluster and in the rest, on all cells."""
    if de.empty:
        return de
    genes = list(dict.fromkeys(de['gene']))
    M, found = gene_matrix(adata, X, var_names, genes)
    labels = adata.obs[key].astype(str).to_numpy()
    groups, _, frac = group_mean_frac(M, labels)
    sizes = pd.Series(labels).value_counts().reindex(groups).to_numpy(dtype=float)[:, None]
    nz = frac * sizes
    out_frac = (nz.sum(0, keepdims=True) - nz) / (sizes.sum() - sizes)
    fi = pd.DataFrame(frac, index=groups, columns=found)
    fo = pd.DataFrame(out_frac, index=groups, columns=found)
    de['pct_in'] = [fi.at[c, g] if g in fi.columns else np.nan for c, g in zip(de['cluster'], de['gene'])]
    de['pct_out'] = [fo.at[c, g] if g in fo.columns else np.nan for c, g in zip(de['cluster'], de['gene'])]
    return de


def marker_tables(adata, M, found, key, markers, min_frac=0.02):
    if not found:
        return pd.DataFrame(), pd.DataFrame()
    groups, mean, frac = group_mean_frac(M, adata.obs[key].to_numpy())
    sd = mean.std(0, ddof=0)
    z = (mean - mean.mean(0)) / np.where(sd > 0, sd, 1)
    # A marker detected in almost no cells of a cluster must not raise that cluster's score
    # (a gene seen in 4 nuclei can still give z > 2 when every other cluster is at 0).
    z = np.where(frac >= min_frac, z, np.minimum(z, 0))
    long = []
    col = {g: i for i, g in enumerate(found)}
    for _, m in markers.iterrows():
        if m['gene_id'] not in col:
            continue
        j = col[m['gene_id']]
        for i, cl in enumerate(groups):
            long.append({'cluster': cl, 'cell_type': m['cell_type'], 'gene_id': m['gene_id'],
                         'symbol': m['symbol'], 'evidence': m['evidence'],
                         'mean': mean[i, j], 'frac': frac[i, j], 'z': z[i, j]})
    long = pd.DataFrame(long).drop_duplicates(['cluster', 'cell_type', 'gene_id'])
    long['is_function'] = long['evidence'] == 'function'
    scores = (long.groupby(['cluster', 'cell_type'])
              .agg(score=('z', 'mean'), frac=('frac', 'mean'), n_markers=('gene_id', 'nunique'),
                   n_function=('is_function', 'sum'))
              .reset_index())
    return long, scores


def composition(adata, key, meta):
    out = {}
    lab = adata.obs[key].astype(str)
    for m in meta:
        if m not in adata.obs.columns:
            continue
        ct = pd.crosstab(lab, adata.obs[m].astype(str), normalize='index')
        glob = adata.obs[m].astype(str).value_counts(normalize=True)
        out[m] = (ct, glob)
    return out


def hierarchy(adata, keys):
    keys = sorted(keys, key=resolution_of)
    rows = []
    for k in keys:
        lab = adata.obs[k].astype(str)
        for cl, n in lab.value_counts().items():
            row = {'key': k, 'cluster': cl, 'n_cells': int(n)}
            mask = (lab == cl).to_numpy()
            for coarse in keys:
                if coarse == k or resolution_of(coarse) >= resolution_of(k):
                    continue
                vc = adata.obs.loc[mask, coarse].astype(str).value_counts(normalize=True)
                row[f'parent_{coarse}'] = f"{vc.index[0]} ({vc.iloc[0]:.0%})"
            rows.append(row)
    df = pd.DataFrame(rows)
    df['_o'] = df['cluster'].map(natural_key)
    df['_k'] = df['key'].map(resolution_of)
    return df.sort_values(['_k', '_o']).drop(columns=['_o', '_k'])


def write_markdown(path, key, adata, de, long, scores, comp, hier, qc_cols, gm, n_show, ann=None, min_frac=0.02,
                   stress=None, stress_flag=0.4, stress_inactive=False):
    lab = adata.obs[key].astype(str)
    sizes = lab.value_counts()
    qc_glob = {k: adata.obs[c].median() for k, c in qc_cols.items()}
    with open(path, 'w') as f:
        f.write(f"# Cluster evidence: `{key}` ({len(sizes)} clusters, {adata.n_obs:,} cells)\n\n")
        f.write("Marker score = mean z (across clusters) of a cell type's marker genes' cluster means; "
                "frac = mean fraction of cells expressing those markers. "
                "`*` = marker with function evidence (characterized cell-type function).\n")
        f.write(f"Scores are capped by the number of clusters: the largest possible z with {len(sizes)} "
                f"clusters is ~{np.sqrt(max(len(sizes) - 1, 1)):.1f}. Compare scores within this key, not across keys "
                f"or subclusterings. A marker counts toward a cluster's score only if >= {min_frac:.0%} of its cells "
                f"express it.\n")
        if stress:
            f.write(f"Stress = fraction of the top {n_show} DE genes on the protoplasting-induced list "
                    f"(flagged at >= {stress_flag:.0%}).\n")
            if stress_inactive:
                f.write("**Stress check inactive**: the stress list matched no gene in this dataset (no gene map "
                        "to Arabidopsis); stress fractions below are not informative.\n")
        if qc_cols:
            f.write('QC shown as cluster median / dataset median: '
                    + ', '.join(f"{k}={qc_glob[k]:.3g} ({c})" for k, c in qc_cols.items()) + '\n')
        f.write('\n')
        for cl in sorted(sizes.index, key=natural_key):
            n = int(sizes[cl])
            f.write(f"## {key} cluster {cl}: {n:,} cells ({n / adata.n_obs:.1%})\n")
            mask = (lab == cl).to_numpy()
            flags = []
            for m, (ct, glob) in comp.items():
                row = ct.loc[cl]
                parts = []
                for lvl in row.sort_values(ascending=False).index:
                    enr = row[lvl] / glob[lvl] if glob[lvl] > 0 else np.nan
                    parts.append(f"{lvl} {row[lvl]:.0%}" + (f" (x{enr:.1f})" if enr >= 1.5 else ''))
                    if row[lvl] >= 0.8 and glob[lvl] < 0.5:
                        flags.append(f"{m}={lvl} dominates ({row[lvl]:.0%})")
                    elif enr >= 2 and row[lvl] >= 0.2:
                        flags.append(f"{m}={lvl} enriched x{enr:.1f}")
                f.write(f"- **{m}**: " + ', '.join(parts) + '\n')
            if qc_cols:
                qparts = []
                for k, c in qc_cols.items():
                    med = adata.obs.loc[mask, c].median()
                    ratio = med / qc_glob[k] if qc_glob[k] else np.nan
                    qparts.append(f"{k} {med:.3g} (x{ratio:.2f})")
                    if k in ('counts', 'genes') and ratio < 0.6:
                        flags.append(f"low {k}")
                f.write('- **QC**: ' + ', '.join(qparts) + '\n')
            d = de[de['cluster'] == cl].head(n_show) if not de.empty else pd.DataFrame()
            if stress and len(d):
                sfrac, shit = stress_fraction(list(d['gene']), gm, stress)
                f.write(f"- **Stress**: {shit}/{len(d)} top DE genes protoplasting-induced ({sfrac:.0%})\n")
                if sfrac >= stress_flag:
                    flags.append(f"dissociation-stress signature ({sfrac:.0%} of top DE)")
            if hier is not None:
                h = hier[(hier['key'] == key) & (hier['cluster'] == cl)]
                pcols = [c for c in h.columns if c.startswith('parent_') and h[c].notna().any()]
                if len(h) and pcols:
                    f.write('- **Parents**: ' + ', '.join(f"{c[7:]}={h.iloc[0][c]}" for c in pcols) + '\n')
            if flags:
                f.write('- **FLAGS**: ' + '; '.join(flags) + '\n')
            if not scores.empty:
                s = scores[scores['cluster'] == cl].sort_values('score', ascending=False).head(4)
                STATE_TYPES = {'s_phase', 'dividing_cells', 'g2_m', 'g2m', 'senescing', 'protoplasting_stress'}
                hi = s[(s['score'] >= 1) & ~s['cell_type'].str.lower().isin(STATE_TYPES)]
                cratio = None
                if 'counts' in qc_cols and qc_glob.get('counts'):
                    cratio = adata.obs.loc[mask, qc_cols['counts']].median() / qc_glob['counts']
                if len(hi) >= 2 and cratio is not None and cratio >= 1.3:
                    flags.append(f"possible doublets: {hi.iloc[0]['cell_type']} + {hi.iloc[1]['cell_type']} "
                                 f"both score >= 1 and counts x{cratio:.2f}")
                    f.write('- **FLAGS**: ' + flags[-1] + '\n')
                parts = []
                for r in s.itertuples():
                    top = (long[(long['cluster'] == cl) & (long['cell_type'] == r.cell_type)]
                           .sort_values('z', ascending=False).head(3))
                    oth = long[(long['cluster'] != cl) & (long['cell_type'] == r.cell_type)]
                    fout = oth.groupby('gene_id')['frac'].mean()
                    drv = ','.join(f"{t.symbol}{'*' if t.is_function else ''}:{t.z:.1f} "
                                   f"({t.frac:.0%} vs {fout.get(t.gene_id, 0):.0%})"
                                   for t in top.itertuples())
                    parts.append(f"{r.cell_type} {r.score:.2f} (frac {r.frac:.2f}; {drv})")
                f.write('- **Marker scores**: ' + ' | '.join(parts) + '\n')
            if len(d):
                f.write('\n| gene | logFC | pct in/out | homolog |\n|---|---|---|---|\n')
                for r in d.itertuples():
                    f.write(f"| {r.gene} | {r.logfc:+.2f} | {r.pct_in:.2f}/{r.pct_out:.2f} | "
                            f"{homolog_str(r.gene, gm, ann=ann)} |\n")
            f.write('\n')


def rasterize(ax):
    for ch in ax.get_children():
        if hasattr(ch, 'set_rasterized'):
            ch.set_rasterized(True)


def plots(adata, keys, markers, pdf_path, use_raw, layer):
    has_umap = 'X_umap' in adata.obsm
    with PdfPages(pdf_path) as pdf:
        for key in keys:
            if has_umap:
                fig, ax = plt.subplots(figsize=(9, 8))
                sc.pl.umap(adata, color=key, ax=ax, show=False, legend_loc='on data',
                           legend_fontsize=7, size=max(1, 120000 / adata.n_obs), title=key)
                rasterize(ax)
                pdf.savefig(fig, dpi=150)
                plt.close('all')
            if markers is not None and len(markers):
                var_src = adata.var_names if (layer or adata.raw is None or use_raw == 'no') \
                    else adata.raw.var_names
                mk = markers[markers['gene_id'].isin(var_src)].drop_duplicates('gene_id')
                if mk.empty:
                    continue
                groups = {}
                for ct, sub in mk.groupby('cell_type', sort=True):
                    groups[ct] = list(sub['gene_id'])
                try:
                    kw = dict(layer=layer, use_raw=False) if layer else \
                        dict(use_raw=(adata.raw is not None and use_raw != 'no'))
                    dp = sc.pl.dotplot(adata, groups, groupby=key, show=False,
                                       standard_scale='var', return_fig=True, **kw)
                    dp.make_figure()
                    fig = plt.gcf()
                    fig.suptitle(f'Markers by {key} (scaled per gene)')
                    pdf.savefig(fig, bbox_inches='tight')
                except Exception as e:  # plotting must never kill the evidence run
                    print(f'  WARN dotplot for {key} failed: {e}')
                plt.close('all')


# ----------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--cluster-keys', nargs='+', default=None,
                   help="obs columns to evaluate (default: all starting with 'leiden')")
    p.add_argument('--markers', nargs='+', default=None,
                   help='one or more marker tables (gene_id, symbol, cell_type[, evidence])')
    p.add_argument('--stress-genes', default=None,
                   help='gene list (one ID per line) of dissociation-induced genes, in target or reference '
                        'IDs, e.g. references/stress/protoplasting_induced_Shahan2022.txt')
    p.add_argument('--stress-flag', type=float, default=0.4,
                   help='flag clusters whose top DE genes are at least this fraction stress genes')
    p.add_argument('--gene-map', default=None, help='gene_map.tsv from map_markers.py')
    p.add_argument('--gene-annotation', default=None,
                   help='gene_id<TAB>symbol<TAB>description for the dataset species (e.g. Phytozome annotation_info '
                        'columns); names DE genes when there is no gene map (same-species runs)')
    p.add_argument('--min-frac', type=float, default=0.02,
                   help='a marker contributes positive z to a cluster only if this fraction of its cells express it')
    p.add_argument('--meta-keys', nargs='*', default=['sample'],
                   help='obs columns for composition (sample, treatment, ...)')
    p.add_argument('--layer', default=None, help='log-normalized layer to use instead of raw/X')
    p.add_argument('--use-raw', choices=['auto', 'yes', 'no'], default='auto')
    p.add_argument('--n-top', type=int, default=25, help='DE genes stored per cluster')
    p.add_argument('--n-show', type=int, default=15, help='DE genes shown per cluster in markdown')
    p.add_argument('--max-cells-per-cluster', type=int, default=2000,
                   help='subsample for Wilcoxon (0 = all cells)')
    p.add_argument('--skip-de', action='store_true')
    p.add_argument('--skip-plots', action='store_true')
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--import-labels', action='append', default=[],
                   help='path:col[:new_name] (repeatable), as in apply_annotations.py; e.g. '
                        'published per-cell labels to evaluate. Pass the new name in --cluster-keys')
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    print(f'[1] Loading {args.h5ad}')
    adata = sc.read_h5ad(args.h5ad)
    print(f'  {adata.n_obs:,} cells x {adata.n_vars:,} genes')
    if 'log1p' in adata.uns and 'base' not in adata.uns['log1p']:
        adata.uns['log1p']['base'] = None
    if args.import_labels:
        from apply_annotations import import_labels
        for spec in args.import_labels:
            import_labels(adata, spec)

    keys = args.cluster_keys or [c for c in adata.obs.columns if c.startswith('leiden')]
    keys = [k for k in keys if k in adata.obs.columns]
    if not keys:
        raise SystemExit('No cluster keys found; pass --cluster-keys')
    keys = sorted(dict.fromkeys(keys), key=resolution_of)
    print(f'  cluster keys: {keys}')

    X, var_names, src = expression_source(adata, args.layer, args.use_raw)
    xmin = X.min() if not sparse.issparse(X) else X.data.min() if X.nnz else 0
    xmax = X.max() if not sparse.issparse(X) else X.data.max() if X.nnz else 0
    print(f'  expression from {src}: min={xmin:.3g} max={xmax:.3g}')
    if xmin < 0:
        print('  WARN negative values: this looks scaled; use --layer or ensure .raw holds log-normalized data')
    if xmax > 50:
        print('  WARN max > 50: this may be raw counts, not log-normalized')
    hv = adata.var['highly_variable'] if 'highly_variable' in adata.var.columns and src == 'X' else None
    if len(var_names) < 12000 or (hv is not None and bool(hv.all())):
        print(f'  WARN only {len(var_names):,} genes in {src}: the gene list looks filtered upstream (HVGs or a '
              f'min-cells cut). Markers outside it read as missing, not absent; use the unfiltered object, '
              f'.raw or --layer if available')

    markers = load_markers(args.markers) if args.markers else None
    if markers is not None:
        present = markers['gene_id'].isin(var_names) | \
            markers['gene_id'].map(lambda g: f'{g}_expr' in adata.obs.columns)
        print(f'  markers: {present.sum()}/{len(markers)} found')
        if (~present).any():
            print('  WARN markers not in the data (not expressed, filtered, or ID mismatch), by cell type:')
            for ct, g in markers[~present].groupby('cell_type'):
                print(f"    {ct:24s} " + ', '.join(f"{s}({i})" if s != i else i
                                                   for s, i in zip(g['symbol'], g['gene_id'])))
        none_left = sorted(set(markers['cell_type']) - set(markers.loc[present, 'cell_type']))
        if none_left:
            print('  WARN cell types with NO marker present in the data: ' + ', '.join(none_left))
        markers = markers[present]

    gm = load_gene_map(args.gene_map) if args.gene_map else None
    if gm is not None:
        rate = var_names.isin(gm.index).mean()
        print(f'  gene map covers {rate:.1%} of expression var_names')
        if rate < 0.5:
            print('  WARN <50% of var_names found in gene map: check --query-strip-regex in map_markers.py')

    ann = load_gene_annotation(args.gene_annotation) if args.gene_annotation else None
    if ann is not None:
        print(f'  gene annotation covers {var_names.isin(ann.index).mean():.1%} of var_names')
    stress = load_stress_genes(args.stress_genes) if args.stress_genes else None
    stress_inactive = False
    if stress:
        ids = set(map(str.upper, var_names))
        if gm is not None:
            ids |= set(gm['ref_gene'].astype(str).str.upper())
        n_match = len(stress & ids)
        print(f'  stress genes: {len(stress):,} ({n_match} matchable in this dataset)')
        if n_match == 0:
            stress_inactive = True
            print('  WARN the stress list matches no gene here (it uses Arabidopsis IDs; pass --gene-map from a '
                  'BLAST run to match through homologs). The stress check is inactive.')

    meta = [m for m in args.meta_keys if m in adata.obs.columns]
    qc_cols = {k: c for k, c in ((k, pick(adata.obs, v)) for k, v in QC_CANDIDATES.items()) if c}
    print(f'  meta: {meta}; QC cols: {qc_cols}')

    if markers is not None:
        Mk, mk_found = gene_matrix(adata, X, var_names, markers['gene_id'])

    print('[2] Cluster hierarchy')
    hier = hierarchy(adata, keys)
    hier.to_csv(os.path.join(args.output, 'cluster_hierarchy.tsv'), sep='\t', index=False)

    for key in keys:
        print(f'[3] {key}: {adata.obs[key].nunique()} clusters')
        de = pd.DataFrame()
        if not args.skip_de:
            de = run_de(adata, key, args.n_top, args.max_cells_per_cluster,
                        args.use_raw, args.layer, args.seed)
            de = add_pct(de, adata, X, var_names, key)
            if gm is not None and not de.empty:
                j = gm.reindex(de['gene'])
                de['ref_gene'] = j['ref_gene'].to_numpy()
                de['ref_symbol'] = j['ref_symbol'].to_numpy()
                de['ref_description'] = j['ref_description'].to_numpy()
                de['pident'] = j['pident'].to_numpy()
            de.to_csv(os.path.join(args.output, f'de_{key}.csv'), index=False)
        long, scores = (marker_tables(adata, Mk, mk_found, key, markers, args.min_frac)
                        if markers is not None else (pd.DataFrame(), pd.DataFrame()))
        if not long.empty:
            long.to_csv(os.path.join(args.output, f'marker_expression_{key}.tsv'),
                        sep='\t', index=False, float_format='%.4g')
            wide = scores.pivot(index='cluster', columns='cell_type', values='score')
            wide = wide.loc[sorted(wide.index, key=natural_key)]
            wide.to_csv(os.path.join(args.output, f'marker_scores_{key}.tsv'),
                        sep='\t', float_format='%.3f')
        comp = composition(adata, key, meta)
        write_markdown(os.path.join(args.output, f'cluster_evidence_{key}.md'), key, adata,
                       de, long, scores, comp, hier, qc_cols, gm, args.n_show, ann=ann, min_frac=args.min_frac,
                       stress=stress, stress_flag=args.stress_flag, stress_inactive=stress_inactive)
        print(f'  wrote cluster_evidence_{key}.md')

    if not args.skip_plots:
        print('[4] Plots')
        plots(adata, keys, markers, os.path.join(args.output, 'evidence_plots.pdf'),
              args.use_raw, args.layer)
    print('Done.')


if __name__ == '__main__':
    main()
