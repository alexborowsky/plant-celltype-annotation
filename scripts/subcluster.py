#!/usr/bin/env python3
"""Subcluster selected clusters to resolve ambiguous / mixed populations.

Subsets the chosen clusters, rebuilds the neighbor graph on the existing
integrated embedding (default X_pca_harmony, else X_pca; X_lsi* for snATAC), recomputes UMAP and
Leiden at several resolutions (obs['leiden_sub_<res>']), and writes a
subcluster h5ad whose obs_names match the parent so labels can be imported
back with apply_annotations.py --import-labels.

--recompute-pca selects HVGs and computes a PCA within the subset (obsm['X_pca_sub']).
Use it when looking for a rare type: the global PCA is dominated by the major
axes of the whole dataset and can hide variation inside one cluster. A PCA
recomputed on the subset is not batch-corrected: pass --batch-key <obs column>
(e.g. sample) to run Harmony (harmonypy) on the subset PCA
(obsm['X_pca_sub_harmony']), which is then used for the neighbor graph. Without
--batch-key, check the subclusters against sample. If harmonypy is not
installed the script warns and continues with the uncorrected subset PCA.

snATAC: --lsi recomputes LSI within the subset instead (TF-IDF on the region counts in layers['counts'] or X,
top --lsi-features most-detected regions, truncated SVD; the first component is dropped when it tracks depth,
|r| > 0.7), with Harmony on --batch-key as above (obsm['X_lsi_sub'] / ['X_lsi_sub_harmony']). Run it on the
region (peak or tile) object, not on a gene-activity object; obs_names are shared, so the subclusters import
onto either. Without --lsi or --recompute-pca the default embedding is the first present of X_pca_harmony,
X_pca, X_lsi_harmony, X_lsi.
"""

import argparse
import warnings

import numpy as np
import scanpy as sc

