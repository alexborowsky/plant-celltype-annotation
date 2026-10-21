#!/usr/bin/env python3
"""Synthetic rice-root dataset for the smoke test.

Genes are real MSU7 IDs from references/markers/rice_root.tsv plus filler genes,
so map_markers.py --no-blast finds real markers. Writes:
  synthetic.h5ad        log-normalized X, .raw, leiden_res0.3/0.8, X_umap, obs sample/truth
  published_labels.csv  barcode,published_label for 80% of cells; barcodes carry a '-1'
                        suffix (to exercise the low-match warning) and labels merge
                        Cortex+Exodermis as "Ground tissue" (a Revise case)
  truth.tsv             barcode -> true type
"""
import argparse, os
import numpy as np, pandas as pd, scanpy as sc, anndata as ad

p = argparse.ArgumentParser()
p.add_argument('--skill', required=True)
p.add_argument('--out', required=True)
p.add_argument('--cells-per-type', type=int, default=150)
a = p.parse_args()
os.makedirs(a.out, exist_ok=True)
rng = np.random.default_rng(0)

m = pd.read_csv(f'{a.skill}/references/markers/rice_root.tsv', sep='\t')
TYPES = {'Trichoblast': 'Trichoblast', 'Cortex': 'Cortex', 'Endodermis': 'Endodermis',
         'Xylem': 'Xylem', 'Exodermis': 'Exodermis', 'S_Phase': 'S_Phase'}
mk = {t: m.loc[m.cell_type == c, 'ref_gene'].tolist() for t, c in TYPES.items()}
markers = sorted({g for v in mk.values() for g in v})
filler = [f'LOC_Os99g{i:05d}' for i in range(400)]
genes = markers + filler

rows, truth, sample = [], [], []
for t in TYPES:
    n = a.cells_per_type
    base = rng.gamma(1.0, 1.0, size=len(genes))
    lam = np.tile(base, (n, 1)) * rng.lognormal(0, 0.3, size=(n, 1))
    for g in mk[t]:
        lam[:, genes.index(g)] *= 25
    rows.append(rng.poisson(lam))
    truth += [t] * n
    sample += list(rng.choice(['rep1', 'rep2'], size=n))
X = np.vstack(rows).astype(np.float32)
obs = pd.DataFrame({'truth': truth, 'sample': sample}, index=[f'CELL{i:05d}' for i in range(len(truth))])
A = ad.AnnData(X=X, obs=obs, var=pd.DataFrame(index=genes))
sc.pp.normalize_total(A, target_sum=1e4); sc.pp.log1p(A)
A.raw = A
sc.pp.pca(A, n_comps=20); sc.pp.neighbors(A, n_neighbors=15); sc.tl.umap(A, random_state=0)
for r in (0.3, 0.8):
    sc.tl.leiden(A, resolution=r, key_added=f'leiden_res{r}', random_state=0)
A.write_h5ad(f'{a.out}/synthetic.h5ad')

pub = obs.sample(frac=0.8, random_state=0).copy()
pub['published_label'] = pub['truth'].replace({'Cortex': 'Ground tissue', 'Exodermis': 'Ground tissue',
                                               'S_Phase': 'Meristem'})
pub.index = pub.index + '-1'
pub[['published_label']].rename_axis('barcode').to_csv(f'{a.out}/published_labels.csv')
obs[['truth']].rename_axis('barcode').to_csv(f'{a.out}/truth.tsv', sep='\t')
print(f'{A.n_obs} cells x {A.n_vars} genes; {len(markers)} marker genes; '
      f'leiden_res0.3 {A.obs.leiden_res0_3.nunique() if "leiden_res0_3" in A.obs else A.obs["leiden_res0.3"].nunique()} clusters')
