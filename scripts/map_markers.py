#!/usr/bin/env python3
"""Map reference marker genes (any reference species) onto a target species.

Reference tables live in references/markers/ (one per reference species/tissue).
Rows carry trait tags: `requires` (the target must have all of them) and
`excludes` (the target must have none of them). Pass the target's traits with
--target-traits, e.g. `grass C4` for maize or `eudicot Solanaceae` for tomato.

Modes:
  BLAST mode (default)  --blast target_vs_reference.tsv [--blast-reverse ...]
                        Target genes whose best hit is a marker locus become markers.
  --no-blast            The reference IDs are already target IDs (e.g. sorghum
                        markers on sorghum data); rows are copied after filtering.

Outputs:
  --out-gene-map   (BLAST mode) one row per (target gene, distinct reference locus),
                   ranked by bitscore; used to annotate DE genes with homolog symbols.
  --out-markers    target marker table (gene_id, symbol, cell_type, evidence, basis, ...).

Lightweight (no scanpy); fine to run in a small job.
"""

import argparse
import re
import sys

import numpy as np
import pandas as pd

LEVELS = {'low': 0, 'medium': 1, 'high': 2}
# Traits implied by more specific ones, so `--target-traits Sorghum` is enough.
IMPLIES = {
    'Sorghum': {'grass', 'C4'},
    'grass': {'monocot'},
    'Brassicaceae': {'eudicot', 'Brassicales'},
    'Solanaceae': {'eudicot'},
    'Oryza': {'grass', 'C3'},
    'Fabaceae': {'eudicot'},
    'Gossypium': {'eudicot'},
    'Rosaceae': {'eudicot'},
    'Apocynaceae': {'eudicot'},
    'Cucurbitaceae': {'eudicot'},
    'Capsicum': {'Solanaceae', 'eudicot'},
    'conifer': {'gymnosperm'},
    'Brassicales': {'eudicot'},
    'liverwort': {'bryophyte'},
    'moss': {'bryophyte'},
    'hornwort': {'bryophyte'},
}
REF_COLS = ['ref_species', 'tissue', 'cell_type', 'ref_gene', 'symbol', 'kind', 'evidence',
            'confidence', 'requires', 'excludes', 'basis', 'source']


def read_blast(path, q_regex, s_regex, max_evalue, min_pident):
    """Parse outfmt 6 (+ optional Araport 'Symbols:' / full-name columns)."""
    rows = []
    q_re = re.compile(q_regex) if q_regex else None
    s_re = re.compile(s_regex) if s_regex else None
    with open(path) as fh:
        for line in fh:
            if not line.strip() or line.startswith('#'):
                continue
            f = line.rstrip('\n').split('\t')
            if len(f) < 12:
                continue
            q = q_re.sub('', f[0]) if q_re else f[0]
            s = s_re.sub('', f[1]) if s_re else f[1]
            symbol, desc = '', ''
            if len(f) >= 16 and f[14].startswith('Symbols:'):
                symbol = f[14].replace('Symbols:', '').strip()
                if symbol == 'no symbol available':
                    symbol = ''
                desc = f[15].strip()
                if desc == 'no full name available':
                    desc = ''
            rows.append((q, s, float(f[2]), float(f[10]), float(f[11]), symbol, desc))
    df = pd.DataFrame(rows, columns=['query_gene', 'ref_gene', 'pident', 'evalue',
                                     'bitscore', 'ref_symbol', 'ref_description'])
    n0 = len(df)
    df = df[(df['evalue'] <= max_evalue) & (df['pident'] >= min_pident)]
    print(f"  {path}: {n0:,} HSPs, {len(df):,} pass evalue<={max_evalue} pident>={min_pident}")
    return df