warnings.filterwarnings('ignore')
sc.settings.verbosity = 1


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True)
    p.add_argument('--cluster-key', required=True, help='e.g. leiden_res0.3')
    p.add_argument('--clusters', nargs='+', required=True)
    p.add_argument('--output-h5ad', required=True)
    p.add_argument('--use-rep', default=None,
                   help='default: first present of X_pca_harmony, X_pca, X_lsi_harmony, X_lsi')
    p.add_argument('--n-neighbors', type=int, default=30)
    p.add_argument('--n-pcs', type=int, default=30)
    p.add_argument('--resolutions', nargs='+', type=float, default=[0.1, 0.3, 0.5, 1.0])
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--recompute-pca', action='store_true',
                   help='select HVGs and run PCA within the subset (X must be log-normalized)')
    p.add_argument('--n-top-genes', type=int, default=2000, help='HVGs for --recompute-pca')
    p.add_argument('--lsi', action='store_true',
                   help='snATAC: recompute TF-IDF + SVD (LSI) within the subset from region counts')
    p.add_argument('--lsi-features', type=int, default=50000, help='most-detected regions used by --lsi')
    p.add_argument('--counts-layer', default='counts', help='region counts for --lsi (default counts, else X)')
    p.add_argument('--batch-key', default=None,
                   help='obs column with the batch (e.g. sample). With --recompute-pca and >1 level in the subset: '
                        'HVGs are selected per batch and Harmony corrects the subset PCA. Without --recompute-pca '
                        'the existing (already integrated) embedding is used and this is only recorded')
    args = p.parse_args()
    if args.lsi and args.recompute_pca:
        raise SystemExit('--lsi and --recompute-pca are alternatives (ATAC regions vs RNA genes): pick one')

    adata = sc.read_h5ad(args.h5ad)
    if 'log1p' in adata.uns and 'base' not in adata.uns['log1p']:
        adata.uns['log1p']['base'] = None
    ids = [str(c) for c in args.clusters]
    sub = adata[adata.obs[args.cluster_key].astype(str).isin(ids)].copy()
    del adata
    print(f'Subset {args.cluster_key} in {ids}: {sub.n_obs:,} cells')
    n_batch = 0
    if args.batch_key:
        if args.batch_key not in sub.obs.columns:
            raise SystemExit(f'--batch-key {args.batch_key!r} not in obs')
        sub.obs[args.batch_key] = sub.obs[args.batch_key].astype(str).astype('category')
        n_batch = sub.obs[args.batch_key].nunique()
        print(f'{args.batch_key}: {n_batch} level(s) in the subset: '
              + ', '.join(f'{k} {v}' for k, v in sub.obs[args.batch_key].value_counts().items()))
    harmony = False

    def run_harmony(base):
        try:
            import harmonypy
        except ImportError:
            print('WARN harmonypy is not installed: continuing with the uncorrected subset embedding; '
                  'check the subclusters against ' + args.batch_key)
            return base, False
        import logging
        logging.getLogger('harmonypy').setLevel(logging.WARNING)
        # harmonypy 0.1.0 may return Z_corr as PCs x cells: orient by n_obs
        # (scanpy's harmony_integrate wrapper mis-orients it for that version).
        ho = harmonypy.run_harmony(np.asarray(sub.obsm[base]), sub.obs, args.batch_key, random_state=args.seed)
        Z = np.asarray(ho.Z_corr)
        Z = Z if Z.shape[0] == sub.n_obs else Z.T
        sub.obsm[base + '_harmony'] = np.ascontiguousarray(Z, dtype=np.float32)
        print(f'Harmony on {args.batch_key} ({n_batch} batches) -> obsm[{base}_harmony]')
        return base + '_harmony', True

    if args.lsi:
        import scipy.sparse as sp
        from sklearn.decomposition import TruncatedSVD
        X = sub.layers[args.counts_layer] if args.counts_layer in sub.layers else sub.X
        X = sp.csr_matrix(X, dtype=np.float32)
        if X.nnz and not np.allclose(X.data[:10000], np.round(X.data[:10000])):
            print('WARN --lsi expects raw region counts; the matrix is not integer (gene activity or normalized?)')
        det = np.asarray((X > 0).sum(0)).ravel()
        keep = np.argsort(-det)[:min(args.lsi_features, int((det > 0).sum()))]
        Xk = X[:, keep]
        depth = np.asarray(Xk.sum(1)).ravel()
        tf = sp.diags(1 / np.maximum(depth, 1)) @ Xk
        idf = np.log1p(sub.n_obs / np.maximum(det[keep], 1))
        T = sp.csr_matrix(tf @ sp.diags(idf.astype(np.float32)))
        T.data = np.log1p(T.data * 1e4)
        n_comp = min(args.n_pcs + 1, T.shape[0] - 1, T.shape[1] - 1)
        Z = TruncatedSVD(n_comp, random_state=args.seed).fit_transform(T)
        r = np.corrcoef(Z[:, 0], np.log1p(depth))[0, 1]
        if abs(r) > 0.7:
            Z = Z[:, 1:]
            print(f'LSI component 1 tracks depth (r = {r:.2f}): dropped')
        Z = (Z - Z.mean(0)) / np.maximum(Z.std(0), 1e-8)
        sub.obsm['X_lsi_sub'] = Z.astype(np.float32)
        print(f'Recomputed LSI on {len(keep):,} regions ({Z.shape[1]} components)')
        rep = 'X_lsi_sub'
        if n_batch > 1:
            rep, harmony = run_harmony(rep)
        elif args.batch_key:
            print(f'{args.batch_key} has one level in the subset: no batch correction needed')
    elif args.recompute_pca:
        if 'log1p' not in sub.uns:
            print('WARN uns has no log1p entry: --recompute-pca assumes X is log-normalized')
        hvg_kw = {}
        if n_batch > 1 and sub.obs[args.batch_key].value_counts().min() >= 2:
            hvg_kw['batch_key'] = args.batch_key
        try:
            sc.pp.highly_variable_genes(sub, n_top_genes=min(args.n_top_genes, sub.n_vars), **hvg_kw)
        except Exception as e:  # tiny batches can break per-batch HVG selection
            print(f'WARN per-batch HVG selection failed ({e}); selecting HVGs on all cells')
            sc.pp.highly_variable_genes(sub, n_top_genes=min(args.n_top_genes, sub.n_vars))
        hv = sub[:, sub.var['highly_variable']].copy()
        sc.pp.scale(hv, max_value=10)
        sc.tl.pca(hv, n_comps=min(args.n_pcs, hv.n_obs - 1, hv.n_vars - 1), random_state=args.seed)
        sub.obsm['X_pca_sub'] = hv.obsm['X_pca']
        del hv
        print(f'Recomputed PCA on {int(sub.var["highly_variable"].sum())} subset HVGs')
        rep = 'X_pca_sub'
        if n_batch > 1:
            rep, harmony = run_harmony(rep)
        elif args.batch_key:
            print(f'{args.batch_key} has one level in the subset: no batch correction needed')
    else:
        if args.batch_key:
            print('NOTE --batch-key without --recompute-pca: using the existing embedding as is '
                  '(it should already be integrated)')
        rep = args.use_rep or next((k for k in ('X_pca_harmony', 'X_pca', 'X_lsi_harmony', 'X_lsi')
                                    if k in sub.obsm), 'X_pca')
    if rep not in sub.obsm:
        raise SystemExit(f'{rep} not in obsm; available: {list(sub.obsm.keys())}')
    n_pcs = min(args.n_pcs, sub.obsm[rep].shape[1])
    print(f'neighbors(use_rep={rep}, n_pcs={n_pcs}, n_neighbors={args.n_neighbors})')
    sc.pp.neighbors(sub, n_neighbors=args.n_neighbors, n_pcs=n_pcs, use_rep=rep,
                    random_state=args.seed)
    sc.tl.umap(sub, random_state=args.seed)
    for r in args.resolutions:
        k = f'leiden_sub_{r}'
        sc.tl.leiden(sub, resolution=r, key_added=k, random_state=args.seed)
        print(f'  {k}: {sub.obs[k].nunique()} clusters')
    sub.uns['subcluster_source'] = {'h5ad': args.h5ad, 'cluster_key': args.cluster_key,
                                    'clusters': ids, 'use_rep': rep,
                                    'recompute_pca': bool(args.recompute_pca), 'lsi': bool(args.lsi),
                                    'batch_key': args.batch_key or '', 'harmony': bool(harmony)}
    sub.write_h5ad(args.output_h5ad)
    print(f'Wrote {args.output_h5ad}')


if __name__ == '__main__':
    main()
