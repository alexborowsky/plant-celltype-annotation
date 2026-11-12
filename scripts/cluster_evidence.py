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
  organellar_DNA           (--assay atac, or with --organelle-regex) >= --organelle-flag of
                           the top DE genes are organelle-like loci: gene ID, var chromosome
                           column or rank-1 reference hit (ATCG/ATMG) matches the regex.
                           In ATAC these are nuclear insertions of plastid/mitochondrial DNA
                           (NUPT/NUMT) picking up organellar reads: the ATAC version of ambient RNA.

Depth-matched mode (--depth-key, on by default with --assay atac): detection rises with depth
(UMIs, fragments), so a deep cluster "wins" unrelated markers on raw in-vs-out fractions. Cells are
binned by depth quantiles (--depth-bins); a gene's expected fraction in a cluster is the
detection rate of the cells outside the cluster in each depth bin, weighted by the cluster's
own depth distribution. O/E = observed / expected fraction. Marker types are then ranked by
score_oe (mean log2 O/E of the type's markers; markers below --min-frac contribute <= 0), the
drivers shown are the top markers by O/E, and the DE genes shown per cluster are reordered by
O/E. The z-based score is kept alongside.

--assay atac (gene activity built from accessibility): turns on the depth-matched mode
(obs total_counts / n_fragments / nCount_peaks ...), the organellar_DNA flag, and reports
markers missing from var_names as unmeasurable (no accessible region). The protoplasting stress
list and the possible-doublet flag are switched off (nuclei; depth outliers are not RNA-style
doublets) and the markdown says so.
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
# ATAC: extra QC columns (shown, never used for flags other than counts/genes)
ATAC_QC = {
    'counts': ['total_counts', 'n_fragments', 'nCount_peaks', 'nCount_ATAC', 'n_counts', 'passed_filters'],
    'genes': ['n_genes_by_counts', 'n_regions', 'n_peaks', 'nFeature_peaks', 'nFeature_ATAC', 'n_genes'],
    'tss': ['tss_enrichment', 'TSSEnrichment', 'tsse', 'TSS_enrichment'],
    'frip': ['frip', 'FRiP', 'pct_reads_in_peaks'],
}
RANK_SHRINK_K = 2  # marker-score ranking: mean x n/(n+2) (1 gene x0.33, 2 x0.5, 4 x0.67, 10 x0.83)
DEPTH_CANDIDATES = ['total_counts', 'n_fragments', 'nCount_peaks', 'nCount_ATAC', 'n_counts', 'nCount_RNA']
# Organelle-like loci, matched against gene ID, var chromosome column and rank-1 reference hit ID.
# Conservative on purpose: unplaced-scaffold names (e.g. Catharanthus CRO.S00...) are not matched;
# pass --organelle-regex for those.
DEFAULT_ORGANELLE = (r'(?i)^(ATCG|ATMG)\d|^(chr)?(C|M|Pt|Mt|Cp|chloroplast|mitochondrion|mitochondria|plastid)'
                     r'([_:.\-]|$)|chloroplast|mitochondri|plastome|plastid_genome')
# Organellar gene products in a gene description (rank-1 reference hit or --gene-annotation). Only products
# encoded in plant organellar genomes (rbcL, ycf, atp8/9, cox1-3, cob, ccm, matR, plastid NDH/PSI/PSII subunits as
# named in Araport); nuclear-encoded paralogs are named differently there.
ORGANELLE_DESC = re.compile(r'(?i)\b(ycf\d+|atp ?8|atp ?9|ATP synthase (9|subunit 9) mitochondrial|matR|ccmF|ccmB|ccmC|'
                            r'ribulose bisphosphate carboxylase large chain|NADH-plastoquinone oxidoreductase subunit|'
                            r'NADH:ubiquinone/plastoquinone oxidoreductase, chain|cytochrome c oxidase,? subunit (I|II|III)\b|'
                            r'plant mitochondrial ATPase|mitochondrially encoded|chloroplast[- ]encoded|'
                            r'Mitovirus RNA-dependent)')
NUMT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references', 'annotation',
                         'arabidopsis_numt_chr2.tsv')


def load_numt():
    try:
        t = pd.read_csv(NUMT_FILE, sep='\t', comment='#', dtype=str)
        return set(t['gene_id'].str.upper())
    except (OSError, KeyError, ValueError):
        return set()


