#!/usr/bin/env python3
"""Subcluster selected clusters to resolve ambiguous / mixed populations.

Subsets the chosen clusters, rebuilds the neighbor graph on the existing
integrated embedding (default X_pca_harmony, else X_pca), recomputes UMAP and
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
    p.add_argument('--use-rep', default=None, help='default: X_pca_harmony if present, else X_pca')
    p.add_argument('--n-neighbors', type=int, default=30)
    p.add_argument('--n-pcs', type=int, default=30)
    p.add_argument('--resolutions', nargs='+', type=float, default=[0.1, 0.3, 0.5, 1.0])
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--recompute-pca', action='store_true',
                   help='select HVGs and run PCA within the subset (X must be log-normalized)')
    p.add_argument('--n-top-genes', type=int, default=2000, help='HVGs for --recompute-pca')
    p.add_argument('--batch-key', default=None,
                   help='obs column with the batch (e.g. sample). With --recompute-pca and >1 level in the subset: '
                        'HVGs are selected per batch and Harmony corrects the subset PCA. Without --recompute-pca '
                        'the existing (already integrated) embedding is used and this is only recorded')
    args = p.parse_args()

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

    if args.recompute_pca:
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
            try:
                import harmonypy
            except ImportError:
                harmonypy = None
                print('WARN harmonypy is not installed: continuing with the uncorrected subset PCA; '
                      'check the subclusters against ' + args.batch_key)
            if harmonypy is not None:
                import logging
                logging.getLogger('harmonypy').setLevel(logging.WARNING)
                # harmonypy 0.1.0 may return Z_corr as PCs x cells: orient by n_obs
                # (scanpy's harmony_integrate wrapper mis-orients it for that version).
                ho = harmonypy.run_harmony(np.asarray(sub.obsm['X_pca_sub']), sub.obs, args.batch_key,
                                           random_state=args.seed)
                Z = np.asarray(ho.Z_corr)
                Z = Z if Z.shape[0] == sub.n_obs else Z.T
                sub.obsm['X_pca_sub_harmony'] = np.ascontiguousarray(Z, dtype=np.float32)
                rep, harmony = 'X_pca_sub_harmony', True
                print(f'Harmony on {args.batch_key} ({n_batch} batches) -> obsm[X_pca_sub_harmony]')
        elif args.batch_key:
            print(f'{args.batch_key} has one level in the subset: no batch correction needed')
    else:
        if args.batch_key:
            print('NOTE --batch-key without --recompute-pca: using the existing embedding as is '
                  '(it should already be integrated)')
        rep = args.use_rep or ('X_pca_harmony' if 'X_pca_harmony' in sub.obsm else 'X_pca')
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
                                    'recompute_pca': bool(args.recompute_pca),
                                    'batch_key': args.batch_key or '', 'harmony': bool(harmony)}
    sub.write_h5ad(args.output_h5ad)
    print(f'Wrote {args.output_h5ad}')


if __name__ == '__main__':
    main()