def read_orthology(path, q_col, r_col, rel_col, q_regex):
    """Orthology table (e.g. OrthoFinder per-gene annotation) -> gene-map-like hits.

    Every listed orthologue is a rank-1 hit (orthologues are not ranked); 1:1 pairs are marked RBH.
    pident/bitscore are NaN, so outputs never show a made-up identity.
    """
    t = pd.read_csv(path, sep='\t', dtype=str).fillna('')
    for c in (q_col, r_col):
        if c not in t.columns:
            sys.exit(f'--orthology: column {c} not in {path} (columns: {list(t.columns)[:20]})')
    rows = []
    q_re = re.compile(q_regex) if q_regex else None
    for q, refs, rel in zip(t[q_col], t[r_col], t[rel_col] if rel_col in t.columns else [''] * len(t)):
        q = q_re.sub('', q) if q_re else q
        for r in re.split(r'[,;\s]+', refs):
            if r:
                rows.append((q, re.sub(r'\.\d+$', '', r), rel))
    df = pd.DataFrame(rows, columns=['query_gene', 'ref_gene', 'relationship']).drop_duplicates(['query_gene', 'ref_gene'])
    df['hit_rank'] = 1
    df['pident'] = np.nan; df['evalue'] = np.nan; df['bitscore'] = np.nan
    df['ref_symbol'] = ''; df['ref_description'] = ''
    df['rbh'] = np.where(df['relationship'].str.replace(' ', '') == '1:1', 'yes', 'no')
    print(f"  {path}: {df['query_gene'].nunique():,} genes with {len(df):,} orthologue pairs "
          f"({(df['rbh'] == 'yes').sum():,} 1:1)")
    return df


def warn_paralog_families(ref):
    """Marker loci of one gene family (symbol before ';' or trailing digits) listed for different cell types."""
    fam = ref['symbol'].str.extract(r'^([A-Za-z]+\d*)[;.]', expand=False)
    t = ref.assign(family=fam).dropna(subset=['family'])
    for f, g in t.groupby('family'):
        cts = sorted(set(g['cell_type']))
        if len(cts) > 1 and g['ref_gene'].nunique() > 1:
            print(f"  WARN paralog family {f} has members listed for different cell types "
                  f"({'; '.join(sorted(set(g['symbol'] + '=' + g['cell_type'])))}). In other species a gene "
                  f"may be a co-orthologue of all of them; do not use this family to split those types.")


def rank_hits(df, key, target, max_hits):
    """Collapse isoforms/HSPs to best per (key, target) pair and rank by bitscore."""
    # Stable sort with explicit tie-breakers: identical paralogs (histones, UBCs) often tie on
    # bitscore, and an unstable sort would make ranks and marker lists change between runs.
    df = df.sort_values(['bitscore', 'pident', 'evalue', target], ascending=[False, False, True, True],
                        kind='mergesort')
    df = df.drop_duplicates([key, target], keep='first')
    # Equal bitscores share a rank (identical paralogs, co-orthologues): none wins alphabetically.
    df['hit_rank'] = df.groupby(key)['bitscore'].rank(method='min', ascending=False).astype(int)
    return df[df['hit_rank'] <= max_hits]


def expand_traits(traits):
    out = set(traits)
    changed = True
    while changed:
        changed = False
        for t in list(out):
            new = IMPLIES.get(t, set()) - out
            if new:
                out |= new
                changed = True
    return out


def tags(s):
    return {t.strip() for t in str(s).split(',') if t.strip()}