NUMT_SET = load_numt()
CHROM_COLS = ['chrom', 'chr', 'seqname', 'seqid', 'Chromosome', 'chromosome', 'seqnames']


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


class DepthBins:
    """Per-cell depth quantile bin (-1 = missing depth) and log depth."""

    def __init__(self, depth, n_bins=20):
        d = np.asarray(depth, dtype=float)
        ok = np.isfinite(d) & (d > 0)
        self.codes = np.full(len(d), -1, dtype=int)
        self.x = np.where(ok, np.log(np.where(ok, d, 1.0)), np.nan)
        if ok.sum() >= 2:
            # rank first so ties (binary/low-count data) still split into quantiles
            r = pd.Series(d[ok]).rank(method='first')
            self.codes[ok] = pd.qcut(r, min(n_bins, int(ok.sum())), labels=False, duplicates='drop').astype(int)
        self.n = int(self.codes.max()) + 1 if ok.any() else 0

    def subset(self, mask):
        out = DepthBins.__new__(DepthBins)
        out.codes, out.x, out.n = self.codes[mask], self.x[mask], self.n
        return out


def depth_bins(depth, n_bins=20):
    return DepthBins(depth, n_bins)


def _cloglog_fit(x, n, y, iters=12):
    """Binomial GLM, complementary log-log link, detection ~ a + b*log(depth), fitted per gene on binned
    counts (x: bins; n: cells per bin; y: bins x genes detected). This is the Poisson detection model
    (P = 1 - exp(-rate * depth)) with a free slope. Returns (a, b) arrays over genes."""
    n = n[:, None] + 1.0
    p = (y + 0.5) / n
    eta = np.log(-np.log1p(-np.clip(p, 1e-6, 1 - 1e-6)))
    X1 = x[:, None]
    for _ in range(iters):
        e = np.exp(np.clip(eta, -30, 5))
        mu = np.clip(1 - np.exp(-e), 1e-6, 1 - 1e-6)
        dmu = np.maximum(e * np.exp(-e), 1e-9)
        w = n * dmu ** 2 / (mu * (1 - mu))
        z = eta + (p - mu) / dmu
        sw, swx, swxx = w.sum(0), (w * X1).sum(0), (w * X1 ** 2).sum(0)
        swz, swxz = (w * z).sum(0), (w * X1 * z).sum(0)
        det = sw * swxx - swx ** 2
        det = np.where(np.abs(det) > 1e-12, det, np.nan)
        b = (sw * swxz - swx * swz) / det
        a = (swz - b * swx) / sw
        b = np.nan_to_num(b, nan=0.0)
        a = np.where(np.isfinite(a), a, eta.mean(0))
        eta = a + b * X1
    return a, b


def depth_expected(M, labels, bins, groups, min_out=20, return_extrap=False):
    """Expected fraction expressing per (group, gene) at the group's own depth distribution.

    For cluster c and gene g: sum over depth bins b of w[c,b] * out_frac[c,b,g], where w is the share
    of c's cells in bin b and out_frac the detection rate of the cells outside c in that bin. Where a
    bin has < min_out outside cells (a cluster much deeper or shallower than the rest), out_frac comes
    from a cloglog fit of detection on log depth over the outside cells, evaluated at the mean log
    depth of c's cells in that bin. Rows follow `groups` (as returned by group_mean_frac); cells with
    bin -1 are ignored. With return_extrap, also the share of each group's cells that needed the fit.
    """
    lab = pd.Series(labels).astype(str).to_numpy()
    gi = {g: i for i, g in enumerate(groups)}
    code = np.array([gi.get(x, -1) for x in lab])
    ok = (code >= 0) & (bins.codes >= 0)
    nb, k = max(bins.n, 1), len(groups)
    comb = code[ok] * nb + bins.codes[ok]
    n = int(ok.sum())
    B = (M[ok] > 0)
    B = B.astype(np.float32) if sparse.issparse(B) else np.asarray(B, dtype=np.float32)
    ind = sparse.csr_matrix((np.ones(n, dtype=np.float32), (comb, np.arange(n))), shape=(k * nb, n))
    D = ind @ B
    D = (D.toarray() if sparse.issparse(D) else np.asarray(D)).reshape(k, nb, -1).astype(np.float64)
    ncb = np.bincount(comb, minlength=k * nb).reshape(k, nb).astype(np.float64)
    xs = np.bincount(comb, weights=bins.x[ok], minlength=k * nb).reshape(k, nb)
    Db, nbt, xbt = D.sum(0), ncb.sum(0), xs.sum(0)
    exp = np.full((k, D.shape[2]), np.nan)
    extrap = np.zeros(k)
    for c in range(k):
        if ncb[c].sum() == 0:
            continue
        n_out = nbt - ncb[c]
        w = ncb[c] / ncb[c].sum()
        with np.errstate(invalid='ignore', divide='ignore'):
            of = (Db - D[c]) / n_out[:, None]
            xc = xs[c] / ncb[c]
        thin = (n_out < min_out) & (w > 0)
        if thin.any():
            use = n_out > 0
            if use.sum() >= 2:
                with np.errstate(invalid='ignore', divide='ignore'):
                    x_out = (xbt - xs[c])[use] / n_out[use]
                a, b = _cloglog_fit(x_out, n_out[use], (Db - D[c])[use])
                fit = 1 - np.exp(-np.exp(np.clip(a[None, :] + b[None, :] * xc[thin][:, None], -30, 5)))
                of[thin] = fit
            else:
                of[thin] = (Db - D[c]).sum(0) / max(n_out.sum(), 1)
            extrap[c] = w[thin].sum()
        of = np.where(np.isfinite(of), of, 0)
        exp[c] = w @ of
    return (exp, extrap) if return_extrap else exp


