#!/usr/bin/env python3
"""Per-cell-type evidence report (PDF) for an applied annotation.

Run after apply_annotations.py. One page per annotated cell type, showing the
strongest marker evidence present in the data:
  - UMAP highlighting the cell type
  - per marker: expression UMAP (viridis), violins across the clusters of the key
    that defined the label (annotated clusters highlighted), and a text panel with
    the marker's evidence tier, homology, basis, and in-data enrichment
  - the annotation table's Evidence text for the rows that produced the label
Markers are chosen by quality first (confidence, then evidence tier), among
markers actually enriched in the cell type. Up to --max-markers are shown, so a
page has at least one high-confidence marker or 2-3 weaker ones when that is
all there is. Cell types with no enriched marker fall back to top DE genes,
labeled as data-driven. Front pages: overview UMAP + summary table. Last page:
dotplot of the shown markers by cell type.
"""

import argparse
import os
import re
import sys
import textwrap
import warnings

import numpy as np
import pandas as pd
import scanpy as sc
from scipy import sparse

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec

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


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cluster_evidence import (expression_source, gene_matrix, load_gene_map, load_markers,  # noqa: E402
                              natural_key, homolog_str)
from apply_annotations import (parse_annotations, resolve_key, semantic_color,  # noqa: E402
                               FALLBACK_COLORS)

warnings.filterwarnings('ignore')
sc.settings.verbosity = 1

HIGHLIGHT = '#D55E00'   # ito vermillion: annotated cells / clusters
BACKGROUND = '#C8C8C8'  # other cells / clusters
ITO = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#56B4E9', '#E69F00', '#F0E442']
SPARSE_RATIO = 3.0      # detection ratio (in/out) for the sparse-marker route
SPARSE_MIN_FRAC = 0.02  # ...with at least 2% of the cell type expressing
STRONG_DELTA = 1.0      # level route: a >= 1 log-unit (~2.7x) mean gap for genes detected nearly everywhere
STRONG_MIN_FRAC = 0.5   # ...with at least half of the cell type expressing
CONF = {'high': 2, 'medium': 1, 'low': 0}
TIER = {'function': 2, 'characterized_enriched': 1, 'expression': 0}

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': False,
    'xtick.direction': 'out', 'ytick.direction': 'out', 'axes.edgecolor': 'black',
    'axes.labelcolor': 'black', 'xtick.color': 'black', 'ytick.color': 'black',
    'pdf.fonttype': 42, 'figure.facecolor': 'white',
})


# ----------------------------------------------------------------------------

def ct_colors(adata, key, colors_file):
    """Precedence: --colors file > semantic default > colors stored in uns > fallback."""
    cats = list(adata.obs[key].cat.categories)
    user = {}
    if colors_file:
        cdf = pd.read_csv(colors_file, sep='\t')
        user = dict(zip(cdf['CellType'], cdf['Color']))
    uns = {}
    if f'{key}_colors' in adata.uns and len(adata.uns[f'{key}_colors']) == len(cats):
        uns = dict(zip(cats, adata.uns[f'{key}_colors']))
    fb = iter(FALLBACK_COLORS + [matplotlib.colors.to_hex(c) for c in plt.get_cmap('tab20').colors])
    return {c: user.get(c) or semantic_color(c) or uns.get(c) or next(fb) for c in cats}


