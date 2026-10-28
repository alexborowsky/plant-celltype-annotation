#!/usr/bin/env python3
"""Which cell type is a state cluster? Judge the type on genes the state does not change.

A stress, defense or cell-cycle state can suppress the identity markers (and promoter reporters) of the type it sits
in, so "the type's marker is not enriched here" does not show the cells are another type. This script compares a query
group (the state cells) with two or more candidate types on each pair's own type-specific genes. It learns those
genes from the candidates, at matched sequencing depth, and leaves out every gene the query induces or represses.

For each candidate pair A/B: the top --n-genes genes more often detected in A than B, and in B than A (detection
difference, among genes detected in >= 20% of A or B). Per cell: mean(A genes) - mean(B genes), scaled so that the
median B cell = 0 and the median A cell = 1. A query median near 1 means the query matches A; near 0, B.
Also reported, all within the depth band:
  - correlation of group mean profiles on the union of the pair genes;
  - detection of --genes (marker IDs) and --reporters (obs columns such as <transgene>_expr; --reporter-cells restricts
    them to e.g. treated samples);
  - the state genes left out (the query's own program).

Groups are written NAME=SPEC. SPEC is key:v1,v2 (an obs column and its values), and several are joined with '&', e.g.
  --query Stressed=sub_cl7:2,4 \\
  --candidate TypeA=sub_cl7:0,1 \\
  --candidate "TypeB=leiden_res0.5:0&cell_state:none" \\
  --control Other=sub_cl7:3
Controls are scored like the query (useful to see what an intermediate score looks like).

First check the query against coarser clusterings (SKILL.md Step 7 item 9): a state cluster whose cells sit in
different type clusters at a coarser resolution is one response shared by those types, and scores midway here.
Verdict: the query is called type A only if it sits >= --call-at (default 0.7) toward A against every other
candidate; otherwise it is "unresolved" (check the coarse split; else label it Unknown or by lineage, plus the state).
Give one candidate per lineage the cells could belong to: a two-candidate score cannot detect a third type (a leaf
defense subset scored 0.85 toward bundle sheath against mesophyll alone, and 0.5 between bundle sheath and pavement
once pavement was a candidate).

Per-cell mode (--per-cell): for a state cluster known to mix types with no coarse split to follow. Not for
cell-cycle clusters, which stay Unknown + State unless clearly subdivided (SKILL.md Step 8). Each query cell (all of
them, not only the depth band) is placed on every pair's
scale and assigned to the candidate it is >= 0.5 toward against every other candidate (else "unresolved"). The split is
printed next to the candidates' shares of cells; --assignments writes barcode -> type for apply_annotations.py
--import-labels <file>:assigned_type:<key>. A cycling cluster that goes almost entirely to one minor type is suspect:
dividing cells look young and provascular whatever their type.

Caveats (print them with the result): candidates defined by the same marker you are testing make the comparison
partly circular, and a shared regional program (cells of one island) can score like the candidate it was learnt from.
Report the score as one line of evidence next to markers, reporters and UMAP position.

Usage:
  python type_under_state.py --h5ad annotated.h5ad --query NAME=SPEC --candidate NAME=SPEC --candidate NAME=SPEC \\
      [--control NAME=SPEC] [--genes <gene IDs>] [--reporters <transgene>_expr] \\
      [--reporter-cells "Treatment:<treated groups>"] [--gene-map gene_map.tsv] \\
      [--depth-key total_counts] [--n-genes 100] [--out checks/type_under_state]
"""
import argparse
import itertools
import os
import sys

import numpy as np
import pandas as pd
import scanpy as sc
from scipy import sparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cluster_evidence import expression_source  # noqa: E402