OE_PSEUDO = 0.01


def oe_ratio(frac, exp):
    """Observed / expected detection with a 1% pseudo-fraction (stable for rare genes)."""
    return (frac + OE_PSEUDO) / (np.nan_to_num(exp, nan=0.0) + OE_PSEUDO)


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


def add_pct(de, adata, X, var_names, key, bins=None):
    """pct expressing inside the cluster and in the rest, on all cells.

    With depth bins: also pct_exp (depth-matched expected fraction) and oe, and the genes of each
    cluster are reordered by O/E (stable; Wilcoxon rank kept in `rank`)."""
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
    if bins is not None and found:
        exp = pd.DataFrame(depth_expected(M, labels, bins, groups), index=groups, columns=found)
        de['pct_exp'] = [exp.at[c, g] if g in exp.columns else np.nan for c, g in zip(de['cluster'], de['gene'])]
        de['oe'] = oe_ratio(de['pct_in'].to_numpy(dtype=float), de['pct_exp'].to_numpy(dtype=float))
        de = (de.assign(_o=de['cluster'].map(natural_key))
              .sort_values(['_o', 'oe'], ascending=[True, False], kind='mergesort')
              .drop(columns='_o').reset_index(drop=True))
    return de


def marker_tables(adata, M, found, key, markers, min_frac=0.02, bins=None):
    if not found:
        return pd.DataFrame(), pd.DataFrame()
    labels = adata.obs[key].to_numpy()
    groups, mean, frac = group_mean_frac(M, labels)
    sd = mean.std(0, ddof=0)
    z = (mean - mean.mean(0)) / np.where(sd > 0, sd, 1)
    # A marker detected in almost no cells of a cluster must not raise that cluster's score
    # (a gene seen in 4 nuclei can still give z > 2 when every other cluster is at 0).
    z = np.where(frac >= min_frac, z, np.minimum(z, 0))
    exp = l2oe = None
    if bins is not None:
        exp = depth_expected(M, labels, bins, groups)
        l2oe = np.log2(oe_ratio(frac, exp))
        l2oe = np.where(frac >= min_frac, l2oe, np.minimum(l2oe, 0))
    long = []
    col = {g: i for i, g in enumerate(found)}
    for _, m in markers.iterrows():
        if m['gene_id'] not in col:
            continue
        j = col[m['gene_id']]
        for i, cl in enumerate(groups):
            r = {'cluster': cl, 'cell_type': m['cell_type'], 'gene_id': m['gene_id'],
                 'symbol': m['symbol'], 'evidence': m['evidence'],
                 'mean': mean[i, j], 'frac': frac[i, j], 'z': z[i, j]}
            if exp is not None:
                r.update(frac_exp=exp[i, j], oe=2 ** l2oe[i, j], log2oe=l2oe[i, j])
            long.append(r)
    long = pd.DataFrame(long).drop_duplicates(['cluster', 'cell_type', 'gene_id'])
    long['is_function'] = long['evidence'] == 'function'
    long['detected'] = long['frac'] >= min_frac
    agg = dict(score=('z', 'mean'), frac=('frac', 'mean'), n_markers=('gene_id', 'nunique'),
               n_detected=('detected', 'sum'), max_frac=('frac', 'max'), n_function=('is_function', 'sum'))
    if exp is not None:
        agg['score_oe'] = ('log2oe', 'mean')
    scores = long.groupby(['cluster', 'cell_type']).agg(**agg).reset_index()
    scores['n_detected'] = scores['n_detected'].astype(int)
    # Ranking keys: the mean shrunk toward 0 by set size, n / (n + RANK_SHRINK_K) with n = markers measured, so a
    # one-gene type (x0.33) does not outrank a coherent multi-gene type on one lucky gene. Scores are unchanged.
    shrink = scores['n_markers'] / (scores['n_markers'] + RANK_SHRINK_K)
    scores['rank_score'] = scores['score'] * shrink
    if exp is not None:
        scores['rank_score_oe'] = scores['score_oe'] * shrink
    return long, scores