def load_reference(paths, tissues, min_conf, traits, ref_strip, id_column='ref_gene'):
    frames = []
    for path in paths:
        df = pd.read_csv(path, sep='\t', dtype=str).fillna('')
        for c in REF_COLS:
            if c not in df.columns:
                df[c] = ''
        df['ref_file'] = path.rsplit('/', 1)[-1]
        frames.append(df)
    ref = pd.concat(frames, ignore_index=True)
    if id_column != 'ref_gene':
        if id_column not in ref.columns:
            sys.exit(f'--id-column {id_column} not in the reference table(s)')
        empty = ref[id_column].str.strip() == ''
        if empty.any():
            print(f"  {int(empty.sum())} rows have no {id_column} and are dropped: "
                  + ', '.join(ref.loc[empty, 'ref_gene'] + '(' + ref.loc[empty, 'symbol'] + ')'))
        ref = ref[~empty].copy()
        ref['ref_gene'] = ref[id_column]
    if ref_strip:
        ref['ref_gene'] = ref['ref_gene'].str.replace(ref_strip, '', regex=True)
    ref['ref_key'] = ref['ref_gene'].str.upper()
    n0 = len(ref)
    if tissues:
        # Tissue values can be compound (leaf_stem_phloem, ovule/seed): match on any token.
        want = {t.lower() for t in tissues}
        tok = ref['tissue'].str.lower().map(lambda s: set(re.split(r'[_,;/ ]+', s)) | {s})
        ref = ref[tok.map(lambda t: bool(t & want))]
    ref = ref[ref['confidence'].map(LEVELS).fillna(0) >= LEVELS[min_conf]]
    print(f"  {n0} reference rows; {len(ref)} after tissue/confidence filters")

    if traits is None:
        print('  WARN no --target-traits given: keeping only rows without `requires` tags; '
              '`excludes` tags are not checked')
        keep = ref['requires'].map(lambda s: not tags(s))
    else:
        tt = expand_traits(traits)
        print(f"  target traits: {sorted(tt)}")
        keep = [tags(r) <= tt and not (tags(e) & tt) for r, e in zip(ref['requires'], ref['excludes'])]
        keep = pd.Series(keep, index=ref.index)
    dropped = ref[~keep]
    if len(dropped):
        uniq = dropped.drop_duplicates(['cell_type', 'symbol'])
        print(f"  {len(dropped)} rows ({len(uniq)} unique cell type x marker) not applicable to this target "
              f"(requires/excludes):")
        for r in uniq.itertuples():
            why = f"requires={r.requires}" if r.requires else f"excludes={r.excludes}"
            print(f"    {r.cell_type:22s} {r.symbol:14s} {why}")
    ref = ref[keep]
    if ref.empty:
        sys.exit('No reference rows left after filtering.')
    return ref