def parse_group(text):
    if '=' not in text:
        sys.exit(f'group must be NAME=SPEC, got {text}')
    name, spec = text.split('=', 1)
    terms = []
    for part in spec.split('&'):
        if ':' not in part:
            sys.exit(f'group spec must be key:v1,v2[&key:v...], got {spec}')
        k, v = part.split(':', 1)
        terms.append((k.strip(), [x.strip() for x in v.split(',') if x.strip()]))
    return name.strip(), terms


def group_mask(obs, terms):
    m = np.ones(len(obs), bool)
    for k, vals in terms:
        if k not in obs.columns:
            sys.exit(f'obs has no column {k}')
        m &= obs[k].astype(str).isin(vals).to_numpy()
    return m


def depth_band(depth, masks, min_cells):
    """Widest depth range shared by all groups: overlap of their 25-75% ranges, widened to 10-90% if too few cells."""
    for lo_q, hi_q in ((25, 75), (10, 90), (5, 95)):
        lo = max(np.percentile(depth[m], lo_q) for m in masks.values())
        hi = min(np.percentile(depth[m], hi_q) for m in masks.values())
        if lo < hi:
            band = (depth >= lo) & (depth <= hi)
            if all((band & m).sum() >= min_cells for m in masks.values()):
                return band, lo, hi
    return None, np.nan, np.nan


def stats(X, m):
    sub = X[np.flatnonzero(m)]
    if sparse.issparse(sub):
        return np.asarray((sub > 0).mean(0)).ravel(), np.asarray(sub.mean(0)).ravel()
    sub = np.asarray(sub)
    return (sub > 0).mean(0), sub.mean(0)