def organelle_mask(genes, adata, gm, rx, ann=None, numt=None):
    """Boolean per gene: ID, var chromosome or rank-1 reference hit matches the organelle regex, the gene (or its
    rank-1 hit) is a known Arabidopsis NUMT locus, or its description (rank-1 hit or --gene-annotation) names an
    organellar-genome product."""
    numt = numt or set()
    chrom = None
    for c in CHROM_COLS:
        if c in adata.var.columns:
            chrom = adata.var[c].astype(str)
            break
    out = []
    for g in genes:
        ids = [str(g)]
        if chrom is not None and g in chrom.index:
            ids.append(chrom[g])
        descs = []
        if gm is not None and g in gm.index:
            ids.append(str(gm.at[g, 'ref_gene']))
            descs.append(str(gm.at[g, 'ref_description']))
        if ann is not None and g in ann.index:
            descs.append(str(ann.at[g, 'description']))
        hit = (any(rx.search(x) for x in ids) or any(x.upper().split('.')[0] in numt for x in ids)
               or any(ORGANELLE_DESC.search(x) for x in descs if x))
        out.append(hit)
    return np.array(out, dtype=bool)


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
                   stress_maps=None, assay='rna', depth_key=None, n_bins=0, organelle=None, organelle_flag=0.5, depth_extrap=None):
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
                "markers measured; `[1 gene]` = score rests on one detected marker. Types are listed by the score "
                f"shrunk by set size (x n/(n+{RANK_SHRINK_K}), n = markers measured), so a one-gene type does not "
                "outrank a coherent multi-gene type; the score shown is unshrunk. "
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
        if assay == 'atac':
            f.write("**Assay: ATAC** (gene activity from chromatin accessibility). Switched off for nuclei: the "
                    "protoplasting stress list and the possible-doublet flag (depth outliers are not RNA-style "
                    "doublets). Markers without an accessible region near the gene are unmeasurable, not absent.\n")
        if depth_key:
            f.write(f"**Depth-matched** on `{depth_key}` ({n_bins} quantile bins): exp = fraction expected from the "
                    f"cells outside the cluster at the cluster's own depth distribution; O/E = observed/expected "
                    f"(+1% pseudo-fraction). Cell types are ranked by `oe` = mean log2 O/E of their markers "
                    f"(z-based score in brackets); DE genes are reordered by O/E. Read O/E, not raw in-vs-out "
                    f"fractions: deep clusters detect every gene more often.\n")
        if organelle is not None:
            f.write(f"organellar_DNA flag: >= {organelle_flag:.0%} of the top {n_show} DE genes are organelle-like "
                    f"loci (regex `{organelle.pattern}` on gene ID, chromosome or reference hit; known Arabidopsis "
                    f"chr2 NUMT loci; or a description naming an organellar-genome product).\n")
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
                if depth_extrap and depth_extrap.get(cl, 0) >= 0.2:
                    f.write(f"- **Depth match**: {depth_extrap[cl]:.0%} of cells are deeper/shallower than almost all "
                            f"other cells; their expected fractions come from a fit of detection on depth "
                            f"(extrapolated: read O/E with care)\n")
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
            if organelle is not None and len(d):
                om = organelle_mask(list(d['gene']), adata, gm, organelle, ann=ann, numt=NUMT_SET)
                if om.mean() >= organelle_flag:
                    flags.append(f"organellar_DNA ({int(om.sum())}/{len(d)} top DE genes on organelle-like loci; "
                                 f"NUPT/NUMT or organellar reads: a QC artefact, not a cell type)")
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
            if len(s_all) and assay != 'atac':
                dflag = doublet_check(cl, s_all, long, aliases, ratios.get('counts'), ratios.get('doublet'), min_frac)
                if dflag:
                    flags.append(dflag)
            if flags:
                f.write('- **FLAGS**: ' + '; '.join(flags) + '\n')
            if len(s_all):
                oe_mode = 'score_oe' in s_all.columns
                rk = 'rank_score_oe' if oe_mode else 'rank_score'
                rk = rk if rk in s_all.columns else ('score_oe' if oe_mode else 'score')
                s = s_all.sort_values(rk, ascending=False).head(4)
                parts = []
                for r in s.itertuples():
                    lt = long[(long['cluster'] == cl) & (long['cell_type'] == r.cell_type)]
                    one = ' [1 gene]' if r.n_detected == 1 else ''
                    if oe_mode:
                        top = lt.sort_values('oe', ascending=False).head(3)
                        drv = ','.join(f"{t.symbol}{'*' if t.is_function else ''}:x{t.oe:.1f} "
                                       f"({t.frac:.0%} vs exp {t.frac_exp:.0%})" for t in top.itertuples())
                        parts.append(f"{r.cell_type} oe {r.score_oe:+.2f}{one} (z {r.score:.2f}; det "
                                     f"{r.n_detected}/{r.n_markers}; best {r.max_frac:.0%}; {drv})")
                        continue
                    top = lt.sort_values('z', ascending=False).head(3)
                    oth = long[(long['cluster'] != cl) & (long['cell_type'] == r.cell_type)]
                    fout = oth.groupby('gene_id')['frac'].mean()
                    drv = ','.join(f"{t.symbol}{'*' if t.is_function else ''}:{t.z:.1f} "
                                   f"({t.frac:.0%} vs {fout.get(t.gene_id, 0):.0%})"
                                   for t in top.itertuples())
                    parts.append(f"{r.cell_type} {r.score:.2f}{one} (frac {r.frac:.2f}; det {r.n_detected}/{r.n_markers}"
                                 f"; best {r.max_frac:.0%}; {drv})")
                f.write('- **Marker scores**: ' + ' | '.join(parts) + '\n')
            if len(d):
                has_oe = 'oe' in d.columns
                if has_oe:
                    f.write('\n| gene | logFC | pct in/out | exp (depth) | O/E | homolog |\n'
                            '|---|---|---|---|---|---|\n')
                else:
                    f.write('\n| gene | logFC | pct in/out | homolog |\n|---|---|---|---|\n')
                for r in d.itertuples():
                    gname = r.gene
                    in_gm = gm is not None and r.gene in gm.index
                    if ann is not None and in_gm and r.gene in ann.index and ann.at[r.gene, 'symbol']:
                        gname = f"{r.gene} ({ann.at[r.gene, 'symbol']})"
                    oe_txt = f" {r.pct_exp:.2f} | x{r.oe:.1f} |" if has_oe else ''
                    f.write(f"| {gname} | {r.logfc:+.2f} | {r.pct_in:.2f}/{r.pct_out:.2f} |{oe_txt} "
                            f"{homolog_str(r.gene, gm, ann=ann, others=others)} |\n")
            f.write('\n')


