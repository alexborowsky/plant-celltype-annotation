#!/usr/bin/env python3
"""Per-cell-type evidence report (PDF) for an applied annotation.

Run after apply_annotations.py. One page per annotated cell type, showing the
strongest marker evidence present in the data:
  - UMAP highlighting the cell type
  - per marker: expression UMAP (viridis), violins across the clusters of the key
    that defined the label (annotated clusters highlighted), and a text panel with
    the marker's evidence tier, homology, basis, in-data enrichment and other copies
  - the annotation table's Evidence text for the rows that produced the label
Marker choice: among table markers enriched in the cell type AND detected in at
least --min-detect (default 10%) of its cells, markers are ranked by specificity,
  max((f_in - f_out) * log2((f_in + 0.01) / (f_out + 0.01)), 0.5 * (mean_in - mean_out) * f_in),
weighted up to 1.4x by evidence tier and confidence (tie-breakers). Markers of the
type itself (or of an alias) come before token-related types. At least one
function-tier marker is shown when one passes the floor. Enriched markers below the
floor are listed in the text panel ("detected in <10%"); they are plotted only when
no marker passes the floor. Up to --max-markers are shown, plus --extra-genes (genes
a call rests on that are not in the marker tables, e.g. DE or hypothesis genes,
labeled "extra (not in marker tables)", or "extra (table marker for X)"). Cell types with no enriched marker fall
back to top DE genes, labeled as data-driven.
Related marker types: exact names, --alias, and references/markers/celltype_aliases.tsv
(alias, canonical) count as the type itself. Otherwise a marker type whose name
tokens are a subset of the cell type's counts as related (Phloem for
Phloem_Companion), except when the extra tokens name a distinct type: Xylem markers
do not count for Xylem_Parenchyma, nor Phloem markers for Phloem_Pole_Pericycle.
Gene names: --gene-map (several allowed, first primary) and --gene-annotation (target
gene_id, symbol, description; used for genes without a gene-map hit). Araport
placeholders ("no symbol available") are treated as empty.
Front pages: overview UMAP (labels pushed apart, with leader lines when moved) and a
summary table; a States page when obs has states (UMAP by state; per state: cells, cell types,
the sample/condition with the highest share, and the annotation rows that set it); cluster pages.
State pages (after the cell-type pages), one per state: the state on the UMAP, the Evidence of
the rows that set it, cell types carrying it, its share per sample/condition (--composition-keys),
and gene panels vs the same cell types without the state (gene IDs cited in the Evidence, then
--state-genes, then top genes), with violins per type split into with (+) / without (-) the state.
Last page: dotplot of the shown genes by cell type.
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
from cluster_evidence import (expression_source, gene_matrix, load_markers, natural_key)  # noqa: E402
from check_genes import (GeneResolver, clean, find_ref_annotation, name_tokens, ref_key,  # noqa: E402
                         SKILL_DIR)
from apply_annotations import (parse_annotations, resolve_key, semantic_color,  # noqa: E402
                               FALLBACK_COLORS, CONF_LEVELS, confidence_key, apply as apply_rows)

warnings.filterwarnings('ignore')
sc.settings.verbosity = 1

HIGHLIGHT = '#D55E00'   # ito vermillion: annotated cells / clusters
BACKGROUND = '#C8C8C8'  # other cells / clusters
ITO = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#56B4E9', '#E69F00', '#F0E442']
SPARSE_RATIO = 3.0      # detection ratio (in/out) for the sparse-marker route
SPARSE_MIN_FRAC = 0.02  # ...with at least 2% of the cell type expressing
STRONG_DELTA = 1.0      # level route: a >= 1 log-unit (~2.7x) mean gap for genes detected nearly everywhere
STRONG_MIN_FRAC = 0.5   # ...with at least half of the cell type expressing
LEVEL_DELTA = 0.3       # confidence only: a type's own markers >= 0.3 log units higher, in most cells everywhere
CONF = {'high': 2, 'medium': 1, 'low': 0}
CONF_COLOR = {'high': '#009E73', 'medium': '#E69F00', 'low': '#D55E00', 'unresolved': '#555555'}
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


def repel_labels(ax, anchors, texts, fontsize=7, pad=0.006, leader_min=0.012, max_iter=400, **kw):
    """Direct labels at data-coordinate anchors, pushed apart until their boxes do not overlap.

    Works in axes-fraction units (no adjustText dependency): overlapping pairs are nudged apart
    along the axis of smaller overlap, labels are kept inside the axes, and a thin leader line
    joins a label to its anchor when it moved more than leader_min."""
    if not texts:
        return []
    fig = ax.figure
    ax.apply_aspect()
    to_ax = ax.transAxes.inverted()
    pos0 = np.array([to_ax.transform(ax.transData.transform(a)) for a in anchors], dtype=float)
    arts = [ax.text(x, y, t, transform=ax.transAxes, fontsize=fontsize, ha='center', va='center', zorder=5, **kw)
            for (x, y), t in zip(pos0, texts)]
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    axbb = ax.get_window_extent(rend)
    wh = np.array([[a.get_window_extent(rend).width / axbb.width, a.get_window_extent(rend).height / axbb.height]
                   for a in arts])
    pos = pos0.copy()
    n = len(arts)
    for _ in range(max_iter):
        moved = False
        for i in range(n):
            for j in range(i + 1, n):
                d = pos[i] - pos[j]
                ov = (wh[i] + wh[j]) / 2 + pad - np.abs(d)
                if ov[0] > 0 and ov[1] > 0:
                    moved = True
                    k = 1 if ov[1] <= ov[0] else 0  # labels are wide: usually separate vertically
                    sgn = np.sign(d[k]) if d[k] != 0 else (1.0 if i < j else -1.0)
                    step = ov[k] / 2 + 1e-4
                    pos[i, k] += sgn * step
                    pos[j, k] -= sgn * step
        pos = np.clip(pos, wh / 2, 1 - wh / 2)
        if not moved:
            break
    for a, p0, p in zip(arts, pos0, pos):
        a.set_position(p)
        if np.hypot(*(p - p0)) > leader_min:
            ax.plot([p0[0], p[0]], [p0[1], p[1]], transform=ax.transAxes, lw=0.5, color='#444444', zorder=4)
    return arts


CLUSTER_COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#56B4E9', '#E69F00', '#F0E442',
                  '#4477AA', '#228833', '#AA3377', '#66CCEE', '#CCBB44', '#EE6677', '#555555']


def plot_cluster_key(fig, ax, axt, um, clus, cell_types, size, unknown_label):
    """UMAP colored by one cluster key with IDs printed on it, plus a cluster -> size / cell type table.

    Cells outside the key (subclusterings cover a subset) are drawn grey. Colors repeat after 14
    clusters, so the IDs on the map, not the colors, identify clusters."""
    ok = (clus != 'nan') & (clus != '')
    ax.scatter(um[~ok, 0], um[~ok, 1], s=size, c=BACKGROUND, lw=0, rasterized=True)
    groups = sorted(pd.unique(clus[ok]), key=natural_key)
    rows = []
    for i, g in enumerate(groups):
        m = clus == g
        ax.scatter(um[m, 0], um[m, 1], s=size, c=CLUSTER_COLORS[i % len(CLUSTER_COLORS)], lw=0,
                   rasterized=True)
        ct = pd.Series(cell_types[m]).value_counts()
        top = ct.index[0]
        share = ct.iloc[0] / m.sum()
        rows.append([g, f'{m.sum():,}', top if share >= 0.995 else f'{top} ({share:.0%})'])
    umap_axes(ax)
    repel_labels(ax, [(np.median(um[clus == g, 0]), np.median(um[clus == g, 1])) for g in groups], list(groups),
                 fontsize=6, pad=0.002, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.75))
    axt.axis('off')
    tbl = axt.table(cellText=rows, colLabels=['Cluster', 'Cells', f'Cell type (share; {unknown_label} = unlabeled)'],
                    loc='upper left', cellLoc='left', colLoc='left', colWidths=[0.16, 0.18, 0.66])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(6 if len(rows) <= 20 else 5)
    tbl.scale(1, 0.85 if len(rows) > 20 else 1.0)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor('#DDDDDD')
        if r == 0:
            cell.set_text_props(fontweight='bold')


def text_panel(ax, lines, width=None):
    """Wrapped text that fits its axes: wrap width and font size (7 down to 4.5 pt) follow the axes'
    physical size; text that still does not fit is cut with a "(truncated)" line.
    Lines starting with ** are bold headings. width (chars) is an optional upper bound."""
    ax.axis('off')
    fig = ax.figure
    bb = ax.get_position()
    w_pt = bb.width * fig.get_figwidth() * 72
    h_pt = bb.height * fig.get_figheight() * 72

    def wrap(w):
        out = []
        for ln in lines:
            bold = ln.startswith('**')
            ln = ln.strip('*')
            wrapped = textwrap.wrap(ln, w) or ['']
            out.extend([(t, bold) for t in wrapped])
        return out

    lead = 1.25  # line height in font sizes
    for fs in (7.0, 6.5, 6.0, 5.5, 5.0, 4.5):
        nchar = max(16, int(w_pt / (fs * 0.56)))
        if width:
            nchar = min(nchar, int(width * 7 / fs))
        out = wrap(nchar)
        if len(out) * fs * lead <= h_pt:
            break
    max_lines = max(1, int(h_pt / (fs * lead)))
    if len(out) > max_lines:
        out = out[:max_lines - 1] + [('... (truncated; see the annotation table / evidence files)', False)]
    step = fs * lead / max(h_pt, 1)
    y = 1.0
    for txt, bold in out:
        ax.text(0, y, txt, transform=ax.transAxes, va='top', ha='left', fontsize=fs,
                fontweight='bold' if bold else 'normal', family='sans-serif', clip_on=False)
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


def load_celltype_aliases(path):
    """alias -> canonical (lower case) from celltype_aliases.tsv (columns alias, canonical[, note]); {} if absent."""
    if not path or not os.path.exists(path):
        return {}
    try:
        t = pd.read_csv(path, sep='\t', dtype=str, comment='#').fillna('')
    except Exception as e:  # a malformed shared file must not kill the report
        print(f'  WARN cannot read {path}: {e}')
        return {}
    if 'alias' not in t.columns or 'canonical' not in t.columns:
        print(f'  WARN {path}: need alias and canonical columns; ignored')
        return {}
    return {a.strip().lower(): c.strip().lower() for a, c in zip(t['alias'], t['canonical'])
            if a.strip() and c.strip()}


# A name token that makes a type distinct from the type named by the remaining tokens:
# Xylem_Parenchyma is not Xylem, Phloem_Pole_Pericycle is not Phloem.
DISTINCT_TOKENS = {'parenchyma', 'pericycle', 'fiber', 'fibre', 'sclerenchyma', 'collenchyma',
                   'sheath', 'idioblast'}


def _tokens(name):
    return set(t for t in re.split(r'[_\s\-/]+', name.lower()) if t)


def candidate_markers(markers, ct, aliases, ct_aliases=None):
    """Exact cell-type matches first, then alias matches (--alias, alias table), then token-related ones."""
    ct_aliases = ct_aliases or {}
    canon = lambda n: ct_aliases.get(n.lower(), n.lower())
    mtypes = markers['cell_type'].astype(str)
    exact = markers[mtypes.str.lower() == ct.lower()].assign(match='exact')
    names = aliases.get(ct)
    if names:  # explicit --alias: only these names (previous behaviour)
        rel = markers[mtypes.isin(names) & (mtypes.str.lower() != ct.lower())].assign(match='alias')
        return pd.concat([exact, rel], ignore_index=True)
    same = mtypes.map(lambda c: c.lower() != ct.lower() and canon(c) == canon(ct))
    alias_rows = markers[same].assign(match='alias')
    toks = _tokens(ct)

    def related(c):
        if c.lower() == ct.lower() or canon(c) == canon(ct):
            return False
        ctoks = _tokens(c)
        return bool(ctoks) and ctoks < toks and not ((toks - ctoks) & DISTINCT_TOKENS)
    rel = markers[mtypes.map(related)].assign(match='related')
    return pd.concat([exact, alias_rows, rel], ignore_index=True)


def specificity(fi, fo, delta):
    """Detection specificity, or level specificity for genes detected nearly everywhere."""
    fi, fo, delta = np.asarray(fi, float), np.asarray(fo, float), np.asarray(delta, float)
    det = np.clip(fi - fo, 0, None) * np.clip(np.log2((fi + 0.01) / (fo + 0.01)), 0, None)
    lvl = 0.5 * np.clip(delta, 0, None) * fi
    return np.maximum(det, lvl)


def select_markers(cand, stats, n_max, min_delta, min_frac_ratio, min_detect=0.10):
    """-> (shown, not_enriched, below_floor, all_rows).

    shown: enriched markers detected in >= min_detect of the type, ranked by specificity
    (evidence tier and confidence as tie-breakers), at least one function-tier marker if any
    passes; when none passes the floor, the best enriched markers below it (flag below_floor)."""
    empty = cand.iloc[0:0]
    if cand.empty:
        return empty, empty, empty, empty
    c = cand.merge(stats, on='gene_id', how='inner')
    if c.empty:
        return empty, empty, empty, empty
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
    # Markers of the type itself or an alias first; token-related types only fill up
    c['q_match'] = c['match'].isin(['exact', 'alias']).astype(int)
    c['spec'] = specificity(c['frac_in'], c['frac_out'], c['delta'])
    # Specificity ranks; tier and confidence only break near-ties (at most x1.4)
    c['rank_score'] = c['spec'] * (1 + 0.1 * (c['q_tier'] + c['q_conf']))
    c = c.sort_values(['q_match', 'rank_score'], ascending=False, kind='mergesort')
    c = c.drop_duplicates('gene_id')
    c['below_floor'] = c['frac_in'] < min_detect
    enr = c[c['enriched']]
    # Paralog copies mapped from one reference locus share a symbol: rank only the best copy.
    good = enr[~enr['below_floor']].drop_duplicates('symbol')
    shown = good.head(n_max)
    fn = good[good['evidence'] == 'function']
    if len(fn) and not (shown['evidence'] == 'function').any() and n_max > 0:
        # A page must show a function-tier marker when one is enriched and detectable
        shown = pd.concat([shown.head(n_max - 1), fn.head(1)])
    below = enr[enr['below_floor'] & ~enr['symbol'].isin(set(shown['symbol']))].drop_duplicates('symbol')
    below = below.sort_values(['q_match', 'q_tier', 'q_conf', 'rank_score'], ascending=False, kind='mergesort')
    if shown.empty and len(below):
        # Nothing reaches the floor: show the best sparse markers, flagged as below it
        shown = below.sort_values(['q_match', 'rank_score'], ascending=False, kind='mergesort').head(n_max)
        below = below[~below['gene_id'].isin(set(shown['gene_id']))]
    not_enriched = c[~c['enriched'] & c['match'].isin(['exact', 'alias'])]
    return shown, not_enriched, below, c


def target_symbol(g, res):
    """Display name of a target gene: rank-1 reference symbol from the gene map, else the target
    annotation's symbol (cluster_evidence semantics), else ''."""
    if res.r1 is not None and g in res.r1.index:
        s = name_tokens(res.r1.at[g, 'ref_symbol'])
        return s[0] if s else str(res.r1.at[g, 'ref_gene'])
    if res.ann is not None and g in res.ann.index:
        s = name_tokens(res.ann.at[g, 'symbol'])
        return s[0] if s else ''
    return ''


