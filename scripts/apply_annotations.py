#!/usr/bin/env python3
"""Apply a cluster -> cell-type annotation table to an AnnData object and validate it.

Annotation rows (Resolution, Cluster, CellType[, Evidence...]) are applied in
FILE ORDER and each row only labels cells no earlier row has claimed ("first match
wins"), so list specific (high-resolution / subcluster) rows before broad ones. A row
with CellType "Unknown" claims its cells too, which excludes clusters (low quality,
doublets) from later, broader rows.
Resolution is either a number (-> obs['leiden_res<number>']) or any obs column,
including columns brought in with --import-labels.

Outputs (in --plots-dir): annotation_log.tsv, cell_type_counts.tsv,
annotation_qc.pdf (UMAP, marker dotplot by cell type, cell type x cluster crosstab).
"""

import argparse
import os
import warnings

import numpy as np
import pandas as pd
import scanpy as sc

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

UNKNOWN_COLOR = '#C8C8C8'

# Semantic defaults (used when no --colors entry exists), matched on lowercase
# substrings in order; specific names precede generic ones. Colors come from the
# Okabe-Ito / Paul Tol colorblind-safe sets: photosynthetic green, phloem warm,
# xylem blue (water), stress/defense wine-red, epidermis orange, cell cycle olive.
# Ten-plus types cannot all be colorblind-separable on one map, so plots should
# also label cell types directly.
SEMANTIC_COLORS = [
    ('defense', '#882255'), ('stress', '#882255'), ('respons', '#882255'),
    ('bundle_sheath', '#117733'), ('mesophyll', '#009E73'), ('palisade', '#009E73'),
    ('spongy', '#44AA99'),
    ('subsidiary', '#7570B3'), ('guard', '#CC79A7'), ('stomat', '#CC79A7'),
    ('atrichoblast', '#E69F00'), ('trichoblast', '#DDAA33'), ('root_hair', '#DDAA33'),
    ('trichome', '#CCBB44'), ('epiderm', '#E69F00'), ('pavement', '#E69F00'),
    ('protoderm', '#E69F00'), ('silica', '#BBBB77'), ('ligule', '#999933'),
    ('phloem_parenchyma', '#EE6677'), ('companion', '#D55E00'), ('sieve', '#AA3377'),
    ('phloem', '#D55E00'),
    ('xylem_parenchyma', '#56B4E9'), ('xylem', '#0072B2'),
    ('procambium', '#88CCEE'), ('vascul', '#88CCEE'), ('stele', '#88CCEE'),
    ('pericycle', '#6699CC'), ('endoderm', '#228833'), ('cortex', '#44AA99'),
    ('sclerenchyma', '#666633'),
    ('quiescent', '#997700'), ('columella', '#997700'), ('root_cap', '#BB9944'),
    ('s_phase', '#999933'), ('dividing', '#999933'), ('g2', '#999933'),
    ('senesc', '#8C510A'),
]
FALLBACK_COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#56B4E9', '#E69F00',
                   '#4477AA', '#228833', '#AA3377', '#66CCEE', '#CCBB44', '#EE6677']


def semantic_color(name):
    n = str(name).lower()
    for pat, col in SEMANTIC_COLORS:
        if pat in n:
            return col
    return None


def parse_annotations(path):
    rows = []
    with open(path) as fh:
        fh.readline()  # header
        for ln, line in enumerate(fh, start=2):
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            if '\t' in line:
                parts = [p.strip() for p in line.rstrip('\n').split('\t')]
                if len(parts) < 3:
                    print(f'  WARN line {ln}: <3 columns, skipped')
                    continue
                res, cl, ct = parts[:3]
                ev = ' '.join(parts[3:])
            else:  # legacy whitespace-delimited
                parts = line.split()
                if len(parts) < 3:
                    print(f'  WARN line {ln}: <3 columns, skipped')
                    continue
                res, cl, ct, ev = parts[0], parts[1], '_'.join(parts[2:]), ''
            rows.append({'line': ln, 'key_spec': res, 'cluster': cl, 'cell_type': ct, 'evidence': ev})
    return pd.DataFrame(rows)


def resolve_key(spec, obs_cols):
    if spec in obs_cols:
        return spec
    try:
        float(spec)
    except ValueError:
        return None
    for cand in (f'leiden_res{spec}', f'snn_res{spec}', f'SCT_snn_res.{spec}', f'RNA_snn_res.{spec}',
                 f'integrated_snn_res.{spec}', f'louvain_res{spec}'):
        if cand in obs_cols:
            return cand
    return None