def rasterize(ax):
    for ch in ax.get_children():
        if hasattr(ch, 'set_rasterized'):
            ch.set_rasterized(True)


def dotplot_pages(mk, max_genes=120, per_type=8, max_pages=6):
    """Split marker genes into dotplot pages: <= per_type genes per cell type (function-evidence rows
    first), cell types kept whole, <= max_genes per page, <= max_pages pages. Returns (pages, n_dropped)."""
    mk = mk.assign(_f=(mk['evidence'] != 'function').astype(int)).sort_values(['cell_type', '_f'], kind='mergesort')
    groups, dropped = [], 0
    for ct, sub in mk.groupby('cell_type', sort=True):
        g = list(dict.fromkeys(sub['gene_id']))
        dropped += max(0, len(g) - per_type)
        groups.append((ct, g[:per_type]))
    pages, cur, n = [], {}, 0
    for ct, g in groups:
        if cur and n + len(g) > max_genes:
            pages.append(cur)
            cur, n = {}, 0
        cur[ct] = g
        n += len(g)
    if cur:
        pages.append(cur)
    if len(pages) > max_pages:
        dropped += sum(len(g) for pg in pages[max_pages:] for g in pg.values())
        pages = pages[:max_pages]
    return pages, dropped


def plots(adata, keys, markers, pdf_path, use_raw, layer, max_genes=120, per_type=8, max_pages=6):
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
                pages, dropped = dotplot_pages(mk, max_genes, per_type, max_pages)
                if dropped:
                    print(f'  NOTE dotplot for {key}: {dropped} marker genes not shown (at most {per_type} per cell '
                          f'type, {max_genes} per page, {max_pages} pages); all are in the evidence tables')
                kw = dict(layer=layer, use_raw=False) if layer else \
                    dict(use_raw=(adata.raw is not None and use_raw != 'no'))
                for i, groups in enumerate(pages):
                    try:
                        dp = sc.pl.dotplot(adata, groups, groupby=key, show=False,
                                           standard_scale='var', return_fig=True, **kw)
                        dp.make_figure()
                        fig = plt.gcf()
                        fig.suptitle(f'Markers by {key} (scaled per gene)'
                                     + (f', page {i + 1}/{len(pages)}' if len(pages) > 1 else ''))
                        pdf.savefig(fig, bbox_inches='tight')
                    except Exception as e:  # plotting must never kill the evidence run
                        print(f'  WARN dotplot for {key} (page {i + 1}) failed: {e}')
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
    p.add_argument('--import-labels', nargs='+', action='extend', default=[],
                   help='path:col[:new_name] (one or more, flag repeatable), as in apply_annotations.py; e.g. '
                        'published per-cell labels to evaluate. Pass the new name in --cluster-keys')
    p.add_argument('--qc-keys', nargs='+', action='extend', default=[],
                   help='extra numeric obs columns shown per cluster in the QC line (e.g. tss_enrichment frip); '
                        'with --assay atac, common TSS-enrichment/FRiP names are included automatically')
    p.add_argument('--assay', choices=['rna', 'atac'], default='rna',
                   help='atac: gene activity from accessibility; depth-matched O/E on, organellar_DNA flag on, '
                        'stress list and doublet flag off, missing markers reported as unmeasurable')
    p.add_argument('--depth-key', default=None,
                   help='obs column with per-cell depth (total_counts, n_fragments, ...): report depth-matched '
                        'expected fractions and O/E and rank by them (default: off for rna; auto for atac). '
                        "'none' turns it off")
    p.add_argument('--depth-bins', type=int, default=20, help='depth quantile bins for the depth-matched mode')
    p.add_argument('--organelle-regex', default=None,
                   help='regex for organelle-like loci (gene ID, var chromosome column or reference hit ID); '
                        'turns the organellar_DNA flag on for rna too. Default (atac): ATCG/ATMG hits and '
                        'chromosome names like ChrC/ChrM/Pt/Mt; unplaced scaffolds are not matched')
    p.add_argument('--organelle-flag', type=float, default=0.5,
                   help='flag a cluster when this fraction of its shown top DE genes are organelle-like loci')
    p.add_argument('--dotplot-max-genes', type=int, default=120,
                   help='marker dotplot: at most this many genes per page (pages split by cell type) and at most '
                        '--dotplot-per-type genes per cell type')
    p.add_argument('--dotplot-per-type', type=int, default=8)
    p.add_argument('--dotplot-max-pages', type=int, default=6, help='dotplot pages per cluster key')
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
    atac = args.assay == 'atac'
    if atac:
        for k, v in ATAC_QC.items():
            QC_CANDIDATES[k] = v
        if args.stress_genes:
            print('  NOTE --assay atac: the protoplasting stress list is ignored (nuclei, gene activity)')
            args.stress_genes = None
    depth_key = args.depth_key
    if depth_key and depth_key.lower() == 'none':
        depth_key = None
    elif depth_key is None and atac:
        depth_key = pick(adata.obs, DEPTH_CANDIDATES)
        if depth_key is None:
            print('  WARN --assay atac but no depth column found (' + ', '.join(DEPTH_CANDIDATES)
                  + '); pass --depth-key. Depth matching is off')
    bins = None
    if depth_key:
        if depth_key not in adata.obs.columns:
            raise SystemExit(f'--depth-key {depth_key} not in obs')
        bins = depth_bins(adata.obs[depth_key].to_numpy(), args.depth_bins)
        nb = bins.n
        print(f'  depth-matched O/E on {depth_key!r} ({nb} quantile bins; '
              f'median {np.nanmedian(adata.obs[depth_key].astype(float)):,.0f})')
    organelle = None
    if args.organelle_regex or atac:
        organelle = re.compile(args.organelle_regex or DEFAULT_ORGANELLE)

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
            if atac:
                print('  NOTE markers not in var_names: in gene activity this usually means no accessible region '
                      'near the gene (unmeasurable here, not absent); if most are missing, check the IDs. By cell type:')
            else:
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
    for c in args.qc_keys:
        if c not in adata.obs.columns:
            print(f'  WARN --qc-keys {c}: not in obs; skipped')
        elif not pd.api.types.is_numeric_dtype(adata.obs[c]):
            print(f'  WARN --qc-keys {c}: not numeric; skipped')
        elif c not in qc_cols.values():
            qc_cols[c] = c
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
            de = add_pct(de, adata, X, var_names, key, bins=bins)
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
        long, scores = (marker_tables(adata, Mk, mk_found, key, markers, args.min_frac, bins=bins)
                        if markers is not None else (pd.DataFrame(), pd.DataFrame()))
        if not long.empty:
            long.to_csv(os.path.join(args.output, f'marker_expression_{key}.tsv'),
                        sep='\t', index=False, float_format='%.4g')
            wide = scores.pivot(index='cluster', columns='cell_type', values='score')
            wide = wide.loc[sorted(wide.index, key=natural_key)]
            wide.to_csv(os.path.join(args.output, f'marker_scores_{key}.tsv'),
                        sep='\t', float_format='%.3f')
            if 'score_oe' in scores.columns:
                w2 = scores.pivot(index='cluster', columns='cell_type', values='score_oe')
                w2.loc[sorted(w2.index, key=natural_key)].to_csv(
                    os.path.join(args.output, f'marker_scores_oe_{key}.tsv'), sep='\t', float_format='%.3f')
            det = scores.copy()
            det['_o'] = det['cluster'].map(natural_key)
            det.sort_values(['_o', 'score'], ascending=[True, False]).drop(columns='_o').to_csv(
                os.path.join(args.output, f'marker_score_details_{key}.tsv'), sep='\t', index=False,
                float_format='%.3f')
        comp = composition(adata, key, meta)
        depth_extrap = {}
        if bins is not None:
            labs = adata.obs[key].astype(str).to_numpy()
            grp = sorted(set(labs), key=natural_key)
            _, ex = depth_expected(np.ones((adata.n_obs, 1), dtype=np.float32), labs, bins, grp, return_extrap=True)
            depth_extrap = dict(zip(grp, ex))
        write_markdown(os.path.join(args.output, f'cluster_evidence_{key}.md'), key, adata,
                       de, long, scores, comp, hier, qc_cols, gm, args.n_show, ann=ann, min_frac=args.min_frac,
                       stress=stress, stress_flag=args.stress_flag, stress_inactive=stress_inactive,
                       keys=keys, others=others, aliases=aliases, stress_maps=gms, assay=args.assay,
                       depth_key=depth_key, n_bins=(bins.n if bins is not None else 0),
                       depth_extrap=depth_extrap,
                       organelle=organelle, organelle_flag=args.organelle_flag)
        print(f'  wrote cluster_evidence_{key}.md')

    if not args.skip_plots:
        print('[4] Plots')
        plots(adata, keys, markers, os.path.join(args.output, 'evidence_plots.pdf'),
              args.use_raw, args.layer, max_genes=args.dotplot_max_genes, per_type=args.dotplot_per_type,
              max_pages=args.dotplot_max_pages)
    print('Done.')


if __name__ == '__main__':
    main()