def umap_axes(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_aspect('equal', adjustable='datalim')


def plot_highlight(ax, um, mask, color, size):
    ax.scatter(um[~mask, 0], um[~mask, 1], s=size, c=BACKGROUND, lw=0, rasterized=True)
    # Rare types (a few hundred guard cells) vanish at background point size: scale up
    n = int(mask.sum())
    hs = size * 1.5 if n >= 2000 else max(size * 1.5, 3.0 if n >= 500 else 6.0)
    ax.scatter(um[mask, 0], um[mask, 1], s=hs, c=color, lw=0, rasterized=True)
    umap_axes(ax)


def plot_expr_umap(ax, um, v, size, label):
    # Non-expressing cells in light grey underneath; viridis only for detected expression,
    # sorted so the highest values sit on top (sparse markers would vanish in dark purple).
    zero = v <= 0
    ax.scatter(um[zero, 0], um[zero, 1], s=size, c=BACKGROUND, lw=0, rasterized=True)
    nzi = np.flatnonzero(~zero)
    nzi = nzi[np.argsort(v[nzi])]
    vmax = np.percentile(v[nzi], 99) if len(nzi) else 1.0
    sca = ax.scatter(um[nzi, 0], um[nzi, 1], s=size * 1.5, c=v[nzi], cmap='viridis',
                     vmin=0, vmax=max(vmax, 1e-3), lw=0, rasterized=True)
    umap_axes(ax)
    cb = plt.colorbar(sca, ax=ax, fraction=0.04, pad=0.01)
    cb.ax.tick_params(labelsize=6)
    cb.outline.set_visible(False)
    ax.text(0.0, 1.0, label, transform=ax.transAxes, ha='left', va='bottom', fontsize=8,
            fontweight='bold')


def plot_violins(ax, v, labels, highlight, max_cells, rng):
    groups = sorted([g for g in pd.unique(labels) if g != 'nan'], key=natural_key)
    data, cols = [], []
    for g in groups:
        idx = np.flatnonzero(labels == g)
        if len(idx) > max_cells:
            idx = rng.choice(idx, max_cells, replace=False)
        vals = v[idx]
        data.append(vals if len(vals) > 1 and np.ptp(vals) > 0 else np.r_[vals, vals + 1e-6])
        cols.append(HIGHLIGHT if g in highlight else BACKGROUND)
    parts = ax.violinplot(data, showextrema=False, widths=0.85)
    for body, c in zip(parts['bodies'], cols):
        body.set_facecolor(c)
        body.set_edgecolor('none')
        body.set_alpha(1.0)
    fracs = [(d > 0).mean() for d in data]
    ax.scatter(np.arange(1, len(groups) + 1), [np.mean(d) for d in data], s=6, c='black', zorder=3)
    ax.set_xticks(np.arange(1, len(groups) + 1))
    ax.set_xticklabels(groups, fontsize=6, rotation=90 if len(groups) > 12 else 0)
    for t, g in zip(ax.get_xticklabels(), groups):
        if g in highlight:
            t.set_color(HIGHLIGHT)
            t.set_fontweight('bold')
    ax.set_ylabel('log expr', fontsize=7)
    ax.tick_params(labelsize=6)
    return dict(zip(groups, fracs))


def text_panel(ax, lines, width=40):
    """Wrapped text that always fits its axes: the font shrinks (and wrap width grows) with line count."""
    ax.axis('off')

    def wrap(w):
        out = []
        for ln in lines:
            bold = ln.startswith('**')
            ln = ln.strip('*')
            wrapped = textwrap.wrap(ln, w) or ['']
            out.extend([(t, bold and i == 0) for i, t in enumerate(wrapped)])
        return out

    out, fs = wrap(width), 7.0
    for _ in range(4):
        step = min(0.075, 0.98 / max(len(out), 1))
        fs = 7 if step >= 0.06 else max(4.5, 7 * step / 0.075)
        new = wrap(int(width * 7 / fs))
        if len(new) == len(out):
            break
        out = new
    step = min(0.075, 0.98 / max(len(out), 1))
    y = 1.0
    for txt, bold in out:
        ax.text(0, y, txt, transform=ax.transAxes, va='top', ha='left', fontsize=fs,
                fontweight='bold' if bold else 'normal', family='sans-serif', clip_on=True)
        y -= step


# ----------------------------------------------------------------------------

def skill_version():
    """Skill version from the VERSION file next to scripts/ (shown in the report so outputs can be traced)."""
    try:
        return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'VERSION')).read().strip()
    except OSError:
        return 'unknown'


