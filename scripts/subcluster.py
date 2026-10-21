#!/usr/bin/env python3
"""Subcluster selected clusters to resolve ambiguous / mixed populations.

Subsets the chosen clusters, rebuilds the neighbor graph on the existing
integrated embedding (default X_pca_harmony, else X_pca), recomputes UMAP and
Leiden at several resolutions (obs['leiden_sub_<res>']), and writes a
subcluster h5ad whose obs_names match the parent so labels can be imported
back with apply_annotations.py --import-labels.

--recompute-pca selects HVGs and computes a PCA within the subset (obsm['X_pca_sub']).
Use it when looking for a rare type: the global PCA is dominated by the major
axes of the whole dataset and can hide variation inside one cluster. It does not
redo batch integration, so check the subclusters against sample.
"""

import argparse
import warnings

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
    args = p.parse_args()

    adata = sc.read_h5ad(args.h5ad)
    if 'log1p' in adata.uns and 'base' not in adata.uns['log1p']:
        adata.uns['log1p']['base'] = None
    ids = [str(c) for c in args.clusters]
    sub = adata[adata.obs[args.cluster_key].astype(str).isin(ids)].copy()
    del adata
    print(f'Subset {args.cluster_key} in {ids}: {sub.n_obs:,} cells')

    if args.recompute_pca:
        if 'log1p' not in sub.uns:
            print('WARN uns has no log1p entry: --recompute-pca assumes X is log-normalized')
        sc.pp.highly_variable_genes(sub, n_top_genes=min(args.n_top_genes, sub.n_vars))
        hv = sub[:, sub.var['highly_variable']].copy()
        sc.pp.scale(hv, max_value=10)
        sc.tl.pca(hv, n_comps=min(args.n_pcs, hv.n_obs - 1, hv.n_vars - 1), random_state=args.seed)
        sub.obsm['X_pca_sub'] = hv.obsm['X_pca']
        del hv
        print(f'Recomputed PCA on {int(sub.var["highly_variable"].sum())} subset HVGs')
        rep = 'X_pca_sub'
    else:
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
                                    'recompute_pca': bool(args.recompute_pca)}
    sub.write_h5ad(args.output_h5ad)
    print(f'Wrote {args.output_h5ad}')


if __name__ == '__main__':
    main()
