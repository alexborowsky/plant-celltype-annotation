#!/usr/bin/env python3
"""Per-cluster evidence for cell-type annotation, across one or more clusterings.

For every cluster key (default: all obs columns starting with 'leiden'):
  de_<key>.csv                 top Wilcoxon genes per cluster (+ homolog annotation, pct in/out)
  marker_expression_<key>.tsv  per cluster x marker gene: mean, frac expressing, z across clusters
  marker_scores_<key>.tsv      cluster x cell type matrix of marker scores (mean marker z)
  marker_score_details_<key>.tsv  long table: cluster, cell_type, score, frac, n_markers,
                               n_detected (markers in >= --min-frac of the cluster), max_frac, n_function
  cluster_evidence_<key>.md    human/LLM-readable per-cluster summary
plus cluster_hierarchy.tsv (nesting across keys) and evidence_plots.pdf.

Expression is read from --layer, else adata.raw (if present), else adata.X, and
must be log-normalized (not scaled).

Markers: "in var_names" vs "found" (detected in >= 1 cell). Markers with zero counts
in every cell are reported as not measurable and left out of the scores, like
markers missing from var_names; a warning fires when >= 20% are missing or all-zero.

Flags in cluster_evidence_<key>.md:
  low counts / low genes   cluster median < 0.6x the dataset median (with the ratio to
                           sibling clusters, i.e. same parent at the next coarser key)
  low-QC candidate         counts AND genes < 0.6x both the dataset and sibling medians
  possible doublets        two unrelated cell types co-score: each >= 1 (second >= 0.5
                           when a doublet score is elevated), >= 2 detected and >= 2 driving
                           markers (z >= 1 in >= 10% of cells), drivers not all
                           expression-tier, no shared driving gene, not states, not related
                           by name token, alias (references/markers/celltype_aliases.tsv)
                           or lineage group, also through a third co-scoring type.
                           Gates: counts >= 1.3x the dataset median and, with a per-cell
                           doublet score (obs doublet_score / scrublet_score /
                           scDblFinder.score, or --doublet-scores), a cluster median
                           >= 1.5x the dataset median.
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
    df['symbol'] = df['symbol'].map(clean_text)
    df['symbol'] = df['symbol'].where(df['symbol'] != '', df['gene_id'])
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
    """Fraction of genes whose own ID or rank-1 reference homolog (in any gene map) is in the stress list."""
    if not stress or not len(genes):
        return np.nan, 0
    gms = gm if isinstance(gm, (list, tuple)) else [gm]
    hit = 0
    for g in genes:
        ids = {str(g).upper()}
        for m in gms:
            if m is not None and g in m.index:
                ids.add(str(m.at[g, 'ref_gene']).upper())
        hit += bool(ids & stress)
    return hit / len(genes), hit


# Araport / TAIR placeholders that must never be shown as a gene name or description.
PLACEHOLDER = re.compile(r'^\s*(no (symbol|full name|description|name) available|none|nan|n/a|-)?\s*$',
                         re.I)


def clean_text(x):
    """'' for NaN, empty and placeholder strings ('no symbol available', ...); else the stripped string."""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ''
    s = str(x).strip()
    return '' if PLACEHOLDER.match(s) else s


def load_gene_map(path):
    gm = pd.read_csv(path, sep='\t', dtype={'query_gene': str, 'ref_gene': str})
    gm = gm[gm['hit_rank'] == 1].drop_duplicates('query_gene').set_index('query_gene')
    for c in ('ref_symbol', 'ref_description'):
        if c in gm.columns:
            gm[c] = gm[c].map(clean_text)
        else:
            gm[c] = ''
    return gm


def gene_map_label(gm, path):
    """Short tag for a secondary gene map: the commonest alphabetic prefix of its ref_gene IDs
    (AT1G01010 -> AT, Mp1g00010 -> Mp, Os01g0100100 -> Os), else the file stem."""
    pre = gm['ref_gene'].astype(str).str.extract(r'^([A-Za-z]+)', expand=False).dropna()
    if len(pre):
        return pre.str[:6].value_counts().index[0]
    return os.path.splitext(os.path.basename(path))[0][:12]


def load_gene_annotation(path):
    """gene_id<TAB>symbol<TAB>description (header optional): names for same-species runs."""
    ann = pd.read_csv(path, sep='\t', header=None, dtype=str, usecols=[0, 1, 2],
                      names=['gene_id', 'symbol', 'description']).fillna('')
    if ann.iloc[0, 0].lower() in ('gene_id', 'gene', 'locus', 'id'):
        ann = ann.iloc[1:]
    ann['symbol'] = ann['symbol'].map(clean_text)
    ann['description'] = ann['description'].map(clean_text)
    return ann.drop_duplicates('gene_id').set_index('gene_id')


def _primary_hit_str(r, max_desc):
    sym = clean_text(r.get('ref_symbol', '')).split(',')[0]
    desc = clean_text(clean_text(r.get('ref_description', '')).split(',')[0])[:max_desc]
    out = f"{sym} ({r['ref_gene']})" if sym else str(r['ref_gene'])
    if desc:
        out += f" {desc}"
    try:
        pid = float(r.get('pident', float('nan')))
    except (TypeError, ValueError):
        pid = float('nan')
    rel = clean_text(r.get('relationship', '')) if 'relationship' in r else ''
    if pid == pid:  # not NaN
        out += f" [{pid:.0f}%"
    else:  # orthology-table gene maps carry a relationship instead of % identity
        out += ' [orthology' + (f' {rel}' if rel else '')
    if str(r.get('rbh', '')) == 'yes':
        out += ', RBH'
    return out + ']'


def other_maps_str(gene, others):
    """'[Mp: SYMBOL (MpXXX)] [Os: OsYYY]' from the secondary gene maps (label, gm)."""
    parts = []
    for label, g2 in others or []:
        if gene in g2.index:
            r = g2.loc[gene]
            sym = clean_text(r.get('ref_symbol', '')).split(',')[0]
            parts.append(f"[{label}: {sym} ({r['ref_gene']})]" if sym else f"[{label}: {r['ref_gene']}]")
    return ' '.join(parts)


def homolog_str(gene, gm, max_desc=60, ann=None, others=None):
    """Primary gene-map hit (else the --gene-annotation name), plus secondary maps in brackets."""
    if gm is None or gene not in gm.index:
        out = ''
        if ann is not None and gene in ann.index:
            r = ann.loc[gene]
            out = ' '.join(x for x in (r['symbol'], r['description'][:max_desc]) if x)
    else:
        out = _primary_hit_str(gm.loc[gene], max_desc)
    extra = other_maps_str(gene, others)
    return f"{out} {extra}".strip() if extra else out


def load_aliases(path):
    """alias -> canonical (lower case) from references/markers/celltype_aliases.tsv, if present."""
    if not path or not os.path.exists(path):
        return {}
    try:
        t = pd.read_csv(path, sep='\t', dtype=str, comment='#').fillna('')
    except Exception as e:
        print(f'  WARN could not read {path}: {e}')
        return {}
    if not {'alias', 'canonical'} <= set(t.columns):
        return {}
    out = {}
    for a, c in zip(t['alias'], t['canonical']):
        if a.strip() and c.strip():
            out[a.strip().lower()] = c.strip().lower()
            out.setdefault(c.strip().lower(), c.strip().lower())
    return out


# Cell types that describe a state, not an identity (never part of a doublet pair).
STATE_TYPES = {'s_phase', 'dividing_cells', 'g2_m', 'g2m', 'senescing', 'protoplasting_stress'}
STATE_RE = re.compile(r's_phase|g2_?m|dividing|cycling|mitotic|senesc|stress|heat_shock|wound', re.I)
# Name tokens too generic to make two types related.
NAME_STOP = {'cell', 'cells', 'like', 'type', 'pub', 'published', 'cluster', 'layer', 'zone', 'region', 'tissue',
             'domain', 'other', 'unknown', 'and', 'of', 'the', 'mature', 'immature', 'young', 'early', 'late',
             'putative', 'high', 'low', 'outer', 'inner', 'proximal', 'distal', 'basal', 'apical'}
# Coarse lineage groups: two types in the same group are related, not a doublet pair.
LINEAGE_GROUPS = [
    ('epidermis', re.compile(r'epiderm|pavement|trichom|guard|stomat|subsidiary|trichoblast|root_hair|hair_cell|'
                             r'protoderm|meristemoid', re.I)),
    ('vascular', re.compile(r'phloem|sieve|companion|xylem|tracheary|vessel|procambi|cambium|vascular', re.I)),
    ('ground tissue', re.compile(r'cortex|cortical|endoderm|ground_meristem', re.I)),
    ('root_cap', re.compile(r'root_cap|columella|border', re.I)),
    ('endosperm', re.compile(r'endosperm|aleurone', re.I)),
    ('mesophyll', re.compile(r'mesophyll|palisade|spongy', re.I)),
]


def is_state(ct):
    return str(ct).lower() in STATE_TYPES or bool(STATE_RE.search(str(ct)))


def name_tokens(ct):
    toks = set()
    for t in re.split(r'[_\s/\-.,()+]+', str(ct).lower()):
        t = re.sub(r'\d+$', '', t)
        if len(t) > 2 and t not in NAME_STOP and not t.startswith('pub'):
            toks.add(t)
    return toks


def related_types(a, b, aliases):
    """Reason string if cell types a and b are related by name, alias or lineage, else ''."""
    ca, cb = aliases.get(a.lower(), a.lower()), aliases.get(b.lower(), b.lower())
    if ca == cb:
        return 'aliases'
    shared = (name_tokens(a) | name_tokens(ca)) & (name_tokens(b) | name_tokens(cb))
    if shared:
        return 'shared name ' + '/'.join(sorted(shared))
    for name, rx in LINEAGE_GROUPS:
        if (rx.search(a) or rx.search(ca)) and (rx.search(b) or rx.search(cb)):
            return f'same lineage ({name})'
    return ''


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
    long['detected'] = long['frac'] >= min_frac
    scores = (long.groupby(['cluster', 'cell_type'])
              .agg(score=('z', 'mean'), frac=('frac', 'mean'), n_markers=('gene_id', 'nunique'),
                   n_detected=('detected', 'sum'), max_frac=('frac', 'max'),
                   n_function=('is_function', 'sum'))
              .reset_index())
    scores['n_detected'] = scores['n_detected'].astype(int)
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


def sibling_map(adata, key, keys):
    """cluster -> list of sibling clusters (same majority parent at the next coarser resolution), and that key."""
    r = resolution_of(key)
    if not np.isfinite(r):
        return {}, None
    coarser = [k for k in keys if k != key and np.isfinite(resolution_of(k)) and resolution_of(k) < r]
    if not coarser:
        return {}, None
    ck = max(coarser, key=resolution_of)
    ct = pd.crosstab(adata.obs[key].astype(str), adata.obs[ck].astype(str))
    parent = ct.idxmax(axis=1)
    sib = {cl: [c for c in parent.index[parent == parent[cl]] if c != cl] for cl in parent.index}
    return sib, ck


DRIVER_Z, DRIVER_FRAC = 1.0, 0.1


def doublet_check(cl, s, long, aliases, cratio, dratio, min_frac):
    """Return a short flag string or ''.

    Candidate types: score >= 1 (>= 0.5 for the second type when a per-cell doublet score is
    elevated >= 1.5x), not a state, >= 2 detected markers and >= 2 driving markers (z >= 1 in
    >= 10% of the cluster's cells), drivers not all expression-tier. A pair is skipped when the
    two types share a driving gene or are related by name/alias/lineage, directly or through
    another candidate type. Gates: counts ratio >= 1.3, and doublet-score ratio >= 1.5 if a
    doublet score exists.
    """
    if cratio is None or not np.isfinite(cratio) or cratio < 1.3:
        return ''
    thr2 = 1.0
    if dratio is not None:
        if not np.isfinite(dratio) or dratio < 1.5:
            return ''
        thr2 = 0.5
    lc = long[long['cluster'] == cl]
    cand = []
    for r in s.sort_values('score', ascending=False).itertuples():
        if r.score < thr2 or is_state(r.cell_type) or r.n_detected < 2:
            continue
        g = lc[lc['cell_type'] == r.cell_type]
        drv = g[(g['z'] >= DRIVER_Z) & (g['frac'] >= max(DRIVER_FRAC, min_frac))].sort_values('z', ascending=False)
        if len(drv) < 2 or (drv['evidence'] == 'expression').all():
            continue
        cand.append((r.cell_type, r.score, set(drv['gene_id']), list(drv['symbol'])))
    if not cand or cand[0][1] < 1.0:
        return ''
    # Related = shared driving gene or related names, transitively (Abaxial_Epidermis shares FIL
    # with Spongy_Mesophyll, which is in the mesophyll lineage: Abaxial_Epidermis + Mesophyll is
    # one programme, not two cells).
    comp = list(range(len(cand)))

    def root(i):
        while comp[i] != i:
            i = comp[i]
        return i
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            if cand[i][2] & cand[j][2] or related_types(cand[i][0], cand[j][0], aliases):
                comp[root(j)] = root(i)
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            (a, sa, ga, na), (b, sb, gb, nb) = cand[i], cand[j]
            if sa < 1.0 or root(i) == root(j):
                continue
            why = [f"distinct markers {','.join(dict.fromkeys(na[:2]))} | {','.join(dict.fromkeys(nb[:2]))}"]
            if cratio is not None:
                why.append(f"counts x{cratio:.2f}")
            if dratio is not None:
                why.append(f"doublet score x{dratio:.1f}")
            return f"possible doublets: {a} {sa:.2f} + {b} {sb:.2f} ({'; '.join(why)})"
    return ''


def write_markdown(path, key, adata, de, long, scores, comp, hier, qc_cols, gm, n_show, ann=None, min_frac=0.02,
                   stress=None, stress_flag=0.4, stress_inactive=False, keys=None, others=None, aliases=None,
                   stress_maps=None):
    lab = adata.obs[key].astype(str)
    sizes = lab.value_counts()
    qc_glob = {k: adata.obs[c].median() for k, c in qc_cols.items()}
    if 'doublet' in qc_cols and not qc_glob['doublet']:  # median 0 (e.g. scDblFinder): fall back to the mean
        qc_glob['doublet'] = adata.obs[qc_cols['doublet']].mean()
    sib, sib_key = sibling_map(adata, key, keys or [key])
    aliases = aliases or {}
    with open(path, 'w') as f:
        f.write(f"# Cluster evidence: `{key}` ({len(sizes)} clusters, {adata.n_obs:,} cells)\n\n")
        f.write("Marker score = mean z (across clusters) of a cell type's marker genes' cluster means; "
                "frac = mean fraction of cells expressing those markers; det = markers detected in the cluster / "
                "markers measured; `[1 gene]` = score rests on one detected marker. "
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
            f.write('QC shown as cluster median (x dataset median'
                    + (f'; sib x median of sibling clusters, i.e. clusters sharing its {sib_key} parent' if sib_key
                       else '') + '): '
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
            ratios, sratios = {}, {}
            if qc_cols:
                qparts = []
                smask = lab.isin(sib.get(cl, [])).to_numpy() if sib.get(cl) else None
                for k, c in qc_cols.items():
                    med = adata.obs.loc[mask, c].median()
                    ratio = med / qc_glob[k] if qc_glob[k] else np.nan
                    ratios[k] = ratio
                    txt = f"{k} {med:.3g} (x{ratio:.2f}"
                    if smask is not None and smask.any():
                        smed = adata.obs.loc[smask, c].median()
                        if k == 'doublet' and not smed:
                            smed = adata.obs.loc[smask, c].mean()
                        sratios[k] = med / smed if smed else np.nan
                        txt += f"; sib x{sratios[k]:.2f}"
                    qparts.append(txt + ')')
                    if k in ('counts', 'genes') and ratio < 0.6:
                        if k in sratios and sratios[k] >= 0.6:
                            flags.append(f"low {k} (but x{sratios[k]:.2f} of siblings)")
                        else:
                            flags.append(f"low {k}")
                f.write('- **QC**: ' + ', '.join(qparts) + '\n')
                if 'counts' in ratios and 'genes' in ratios and ratios['counts'] < 0.6 and ratios['genes'] < 0.6:
                    n_before = len(flags)
                    if sratios.get('counts') is not None and sratios.get('genes') is not None:
                        if sratios['counts'] < 0.6 and sratios['genes'] < 0.6:
                            flags.append(f"low-QC candidate (counts/genes x{ratios['counts']:.2f}/x{ratios['genes']:.2f} "
                                         f"of dataset, x{sratios['counts']:.2f}/x{sratios['genes']:.2f} of siblings); "
                                         f"compare with siblings before calling Low_Quality")
                    elif not sib.get(cl):
                        flags.append(f"low-QC candidate (counts/genes x{ratios['counts']:.2f}/x{ratios['genes']:.2f} "
                                     f"of dataset; no sibling clusters); compare with siblings before calling "
                                     f"Low_Quality")
                    if len(flags) > n_before:  # the candidate flag replaces the separate low counts/genes ones
                        flags = [x for x in flags if not x.startswith(('low counts', 'low genes'))]
            d = de[de['cluster'] == cl].head(n_show) if not de.empty else pd.DataFrame()
            if stress and len(d):
                sfrac, shit = stress_fraction(list(d['gene']), stress_maps if stress_maps else gm, stress)
                f.write(f"- **Stress**: {shit}/{len(d)} top DE genes protoplasting-induced ({sfrac:.0%})\n")
                if sfrac >= stress_flag:
                    flags.append(f"dissociation-stress signature ({sfrac:.0%} of top DE)")
            if hier is not None:
                h = hier[(hier['key'] == key) & (hier['cluster'] == cl)]
                pcols = [c for c in h.columns if c.startswith('parent_') and h[c].notna().any()]
                if len(h) and pcols:
                    f.write('- **Parents**: ' + ', '.join(f"{c[7:]}={h.iloc[0][c]}" for c in pcols) + '\n')
            s_all = scores[scores['cluster'] == cl] if not scores.empty else pd.DataFrame()
            if len(s_all):
                dflag = doublet_check(cl, s_all, long, aliases, ratios.get('counts'), ratios.get('doublet'), min_frac)
                if dflag:
                    flags.append(dflag)
            if flags:
                f.write('- **FLAGS**: ' + '; '.join(flags) + '\n')
            if len(s_all):
                s = s_all.sort_values('score', ascending=False).head(4)
                parts = []
                for r in s.itertuples():
                    top = (long[(long['cluster'] == cl) & (long['cell_type'] == r.cell_type)]
                           .sort_values('z', ascending=False).head(3))
                    oth = long[(long['cluster'] != cl) & (long['cell_type'] == r.cell_type)]
                    fout = oth.groupby('gene_id')['frac'].mean()
                    drv = ','.join(f"{t.symbol}{'*' if t.is_function else ''}:{t.z:.1f} "
                                   f"({t.frac:.0%} vs {fout.get(t.gene_id, 0):.0%})"
                                   for t in top.itertuples())
                    one = ' [1 gene]' if r.n_detected == 1 else ''
                    parts.append(f"{r.cell_type} {r.score:.2f}{one} (frac {r.frac:.2f}; det {r.n_detected}/{r.n_markers}"
                                 f"; best {r.max_frac:.0%}; {drv})")
                f.write('- **Marker scores**: ' + ' | '.join(parts) + '\n')
            if len(d):
                f.write('\n| gene | logFC | pct in/out | homolog |\n|---|---|---|---|\n')
                for r in d.itertuples():
                    gname = r.gene
                    in_gm = gm is not None and r.gene in gm.index
                    if ann is not None and in_gm and r.gene in ann.index and ann.at[r.gene, 'symbol']:
                        gname = f"{r.gene} ({ann.at[r.gene, 'symbol']})"
                    f.write(f"| {gname} | {r.logfc:+.2f} | {r.pct_in:.2f}/{r.pct_out:.2f} | "
                            f"{homolog_str(r.gene, gm, ann=ann, others=others)} |\n")
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
    p.add_argument('--gene-map', nargs='+', default=None,
                   help='one or more gene_map.tsv files from map_markers.py. The first is primary (its symbol and '
                        'description are shown); hits from the others are appended as [<prefix>: SYMBOL (ID)], '
                        'the prefix being the commonest letter prefix of that map\'s ref_gene IDs (AT, Mp, Os, ...)')
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
    p.add_argument('--doublet-scores', default=None,
                   help='per-cell doublet scores (TSV/CSV, cell barcode in the first column; column doublet_score, '
                        'scrublet_score or scDblFinder.score, else the first numeric column), stored as '
                        'obs[doublet_score]. Not needed when obs already has one of those columns. With a doublet '
                        'score, the possible-doublet flag needs a cluster median >= 1.5x the dataset median')
    p.add_argument('--aliases', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references',
                                                     'markers', 'celltype_aliases.tsv'),
                   help='alias<TAB>canonical table; aliased cell types are never paired in the doublet flag '
                        '(default: references/markers/celltype_aliases.tsv, skipped if missing)')
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

    if args.doublet_scores:
        sep = ',' if args.doublet_scores.endswith('.csv') else '\t'
        t = pd.read_csv(args.doublet_scores, sep=sep, index_col=0)
        t.index = t.index.astype(str)
        col = pick(t, QC_CANDIDATES['doublet']) or next(
            (c for c in t.columns if pd.api.types.is_numeric_dtype(t[c]) and t[c].dtype != bool), None)
        if col is None:
            raise SystemExit(f'{args.doublet_scores}: no numeric doublet-score column')
        match = adata.obs_names.isin(t.index).mean()
        print(f'  doublet scores: {args.doublet_scores} column {col!r}, {match:.1%} of cells matched')
        if match < 0.5:
            print('  WARN <50% of cells have a doublet score: check barcode suffixes; doublet gate uses the matched cells')
        for c in QC_CANDIDATES['doublet']:
            if c in adata.obs.columns and c != 'doublet_score':
                print(f'  NOTE obs[{c!r}] is ignored; using obs[doublet_score] from --doublet-scores')
        adata.obs['doublet_score'] = t[col].reindex(adata.obs_names).astype(float).to_numpy()
        QC_CANDIDATES['doublet'] = ['doublet_score']

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
        # Detected = nonzero in >= 1 cell. A gene in var_names with zero counts everywhere is not
        # measurable here (filtered counts, unexpressed in this tissue, or reads lost to multimapping).
        Mk0, found0 = gene_matrix(adata, X, var_names, markers.loc[present, 'gene_id'])
        nnz = (np.asarray((Mk0 != 0).sum(0)).ravel() if found0 else np.zeros(0))
        detected = {g for g, k in zip(found0, nnz) if k > 0}
        del Mk0
        expressed = markers['gene_id'].isin(detected)
        zero = present & ~expressed
        n_tot = len(markers)
        print(f'  markers: {int(present.sum())}/{n_tot} in var_names, {int(expressed.sum())}/{n_tot} found '
              f'(detected in >= 1 cell)')
        def by_type(sub):
            for ct, g in sub.groupby('cell_type'):
                print(f"    {ct:24s} " + ', '.join(f"{s}({i})" if s != i else i
                                                   for s, i in zip(g['symbol'], g['gene_id'])))
        if (~present).any():
            print('  WARN markers not in var_names (filtered upstream or ID mismatch), by cell type:')
            by_type(markers[~present])
        if zero.any():
            print('  WARN markers in var_names but with 0 counts in every cell: not measurable here, by cell type:')
            by_type(markers[zero])
        miss = 1 - expressed.mean() if n_tot else 0
        if miss >= 0.2:
            print(f'  WARN {miss:.0%} of marker rows are missing or all-zero ({int((~present).sum())} not in '
                  f'var_names, {int(zero.sum())} all-zero). Absent evidence for those types is not evidence of '
                  f'absence: check the gene list (unfiltered object / .raw), ID versions, and the marker table')
        none_left = sorted(set(markers['cell_type']) - set(markers.loc[expressed, 'cell_type']))
        if none_left:
            print('  WARN cell types with NO measurable marker in the data: ' + ', '.join(none_left))
        markers = markers[expressed]

    gms = [load_gene_map(g) for g in (args.gene_map or [])]
    gm = gms[0] if gms else None
    others = [(gene_map_label(g, path), g) for g, path in zip(gms[1:], (args.gene_map or [])[1:])]
    for i, (g, path) in enumerate(zip(gms, args.gene_map or [])):
        rate = var_names.isin(g.index).mean()
        tag = 'gene map' if i == 0 else f'gene map {i + 1} [{others[i - 1][0]}]'
        print(f'  {tag} ({os.path.basename(path)}) covers {rate:.1%} of expression var_names')
        if rate < 0.5:
            print('  WARN <50% of var_names found in gene map: check --query-strip-regex in map_markers.py')
    aliases = load_aliases(args.aliases)
    if aliases:
        print(f'  cell-type aliases: {len(aliases)} names from {args.aliases}')

    ann = load_gene_annotation(args.gene_annotation) if args.gene_annotation else None
    if ann is not None:
        print(f'  gene annotation covers {var_names.isin(ann.index).mean():.1%} of var_names')
    stress = load_stress_genes(args.stress_genes) if args.stress_genes else None
    stress_inactive = False
    if stress:
        ids = set(map(str.upper, var_names))
        for g in gms:
            ids |= set(g['ref_gene'].astype(str).str.upper())
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
            if (gm is not None or ann is not None) and not de.empty:
                # ref_symbol / ref_description: primary gene-map hit, else the --gene-annotation name
                sym = pd.Series('', index=de.index)
                desc = pd.Series('', index=de.index)
                if gm is not None:
                    j = gm.reindex(de['gene'])
                    de['ref_gene'] = j['ref_gene'].to_numpy()
                    sym = pd.Series(j['ref_symbol'].map(clean_text).to_numpy(), index=de.index)
                    desc = pd.Series(j['ref_description'].map(clean_text).to_numpy(), index=de.index)
                    de['pident'] = j['pident'].to_numpy()
                if ann is not None:
                    a = ann.reindex(de['gene']).fillna('')
                    de['symbol'] = a['symbol'].to_numpy()
                    nohit = (sym == '') & (desc == '')
                    if gm is not None:
                        nohit &= de['ref_gene'].isna()
                    sym = sym.where(~nohit, a['symbol'].to_numpy())
                    desc = desc.where(~nohit, a['description'].to_numpy())
                de['ref_symbol'] = sym.to_numpy()
                de['ref_description'] = desc.to_numpy()
                if others:
                    de['other_homologs'] = [other_maps_str(g, others) for g in de['gene']]
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
            det = scores.copy()
            det['_o'] = det['cluster'].map(natural_key)
            det.sort_values(['_o', 'score'], ascending=[True, False]).drop(columns='_o').to_csv(
                os.path.join(args.output, f'marker_score_details_{key}.tsv'), sep='\t', index=False,
                float_format='%.3f')
        comp = composition(adata, key, meta)
        write_markdown(os.path.join(args.output, f'cluster_evidence_{key}.md'), key, adata,
                       de, long, scores, comp, hier, qc_cols, gm, args.n_show, ann=ann, min_frac=args.min_frac,
                       stress=stress, stress_flag=args.stress_flag, stress_inactive=stress_inactive,
                       keys=keys, others=others, aliases=aliases, stress_maps=gms)
        print(f'  wrote cluster_evidence_{key}.md')

    if not args.skip_plots:
        print('[4] Plots')
        plots(adata, keys, markers, os.path.join(args.output, 'evidence_plots.pdf'),
              args.use_raw, args.layer)
    print('Done.')


if __name__ == '__main__':
    main()