def _num(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return np.nan
    return x


def identity_text(pident, relationship, via, rbh):
    """'55% id, RBH' for BLAST hits; 'orthology (1:1)' when there is no identity (orthology tables)."""
    pid = _num(pident)
    if not np.isnan(pid):
        return f"{pid:.0f}% id" + (', RBH' if str(rbh) == 'yes' else '')
    rel = clean(relationship)
    if rel:
        return f"orthology ({rel})"
    if str(via) == 'orthology':
        return 'orthology' + (' (1:1)' if str(rbh) == 'yes' else '')
    return 'identity n/a'


def hom_line(r, res):
    """Homology text for a marker row (empty for same-species rows)."""
    if not clean(r['ref_gene']) or str(r['via']) == 'same_species':
        return ''
    rel = clean(r.get('relationship', ''))
    if not rel and res.gm is not None and 'relationship' in res.gm.columns:
        if not hasattr(res, '_rel'):
            sub = res.gm[res.gm['relationship'] != '']
            res._rel = dict(zip(zip(sub['query_gene'], sub['ref_key']), sub['relationship']))
        rel = res._rel.get((r['gene_id'], ref_key(r['ref_gene'])), '')
    rank = _num(r['hit_rank'])
    rk = f" rank {int(rank)}" if not np.isnan(rank) else ''
    return (f"Homolog: {r['ref_gene']}{rk}, {identity_text(r['pident'], rel, r['via'], r['rbh'])}"
            + (f", via {r['via']}" if str(r['via']) == 'reverse_best' else ''))


def gene_desc(g, res, max_desc=60):
    """'SYM (AGI) description [55%, RBH]' from the gene map, else the target annotation's symbol/description."""
    h = res.homolog_info(g)
    if h:
        r = res.r1.loc[g]
        desc = (name_tokens(r['ref_description']) or [''])[0][:max_desc]
        out = f"{h['ref_symbol']} ({h['ref_gene']})" if h['ref_symbol'] else str(h['ref_gene'])
        return out + (f" {desc}" if desc else '') + f" [{identity_text(h['pident'], h['relationship'], '', h['rbh'])}]"
    if res.ann is not None and g in res.ann.index:
        r = res.ann.loc[g]
        return ' '.join(x for x in (r['symbol'], r['description'][:max_desc]) if x)
    return ''


def other_copies(allc, sym, g, n=4):
    """Other gene copies of a marker symbol among the candidates, with their detection in/out."""
    if allc is None or not len(allc):
        return ''
    o = allc[(allc['symbol'] == sym) & (allc['gene_id'] != g)].drop_duplicates('gene_id')
    if o.empty:
        return ''
    items = [f"{r.gene_id} ({r.frac_in:.0%} vs {r.frac_out:.0%})" for r in o.head(n).itertuples()]
    return ', '.join(items) + (f", +{len(o) - n} more" if len(o) > n else '')


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
# Overall confidence per cell type = the lower of (a) the analyst's Confidence of the rows that labelled its cells
# (cell-weighted median) and (b) the marker evidence the report finds in the data; _like labels are capped at medium.

RANK = {'low': 0, 'medium': 1, 'high': 2}


def analyst_confidence(conf_cells):
    """Cell-weighted median of the per-cell analyst confidence -> (level or '', 'high 10%, medium 90%')."""
    vc = pd.Series(conf_cells).value_counts()
    vc = vc[[c for c in CONF_LEVELS if c in vc.index]]
    if vc.empty:
        return '', 'not given'
    ranks = np.repeat([RANK[c] for c in vc.index], vc.values)
    med = int(np.floor(np.median(ranks)))
    share = ', '.join(f'{c} {n / vc.sum():.0%}' for c, n in vc.items())
    n_none = len(conf_cells) - vc.sum()
    if n_none:
        share += f', none given {n_none / len(conf_cells):.0%}'
    return CONF_LEVELS[::-1][med], share


def evidence_grade(pl, min_detect):
    """Marker evidence found in the data -> (level, reason)."""
    sh = pl['shown']
    ok = sh[~sh['below_floor'].astype(bool)] if len(sh) else sh
    tiers = list(ok['evidence']) if len(ok) else []
    st = pl['stats']
    x_ok = [d['term'] for d in pl['extras'] if st is not None and d['copy']['gene_id'] in st.index
            and st.at[d['copy']['gene_id'], 'frac_in'] >= min_detect]
    n_all = len(tiers) + len(x_ok)
    fun = [r.symbol for r in ok.itertuples() if r.evidence == 'function'] if len(ok) else []
    char = [r.symbol for r in ok.itertuples() if r.evidence == 'characterized_enriched'] if len(ok) else []
    if fun and n_all >= 2:
        return 'high', f"function-tier {fun[0]} + {n_all - 1} more enriched gene(s)"
    if fun or char:
        return 'medium', f"{'function' if fun else 'characterized'}-tier {(fun or char)[0]}" + (
            f" + {n_all - 1} more" if n_all > 1 else ' only')
    if n_all >= 2:
        return 'medium', f"{n_all} enriched expression-level/extra genes, no characterized marker"
    # Majority types (leaf mesophyll) are called by level: their markers are in nearly every cell (ambient RNA),
    # so none passes the enrichment routes, but the type's own markers sit clearly higher in it
    ac = pl['allc']
    if len(ac):
        lvl = ac[ac['match'].isin(['exact', 'alias']) & ~ac['enriched'].astype(bool) & (ac['frac_in'] >= 0.5)
                 & (ac['delta'] >= LEVEL_DELTA)].drop_duplicates('symbol')
        if len(lvl) >= 2:
            return 'medium', (f"level only: {len(lvl)} markers higher here, in most cells everywhere "
                              f"({', '.join(lvl['symbol'].astype(str).head(3))})")
    if n_all == 1:
        return 'low', 'a single expression-level or extra gene'
    if len(sh):
        return 'low', f'markers enriched but detected in <{min_detect:.0%} of cells'
    return 'low', 'no enriched marker: DE genes only'


def overall_confidence(ct, analyst, grade):
    """-> (level, note). Unknown_* labels are unresolved; _like labels are capped at medium."""
    if re.match(r'(?i)^unknown', ct):
        return 'unresolved', 'Unknown label'
    lv, note = grade, 'markers only (no analyst Confidence)'
    if analyst:
        lv = analyst if RANK[analyst] <= RANK[grade] else grade
        note = 'analyst' if RANK[analyst] < RANK[grade] else 'markers' if RANK[grade] < RANK[analyst] else 'both'
    if re.search(r'(?i)_like$', ct) and RANK[lv] > RANK['medium']:
        lv, note = 'medium', '_like label (capped)'
    return lv, note


# ----------------------------------------------------------------------------
# States (State column of the annotation table -> obs['cell_state'])

COMPOSITION_RE = re.compile(r'^(sample|samples|batch|treatment|condition|genotype|replicate|rep|timepoint|time|'
                            r'tissue|organ|library|orig\.ident)$', re.I)
STATE_COLORS = ['#D55E00', '#0072B2', '#009E73', '#CC79A7', '#E69F00', '#56B4E9', '#F0E442',
                '#AA3377', '#228833', '#4477AA', '#EE6677', '#CCBB44', '#66CCEE', '#555555']


def contrast_stats(X, idx_in, idx_out):
    """Detection fraction and mean of every gene in two sets of cells -> (fi, fo, mi, mo) arrays."""
    out = []
    for idx in (idx_in, idx_out):
        A = X[np.sort(idx)]
        if sparse.issparse(A):
            A = A.tocsr()
            out.append((np.asarray((A > 0).mean(0)).ravel(), np.asarray(A.mean(0)).ravel()))
        else:
            A = np.asarray(A)
            out.append(((A > 0).mean(0), A.mean(0)))
    (fi, mi), (fo, mo) = out
    return fi, fo, mi, mo


def cited_genes(texts, var_names):
    """Gene IDs of the data that are written in Evidence texts, in order of first mention."""
    vu = {str(v).upper(): v for v in var_names}
    out = []
    for t in texts:
        for tok in re.findall(r'[A-Za-z0-9_.:\-]+', str(t)):
            g = vu.get(tok.strip('.:-').upper())
            if g is not None and g not in out:
                out.append(g)
    return out


def composition_text(obs, mask, keys, n=6):
    """Per composition key: share of each group's cells that carry the state, highest first."""
    lines = []
    for k in keys:
        v = obs[k].astype(str).to_numpy()
        tab = pd.Series(mask).groupby(v).mean().sort_values(ascending=False)
        if len(tab) < 2:
            continue
        lo = tab.iloc[-1]
        ratio = (f"; highest/lowest {tab.iloc[0] / lo:.1f}x" if lo > 0 else '; absent from '
                 + ', '.join(tab.index[tab == 0][:4]) + (' ...' if (tab == 0).sum() > 4 else ''))
        items = [f"{g} {x:.1%}" for g, x in tab.head(n).items()]
        lines.append(f"{k}: " + ', '.join(items) + (f", ... ({len(tab) - n} more)" if len(tab) > n else '') + ratio)
    return lines


# ----------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True, help='annotated h5ad (output of apply_annotations.py)')
    p.add_argument('--key', default='cell_type')
    p.add_argument('--annotations', required=True, help='annotation table used to label the cells')
    p.add_argument('--markers', nargs='+', required=True, help='target marker table(s) from map_markers.py')
    p.add_argument('--gene-map', nargs='+', default=None,
                   help='gene_map.tsv file(s) from map_markers.py (first is primary): homolog names for DE '
                        'fallbacks and extra genes, symbol -> gene resolution, orthology relationships')
    p.add_argument('--gene-annotation', nargs='+', default=None,
                   help='target-species gene_id, symbol, description table(s) (as in cluster_evidence.py): '
                        'names for genes without a gene-map hit')
    p.add_argument('--ref-annotation', nargs='+', default=None,
                   help='reference-species gene_id, symbol table(s) to resolve --extra-genes symbols '
                        '(default: a shipped Araport11 table if present)')
    p.add_argument('--colors', default=None, help='CellType<TAB>Color table')
    p.add_argument('--alias', action='append', default=[],
                   help='AnnotatedType=MarkerType1,MarkerType2 (repeatable): marker cell types to use '
                        'for a differently named annotation, e.g. Procambium_Dividing=Procambium,Dividing_cells')
    p.add_argument('--celltype-aliases', default=os.path.join(SKILL_DIR, 'references', 'markers',
                                                              'celltype_aliases.tsv'),
                   help='alias table (alias, canonical, note); names with the same canonical name count as '
                        'the same type. Used if present; "" to disable')
    p.add_argument('--extra-genes', action='append', default=[],
                   help='CellType=GENE1,GENE2 (repeatable): genes a call rests on that are not in the marker '
                        'tables (DE or hypothesis genes); target IDs or symbols resolved through the gene '
                        'map / annotation / marker tables. Shown as "extra (not in marker tables)"')
    p.add_argument('--max-extra', type=int, default=4, help='max extra genes shown per cell type')
    p.add_argument('--output', required=True, help='report PDF path')
    p.add_argument('--title', default=None)
    p.add_argument('--unknown-label', default='Unknown')
    p.add_argument('--max-markers', type=int, default=3)
    p.add_argument('--min-detect', type=float, default=0.10,
                   help='detection floor: a marker must be detected in at least this fraction of the cell '
                        'type to be ranked (markers below are listed, and shown only if none passes)')
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
    p.add_argument('--state-key', default=None,
                   help="obs column with cell states (default: cell_state for --key cell_type, else <key>_state)")
    p.add_argument('--state-genes', action='append', default=[],
                   help='STATE=GENE1,GENE2: genes a state call rests on (symbols or IDs, resolved like '
                        '--extra-genes); shown on the state page before data-driven genes. Repeatable')
    p.add_argument('--max-state-genes', type=int, default=3, help='gene panels per state page')
    p.add_argument('--composition-keys', nargs='*', default=None,
                   help='obs columns for state composition (default: sample/batch/treatment/condition/'
                        'genotype/replicate/timepoint columns that exist)')
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
    ref_ann = args.ref_annotation
    if ref_ann is None and args.extra_genes:
        auto = find_ref_annotation()
        ref_ann = [auto] if auto else None
    res = GeneResolver(var_names, adata.obs.columns, args.gene_map, args.markers, args.gene_annotation,
                       ref_ann, max_rank=2)
    if res.ann is not None:
        print(f'  gene annotation covers {var_names.isin(res.ann.index).mean():.1%} of var_names')
    markers = load_markers(args.markers)
    for c in ['evidence', 'confidence', 'basis', 'ref_gene', 'hit_rank', 'pident', 'rbh', 'via', 'source',
              'relationship']:
        if c not in markers.columns:
            markers[c] = ''
    # Placeholder or missing symbols: the target annotation's symbol, else the gene ID
    markers['symbol'] = [clean(s) if clean(s) and s != g else (target_symbol(g, res) or g)
                         for s, g in zip(markers['symbol'], markers['gene_id'])]
    aliases = {}
    for a in args.alias:
        k, v = a.split('=', 1)
        aliases[k] = [x for x in v.split(',') if x]
    ct_aliases = load_celltype_aliases(args.celltype_aliases)
    if ct_aliases:
        print(f'  cell-type alias table: {len(ct_aliases)} aliases ({args.celltype_aliases})')
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

    # --extra-genes: resolve every term to its copies in the data (never guessed)
    extra_terms = {}
    for e in args.extra_genes:
        if '=' not in e:
            sys.exit(f'--extra-genes expects CellType=GENE1,GENE2, got {e}')
        k, v = e.split('=', 1)
        hit = [c for c in cts + qc_cts if c.lower() == k.strip().lower()]
        if not hit:
            print(f'  WARN --extra-genes: cell type {k} not in {args.key}; ignored')
            continue
        extra_terms.setdefault(hit[0], [])
        extra_terms[hit[0]] += [t for t in re.split(r'[,\s]+', v) if t]
    extra_copies, extra_missing = {}, {}
    for ct, terms in extra_terms.items():
        for t in dict.fromkeys(terms):
            cs = [d for d in res.resolve(t) if d['in_data']]
            if cs:
                extra_copies.setdefault(ct, []).append((t, cs))
            else:
                extra_missing.setdefault(ct, []).append(t)
                print(f'  WARN --extra-genes {ct}: {t} resolves to no gene in the data; not shown')
    xgenes = list(dict.fromkeys(d['gene_id'] for v in extra_copies.values() for _, cs in v for d in cs))

    Mk, mk_found = gene_matrix(adata, X, var_names, list(markers['gene_id']) + xgenes)
    Mk = Mk.tocsr() if sparse.issparse(Mk) else Mk
    col = {g: i for i, g in enumerate(mk_found)}
    print(f'  {len(cts)} cell types; {len(set(markers["gene_id"]) & set(mk_found))} marker genes in data'
          + (f'; {len(xgenes)} extra gene copies' if xgenes else ''))

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
        shown, not_enriched, below, allc = select_markers(
            candidate_markers(markers, ct, aliases, ct_aliases), stats, args.max_markers,
            args.min_delta, args.min_frac_ratio, args.min_detect)
        # Extra genes: best copy (by specificity in this type) of each term, others listed
        extras = []
        st = stats.set_index('gene_id') if len(stats) else None
        for t, cs in extra_copies.get(ct, []):
            cs = [d for d in cs if st is not None and d['gene_id'] in st.index
                  and d['gene_id'] not in set(shown['gene_id'])]
            if not cs:
                continue
            sp = [float(specificity(st.at[d['gene_id'], 'frac_in'], st.at[d['gene_id'], 'frac_out'],
                                    st.at[d['gene_id'], 'mean_in'] - st.at[d['gene_id'], 'mean_out']))
                  for d in cs]
            order = np.argsort(sp)[::-1]
            best = cs[order[0]]
            others = [(cs[i]['gene_id'], st.at[cs[i]['gene_id'], 'frac_in'], st.at[cs[i]['gene_id'], 'frac_out'])
                      for i in order[1:]]
            extras.append(dict(term=t, copy=best, others=others))
        if len(extras) > args.max_extra:
            print(f'  WARN {ct}: {len(extras)} extra genes, showing the first {args.max_extra}')
            extras = extras[:args.max_extra]
        plans[ct] = dict(mask=mask, key=best_key, clusters=clusters, rows=rows, shown=shown,
                         not_enriched=not_enriched, below=below, allc=allc, stats=st, extras=extras,
                         extra_missing=extra_missing.get(ct, []))
        if shown.empty and not extras:
            need_de.append(ct)
    print(f'  DE fallback for: {need_de}')
    de = de_fallback(adata, args.key, need_de, 10, args.use_raw, 2000, rng)

    # ---- states: who carries them, where they come from, and the genes that set them apart from the same
    # cell types without the state (so the page shows the state program, not type differences)
    skey = args.state_key or ('cell_state' if args.key == 'cell_type' else f'{args.key}_state')
    sl = adata.obs[skey].astype(str).to_numpy() if skey in adata.obs.columns else None
    state_names = []
    if sl is not None:
        vc = pd.Series(sl[sl != 'none']).value_counts()
        state_names = [st for st in vc.index if st not in ('', 'nan')]
    comp_keys = (args.composition_keys if args.composition_keys is not None else
                 [c for c in adata.obs.columns if COMPOSITION_RE.match(str(c))
                  and 1 < adata.obs[c].astype(str).nunique() <= 60][:3])
    state_terms = {}
    for e in args.state_genes:
        if '=' not in e:
            sys.exit(f'--state-genes expects STATE=GENE1,GENE2, got {e}')
        k, v = e.split('=', 1)
        hit = [st for st in state_names if st.lower() == k.strip().lower()]
        if not hit:
            print(f'  WARN --state-genes: state {k} not in obs[{skey}]; ignored')
            continue
        state_terms.setdefault(hit[0], []).extend(t for t in re.split(r'[,\s]+', v) if t)
    splans = {}
    for st in state_names:
        m = sl == st
        rows = ann[ann['state'].astype(str).str.strip().str.lower() == st.lower()] if 'state' in ann.columns \
            else ann.iloc[:0]
        types = pd.Series(labels[m]).value_counts()
        ref = np.isin(labels, types.index) & (sl == 'none')
        contrast = 'the same cell types without a state'
        if ref.sum() < 20:
            ref, contrast = ~m, 'all other cells'
        idx_in, idx_out = np.flatnonzero(m), np.flatnonzero(ref)
        idx_in = rng.choice(idx_in, min(len(idx_in), 3000), replace=False)
        idx_out = rng.choice(idx_out, min(len(idx_out), 3000), replace=False)
        fi, fo, mi, mo = contrast_stats(X, idx_in, idx_out)
        spec = specificity(fi, fo, mi - mo)
        stat = pd.DataFrame({'frac_in': fi, 'frac_out': fo, 'mean_in': mi, 'mean_out': mo, 'spec': spec},
                            index=var_names)
        genes = []  # (gene, route)
        for g in cited_genes(rows['evidence'], var_names):
            genes.append((g, 'cited in the Evidence'))
        for t in dict.fromkeys(state_terms.get(st, [])):
            cs = [d['gene_id'] for d in res.resolve(t) if d['in_data'] and d['gene_id'] in stat.index]
            if not cs:
                print(f'  WARN --state-genes {st}: {t} resolves to no gene in the data; not shown')
                continue
            best = max(cs, key=lambda g: stat.at[g, 'spec'])
            genes.append((best, f"--state-genes '{t}'"))
        cited = list(dict.fromkeys(g for g, _ in genes))
        # cited genes that are enriched first (most specific first), then data-driven top genes
        enr = [g for g in cited if stat.at[g, 'spec'] > 0]
        enr = sorted(enr, key=lambda g: -stat.at[g, 'spec'])
        route = dict(genes)
        show = enr[:args.max_state_genes]
        top = stat[(stat['frac_in'] >= 0.10)].sort_values('spec', ascending=False)
        for g in top.index:
            if len(show) >= args.max_state_genes:
                break
            if g not in show:
                show.append(g)
                route.setdefault(g, f'top gene vs {contrast} (data-driven)')
        splans[st] = dict(mask=m, rows=rows, types=types, contrast=contrast, stat=stat, show=show,
                          route=route, cited=cited, top=list(top.index[:8]))
    if state_names:
        print(f'  {len(state_names)} states in obs[{skey}]; composition keys {comp_keys}')

    # ---- overall confidence per cell type
    ckey = confidence_key(args.key)
    conf_cells = None
    if ckey in adata.obs.columns:
        conf_cells = adata.obs[ckey].astype(str).to_numpy()
    elif ann['confidence'].astype(str).str.strip().ne('').any():
        # older h5ad without the column: replay the table's rows to assign each cell its row's confidence
        import contextlib
        import io
        tmp = sc.AnnData(obs=adata.obs.copy())
        with contextlib.redirect_stdout(io.StringIO()):
            apply_rows(tmp, ann, '_conf_replay', args.unknown_label)
        ck2 = confidence_key('_conf_replay')
        if ck2 in tmp.obs.columns:
            conf_cells = tmp.obs[ck2].astype(str).to_numpy()
            print(f'  analyst confidence replayed from the annotation table ({ckey} not in obs)')
    conf = {}
    for ct in cts + qc_cts:
        m = labels == ct
        an, share = analyst_confidence(conf_cells[m]) if conf_cells is not None else ('', 'not given')
        if ct in plans:
            gr, why = evidence_grade(plans[ct], args.min_detect)
        else:
            gr, why = 'low', 'QC class'
        lv, note = overall_confidence(ct, an, gr)
        conf[ct] = dict(overall=lv, decided_by=note, analyst=an or 'none', analyst_cells=share,
                        markers=gr, marker_reason=why)
    conf_tsv = os.path.splitext(args.output)[0] + '_confidence.tsv'
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    cdf = pd.DataFrame.from_dict(conf, orient='index').rename_axis('cell_type')
    cdf.insert(0, 'cells', [int((labels == c).sum()) for c in cdf.index])
    cdf.to_csv(conf_tsv, sep='\t')
    print(f'  overall confidence: {cdf["overall"].value_counts().to_dict()} -> {conf_tsv}')

    # ---- PDF
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    summary = []
    shown_all = {}
    with PdfPages(args.output) as pdf:
        # Overview page
        fig = plt.figure(figsize=(8.5, 11))
        gs = GridSpec(2, 1, height_ratios=[1.25, 1], figure=fig, hspace=0.1)
        ax = fig.add_subplot(gs[0])
        anchors, names = [], []
        for ct in list(adata.obs[args.key].cat.categories):
            m = labels == ct
            c = BACKGROUND if ct == args.unknown_label else pal[ct]
            ax.scatter(um[m, 0], um[m, 1], s=size, c=c, lw=0, rasterized=True, label=ct)
            if ct != args.unknown_label and m.sum():
                anchors.append((np.median(um[m, 0]), np.median(um[m, 1])))
                names.append(ct)
        umap_axes(ax)
        # Labels of neighbouring types (Phloem_Parenchyma / Xylem_Parenchyma) are pushed apart
        repel_labels(ax, anchors, names, fontsize=7, color='black',
                     bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.8))
        # Direct labels identify cell types (colors alone cannot separate 10+ types for all
        # readers); only the Unknown grey needs a key.
        ax.text(0.0, 0.0, f'grey = {args.unknown_label}', transform=ax.transAxes, fontsize=7,
                color='#555555', ha='left', va='bottom')
        fig.text(0.06, 0.97, args.title or f'Cell-type annotation report: {os.path.basename(args.h5ad)}',
                 fontsize=11, fontweight='bold')
        sub = (f'{adata.n_obs:,} cells; annotation table {os.path.basename(args.annotations)}; '
               f'markers {", ".join(os.path.basename(m) for m in args.markers)}; '
               f'plant-celltype-annotation v{skill_version()}')
        fig.text(0.06, 0.958, '\n'.join(textwrap.wrap(sub, 150)), fontsize=7, va='top')
        axt = fig.add_subplot(gs[1])
        axt.axis('off')
        for ct in cts:
            pl = plans[ct]
            sh = pl['shown']
            if len(sh):
                r0 = sh.iloc[0]
                best = (f"{r0['symbol']} ({r0['evidence'] or 'no tier'}, {r0['confidence'] or '-'}; "
                        f"{r0['frac_in']:.0%} vs {r0['frac_out']:.0%})"
                        + (' <floor' if r0['below_floor'] else ''))
            elif pl['extras']:
                d = pl['extras'][0]
                best = f"{d['term']}: extra gene only (not in marker tables)"
            else:
                best = 'none enriched: DE only'
            nshow = f"{len(sh)}" + (f"+{len(pl['extras'])}x" if pl['extras'] else '')
            summary.append([ct, f"{pl['mask'].sum():,}", f"{pl['mask'].mean():.1%}", conf[ct]['overall'], nshow,
                            best])
        for ct in qc_cts:
            m = labels == ct
            summary.append([ct, f"{m.sum():,}", f"{m.mean():.1%}", '-', '-', 'QC class (no page)'])
        if summary:
            tbl = axt.table(cellText=summary, colLabels=['Cell type', 'Cells', '%', 'Confidence', 'Markers',
                                                         'Strongest marker'],
                            loc='upper center', cellLoc='left', colLoc='left',
                            colWidths=[0.21, 0.08, 0.06, 0.115, 0.08, 0.455])
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(7)
            for (r, c), cell in tbl.get_celld().items():
                cell.set_edgecolor('#DDDDDD')
                if r == 0:
                    cell.set_text_props(fontweight='bold')
                elif c == 3:
                    cell.set_text_props(color=CONF_COLOR.get(summary[r - 1][3], 'black'))
            fig.text(0.06, 0.035, '\n'.join(textwrap.wrap(
                "Confidence: the lower of the annotation table's Confidence (cell-weighted) and the marker evidence "
                'found here (high: a function-tier marker + another enriched gene; medium: a characterized marker, '
                'two enriched genes, or level only; low: one expression-level gene or DE only). _like labels are '
                f'capped at medium. Details on each page and in {os.path.basename(conf_tsv)}.', 175)),
                fontsize=6, va='bottom', color='#333333')
        pdf.savefig(fig)
        plt.close(fig)

        # States overview: which cells carry each state, in which types and samples, set by which rows
        if state_names:
            scol = {st: STATE_COLORS[i % len(STATE_COLORS)] for i, st in enumerate(state_names)}
            fig = plt.figure(figsize=(8.5, 11))
            gs = GridSpec(2, 1, height_ratios=[1.1, 1], figure=fig, hspace=0.08,
                          left=0.05, right=0.97, top=0.92, bottom=0.03)
            fig.text(0.05, 0.965, 'States', fontsize=13, fontweight='bold')
            fig.text(0.05, 0.948, '\n'.join(textwrap.wrap(
                f"obs['{skey}']: states are recorded on top of the cell type (annotation table State column); "
                f"{int((sl != 'none').sum()):,} cells ({(sl != 'none').mean():.1%}) carry one. One page per state "
                'follows the cell-type pages.', 115)), fontsize=8, va='top')
            ax = fig.add_subplot(gs[0])
            none = sl == 'none'
            ax.scatter(um[none, 0], um[none, 1], s=size, c=BACKGROUND, lw=0, rasterized=True)
            anchors = []
            for st in state_names[::-1]:
                m = sl == st
                ax.scatter(um[m, 0], um[m, 1], s=size * 1.5, c=scol[st], lw=0, rasterized=True)
            for st in state_names:
                m = sl == st
                anchors.append((np.median(um[m, 0]), np.median(um[m, 1])))
            umap_axes(ax)
            repel_labels(ax, anchors, state_names, fontsize=7, color='black',
                         bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.8))
            ax.text(0.0, 0.0, 'grey = no state', transform=ax.transAxes, fontsize=7, color='#555555')
            axt = fig.add_subplot(gs[1])
            axt.axis('off')
            srows = []
            for st in state_names:
                sp = splans[st]
                m = sp['mask']
                tys = ', '.join(f"{t} {n / m.sum():.0%}" for t, n in sp['types'].head(3).items())
                enr = ''
                if comp_keys:
                    k = comp_keys[0]
                    tab = pd.Series(m).groupby(adata.obs[k].astype(str).to_numpy()).mean()
                    enr = f"{tab.idxmax()} {tab.max():.1%} (median {tab.median():.1%})"
                defs = '; '.join(f"{r.key_spec}:{r.cluster}" + (' (state only)' if str(r.cell_type).strip()
                                 .lower() in ('', '-', 'na', 'none') else '') for r in sp['rows'].itertuples())
                srows.append([st, f"{m.sum():,}", f"{m.mean():.1%}", tys, enr, defs or '(no table row)'])
            wrap = lambda t, w: '\n'.join(textwrap.wrap(t, w)) or ''
            srows = [[wrap(r[0], 22), r[1], r[2], wrap(r[3], 34), wrap(r[4], 22), wrap(r[5], 30)] for r in srows]
            tbl = axt.table(cellText=srows, colLabels=['State', 'Cells', '%', 'Cell types', 'Highest share'
                            + (f' ({comp_keys[0]})' if comp_keys else ''), 'Set by rows'],
                            loc='upper center', cellLoc='left', colLoc='left',
                            colWidths=[0.17, 0.08, 0.06, 0.27, 0.19, 0.23])
            tbl.auto_set_font_size(False)
            tbl.set_fontsize(6)
            for (r, c), cell in tbl.get_celld().items():
                cell.set_edgecolor('#DDDDDD')
                if r == 0:
                    cell.set_text_props(fontweight='bold')
                else:
                    nl = max(str(x).count('\n') for x in srows[r - 1]) + 1
                    cell.set_height(cell.get_height() * (0.7 + 0.55 * nl))
            pdf.savefig(fig)
            plt.close(fig)

        # Cluster definitions: every cluster key used by the annotation rows or the violin plots,
        # so cluster IDs on the cell-type pages can be looked up without the h5ad (two keys per page)
        ckeys = [k for k in dict.fromkeys([pl['key'] for pl in plans.values()] + list(ann['obs_key']))
                 if k and k in adata.obs.columns]
        ckeys = sorted(ckeys, key=lambda k: adata.obs[k].astype(str).nunique())
        for i0 in range(0, len(ckeys), 2):
            fig = plt.figure(figsize=(8.5, 11))
            gs = GridSpec(2, 2, figure=fig, width_ratios=[1.35, 1], hspace=0.15, wspace=0.05,
                          left=0.04, right=0.97, top=0.91, bottom=0.03)
            fig.text(0.05, 0.965, 'Clusters', fontsize=13, fontweight='bold')
            fig.text(0.05, 0.948, 'Cluster keys used by the annotation table and the violin plots; '
                     'the table gives each cluster\'s size and the cell type its cells were assigned', fontsize=8)
            for j, k in enumerate(ckeys[i0:i0 + 2]):
                ax = fig.add_subplot(gs[j, 0])
                n_in = int((~adata.obs[k].isna()).sum()) if adata.obs[k].isna().any() else adata.n_obs
                ax.set_title(k + (f'  (covers {n_in:,} of {adata.n_obs:,} cells; others grey)' if n_in < adata.n_obs
                                  else ''), fontsize=9, fontweight='bold', loc='left')
                plot_cluster_key(fig, ax, fig.add_subplot(gs[j, 1]), um, adata.obs[k].astype(str).to_numpy(),
                                 labels, size, args.unknown_label)
            pdf.savefig(fig)
            plt.close(fig)

        # One page per cell type
        for ct in cts:
            pl = plans[ct]
            mask, key, clusters = pl['mask'], pl['key'], pl['clusters']
            sh = pl['shown']
            entries = [('marker', r) for _, r in sh.iterrows()] + [('extra', d) for d in pl['extras']]
            fallback = not entries
            if fallback:
                entries = [('de', g) for g in de.get(ct, []) if g in var_names][:2]
            n_rows = max(1, len(entries))
            fig = plt.figure(figsize=(8.5, 11))
            gs = GridSpec(1 + n_rows, 3, figure=fig, height_ratios=[1.6] + [1] * n_rows,
                          width_ratios=[1, 1.25, 1.15], hspace=0.4, wspace=0.3,
                          left=0.05, right=0.97, top=0.9, bottom=0.05)
            fig.text(0.05, 0.965, ct, fontsize=13, fontweight='bold', color='black')
            skey = 'cell_state' if args.key == 'cell_type' else f'{args.key}_state'
            st_text = ''
            if skey in adata.obs.columns:
                vc = adata.obs.loc[mask, skey].astype(str).value_counts()
                vc = vc[vc.index != 'none']
                if len(vc):
                    st_text = '; states: ' + ', '.join(f'{k} {v / mask.sum():.0%}' for k, v in vc.head(4).items())
            fig.text(0.05, 0.948, f"{mask.sum():,} cells ({mask.mean():.1%})"
                     + (f"; defined at {key}, cluster(s) {', '.join(clusters)}" if key else '') + st_text, fontsize=8)
            cf_ = conf[ct]
            t0 = fig.text(0.05, 0.934, f"Confidence: {cf_['overall']}", fontsize=8, fontweight='bold', va='top',
                          color=CONF_COLOR.get(cf_['overall'], 'black'))
            x1 = fig.transFigure.inverted().transform(
                t0.get_window_extent(fig.canvas.get_renderer()).p1)[0] + 0.008
            fig.text(x1, 0.934, '\n'.join(textwrap.wrap(
                f"(table rows: {cf_['analyst_cells']}; markers: {cf_['markers']}, {cf_['marker_reason']}; "
                f"set by {cf_['decided_by']})", 125)), fontsize=7, va='top')
            ax = fig.add_subplot(gs[0, 0:2])
            plot_highlight(ax, um, mask, pal.get(ct, HIGHLIGHT), size)
            axt = fig.add_subplot(gs[0, 2])
            lines = ['**Annotation rows (applied in file order)']
            for r in pl['rows'].itertuples():
                lines.append(f"{r.key_spec} cluster {r.cluster}: {r.evidence or '(no Evidence text)'}")
            bl = pl['below']
            if len(bl):
                lines.append(f"**Enriched but detected in <{args.min_detect:.0%} of these cells (not ranked)")
                items = [f"{r.symbol} ({r.evidence or 'no tier'}, {r.confidence or '-'}; "
                         f"{r.frac_in:.0%} vs {r.frac_out:.0%})" for r in bl.itertuples()]
                lines.append(', '.join(items[:8]) + (f", and {len(items) - 8} more" if len(items) > 8 else ''))
            ne = pl['not_enriched']
            if len(ne):
                lines.append('**Not enriched here (other markers, or other paralog copies of markers shown below)')
                ne = ne.drop_duplicates('symbol')
                items = [f"{r.symbol} ({r.evidence}, {r.confidence})" for r in ne.itertuples()]
                lines.append(', '.join(items[:12]) + (f", and {len(items) - 12} more" if len(items) > 12 else ''))
            if pl['extra_missing']:
                lines.append('**Extra genes not found in the data or tables: ' + ', '.join(pl['extra_missing']))
            if fallback:
                lines.append('**No enriched marker from the tables: showing top DE genes (data-driven only)')
            text_panel(axt, lines)

            vlabels = adata.obs[key].astype(str).to_numpy() if key else labels
            vhigh = set(clusters) if key else {ct}
            for i, (kind, item) in enumerate(entries):
                j = 1 + i
                g = item['gene_id'] if kind == 'marker' else item['copy']['gene_id'] if kind == 'extra' else item
                if g in col:
                    v = Mk[:, col[g]]
                else:
                    v, _ = gene_matrix(adata, X, var_names, [g])
                v = v.toarray().ravel() if sparse.issparse(v) else np.asarray(v).ravel()
                fin, fout = (v[mask] > 0).mean(), (v[~mask] > 0).mean()
                min_, mout = v[mask].mean(), v[~mask].mean()
                spec = float(specificity(fin, fout, min_ - mout))
                indata = (f"In data: detected in {fin:.1%} of cells vs {fout:.1%} elsewhere "
                          f"({fin / max(fout, 0.001):.0f}x); mean {min_:.2f} vs {mout:.2f}; specificity {spec:.2f}")
                if kind == 'marker':
                    r = item
                    sym = r['symbol']
                    rel = '' if r['match'] in ('exact', 'alias') else f" [marker for {r['cell_type']}]"
                    if r['match'] == 'alias' and str(r['cell_type']).lower() != ct.lower():
                        rel = f" [alias: {r['cell_type']}]"
                    tl = [f"**{sym}{rel}", f"{g}", f"Evidence: {r['evidence'] or '(none)'} / {r['confidence'] or '-'}"]
                    hom = hom_line(r, res)
                    if hom:
                        tl.append(hom)
                    tl += [f"Basis: {r['basis'] or '(none recorded)'}", indata]
                    if r['below_floor']:
                        tl.append(f"Below the detection floor (<{args.min_detect:.0%} of these cells): "
                                  f"no marker reached it")
                    oc = other_copies(pl['allc'], sym, g)
                    if oc:
                        tl.append('Other copies: ' + oc)
                    if str(r['source']):
                        tl.append(f"Source: {r['source']}")
                elif kind == 'extra':
                    d = item['copy']
                    sym = item['term'] if item['term'].upper() != str(g).upper() else (target_symbol(g, res) or g)
                    mt = sorted(set(markers.loc[markers['gene_id'] == g, 'cell_type']))
                    tag = f"extra (table marker for {', '.join(mt)})" if mt else 'extra (not in marker tables)'
                    tl = [f"**{sym}: {tag}", f"{g}",
                          f"Resolved from '{item['term']}': {d['route']}",
                          f"Homolog: {gene_desc(g, res) or 'none'}", indata]
                    if item['others']:
                        tl.append('Other copies: ' + ', '.join(f"{o} ({fi:.0%} vs {fo:.0%})"
                                                               for o, fi, fo in item['others'][:4]))
                else:
                    sym = target_symbol(g, res) or g
                    tl = [f"**{g}", f"Homolog: {gene_desc(g, res) or 'none'}",
                          'Evidence: top DE gene only (not a curated marker)', indata]
                axu = fig.add_subplot(gs[j, 0])
                plot_expr_umap(axu, um, v, size, sym if kind != 'extra' else f'{sym} (extra)')
                axv = fig.add_subplot(gs[j, 1])
                plot_violins(axv, v, vlabels, vhigh, args.max_cells_violin, rng)
                axv.set_xlabel(key or args.key, fontsize=7)
                axx = fig.add_subplot(gs[j, 2])
                text_panel(axx, tl)
                shown_all.setdefault(ct, []).append((g, sym))
            pdf.savefig(fig)
            plt.close(fig)
            print(f'  page: {ct} ({len(entries)} {"DE" if fallback else "marker/extra"} gene(s))')

        # One page per state
        for st in state_names:
            sp = splans[st]
            m, stat = sp['mask'], sp['stat']
            n_rows = max(1, len(sp['show']))
            fig = plt.figure(figsize=(8.5, 11))
            gs = GridSpec(2 + n_rows, 3, figure=fig, height_ratios=[1.5, 0.8] + [1] * n_rows,
                          width_ratios=[1, 1.25, 1.15], hspace=0.6, wspace=0.3,
                          left=0.05, right=0.97, top=0.93, bottom=0.05)
            fig.text(0.05, 0.965, f'State: {st}', fontsize=13, fontweight='bold')
            fig.text(0.05, 0.952, '\n'.join(textwrap.wrap(
                f"{m.sum():,} cells ({m.mean():.1%}); in "
                + ', '.join(f"{t} ({n:,}, {n / max((labels == t).sum(), 1):.0%} of that type)"
                            for t, n in sp['types'].head(4).items())
                + (f", +{len(sp['types']) - 4} more" if len(sp['types']) > 4 else ''), 115)), fontsize=8, va='top')
            ax = fig.add_subplot(gs[0, 0:2])
            plot_highlight(ax, um, m, HIGHLIGHT, size)
            lines = ['**Annotation rows that set this state']
            for r in sp['rows'].itertuples():
                ct = str(r.cell_type).strip()
                who = 'state only (type from other rows)' if ct.lower() in ('', '-', 'na', 'none') else ct
                lines.append(f"{r.key_spec} cluster {r.cluster} -> {who}: {r.evidence or '(no Evidence text)'}")
            if sp['rows'].empty:
                lines.append('(none found: the state is not in the annotation table)')
            nc = [g for g in sp['cited'] if stat.at[g, 'spec'] <= 0]
            if nc:
                lines.append('**Cited genes NOT enriched vs ' + sp['contrast'])
                lines.append(', '.join(f"{g} ({stat.at[g, 'frac_in']:.0%} vs {stat.at[g, 'frac_out']:.0%})"
                                       for g in nc[:10]))
            if not sp['cited']:
                lines.append('**No gene ID cited in the Evidence and no --state-genes: genes below are '
                             'data-driven only')
            text_panel(fig.add_subplot(gs[0, 2]), lines)
            # composition: cell types carrying the state, and share of each sample/condition
            axc = fig.add_subplot(gs[1, 0])
            tys = sp['types'].head(8)[::-1]
            axc.barh(range(len(tys)), tys.values, color=[pal.get(t, HIGHLIGHT) for t in tys.index])
            for yi, (t, n) in enumerate(tys.items()):  # direct labels: type names are too long for tick labels
                axc.text(n + tys.max() * 0.03, yi, f'{t} ({n:,})', va='center', fontsize=6)
            axc.set_xlim(0, tys.max() * 2.2)
            axc.set_yticks([])
            axc.spines['left'].set_visible(False)
            axc.set_xlabel('cells in state', fontsize=7)
            axc.tick_params(labelsize=6)
            if comp_keys:
                k = comp_keys[0]
                tab = pd.Series(m).groupby(adata.obs[k].astype(str).to_numpy()).mean()
                tab = tab.reindex(sorted(tab.index, key=natural_key))
                axs = fig.add_subplot(gs[1, 1])
                axs.bar(range(len(tab)), tab.values * 100, color=HIGHLIGHT)
                pre = os.path.commonprefix(list(tab.index)) if len(tab) > 1 else ''
                short = [g[len(pre):] or g for g in tab.index]
                axs.set_xticks(range(len(tab)))
                axs.set_xticklabels(short, fontsize=6, rotation=90 if max(map(len, short)) * len(tab) > 40 else 0)
                axs.set_xlabel(f'{k}' + (f' ({pre}...)' if pre else ''), fontsize=7)
                axs.set_ylabel('% of cells in state', fontsize=7)
                axs.tick_params(labelsize=6)
            ctext = composition_text(adata.obs, m, comp_keys)
            ctext = ['**Share of each group in this state'] + (ctext or ['(no sample/condition column found; '
                                                                          'use --composition-keys)'])
            ctext += ['**Top genes vs ' + sp['contrast'],
                      ', '.join(f"{target_symbol(g, res) or g} ({stat.at[g, 'frac_in']:.0%} vs "
                                f"{stat.at[g, 'frac_out']:.0%})" for g in sp['top'][:6])]
            text_panel(fig.add_subplot(gs[1, 2]), ctext)
            # gene panels: violins per carrying type, with vs without the state
            tys = list(sp['types'].index[:4])
            in_t = np.isin(labels, tys)
            vlab = np.where(in_t, np.char.add(labels.astype(str), np.where(m, ' +', ' -')), 'other')
            vhigh = {f'{t} +' for t in tys}
            for i, g in enumerate(sp['show']):
                v, _ = gene_matrix(adata, X, var_names, [g])
                v = v.toarray().ravel() if sparse.issparse(v) else np.asarray(v).ravel()
                sym = target_symbol(g, res) or g
                plot_expr_umap(fig.add_subplot(gs[2 + i, 0]), um, v, size, sym)
                axv = fig.add_subplot(gs[2 + i, 1])
                plot_violins(axv, v, vlab, vhigh, args.max_cells_violin, rng)
                for t in axv.get_xticklabels():
                    t.set_rotation(30)
                    t.set_ha('right')
                axv.set_xlabel('')
                axv.text(1.0, 1.02, '+ with / - without the state', transform=axv.transAxes, ha='right',
                         va='bottom', fontsize=6, color='#555555')
                r = stat.loc[g]
                text_panel(fig.add_subplot(gs[2 + i, 2]), [
                    f"**{sym}", f"{g}", f"Shown because: {sp['route'].get(g, '')}",
                    f"Homolog: {gene_desc(g, res) or 'none'}",
                    f"In state: {r['frac_in']:.1%} of cells vs {r['frac_out']:.1%} in {sp['contrast']}; "
                    f"mean {r['mean_in']:.2f} vs {r['mean_out']:.2f}; specificity {r['spec']:.2f}"])
            pdf.savefig(fig)
            plt.close(fig)
            print(f'  state page: {st} ({len(sp["show"])} gene(s); {len(sp["cited"])} cited)')

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