def marker_stats(M, found, mask):
    """Per-gene mean/frac inside vs outside mask."""
    def mean_frac(A):
        if sparse.issparse(A):
            mean = np.asarray(A.mean(0)).ravel()
            frac = np.asarray((A > 0).mean(0)).ravel()
        else:
            mean, frac = A.mean(0), (A > 0).mean(0)
        return mean, frac
    mi, fi = mean_frac(M[mask])
    mo, fo = mean_frac(M[~mask])
    return pd.DataFrame({'gene_id': found, 'mean_in': mi, 'mean_out': mo, 'frac_in': fi, 'frac_out': fo})


def candidate_markers(markers, ct, aliases):
    """Exact cell-type matches first, then related ones (alias or name-token subset)."""
    names = aliases.get(ct)
    exact = markers[markers['cell_type'] == ct].assign(match='exact')
    if names:
        rel = markers[markers['cell_type'].isin(names)].assign(match='alias')
    else:
        toks = set(ct.lower().split('_'))
        rel = markers[markers['cell_type'].map(
            lambda c: c != ct and set(c.lower().split('_')) <= toks)].assign(match='related')
    return pd.concat([exact, rel], ignore_index=True)


def select_markers(cand, stats, n_max, min_delta, min_frac_ratio):
    if cand.empty:
        return cand, cand
    c = cand.merge(stats, on='gene_id', how='inner')
    c['delta'] = c['mean_in'] - c['mean_out']
    c['ratio'] = c['frac_in'] / np.maximum(c['frac_out'], 0.001)
    # Routes to "enriched": a clear expression gap, or a strong detection ratio for sparsely
    # captured regulators/channels (tomato guard cells: FAMA 12% vs 0.0%, SLAC1 3.6% vs 0.0%;
    # mean gaps only 0.06-0.18). The detection floor keeps noise-level genes out.
    c['enriched'] = (((c['delta'] >= min_delta) & (c['ratio'] >= min_frac_ratio))
                     | ((c['ratio'] >= SPARSE_RATIO) & (c['frac_in'] >= SPARSE_MIN_FRAC))
                     # Third route: abundant genes detected in most nuclei everywhere (ambient-rich nuclei data),
                     # enriched by level only (an inulin enzyme in 94% vs 70% of nuclei, mean 3.5 vs 2.0).
                     | ((c['delta'] >= STRONG_DELTA) & (c['frac_in'] >= STRONG_MIN_FRAC)))
    c['q_conf'] = c['confidence'].map(CONF).fillna(0)
    c['q_tier'] = c['evidence'].map(TIER).fillna(0)
    c['q_match'] = (c['match'] == 'exact').astype(int)
    c = c.sort_values(['q_match', 'q_conf', 'q_tier', 'delta'], ascending=False, kind='mergesort')
    c = c.drop_duplicates('gene_id')
    good = c[c['enriched']]
    # Paralog copies mapped from one reference locus share a symbol: show only the best copy.
    good = good.drop_duplicates('symbol')
    # Show the best markers; never let a related-type marker displace an exact one
    shown = good.head(n_max)
    not_enriched = c[~c['enriched'] & (c['match'] == 'exact')]
    return shown, not_enriched


def de_fallback(adata, key, cts, n_genes, use_raw, max_cells, rng):
    if not cts:
        return {}
    labels = adata.obs[key].astype(str)
    keep = []
    for g, idx in labels.groupby(labels).indices.items():
        if len(idx) > max_cells:
            idx = rng.choice(idx, max_cells, replace=False)
        keep.append(idx)
    sub = adata[np.sort(np.concatenate(keep))].copy()
    sub.obs[key] = pd.Categorical(sub.obs[key].astype(str))
    if 'log1p' in sub.uns and 'base' not in sub.uns['log1p']:
        sub.uns['log1p']['base'] = None
    sc.tl.rank_genes_groups(sub, key, groups=cts, method='wilcoxon', n_genes=n_genes,
                            use_raw=(sub.raw is not None and use_raw != 'no'), key_added='rgg_rep')
    res = sub.uns['rgg_rep']
    return {g: list(res['names'][g]) for g in res['names'].dtype.names}