def row_mean(X, rows, cols):
    sub = X[rows][:, cols]
    return np.asarray(sub.mean(1)).ravel()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--h5ad', required=True)
    p.add_argument('--query', required=True, help='NAME=SPEC: the state cells whose type is in question')
    p.add_argument('--candidate', action='append', required=True, help='NAME=SPEC (>= 2): candidate types, '
                   'defined by cells without the state')
    p.add_argument('--control', action='append', default=[], help='NAME=SPEC: other groups scored like the query')
    p.add_argument('--genes', default='', help='comma-separated gene IDs to tabulate (markers)')
    p.add_argument('--reporters', default='', help='comma-separated obs columns (detected if > 0)')
    p.add_argument('--reporter-cells', default=None, help='SPEC restricting the reporter columns (e.g. treated)')
    p.add_argument('--gene-map', default=None, help='map_markers gene map, to name genes (rank-1 ref_symbol)')
    p.add_argument('--depth-key', default='total_counts')
    p.add_argument('--n-genes', type=int, default=100)
    p.add_argument('--call-at', type=float, default=0.7,
                   help='verdict: call type A when the query median is >= this toward A against every other candidate')
    p.add_argument('--state-delta', type=float, default=0.15,
                   help='a gene is a state gene if its detection in the query differs from every candidate by more '
                        'than this (induced) or is below all candidates by more than this (repressed)')
    p.add_argument('--state-ref', choices=['median', 'max'], default='median',
                   help='state genes differ from the median candidate (default) or from every candidate (max)')
    p.add_argument('--max-cells', type=int, default=15000, help='cells sampled per group')
    p.add_argument('--min-cells', type=int, default=100, help='cells per group required in the depth band')
    p.add_argument('--layer', default=None)
    p.add_argument('--use-raw', choices=['auto', 'yes', 'no'], default='auto')
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--out', default=None, help='output prefix (writes <out>_scores.tsv, <out>_genes.tsv)')
    p.add_argument('--per-cell', action='store_true',
                   help='assign each query cell to a candidate (cell-cycle clusters: dividing cells of several types)')
    p.add_argument('--assignments', default=None, help='with --per-cell: write barcode -> assigned_type TSV here')
    a = p.parse_args()
    if len(a.candidate) < 2:
        sys.exit('give at least two --candidate groups')
    if len(a.candidate) == 2:
        print('WARN only two candidates: a two-candidate score cannot detect a third type. Give one candidate per '
              'lineage the cells could belong to (e.g. epidermis, mesophyll, bundle sheath, vascular).')
    rng = np.random.default_rng(a.seed)

    adata = sc.read_h5ad(a.h5ad)
    X, var_names, src = expression_source(adata, a.layer, a.use_raw)
    X = X.tocsr() if sparse.issparse(X) else np.asarray(X)
    obs = adata.obs
    if a.depth_key not in obs.columns:
        sys.exit(f'obs has no {a.depth_key}; give --depth-key (e.g. n_counts)')
    qname, qterms = parse_group(a.query)
    groups = {qname: group_mask(obs, qterms)}
    cands = []
    for c in a.candidate:
        n, t = parse_group(c)
        groups[n] = group_mask(obs, t)
        cands.append(n)
    ctrls = []
    for c in a.control:
        n, t = parse_group(c)
        groups[n] = group_mask(obs, t)
        ctrls.append(n)
    order = [qname] + cands + ctrls
    full_n = {n: int(groups[n].sum()) for n in order}
    q_all = np.flatnonzero(groups[qname])  # per-cell mode scores every query cell
    for n in order:
        idx = np.flatnonzero(groups[n])
        if len(idx) == 0:
            sys.exit(f'group {n} has no cells')
        if len(idx) > a.max_cells:
            keep = np.zeros(len(obs), bool)
            keep[rng.choice(idx, a.max_cells, replace=False)] = True
            groups[n] = keep
    over = [(x, y) for x, y in itertools.combinations(order, 2) if (groups[x] & groups[y]).any()]
    if over:
        print(f'WARN overlapping groups: {over}')

    depth = obs[a.depth_key].to_numpy().astype(float)
    print(f'{adata.n_obs:,} cells; expression from {src}')
    print('group sizes and median depth (all cells):')
    for n in order:
        print(f'  {n:24s} {groups[n].sum():>7,}  median {a.depth_key} {np.median(depth[groups[n]]):,.0f}')
    band, lo, hi = depth_band(depth, groups, a.min_cells)
    if band is None:
        print('WARN no depth range is shared by all groups with enough cells: comparing without depth matching')
        band, lo, hi = np.ones(len(obs), bool), depth.min(), depth.max()
    else:
        print(f'depth band {a.depth_key} {lo:,.0f}-{hi:,.0f}: '
              + ', '.join(f'{n} {(band & groups[n]).sum():,}' for n in order))
    gm = {n: groups[n] & band for n in order}
    st = {n: stats(X, gm[n]) for n in order}  # (frac, mean)

    # State genes: query detection differs from every candidate by > state_delta in the same direction
    fq = st[qname][0]
    fc = np.vstack([st[c][0] for c in cands])
    # A gene belongs to the state when the query differs from the typical (median) candidate. Comparing with every
    # candidate (max) keeps state genes that one candidate shares (a candidate with some dividing cells keeps the
    # S-phase genes as "type genes" and attracts every dividing cell).
    ref_hi = np.median(fc, 0) if a.state_ref == 'median' else fc.max(0)
    ref_lo = np.median(fc, 0) if a.state_ref == 'median' else fc.min(0)
    induced = (fq - ref_hi) > a.state_delta
    repressed = (ref_lo - fq) > a.state_delta
    state = induced | repressed
    print(f'state genes left out: {induced.sum()} induced, {repressed.sum()} repressed in {qname} vs the {a.state_ref} candidate')

    sym = {}
    if a.gene_map:
        g = pd.read_csv(a.gene_map, sep='\t', dtype=str).fillna('')
        if 'hit_rank' in g.columns:
            g = g[g['hit_rank'] == '1']
        sym = {r.query_gene: (r.ref_symbol or r.ref_gene) for r in g.itertuples()}
    name = lambda i: f"{var_names[i]}" + (f" ({sym[var_names[i]]})" if sym.get(var_names[i]) else '')

    rows, gene_rows = [], []
    toward = {c: [] for c in cands}  # per candidate: query median toward it, one per pair
    wins = {c: np.zeros(len(q_all), int) for c in cands}  # per-cell pairwise wins
    margin = {c: np.full(len(q_all), np.inf) for c in cands}  # per cell: weakest score toward c over its pairs
    allidx = {n: np.flatnonzero(gm[n]) for n in order}
    for A, B in itertools.combinations(cands, 2):
        fa, fb = st[A][0], st[B][0]
        ok = ~state & (np.maximum(fa, fb) >= 0.2)
        d = np.where(ok, fa - fb, 0)
        a_up = np.argsort(-d)[:a.n_genes]
        a_up = a_up[d[a_up] > 0]
        b_up = np.argsort(d)[:a.n_genes]
        b_up = b_up[d[b_up] < 0]
        if len(a_up) < 10 or len(b_up) < 10:
            print(f'WARN {A} vs {B}: only {len(a_up)}/{len(b_up)} type genes; skipped')
            continue
        score = {n: row_mean(X, allidx[n], a_up) - row_mean(X, allidx[n], b_up) for n in order}
        m0, m1 = np.median(score[B]), np.median(score[A])
        if m1 - m0 <= 0:
            print(f'WARN {A} vs {B}: candidates not separated; skipped')
            continue
        print(f'\n{A} (=1) vs {B} (=0): {len(a_up)}+{len(b_up)} type genes; detection gap '
              f'{d[a_up].min():.2f}-{d[a_up].max():.2f} / {-d[b_up].max():.2f}-{-d[b_up].min():.2f}')
        for n in order:
            z = (score[n] - m0) / (m1 - m0)
            q1, q2, q3 = np.percentile(z, [25, 50, 75])
            rows.append(dict(pair=f'{A}_vs_{B}', group=n, role='query' if n == qname else 'candidate'
                             if n in cands else 'control', n=len(z), q25=round(q1, 2), median=round(q2, 2),
                             q75=round(q3, 2)))
            print(f'  {n:24s} median {q2:5.2f}  (IQR {q1:.2f} to {q3:.2f})')
            if n == qname:
                toward[A].append(q2)
                toward[B].append(1 - q2)
        if a.per_cell:
            zq = (row_mean(X, q_all, a_up) - row_mean(X, q_all, b_up) - m0) / (m1 - m0)
            wins[A] += zq >= 0.5
            wins[B] += zq < 0.5
            margin[A] = np.minimum(margin[A], zq)
            margin[B] = np.minimum(margin[B], 1 - zq)
        cols = np.r_[a_up, b_up]
        P = pd.DataFrame({n: st[n][1][cols] for n in order})
        cor = P.corr().loc[qname, cands]
        print('  profile correlation of ' + qname + ': ' + ', '.join(f'{c} {v:.3f}' for c, v in cor.items()))
        print(f'  top {A} genes: ' + ', '.join(name(i) for i in a_up[:12]))
        print(f'  top {B} genes: ' + ', '.join(name(i) for i in b_up[:12]))
        for i in a_up:
            gene_rows.append(dict(pair=f'{A}_vs_{B}', side=A, gene=var_names[i], symbol=sym.get(var_names[i], ''),
                                  **{f'frac_{n}': round(st[n][0][i], 3) for n in order}))
        for i in b_up:
            gene_rows.append(dict(pair=f'{A}_vs_{B}', side=B, gene=var_names[i], symbol=sym.get(var_names[i], ''),
                                  **{f'frac_{n}': round(st[n][0][i], 3) for n in order}))

    if a.per_cell:
        need = len(cands) - 1
        assigned = np.array(['unresolved'] * len(q_all), dtype=object)
        best = np.full(len(q_all), -np.inf)
        for c in cands:
            ok = (wins[c] == need) & (margin[c] > best)
            assigned[ok] = c
            best[ok] = margin[c][ok]
        split = pd.Series(assigned).value_counts()
        tot_c = sum(full_n[c] for c in cands)
        print(f'\nPER-CELL split of {qname} ({len(q_all):,} cells) vs the candidates\' shares of cells:')
        for c in cands + ['unresolved']:
            n = int(split.get(c, 0))
            ref = f'{full_n[c] / tot_c:.0%}' if c in full_n else '-'
            print(f'  {c:24s} {n:>7,} ({n / len(q_all):.0%})   candidates share {ref}')
        top = split.drop('unresolved', errors='ignore')
        if len(top) and top.iloc[0] / len(q_all) > 0.8 and full_n[top.index[0]] / tot_c < 0.4:
            print(f'  WARN {top.index[0]} takes {top.iloc[0] / len(q_all):.0%} of the query but is '
                  f'{full_n[top.index[0]] / tot_c:.0%} of the candidates: dividing cells look young/provascular; check '
                  'the candidates (add the majority types) before using this split.')
        if a.assignments:
            os.makedirs(os.path.dirname(os.path.abspath(a.assignments)), exist_ok=True)
            pd.DataFrame({'barcode': obs.index[q_all], 'assigned_type': assigned,
                          'margin': np.round(best, 3)}).to_csv(a.assignments, sep='\t', index=False)
            print(f'Wrote {a.assignments}')
    tested = {c: v for c, v in toward.items() if v}
    called = [c for c, v in tested.items() if len(v) == len(cands) - 1 and min(v) >= a.call_at]
    print(f'\nVERDICT for {qname}: ' + (f'{called[0]} (>= {a.call_at} toward it against every other candidate)'
                                       if len(called) == 1 else
                                       'unresolved: no candidate wins every pair. If the query\'s cells sit in '
                                       'different type clusters at a coarser resolution, type each part by its coarse '
                                       'cluster; otherwise label Unknown or by lineage + the state'))
    print('  lowest score toward each candidate: ' + ', '.join(f'{c} {min(v):.2f}' for c, v in tested.items()))
    top_state = np.argsort(-(fq - ref_hi))[:12]
    print(f'\n{qname} state program (left out), top induced: '
          + ', '.join(f'{name(i)} {fq[i]:.0%} vs <={fc.max(0)[i]:.0%}' for i in top_state if induced[i]))

    genes = [g for g in a.genes.split(',') if g]
    if genes:
        print('\nmarker detection in the depth band:')
        for g in genes:
            if g not in var_names:
                print(f'  {g}: not in the data')
                continue
            i = var_names.get_loc(g)
            print(f'  {name(i):28s} ' + '  '.join(f'{n} {st[n][0][i]:.0%}' for n in order))
    reps = [r for r in a.reporters.split(',') if r]
    if reps:
        rc = np.ones(len(obs), bool)
        if a.reporter_cells:
            rc = group_mask(obs, parse_group('cells=' + a.reporter_cells)[1])
        print('\nreporter detection in the depth band' + (f' ({a.reporter_cells})' if a.reporter_cells else '') + ':')
        for r in reps:
            if r not in obs.columns:
                print(f'  {r}: not in obs')
                continue
            v = obs[r].to_numpy().astype(float) > 0
            print(f'  {r:28s} ' + '  '.join(f'{n} {v[gm[n] & rc].mean():.0%}' for n in order))
    print('\nCaveats: candidates defined by a marker under test make this partly circular; a shared regional program '
          'can score like the candidate it was learnt from. Use it next to markers, reporters and UMAP position.')
    if a.out and rows:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        pd.DataFrame(rows).to_csv(f'{a.out}_scores.tsv', sep='\t', index=False)
        pd.DataFrame(gene_rows).to_csv(f'{a.out}_genes.tsv', sep='\t', index=False)
        print(f'Wrote {a.out}_scores.tsv, {a.out}_genes.tsv')


if __name__ == '__main__':
    main()