def cluster_mask(series, cluster):
    """Cells whose cluster is in a comma-separated list ("0,1,12" or a single value)."""
    wanted = {c.strip() for c in str(cluster).split(',') if c.strip()}
    return series.astype(str).isin(wanted).to_numpy()


def import_labels(adata, spec):
    """spec = path:col[:new_name]; copies labels onto matching cells.

    path is an .h5ad (col is an obs column) or a .csv/.tsv/.txt table whose
    first column holds cell barcodes (e.g. published per-cell labels).
    """
    parts = spec.split(':')
    if len(parts) < 2:
        raise SystemExit(f'--import-labels expects path:col[:new_name], got {spec}')
    path, col = parts[0], parts[1]
    new = parts[2] if len(parts) > 2 else col
    if path.endswith('.h5ad'):
        sub = sc.read_h5ad(path, backed='r')
        labels = sub.obs[col].astype(str).copy()
        sub.file.close()
    else:
        tab = pd.read_csv(path, sep=None, engine='python', index_col=0, dtype=str)
        if col not in tab.columns:
            raise SystemExit(f'{col} not in {path}; columns: {list(tab.columns)}')
        labels = tab[col].dropna().astype(str)
        labels.index = labels.index.astype(str)
    common = adata.obs_names.intersection(labels.index)
    if len(common) < 0.5 * len(labels) and 'sample' in adata.obs.columns:
        # try the sample-prefixed uniquification used when obs_names collide across samples
        alt = pd.Index(adata.obs['sample'].astype(str) + '_' + adata.obs_names.astype(str))
        c2 = alt.intersection(labels.index)
        if len(c2) > len(common):
            m = pd.Series(adata.obs_names, index=alt)
            labels = labels.loc[c2]
            labels.index = m.loc[c2].values
            common = labels.index
    print(f'  imported {col} from {path} as {new}: {len(common):,}/{len(labels):,} cells matched')
    if len(common) < 0.5 * len(labels):
        print(f'  WARN low match; example barcodes: labels {list(labels.index[:3])}, '
              f'h5ad {list(adata.obs_names[:3])}')
    if len(common) == 0:
        raise SystemExit(f'No barcode overlap between {path} and the h5ad obs_names')
    adata.obs[new] = pd.Series(labels.loc[common].values, index=common).reindex(adata.obs_names).values
    return new


def canonical_names(ann, colors):
    lut = {k.lower(): k for k in colors}
    fixed = ann['cell_type'].map(lambda c: lut.get(c.lower(), c))
    for a, b in zip(ann['cell_type'], fixed):
        if a != b:
            print(f'  renamed {a} -> {b} (matches color table)')
    ann['cell_type'] = fixed
    return ann


def apply(adata, ann, out_key, unknown):
    lab = np.array([unknown] * adata.n_obs, dtype=object)
    claimed = np.zeros(adata.n_obs, dtype=bool)  # an explicit Unknown row also claims its cells
    log = []
    cols = set(adata.obs.columns)
    for r in ann.itertuples():
        key = resolve_key(r.key_spec, cols)
        if key is None:
            print(f'  WARN line {r.line}: no obs column for "{r.key_spec}"; skipped')
            log.append({**r._asdict(), 'obs_key': '', 'n_cluster': 0, 'n_new': 0, 'n_shadowed': 0,
                        'status': 'missing_key'})
            continue
        in_cl = cluster_mask(adata.obs[key], r.cluster)
        free = ~claimed
        n_new = int((in_cl & free).sum())
        n_sh = int((in_cl & ~free).sum())
        lab[in_cl & free] = r.cell_type
        claimed |= in_cl
        status = 'ok'
        if in_cl.sum() == 0:
            status = 'no_such_cluster'
        elif n_new == 0:
            status = 'fully_shadowed'
        elif n_sh > 0.5 * in_cl.sum():
            status = 'mostly_shadowed'
        if status != 'ok':
            print(f'  WARN line {r.line}: {key}={r.cluster} -> {r.cell_type}: {status}')
        print(f'  {key:>22s} {str(r.cluster):>5s} -> {r.cell_type:24s} {n_new:>9,} new {n_sh:>9,} already')
        log.append({**r._asdict(), 'obs_key': key, 'n_cluster': int(in_cl.sum()),
                    'n_new': n_new, 'n_shadowed': n_sh, 'status': status})
    cats = sorted(set(lab) - {unknown}) + ([unknown] if unknown in set(lab) else [])
    adata.obs[out_key] = pd.Categorical(lab, categories=cats)
    return pd.DataFrame(log).drop(columns=['Index'], errors='ignore')