def summarize(out, ref, note):
    print(f"  {len(out)} target marker rows for {out['ref_gene'].nunique()}/{ref['ref_gene'].nunique()} "
          f"reference loci {note}")
    by = out.groupby('cell_type').agg(n_rows=('gene_id', 'size'),
                                     n_function=('evidence', lambda e: int((e == 'function').sum())))
    print('  per cell type (rows / function-evidence rows):')
    for ct, r in by.iterrows():
        print(f"    {ct:24s} {r.n_rows:4d} / {r.n_function}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--blast', default=None, help='target(query) vs reference(subject) outfmt 6')
    p.add_argument('--blast-reverse', default=None,
                   help='optional reference(query) vs target(subject) outfmt 6; enables RBH and paralog rescue')
    p.add_argument('--no-blast', action='store_true',
                   help='reference IDs are already target IDs (same species); skip homology mapping')
    p.add_argument('--query-strip-regex', default='',
                   help="regex removed from target IDs so they match adata.var_names; pass as "
                        "--query-strip-regex='-mRNA$' (with =) when it starts with '-'")
    p.add_argument('--ref-strip-regex', default=None,
                   help=r"regex removed from reference IDs (default '\.\d+$' in BLAST mode, none with --no-blast)")
    p.add_argument('--ref-annotation', default=None,
                   help='optional TSV: ref_gene<TAB>symbol<TAB>description (overrides BLAST-embedded symbols)')
    p.add_argument('--max-hits', type=int, default=5, help='distinct reference loci kept per target gene')
    p.add_argument('--max-evalue', type=float, default=1e-5)
    p.add_argument('--min-pident', type=float, default=0.0)
    p.add_argument('--reference', nargs='+', default=None,
                   help='one or more marker tables from references/markers/ (same reference species)')
    p.add_argument('--target-traits', nargs='*', default=None,
                   help='traits of the target species, e.g. eudicot Solanaceae | grass C4 | Sorghum')
    p.add_argument('--tissue', action='append', default=None,
                   help="tissue(s) to keep (repeatable, e.g. --tissue leaf --tissue any). Default: all")
    p.add_argument('--min-confidence', choices=list(LEVELS), default='low')
    p.add_argument('--max-marker-rank', type=int, default=1,
                   help='target gene counts as a marker if the marker locus is within its top-N hits (default 1)')
    p.add_argument('--rescue-min-ratio', type=float, default=0.85,
                   help='reverse-best rescue only if bitscore(gene, marker) >= this x bitscore(gene, its best hit)')
    p.add_argument('--max-copies', type=int, default=5,
                   help='max target genes kept per reference marker locus (RBH first, then bitscore)')
    p.add_argument('--id-column', default='ref_gene',
                   help='reference-table column holding the gene IDs to use (e.g. alt_id for rice RAP-DB '
                        'IDs; rice_root.tsv keeps MSU7 IDs in ref_gene)')
    p.add_argument('--orthology', default=None,
                   help='orthology table instead of BLAST (e.g. OrthoFinder per-gene annotation): one row per '
                        'target gene, reference orthologues comma/space-separated; all count as rank-1 hits')
    p.add_argument('--orth-query-col', default='gene_id')
    p.add_argument('--orth-ref-col', default='At_orthologues', help='e.g. At_orthologues or Mp_orthologues')
    p.add_argument('--orth-rel-col', default='At_relationship', help='1:1 rows are marked RBH')
    p.add_argument('--out-gene-map', default=None)
    p.add_argument('--out-markers', default=None)
    args = p.parse_args()

    if args.no_blast:
        if not (args.reference and args.out_markers):
            sys.exit('--no-blast needs --reference and --out-markers')
        print('[1] Same-species mode (no homology mapping)')
        ref = load_reference(args.reference, args.tissue, args.min_confidence, args.target_traits,
                             args.ref_strip_regex, args.id_column)
        warn_paralog_families(ref)
        out = pd.DataFrame({
            'gene_id': ref['ref_gene'], 'symbol': ref['symbol'], 'cell_type': ref['cell_type'],
            'kind': ref['kind'], 'tissue': ref['tissue'], 'evidence': ref['evidence'],
            'confidence': ref['confidence'], 'ref_species': ref['ref_species'],
            'ref_gene': ref['ref_gene'], 'hit_rank': 0, 'pident': 100.0, 'rbh': '', 'via': 'same_species',
            'basis': ref['basis'], 'source': ref['source'],
        }).drop_duplicates(['gene_id', 'cell_type'])
        out.to_csv(args.out_markers, sep='\t', index=False)
        summarize(out, ref, f'-> {args.out_markers}')
        return

    if not (args.blast or args.orthology) or not args.out_gene_map:
        sys.exit('Homology mode needs --blast (or --orthology) and --out-gene-map (or use --no-blast)')
    ref_strip = r'\.\d+$' if args.ref_strip_regex is None else args.ref_strip_regex

    if args.orthology:
        print('[1] Reading orthology table')
        fwd = read_orthology(args.orthology, args.orth_query_col, args.orth_ref_col, args.orth_rel_col,
                             args.query_strip_regex)
        gm = fwd.copy()
        depth = pd.Series([2])  # orthology tables list all orthologues; no depth warning
    else:
        print('[1] Reading forward BLAST')
        fwd = read_blast(args.blast, args.query_strip_regex, ref_strip, args.max_evalue, args.min_pident)
        if fwd.empty:
            sys.exit('No BLAST hits passed filters.')
        gm = rank_hits(fwd, 'query_gene', 'ref_gene', args.max_hits)
        depth = fwd.groupby('query_gene')['ref_gene'].nunique()
    if depth.median() <= 1 and (depth > 1).mean() < 0.05:
        print(f'  WARN the BLAST file has ~1 subject per query (median {depth.median():.0f}; '
              f'{(depth > 1).mean():.1%} of queries have >1). It was probably run with -max_target_seqs 1, so '
              f'markers whose target gene best-hits a paralog are lost (often histones, PCNA, cyclins, CDKs) and '
              f'paralog rescue is impossible. Rerun with -max_target_seqs 5 (or more) and add --blast-reverse.')

    # Symbols: fill per-locus from any HSP that carried them, then optional file
    sym = (fwd[fwd['ref_symbol'] != ''].drop_duplicates('ref_gene')
           .set_index('ref_gene')[['ref_symbol', 'ref_description']])
    gm = gm.drop(columns=['ref_symbol', 'ref_description']).join(sym, on='ref_gene')
    if args.ref_annotation:
        ann = pd.read_csv(args.ref_annotation, sep='\t', header=None, dtype=str,
                          names=['ref_gene', 'ref_symbol', 'ref_description'], usecols=[0, 1, 2])
        if ref_strip:
            ann['ref_gene'] = ann['ref_gene'].str.replace(ref_strip, '', regex=True)
        ann = ann.drop_duplicates('ref_gene').set_index('ref_gene')
        gm = gm.drop(columns=['ref_symbol', 'ref_description']).join(ann, on='ref_gene')
    gm[['ref_symbol', 'ref_description']] = gm[['ref_symbol', 'ref_description']].fillna('')

    if not args.orthology:
        gm['rbh'] = ''
    rev_best = {}
    if args.blast_reverse:
        print('[1b] Reading reverse BLAST for reciprocal best hits')
        # reverse: query = reference, subject = target, so swap the regexes
        rev = read_blast(args.blast_reverse, ref_strip, args.query_strip_regex,
                         args.max_evalue, args.min_pident)
        rev = rank_hits(rev, 'query_gene', 'ref_gene', 1)  # columns: ref locus in query_gene
        rev_best = dict(zip(rev['query_gene'].str.upper(), rev['ref_gene']))
        gm['rbh'] = [
            'yes' if (r == 1 and rev_best.get(ref.upper()) == q) else 'no'
            for q, ref, r in zip(gm['query_gene'], gm['ref_gene'], gm['hit_rank'])
        ]
        print(f"  RBH pairs: {(gm['rbh'] == 'yes').sum():,}")

    cols = ['query_gene', 'hit_rank', 'ref_gene', 'ref_symbol', 'ref_description',
            'pident', 'evalue', 'bitscore', 'rbh']
    gm = gm.sort_values(['query_gene', 'hit_rank'])[cols]
    gm.to_csv(args.out_gene_map, sep='\t', index=False)
    print(f"  gene map: {gm['query_gene'].nunique():,} target genes -> {args.out_gene_map}")

    if not args.reference:
        return
    if not args.out_markers:
        sys.exit('--out-markers required with --reference')

    print('[2] Mapping reference markers')
    ref = load_reference(args.reference, args.tissue, args.min_confidence, args.target_traits, ref_strip,
                         args.id_column)
    warn_paralog_families(ref)
    ref_keys = set(ref['ref_key'])

    gm_u = gm.assign(ref_key=gm['ref_gene'].str.upper())
    gm_u = gm_u[gm_u['ref_key'].isin(ref_keys)]
    hits = gm_u[gm_u['hit_rank'] <= args.max_marker_rank].assign(via='orthology' if args.orthology else 'forward')
    if rev_best:
        # Rescue paralog misses: the target gene that is the marker locus's own best hit,
        # even if that gene's best hit is a different paralog (e.g. PCNA1 vs PCNA2).
        pairs = pd.DataFrame({'ref_key': list(rev_best), 'query_gene': list(rev_best.values())})
        pairs = pairs[pairs['ref_key'].isin(ref_keys)]
        rescue = pairs.merge(gm_u, on=['ref_key', 'query_gene'], how='inner')
        rescue = rescue[rescue['hit_rank'] > args.max_marker_rank].assign(via='reverse_best')
        # Only rescue near-equivalent paralogs (PCNA1/2, SWEET11/12: ratio ~0.9-1.0). When the target
        # lacks a true ortholog, the marker's best hit is a different subfamily (SUC2 -> grass SUT4-type
        # at 0.78), and the gene's own best hit scores clearly higher.
        # tied hits share rank 1, so take the max per gene
        best_bits = gm.loc[gm['hit_rank'] == 1].groupby('query_gene')['bitscore'].max()
        rescue = rescue.assign(ratio=rescue['bitscore'] / rescue['query_gene'].map(best_bits))
        low = rescue[rescue['ratio'] < args.rescue_min_ratio]
        if len(low):
            print(f'  NOT rescued (bitscore ratio < {args.rescue_min_ratio}, likely a different subfamily): '
                  + ', '.join(f'{q}->{r} ({x:.2f})' for q, r, x in zip(low['query_gene'], low['ref_gene'], low['ratio'])))
        rescue = rescue[rescue['ratio'] >= args.rescue_min_ratio].drop(columns='ratio')
        if len(rescue):
            print(f'  rescued {len(rescue)} marker genes via reverse best hit: '
                  + ', '.join(f'{q}->{r}' for q, r in zip(rescue['query_gene'], rescue['ref_gene'])))
        hits = pd.concat([hits, rescue], ignore_index=True)
    # Cap copies per reference locus: large families (LTPs, chitinases, BAHDs) otherwise map one
    # marker to dozens of target genes and dilute the score. Prefer RBH, then bitscore.
    hits = hits.assign(_rbh=(hits['rbh'] == 'yes').astype(int))
    hits = hits.sort_values(['ref_key', '_rbh', 'bitscore', 'hit_rank', 'query_gene'],
                            ascending=[True, False, False, True, True], kind='mergesort')
    n_before = hits.groupby('ref_key').size()
    hits = hits.groupby('ref_key').head(args.max_copies).drop(columns='_rbh')
    capped = n_before[n_before > args.max_copies]
    if len(capped):
        print(f'  capped to {args.max_copies} copies: '
              + ', '.join(f'{k}({v})' for k, v in capped.items()))
    merged = ref.merge(hits.drop(columns='ref_gene'), on='ref_key')
    out = pd.DataFrame({
        'gene_id': merged['query_gene'],
        'symbol': merged['symbol'],
        'cell_type': merged['cell_type'],
        'kind': merged['kind'],
        'tissue': merged['tissue'],
        'evidence': merged['evidence'],
        'confidence': merged['confidence'],
        'ref_species': merged['ref_species'],
        'ref_gene': merged['ref_gene'],
        'hit_rank': merged['hit_rank'],
        'pident': merged['pident'].round(1),
        'rbh': merged['rbh'],
        'via': merged['via'],
        'basis': merged['basis'],
        'source': merged['source'],
    })
    # A target gene can map to a locus listed for two cell types; keep both, drop exact repeats
    out = out.drop_duplicates(['gene_id', 'cell_type', 'ref_gene']).sort_values(
        ['cell_type', 'symbol', 'hit_rank', 'pident'], ascending=[True, True, True, False], kind='mergesort')
    out.to_csv(args.out_markers, sep='\t', index=False)
    summarize(out, ref, f'-> {args.out_markers}')

    missing = ref[~ref['ref_key'].isin(set(merged['ref_key']))].drop_duplicates(['ref_key', 'cell_type'])
    if len(missing):
        print(f"  WARN {missing['ref_key'].nunique()} reference markers have no target gene with "
              f"rank<={args.max_marker_rank} hit, by cell type:")
        for ct, g in missing.groupby('cell_type'):
            print(f"    {ct:24s} " + ', '.join(f"{r.symbol}({r.ref_gene}, {r.evidence})" for r in g.itertuples()))
        empty = sorted(set(ref['cell_type']) - set(out['cell_type']))
        if empty:
            print('  WARN cell types left with NO mapped marker: ' + ', '.join(empty)
                  + '. A call of "absent" for these is not supported by the markers.')


if __name__ == '__main__':
    main()