# ----------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True, help='annotated h5ad (output of apply_annotations.py)')
    p.add_argument('--key', default='cell_type')
    p.add_argument('--annotations', required=True, help='annotation table used to label the cells')
    p.add_argument('--markers', nargs='+', required=True, help='target marker table(s) from map_markers.py')
    p.add_argument('--gene-map', default=None, help='gene_map.tsv, for homolog labels on DE fallbacks')
    p.add_argument('--colors', default=None, help='CellType<TAB>Color table')
    p.add_argument('--alias', action='append', default=[],
                   help='AnnotatedType=MarkerType1,MarkerType2 (repeatable): marker cell types to use '
                        'for a differently named annotation, e.g. Procambium_Dividing=Procambium,Dividing_cells')
    p.add_argument('--output', required=True, help='report PDF path')
    p.add_argument('--title', default=None)
    p.add_argument('--unknown-label', default='Unknown')
    p.add_argument('--max-markers', type=int, default=3)
    p.add_argument('--qc-labels', default=r'(?i)^(low_quality|doublet|unresolved|ambient|exclude|qc_)',
                   help='regex for labels that are QC classes, not cell types (no page); "" to disable')
    p.add_argument('--min-delta', type=float, default=0.25,
                   help='min difference in mean log expression (in - out) to count as enriched')
    p.add_argument('--min-frac-ratio', type=float, default=1.5,
                   help='min ratio of fraction expressing (in / out) to count as enriched')
    p.add_argument('--max-cells-violin', type=int, default=1500)
    p.add_argument('--layer', default=None)
    p.add_argument('--use-raw', choices=['auto', 'yes', 'no'], default='auto')
    p.add_argument('--seed', type=int, default=0)
    args = p.parse_args()

    rng = np.random.default_rng(args.seed)
    print(f'[1] Loading {args.h5ad}')
    adata = sc.read_h5ad(args.h5ad)
    if args.key not in adata.obs.columns:
        sys.exit(f'{args.key} not in obs; run apply_annotations.py first')
    if not hasattr(adata.obs[args.key], 'cat'):
        adata.obs[args.key] = pd.Categorical(adata.obs[args.key].astype(str))
    if 'X_umap' not in adata.obsm:
        sys.exit('X_umap missing')
    um = adata.obsm['X_umap']
    size = max(0.3, min(4.0, 60000 / adata.n_obs))
    X, var_names, src = expression_source(adata, args.layer, args.use_raw)
    print(f'  {adata.n_obs:,} cells; expression from {src}')

    ann = parse_annotations(args.annotations)
    ann['obs_key'] = [resolve_key(s, set(adata.obs.columns)) for s in ann['key_spec']]
    markers = load_markers(args.markers)
    for c in ['evidence', 'confidence', 'basis', 'ref_gene', 'hit_rank', 'pident', 'rbh', 'via', 'source']:
        if c not in markers.columns:
            markers[c] = ''
    gm = load_gene_map(args.gene_map) if args.gene_map else None
    aliases = {}
    for a in args.alias:
        k, v = a.split('=', 1)
        aliases[k] = [x for x in v.split(',') if x]
    pal = ct_colors(adata, args.key, args.colors)

    labels = adata.obs[args.key].astype(str).to_numpy()
    cts = [c for c in adata.obs[args.key].cat.categories if c != args.unknown_label and (labels == c).any()]
    qc_re = re.compile(args.qc_labels) if args.qc_labels else None
    qc_cts = [c for c in cts if qc_re and qc_re.search(c)]
    if qc_cts:
        print(f'  QC classes (listed on the overview, no page): {qc_cts}')
    cts = [c for c in cts if c not in qc_cts]
    # Most abundant cell type first (overview table, pages, dotplot), not alphabetical
    n_by = pd.Series(labels).value_counts()
    cts = sorted(cts, key=lambda c: (-n_by.get(c, 0), natural_key(c)))
    qc_cts = sorted(qc_cts, key=lambda c: (-n_by.get(c, 0), natural_key(c)))
    Mk, mk_found = gene_matrix(adata, X, var_names, markers['gene_id'])
    Mk = Mk.tocsr() if sparse.issparse(Mk) else Mk
    col = {g: i for i, g in enumerate(mk_found)}
    print(f'  {len(cts)} cell types; {len(mk_found)} marker genes in data')

    # ---- per cell type: choose key, clusters, markers
    plans = {}
    need_de = []
    for ct in cts:
        mask = labels == ct
        rows = ann[ann['cell_type'].str.lower() == ct.lower()]  # apply_annotations may re-case names
        best_key, best_n, clusters = None, -1, []
        for k, sub in rows.groupby('obs_key'):
            if not k:
                continue
            kl = adata.obs[k].astype(str).to_numpy()
            cls = [c.strip() for v in sub['cluster'].astype(str) for c in v.split(',') if c.strip()]
            n = int((mask & np.isin(kl, cls)).sum())
            if n > best_n:
                best_key, best_n, clusters = k, n, cls
        stats = marker_stats(Mk, mk_found, mask) if mk_found else pd.DataFrame(columns=['gene_id'])
        shown, not_enriched = select_markers(candidate_markers(markers, ct, aliases), stats,
                                             args.max_markers, args.min_delta, args.min_frac_ratio)
        plans[ct] = dict(mask=mask, key=best_key, clusters=clusters, rows=rows, shown=shown,
                         not_enriched=not_enriched)
        if shown.empty:
            need_de.append(ct)
    print(f'  DE fallback for: {need_de}')
    de = de_fallback(adata, args.key, need_de, 10, args.use_raw, 2000, rng)

    # ---- PDF
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    summary = []
    shown_all = {}
    with PdfPages(args.output) as pdf:
        # Overview page
        fig = plt.figure(figsize=(8.5, 11))
        gs = GridSpec(2, 1, height_ratios=[1.25, 1], figure=fig, hspace=0.1)
        ax = fig.add_subplot(gs[0])
        for ct in list(adata.obs[args.key].cat.categories):
            m = labels == ct
            c = BACKGROUND if ct == args.unknown_label else pal[ct]
            ax.scatter(um[m, 0], um[m, 1], s=size, c=c, lw=0, rasterized=True, label=ct)
            if ct != args.unknown_label and m.sum():
                cx, cy = np.median(um[m, 0]), np.median(um[m, 1])
                ax.text(cx, cy, ct, fontsize=7, ha='center', va='center', color='black',
                        bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.7))
        umap_axes(ax)
        # Direct labels identify cell types (colors alone cannot separate 10+ types for all
        # readers); only the Unknown grey needs a key.
        ax.text(0.0, 0.0, f'grey = {args.unknown_label}', transform=ax.transAxes, fontsize=7,
                color='#555555', ha='left', va='bottom')
        fig.text(0.06, 0.97, args.title or f'Cell-type annotation report: {os.path.basename(args.h5ad)}',
                 fontsize=11, fontweight='bold')
        fig.text(0.06, 0.955, f'{adata.n_obs:,} cells; annotation table {os.path.basename(args.annotations)}; '
                 f'markers {", ".join(os.path.basename(m) for m in args.markers)}; '
                 f'plant-celltype-annotation v{skill_version()}', fontsize=7)
        axt = fig.add_subplot(gs[1])
        axt.axis('off')
        for ct in cts:
            pl = plans[ct]
            sh = pl['shown']
            best = (f"{sh.iloc[0]['symbol']} ({sh.iloc[0]['evidence']}, {sh.iloc[0]['confidence']})"
                    if len(sh) else 'none enriched: DE only')
            summary.append([ct, f"{pl['mask'].sum():,}", f"{pl['mask'].mean():.1%}", str(len(sh)), best])
        for ct in qc_cts:
            m = labels == ct
            summary.append([ct, f"{m.sum():,}", f"{m.mean():.1%}", '-', 'QC class (no page)'])
        if summary:
            tbl = axt.table(cellText=summary, colLabels=['Cell type', 'Cells', '%', 'Markers', 'Strongest marker'],
                            loc='upper center', cellLoc='left', colLoc='left',
                            colWidths=[0.25, 0.1, 0.08, 0.08, 0.49])
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(7)
            for (r, c), cell in tbl.get_celld().items():
                cell.set_edgecolor('#DDDDDD')
                if r == 0:
                    cell.set_text_props(fontweight='bold')
        pdf.savefig(fig)
        plt.close(fig)

        # One page per cell type
        for ct in cts:
            pl = plans[ct]
            mask, key, clusters = pl['mask'], pl['key'], pl['clusters']
            sh = pl['shown']
            fallback = sh.empty
            genes = list(sh['gene_id']) if not fallback else [g for g in de.get(ct, []) if g in var_names][:2]
            n_rows = max(1, len(genes))
            fig = plt.figure(figsize=(8.5, 11))
            gs = GridSpec(1 + n_rows, 3, figure=fig, height_ratios=[1.6] + [1] * n_rows,
                          width_ratios=[1, 1.25, 1.15], hspace=0.4, wspace=0.3,
                          left=0.05, right=0.97, top=0.93, bottom=0.05)
            fig.text(0.05, 0.965, ct, fontsize=13, fontweight='bold', color='black')
            fig.text(0.05, 0.948, f"{mask.sum():,} cells ({mask.mean():.1%})"
                     + (f"; defined at {key}, cluster(s) {', '.join(clusters)}" if key else ''), fontsize=8)
            ax = fig.add_subplot(gs[0, 0:2])
            plot_highlight(ax, um, mask, pal.get(ct, HIGHLIGHT), size)
            axt = fig.add_subplot(gs[0, 2])
            lines = ['**Annotation rows (applied in file order)']
            for r in pl['rows'].itertuples():
                lines.append(f"{r.key_spec} cluster {r.cluster}: {r.evidence or '(no Evidence text)'}")
            ne = pl['not_enriched']
            if len(ne):
                lines.append('**Not enriched here (other markers, or other paralog copies of markers shown below)')
                ne = ne.drop_duplicates('symbol')
                items = [f"{r.symbol} ({r.evidence}, {r.confidence})" for r in ne.itertuples()]
                lines.append(', '.join(items[:12]) + (f", and {len(items) - 12} more" if len(items) > 12 else ''))
            if fallback:
                lines.append('**No enriched marker from the tables: showing top DE genes (data-driven only)')
            text_panel(axt, lines, width=36)

            vlabels = adata.obs[key].astype(str).to_numpy() if key else labels
            vhigh = set(clusters) if key else {ct}
            for i, g in enumerate(genes):
                j = 1 + i
                if g in col:
                    v = Mk[:, col[g]]
                else:
                    v, _ = gene_matrix(adata, X, var_names, [g])
                v = v.toarray().ravel() if sparse.issparse(v) else np.asarray(v).ravel()
                if fallback:
                    sym = (homolog_str(g, gm).split(' ')[0] if gm is not None and g in gm.index else g)
                    r = None
                else:
                    r = sh.iloc[i]
                    sym = r['symbol']
                axu = fig.add_subplot(gs[j, 0])
                plot_expr_umap(axu, um, v, size, sym)
                axv = fig.add_subplot(gs[j, 1])
                plot_violins(axv, v, vlabels, vhigh, args.max_cells_violin, rng)
                axv.set_xlabel(key or args.key, fontsize=7)
                fin, fout = (v[mask] > 0).mean(), (v[~mask] > 0).mean()
                min_, mout = v[mask].mean(), v[~mask].mean()
                axx = fig.add_subplot(gs[j, 2])
                if r is not None:
                    hom = ''
                    if str(r['ref_gene']) and str(r['via']) != 'same_species':
                        hom = (f"Homolog: {r['ref_gene']} rank {r['hit_rank']}, {r['pident']}% id"
                               + (', RBH' if str(r['rbh']) == 'yes' else '')
                               + (f", via {r['via']}" if str(r['via']) == 'reverse_best' else ''))
                    rel = '' if r['match'] == 'exact' else f" [marker for {r['cell_type']}]"
                    tl = [f"**{sym}{rel}", f"{g}", f"Evidence: {r['evidence']} / {r['confidence']}"]
                    if hom:
                        tl.append(hom)
                    tl += [f"Basis: {r['basis'] or '(none recorded)'}",
                           f"In data: detected in {fin:.1%} of cells vs {fout:.1%} elsewhere "
                           f"({fin / max(fout, 0.001):.0f}x); mean {min_:.2f} vs {mout:.2f}"]
                    if str(r['source']):
                        tl.append(f"Source: {r['source']}")
                else:
                    tl = [f"**{g}", f"Homolog: {homolog_str(g, gm) or 'none'}",
                          'Evidence: top DE gene only (not a curated marker)',
                          f"In data: detected in {fin:.1%} of cells vs {fout:.1%} elsewhere "
                           f"({fin / max(fout, 0.001):.0f}x); mean {min_:.2f} vs {mout:.2f}"]
                text_panel(axx, tl, width=46)
                shown_all.setdefault(ct, []).append((g, sym))
            pdf.savefig(fig)
            plt.close(fig)
            print(f'  page: {ct} ({len(genes)} {"DE" if fallback else "marker"} gene(s))')

        # Dotplot of shown markers
        # Built from a small matrix of just the shown genes so axis labels can be marker symbols
        order, label = [], {}
        for ct, pairs in shown_all.items():
            for g, s in pairs:
                if g not in label:
                    lab = str(s)
                    while lab in label.values():
                        lab += "'"  # same symbol on two paralogs: SWEET12, SWEET12'
                    label[g] = lab
                    order.append(g)
        if order:
            try:
                M, found = gene_matrix(adata, X, var_names, order)
                keep = adata.obs[args.key].astype(str).to_numpy() != args.unknown_label
                small = sc.AnnData(X=sparse.csr_matrix(M)[keep] if sparse.issparse(M) else M[keep],
                                   obs=adata.obs.loc[keep, [args.key]].copy(),
                                   var=pd.DataFrame(index=[label[g] for g in found]))
                small.obs[args.key] = small.obs[args.key].cat.remove_unused_categories()
                present = set(small.obs[args.key].cat.categories)
                small.obs[args.key] = small.obs[args.key].cat.reorder_categories(
                    [c for c in cts + qc_cts if c in present] + [c for c in small.obs[args.key].cat.categories
                                                                 if c not in set(cts + qc_cts)])
                groups = {ct: [label[g] for g, _ in pairs if g in found] for ct, pairs in shown_all.items()}
                groups = {k: list(dict.fromkeys(v)) for k, v in groups.items() if v}
                dp = sc.pl.dotplot(small, groups, groupby=args.key, standard_scale='var', cmap='viridis',
                                   use_raw=False, show=False, return_fig=True)
                dp.make_figure()
                pdf.savefig(plt.gcf(), bbox_inches='tight')
            except Exception as e:  # the report must not die on the summary plot
                print(f'  WARN dotplot failed: {e}')
            plt.close('all')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