def set_colors(adata, key, colors, unknown):
    cats = list(adata.obs[key].cat.categories)
    auto = iter(FALLBACK_COLORS + [matplotlib.colors.to_hex(c) for c in plt.get_cmap('tab20').colors])
    pal = []
    for c in cats:
        if c == unknown:
            pal.append(UNKNOWN_COLOR)
        elif c in colors:
            pal.append(colors[c])
        else:
            sem = semantic_color(c)
            pal.append(sem or next(auto))
            print(f'  no color for {c}; assigned {"semantic" if sem else "fallback"} {pal[-1]}')
    adata.uns[f'{key}_colors'] = np.array(pal)


def load_markers(paths):
    alias = {'NbID': 'gene_id', 'Gene': 'symbol', 'CellType': 'cell_type'}
    frames = []
    for path in paths:
        df = pd.read_csv(path, sep='\t', dtype=str).fillna('')
        df = df.rename(columns={k: v for k, v in alias.items() if k in df.columns and v not in df.columns})
        if 'symbol' not in df.columns:
            df['symbol'] = df['gene_id']
        frames.append(df)
    return pd.concat(frames, ignore_index=True).fillna('').drop_duplicates(['gene_id', 'cell_type'])


def qc_report(adata, key, markers, plots_dir, cluster_key, meta, unknown):
    pdf_path = os.path.join(plots_dir, 'annotation_qc.pdf')
    with PdfPages(pdf_path) as pdf:
        if 'X_umap' in adata.obsm:
            fig, ax = plt.subplots(figsize=(10, 8))
            sc.pl.umap(adata, color=key, ax=ax, show=False, size=max(1, 120000 / adata.n_obs),
                       title=key)
            for ch in ax.get_children():
                if hasattr(ch, 'set_rasterized'):
                    ch.set_rasterized(True)
            pdf.savefig(fig, dpi=150, bbox_inches='tight')
            plt.close('all')
        if markers is not None:
            src = adata.raw if adata.raw is not None else adata
            var_src = pd.Index(src.var_names)
            mk = markers[markers['gene_id'].isin(var_src)].drop_duplicates('gene_id').copy()
            # At most 4 markers per annotated type, best evidence/confidence first, labelled by symbol.
            tier = {'function': 0, 'characterized_enriched': 1, 'expression': 2}
            conf = {'high': 0, 'medium': 1, 'low': 2}
            mk['_r'] = mk.get('evidence', '').map(tier).fillna(3) * 3 + mk.get('confidence', '').map(conf).fillna(3)
            order = [c for c in adata.obs[key].cat.categories if c != unknown]
            groups, labels, used = {}, {}, set()
            for ct in order:
                g = mk[mk['cell_type'] == ct].sort_values('_r').head(4)
                names = []
                for gid, sym in zip(g['gene_id'], g.get('symbol', g['gene_id'])):
                    lab = str(sym) if str(sym) not in ('', '-', 'nan') else gid
                    while lab in used:
                        lab += "'"
                    used.add(lab); labels[gid] = lab; names.append(lab)
                if names:
                    groups[ct] = names
            if groups:
                try:
                    import anndata
                    gids = list(labels)
                    Xs = src[:, gids].X if adata.raw is not None else adata[:, gids].X
                    tmp = anndata.AnnData(X=Xs, obs=adata.obs[[key]].copy(),
                                          var=pd.DataFrame(index=[labels[g] for g in gids]))
                    dp = sc.pl.dotplot(tmp, groups, groupby=key, show=False, standard_scale='var',
                                       cmap='viridis', return_fig=True)
                    dp.make_figure()
                    pdf.savefig(plt.gcf(), bbox_inches='tight')
                except Exception as e:
                    print(f'  WARN dotplot failed: {e}')
                plt.close('all')
        if cluster_key and cluster_key in adata.obs.columns:
            ct = pd.crosstab(adata.obs[key], adata.obs[cluster_key].astype(str), normalize='columns')
            ct = ct[sorted(ct.columns, key=lambda s: (0, int(s)) if s.isdigit() else (1, s))]
            fig, ax = plt.subplots(figsize=(max(8, 0.35 * ct.shape[1]), max(4, 0.35 * ct.shape[0])))
            im = ax.imshow(ct.values, aspect='auto', cmap='Blues', vmin=0, vmax=1)
            ax.set_xticks(range(ct.shape[1]))
            ax.set_xticklabels(ct.columns, rotation=90, fontsize=7)
            ax.set_yticks(range(ct.shape[0]))
            ax.set_yticklabels(ct.index, fontsize=8)
            ax.set_xlabel(cluster_key)
            ax.set_title('Fraction of each cluster assigned to each cell type')
            fig.colorbar(im, ax=ax, fraction=0.03)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close('all')
        for m in meta:
            if m not in adata.obs.columns:
                continue
            ct = pd.crosstab(adata.obs[key], adata.obs[m].astype(str), normalize='columns')
            fig, ax = plt.subplots(figsize=(max(6, 0.6 * ct.shape[1] + 3), 6))
            ct.T.plot(kind='bar', stacked=True, ax=ax, width=0.85,
                      color=list(adata.uns.get(f'{key}_colors', [])) or None, legend=False)
            ax.set_ylabel('fraction of cells')
            ax.set_title(f'Cell-type composition by {m}')
            ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize=7)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close('all')
    print(f'  QC report: {pdf_path}')


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True)
    p.add_argument('--annotations', required=True)
    out = p.add_mutually_exclusive_group(required=True)
    out.add_argument('--out-h5ad', help='write annotated object here')
    out.add_argument('--inplace', action='store_true', help='overwrite --h5ad')
    out.add_argument('--no-write', action='store_true', help='only produce logs/plots')
    p.add_argument('--colors', default=None, help='CellType<TAB>Color table')
    p.add_argument('--markers', nargs='+', default=None, help='marker table(s) for the validation dotplot')
    p.add_argument('--import-labels', action='append', default=[],
                   help='path:col[:new_name] (repeatable); path is an .h5ad (e.g. subcluster '
                        'labels) or a barcode-indexed .csv/.tsv (e.g. published labels)')
    p.add_argument('--key', default='cell_type', help='obs column to write')
    p.add_argument('--unknown-label', default='Unknown')
    p.add_argument('--plots-dir', default=None)
    p.add_argument('--cluster-key', default=None,
                   help='cluster column for the crosstab (default: finest key used in the table)')
    p.add_argument('--meta-keys', nargs='*', default=['sample'])
    args = p.parse_args()

    print(f'[1] Loading {args.h5ad}')
    adata = sc.read_h5ad(args.h5ad)
    print(f'  {adata.n_obs:,} cells x {adata.n_vars:,} genes')
    if 'log1p' in adata.uns and 'base' not in adata.uns['log1p']:
        adata.uns['log1p']['base'] = None
    for spec in args.import_labels:
        import_labels(adata, spec)

    print(f'[2] Parsing {args.annotations}')
    ann = parse_annotations(args.annotations)
    print(f'  {len(ann)} rows')
    colors = {}
    if args.colors:
        cdf = pd.read_csv(args.colors, sep='\t')
        colors = dict(zip(cdf['CellType'], cdf['Color']))
        ann = canonical_names(ann, colors)

    print('[3] Applying (file order, first match wins)')
    log = apply(adata, ann, args.key, args.unknown_label)
    set_colors(adata, args.key, colors, args.unknown_label)

    vc = adata.obs[args.key].value_counts()
    print('\n  Summary:')
    for ct, n in vc.items():
        print(f'    {ct:28s} {n:>9,} ({n / adata.n_obs:5.1%})')

    if args.plots_dir:
        os.makedirs(args.plots_dir, exist_ok=True)
        log.to_csv(os.path.join(args.plots_dir, 'annotation_log.tsv'), sep='\t', index=False)
        meta = [m for m in args.meta_keys if m in adata.obs.columns]
        counts = pd.crosstab(adata.obs[args.key], [adata.obs[m].astype(str) for m in meta]) \
            if meta else vc.to_frame('n_cells')
        counts.to_csv(os.path.join(args.plots_dir, 'cell_type_counts.tsv'), sep='\t')
        ck = args.cluster_key
        if ck is None:
            used = [k for k in log.get('obs_key', []) if k]
            ck = max(used, key=lambda k: adata.obs[k].nunique()) if used else None
        markers = load_markers(args.markers) if args.markers else None
        print('[4] QC plots')
        qc_report(adata, args.key, markers, args.plots_dir, ck, meta, args.unknown_label)

    if not args.no_write:
        dest = args.h5ad if args.inplace else args.out_h5ad
        print(f'[5] Writing {dest}')
        adata.write_h5ad(dest)
    print('Done.')


if __name__ == '__main__':
    main()
