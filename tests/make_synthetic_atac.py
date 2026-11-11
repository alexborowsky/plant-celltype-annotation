#!/usr/bin/env python3
"""Small synthetic snATAC dataset for the smoke test of gene_activity.py and subcluster.py --lsi.

Three types (A, B, C) x 2 samples, 2 chromosomes, 40 genes on both strands. Each type opens the promoter
peak of its own marker genes. Writes:
  atac.h5ad             nuclei x peaks, raw counts in X and layers['counts'], var chrom/start/end,
                        obs sample/barcode_raw/truth, obsm X_lsi, leiden_res0.5 (= truth)
  genes.gff3            gene features (ID=gene:G00 style, to exercise prefix stripping)
  frag/s1_fragments.tsv.gz, frag/s2_fragments.tsv.gz   fragments (barcode = barcode_raw)
  expect.tsv            gene, type (marker genes), plus strand checks:
                        G_MINUS_UP  (minus strand, peak 1 kb past its end = upstream -> measurable)
                        G_MINUS_DN  (minus strand, peak 1.5 kb before its start = downstream -> unmeasurable)
"""
import argparse
import gzip
import os

import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp

p = argparse.ArgumentParser()
p.add_argument('--out', required=True)
p.add_argument('--cells-per-type', type=int, default=120)
a = p.parse_args()
os.makedirs(f'{a.out}/frag', exist_ok=True)
rng = np.random.default_rng(1)

TYPES = ['A', 'B', 'C']
genes, peaks = [], []
pos = {'chr1': 10_000, 'chr2': 10_000}
for i in range(40):
    chrom = 'chr1' if i < 20 else 'chr2'
    strand = '+' if i % 2 == 0 else '-'
    s = pos[chrom]
    e = s + 3000
    gid = f'G{i:02d}'
    genes.append((chrom, s + 1, e, strand, gid))  # GFF: 1-based inclusive
    tss = s if strand == '+' else e
    peaks.append((chrom, tss - 500 if strand == '+' else tss - 200, tss + 200 if strand == '+' else tss + 500,
                  TYPES[i % 3] if i < 30 else 'all'))
    pos[chrom] = e + 8000
# strand checks: minus-strand genes with one peak each, 1 kb upstream (past the end) / 1.5 kb downstream
for gid, off in [('G_MINUS_UP', 'up'), ('G_MINUS_DN', 'dn')]:
    s = pos['chr2']
    e = s + 2000
    genes.append(('chr2', s + 1, e, '-', gid))
    peaks.append(('chr2', e + 800, e + 1200, 'all') if off == 'up' else ('chr2', s - 1700, s - 1300, 'all'))
    pos['chr2'] = e + 10000
genes.append(('chr2', pos['chr2'] + 1, pos['chr2'] + 2000, '+', 'G_NOPEAK'))
for k in range(30):  # intergenic background peaks
    peaks.append(('chr1', 1_000_000 + k * 5000, 1_000_000 + k * 5000 + 400, 'all'))

with open(f'{a.out}/genes.gff3', 'w') as f:
    f.write('##gff-version 3\n')
    for chrom, s, e, strand, gid in genes:
        f.write(f'{chrom}\tsyn\tgene\t{s}\t{e}\t.\t{strand}\t.\tID=gene:{gid};Name={gid.lower()}\n')
        f.write(f'{chrom}\tsyn\tmRNA\t{s}\t{e}\t.\t{strand}\t.\tID=transcript:{gid}.1;Parent=gene:{gid}\n')

pk = pd.DataFrame(peaks, columns=['chrom', 'start', 'end', 'open_in'])
cells = []
for smp in ['s1', 's2']:
    for t in TYPES:
        for j in range(a.cells_per_type // 2):
            cells.append((smp, f'{t}{smp}{j:04d}ACGT-1', t))
obs = pd.DataFrame(cells, columns=['sample', 'barcode_raw', 'truth'])
obs.index = obs['sample'] + '_' + obs['barcode_raw']
depth = rng.lognormal(0, 0.5, len(obs))
P = np.where((pk['open_in'].values[None, :] == obs['truth'].values[:, None]), 2.0,
             np.where(pk['open_in'].values[None, :] == 'all', 0.6, 0.05)) * depth[:, None]
C = rng.poisson(P).astype(np.float32)

# fragments: one fragment per count, inside its peak (insertions inside the peak)
frs = {s: [] for s in ['s1', 's2']}
for ci, ji in zip(*np.nonzero(C)):
    smp, bc = obs['sample'].iat[ci], obs['barcode_raw'].iat[ci]
    ps, pe = int(pk['start'].iat[ji]), int(pk['end'].iat[ji])
    for _ in range(int(C[ci, ji])):
        st = int(rng.integers(ps, pe - 60))
        frs[smp].append((pk['chrom'].iat[ji], st, min(st + int(rng.integers(40, 300)), pe), bc, 1))
for smp, rows in frs.items():
    rows.sort(key=lambda r: (r[0], r[1]))
    with gzip.open(f'{a.out}/frag/{smp}_fragments.tsv.gz', 'wt') as f:
        f.write('# synthetic fragments\n')
        for r in rows:
            f.write('\t'.join(map(str, r)) + '\n')

var = pk[['chrom', 'start', 'end']].copy()
var.index = var['chrom'] + ':' + var['start'].astype(str) + '-' + var['end'].astype(str)
adata = ad.AnnData(X=sp.csr_matrix(C), obs=obs, var=var)
adata.layers['counts'] = adata.X.copy()
adata.obs['total_counts'] = C.sum(1)
adata.obs['leiden_res0.5'] = pd.Categorical(adata.obs['truth'].map({'A': '0', 'B': '1', 'C': '2'}))
from sklearn.decomposition import TruncatedSVD  # noqa: E402
tf = C / np.maximum(C.sum(1, keepdims=True), 1)
idf = np.log1p(C.shape[0] / np.maximum((C > 0).sum(0), 1))
adata.obsm['X_lsi'] = TruncatedSVD(10, random_state=0).fit_transform(np.log1p(tf * idf * 1e4))
adata.write_h5ad(f'{a.out}/atac.h5ad')
ex = [(g, TYPES[int(g[1:]) % 3]) for _, _, _, _, g in genes if g.startswith('G') and g[1:].isdigit() and int(g[1:]) < 30]
pd.DataFrame(ex + [('G_MINUS_UP', 'measurable'), ('G_MINUS_DN', 'unmeasurable'), ('G_NOPEAK', 'unmeasurable')],
             columns=['gene', 'type']).to_csv(f'{a.out}/expect.tsv', sep='\t', index=False)
print(f'synthetic ATAC: {adata.n_obs} nuclei x {adata.n_vars} peaks, {len(genes)} genes, '
      f'{sum(len(v) for v in frs.values()):,} fragments')
