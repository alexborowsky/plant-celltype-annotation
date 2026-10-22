#!/usr/bin/env python3
"""Map reference marker genes (any reference species) onto a target species.

Reference tables live in references/markers/ (one per reference species/tissue).
Rows carry trait tags: `requires` (the target must have all of them) and
`excludes` (the target must have none of them). Pass the target's traits with
--target-traits, e.g. `grass C4` for maize, `eudicot Solanaceae` for tomato,
`liverwort` / `moss` for bryophytes, `gymnosperm` (or `conifer`), `lycophyte`, `fern`.

Modes:
  BLAST mode (default)  --blast target_vs_reference.tsv [--blast-reverse ...]
                        Target genes whose best hit is a marker locus become markers.
  --orthology TABLE     Orthology table (e.g. OrthoFinder per-gene annotation) instead of BLAST.
                        Symbols/descriptions are read from the table's <prefix>_symbols /
                        <prefix>_descriptions columns when present (--orth-symbol-col/--orth-desc-col).
                        Outputs carry `relationship` (1:1, many:1 ...) and an empty `pident`.
  --no-blast            The reference IDs are already target IDs (e.g. sorghum
                        markers on sorghum data); rows are copied after filtering.

Gene IDs:
  --target-genes FILE / --h5ad FILE   the target's gene IDs (var_names; the h5ad is read with h5py,
                        var names only). Prints how many reference (--no-blast) or query (homology) IDs
                        are found there and warns when < 50%.
  --match-unversioned   match IDs after stripping a version/transcript suffix (.1, .3.1, .t1, .p, .1.p,
                        .v2.1, -mRNA-1, _T001, -RA) on both sides; with --target-genes/--h5ad the output
                        uses the target's own (versioned) IDs.
  --id-rewrite 'FROM=>TO'      regex rewrite of the marker-table IDs (repeatable), e.g. 'Glyma\\.=>GLYMA_'.
  --query-rewrite 'FROM=>TO'   the same for target/query IDs of the BLAST/orthology table, e.g. '_evm=>-evm'.

Paralog rescue (BLAST mode with --blast-reverse): a target gene that is a marker locus's reverse best
hit, but whose own best hit is another reference paralog, is kept when
  (a) bitscore(gene, marker) >= --rescue-min-ratio x bitscore(gene, its best hit)   [default 0.85], or
  (b) its identity to the marker over the aligned residues (indels ignored) >= --rescue-min-pident
      [default 90; close species, e.g. maize PPDK -> sorghum at ratio 0.84 because the maize model is shorter].

Outputs:
  --out-gene-map   (BLAST/orthology mode) one row per (target gene, distinct reference locus),
                   ranked by bitscore; used to annotate DE genes with homolog symbols.
  --out-markers    target marker table (gene_id, symbol, cell_type, evidence, basis, ..., relationship).

Warnings worth reading: rows dropped by trait tags, reference markers without a target hit,
cell types left without markers, and target genes listed as markers of several cell types whose
names are not aliases (references/markers/celltype_aliases.tsv), e.g. Seed_Coat_Endothelium vs Endothelium.

Lightweight (no scanpy); fine to run in a small job.
"""

import argparse
import os
import re
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

LEVELS = {'low': 0, 'medium': 1, 'high': 2}
# Traits implied by more specific ones, so `--target-traits Sorghum` is enough.
# Lineage traits used by lineage_tags.py: bryophyte (liverwort/moss/hornwort), lycophyte, fern,
# gymnosperm (conifer), angiosperm (eudicot/monocot/magnoliid). None of them implies bryophyte.
IMPLIES = {
    'Sorghum': {'grass', 'C4'},
    'grass': {'monocot'},
    'Triticeae': {'grass', 'C3'},
    'Brassicaceae': {'eudicot', 'Brassicales'},
    'Solanaceae': {'eudicot'},
    'Oryza': {'grass', 'C3'},
    'Fabaceae': {'eudicot'},
    'Phaseoleae': {'Fabaceae'},
    'Gossypium': {'eudicot'},
    'Rosaceae': {'eudicot'},
    'Apocynaceae': {'eudicot'},
    'Cucurbitaceae': {'eudicot'},
    'Euphorbiaceae': {'eudicot'},
    'Capsicum': {'Solanaceae', 'eudicot'},
    'Brassicales': {'eudicot'},
    'eudicot': {'angiosperm'},
    'monocot': {'angiosperm'},
    'magnoliid': {'angiosperm'},
    'angiosperm': {'tracheophyte'},
    'conifer': {'gymnosperm'},
    'gymnosperm': {'tracheophyte'},
    'fern': {'tracheophyte'},
    'lycophyte': {'tracheophyte'},
    'liverwort': {'bryophyte'},
    'moss': {'bryophyte'},
    'hornwort': {'bryophyte'},
}
REF_COLS = ['ref_species', 'tissue', 'cell_type', 'ref_gene', 'symbol', 'kind', 'evidence',
            'confidence', 'requires', 'excludes', 'basis', 'source']
# Version / transcript / protein suffixes stripped by --match-unversioned (one suffix group, anchored):
# .1  .3.1  .1.p  .v2.1  .t1  .t1.2  .p  .p1  -mRNA-1  _mRNA  .mRNA1  _T001  _P001  -RA  -PA
VERSION_SUFFIX = (r'(?:\.v?\d+(?:\.\d+)*(?:\.p)?|\.t\d+(?:\.\d+)?|\.p\d*|[-_.]mRNA(?:-?\d+)?'
                  r'|_[TP]\d{3}|-[RP][A-Z])$')
ALIAS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references', 'markers',
                          'celltype_aliases.tsv')


# ----------------------------------------------------------------------------------------- IDs
def parse_rewrites(rules, flag):
    out = []
    for r in rules or []:
        if '=>' not in r:
            sys.exit(f"{flag} {r!r}: expected 'FROM=>TO' (regex => replacement)")
        a, b = r.split('=>', 1)
        try:
            out.append((re.compile(a), b))
        except re.error as e:
            sys.exit(f'{flag} {r!r}: bad regex ({e})')
    return out


def apply_rewrites(s, rules):
    """Apply (compiled regex, replacement) rules in order to a string Series."""
    for rx, rep in rules:
        s = s.map(lambda x, rx=rx, rep=rep: rx.sub(rep, x))
    return s


def unversion(x, rx=VERSION_SUFFIX):
    return re.sub(rx, '', x)


def read_target_genes(target_genes=None, h5ad=None):
    """Target gene IDs from a list file (first column) and/or an h5ad's var (and raw/var) index."""
    if not target_genes and not h5ad:
        return None
    genes = set()
    if target_genes:
        with open(target_genes) as fh:
            for ln in fh:
                f = ln.strip().split('\t')[0].split(',')[0].strip()
                if f and not f.startswith('#'):
                    genes.add(f)
    if h5ad:
        import h5py
        with h5py.File(h5ad, 'r') as f:
            for grp in ('var', 'raw/var'):
                if grp not in f:
                    continue
                g = f[grp]
                if isinstance(g, h5py.Dataset):  # very old anndata: structured array
                    names = g['index'][:]
                else:
                    idx = g.attrs.get('_index', '_index')
                    idx = idx.decode() if isinstance(idx, bytes) else idx
                    if idx not in g:
                        continue
                    names = g[idx][:]
                genes.update(n.decode() if isinstance(n, bytes) else str(n) for n in names)
    print(f'  target gene list: {len(genes):,} IDs')
    return genes


def match_ids(ids, targets, unversioned):
    """Map IDs to target IDs: exact, then case-insensitive, then (if unversioned) by the unversioned base.

    Returns dict id -> sorted list of target IDs (several when several target versions share a base),
    plus the number of ids matched only through an ambiguous base.
    """
    exact = set(targets)
    upper = defaultdict(list)
    base = defaultdict(list)
    for t in targets:
        upper[t.upper()].append(t)
        if unversioned:
            base[unversion(t).upper()].append(t)
    out, n_amb = {}, 0
    for i in set(ids):
        if i in exact:
            out[i] = [i]
        elif i.upper() in upper:
            out[i] = sorted(upper[i.upper()])
        elif unversioned:
            b = unversion(i).upper()
            if b in upper:
                out[i] = sorted(upper[b])
            elif b in base:
                out[i] = sorted(base[b])
                n_amb += len(base[b]) > 1
    return out, n_amb


def report_match(label, ids, mapping, targets, hint):
    ids = sorted(set(ids))
    n = len(ids)
    k = sum(i in mapping for i in ids)
    rate = k / n if n else 0
    print(f'  {label}: {k:,}/{n:,} ({rate:.0%}) found in the target gene list')
    if n and rate < 0.5:
        miss = [i for i in ids if i not in mapping][:4]
        ex = sorted(targets)[:4]
        print(f'  WARN only {rate:.0%} of {label} match the target genes. Unmatched examples: {", ".join(miss)}; '
              f'target examples: {", ".join(ex)}. {hint}')
    return rate


def explode_ids(df, col, mapping):
    """Replace df[col] by its mapped target IDs (one row per target ID); unmapped rows keep their ID."""
    new = df[col].map(lambda x: mapping.get(x, [x]))
    df = df.assign(**{col: new}).explode(col)
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------------- readers
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
            pident, length = float(f[2]), float(f[3])
            # Identity over the aligned residues, ignoring indels: matches / shorter aligned span.
            # Differs from pident when one gene model is truncated or has an extra exon.
            try:
                span = min(abs(int(f[7]) - int(f[6])) + 1, abs(int(f[9]) - int(f[8])) + 1)
                ident_nogap = min(100.0, pident * length / span) if span > 0 else pident
            except ValueError:
                ident_nogap = pident
            rows.append((q, s, pident, float(f[10]), float(f[11]), symbol, desc, ident_nogap))
    df = pd.DataFrame(rows, columns=['query_gene', 'ref_gene', 'pident', 'evalue',
                                     'bitscore', 'ref_symbol', 'ref_description', 'ident_nogap'])
    n0 = len(df)
    df = df[(df['evalue'] <= max_evalue) & (df['pident'] >= min_pident)]
    print(f"  {path}: {n0:,} HSPs, {len(df):,} pass evalue<={max_evalue} pident>={min_pident}")
    return df


def _split_parallel(val, n, sep):
    """Split a per-gene list column into n items, or None when the count does not match."""
    if n == 1:
        return [val.strip()]
    parts = [p.strip() for p in re.split(sep, val)] if val.strip() else []
    return parts if len(parts) == n else None


def read_orthology(path, q_col, r_col, rel_col, q_regex, sym_col=None, desc_col=None, q_rules=()):
    """Orthology table (e.g. OrthoFinder per-gene annotation) -> gene-map-like hits.

    Every listed orthologue is a rank-1 hit (orthologues are not ranked); 1:1 pairs are marked RBH.
    pident/bitscore are NaN (written empty), so outputs never show a made-up identity; `relationship`
    carries the orthology relationship. Symbols/descriptions come from sym_col/desc_col when present:
    symbols comma/semicolon-separated, descriptions ' | '-separated, in the orthologue order. Rows whose
    item count differs from the orthologue count are not used for symbols (ambiguous order).
    """
    t = pd.read_csv(path, sep='\t', dtype=str).fillna('')
    for c in (q_col, r_col):
        if c not in t.columns:
            sys.exit(f'--orthology: column {c} not in {path} (columns: {list(t.columns)[:20]})')
    for c, flag in ((sym_col, '--orth-symbol-col'), (desc_col, '--orth-desc-col')):
        if c and c not in t.columns:
            sys.exit(f'{flag}: column {c} not in {path}')
    rows = []
    sym, desc = {}, {}
    n_mismatch = 0
    q_re = re.compile(q_regex) if q_regex else None
    rels = t[rel_col] if rel_col in t.columns else pd.Series([''] * len(t))
    syms = t[sym_col] if sym_col else pd.Series([''] * len(t))
    descs = t[desc_col] if desc_col else pd.Series([''] * len(t))
    for q, refs, rel, s, d in zip(t[q_col], t[r_col], rels, syms, descs):
        q = q_re.sub('', q) if q_re else q
        loci = [re.sub(r'\.\d+$', '', r) for r in re.split(r'[,;\s]+', refs) if r]
        for r in loci:
            rows.append((q, r, rel))
        if not loci:
            continue
        if sym_col and s.strip():
            ss = _split_parallel(s, len(loci), r'[,;]')
            if ss is None:
                n_mismatch += 1
            else:
                for r, x in zip(loci, ss):
                    if x and x.upper() != r.upper() and r not in sym:
                        sym[r] = x
        if desc_col and d.strip():
            dd = _split_parallel(d, len(loci), r'\s\|\s')
            if dd is not None:
                for r, x in zip(loci, dd):
                    if x and r not in desc:
                        desc[r] = x
    df = pd.DataFrame(rows, columns=['query_gene', 'ref_gene', 'relationship']).drop_duplicates(['query_gene', 'ref_gene'])
    if q_rules:
        df['query_gene'] = apply_rewrites(df['query_gene'], q_rules)
    df['hit_rank'] = 1
    df['pident'] = np.nan; df['evalue'] = np.nan; df['bitscore'] = np.nan; df['ident_nogap'] = np.nan
    df['ref_symbol'] = df['ref_gene'].map(sym).fillna('')
    df['ref_description'] = df['ref_gene'].map(desc).fillna('')
    df['rbh'] = np.where(df['relationship'].str.replace(' ', '') == '1:1', 'yes', 'no')
    print(f"  {path}: {df['query_gene'].nunique():,} genes with {len(df):,} orthologue pairs "
          f"({(df['rbh'] == 'yes').sum():,} 1:1)")
    if sym_col:
        print(f"  symbols from {sym_col}: {len(sym):,} loci named"
              + (f"; {n_mismatch:,} rows skipped (symbol count != orthologue count)" if n_mismatch else ''))
    if desc_col:
        print(f"  descriptions from {desc_col}: {len(desc):,} loci")
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


def load_aliases(path):
    """alias -> canonical (lower-case keys) from celltype_aliases.tsv; empty dict when absent."""
    if not path or not os.path.exists(path):
        return {}
    try:
        a = pd.read_csv(path, sep='\t', dtype=str, comment='#').fillna('')
    except Exception as e:  # noqa: BLE001
        print(f'  WARN could not read {path}: {e}')
        return {}
    if not {'alias', 'canonical'} <= set(a.columns):
        return {}
    return {x.strip().lower(): y.strip() for x, y in zip(a['alias'], a['canonical']) if x.strip() and y.strip()}


def warn_multi_celltype(out, aliases, max_lines=15):
    """Warn when one target gene is a marker of several cell types whose names are not aliases.

    State rows (kind=state: cell cycle, stress) are ignored. Pairs where one name's tokens contain
    the other's (Seed_Coat_Endothelium vs Endothelium) are flagged as possible fragmented names.
    """
    t = out[out['kind'].astype(str) != 'state'] if 'kind' in out.columns else out
    if t.empty:
        return
    canon = t['cell_type'].map(lambda c: aliases.get(str(c).lower(), c))
    t = t.assign(_ct=canon, _lab=t['gene_id'].astype(str) + '(' + t['symbol'].astype(str) + ')')
    groups = (t.groupby('gene_id')
              .agg(cts=('_ct', lambda s: tuple(sorted(set(s)))),
                   sym=('_lab', lambda s: sorted(set(s))[0])))
    multi = groups[groups['cts'].map(len) > 1]
    if multi.empty:
        return

    def toks(c):
        return set(str(c).lower().split('_'))

    def fragmented(cts):
        return any(toks(a) < toks(b) or toks(b) < toks(a) for i, a in enumerate(cts) for b in cts[i + 1:])

    combos = multi.groupby('cts')['sym'].agg(['size', lambda s: ', '.join(list(s)[:3])])
    combos.columns = ['n', 'examples']
    combos['frag'] = [fragmented(c) for c in combos.index]
    combos = combos.sort_values(['frag', 'n'], ascending=[False, False])
    print(f"  WARN {len(multi)} target genes are markers of more than one cell type ({len(combos)} combinations; "
          f"names mapped through {'celltype_aliases.tsv' if aliases else 'no alias table'}). Shared markers cannot "
          f"separate these types; '*' = one name contains the other: a subtype, or a fragmented name to merge "
          f"via celltype_aliases.tsv):")
    for cts, r in combos.head(max_lines).iterrows():
        print(f"    {'*' if r.frag else ' '} {' + '.join(cts)}: {r.n} genes ({r.examples})")
    if len(combos) > max_lines:
        print(f"    ... {len(combos) - max_lines} more combinations")


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


def load_reference(paths, tissues, min_conf, traits, ref_strip, id_column='ref_gene', id_rules=(),
                   unversioned=False, return_dropped=False, verbose=True):
    """Read and filter marker tables. ref_key = upper-case (optionally unversioned) ID used for matching."""
    log = print if verbose else (lambda *a, **k: None)
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
            log(f"  {int(empty.sum())} rows have no {id_column} and are dropped: "
                + ', '.join(ref.loc[empty, 'ref_gene'] + '(' + ref.loc[empty, 'symbol'] + ')'))
        ref = ref[~empty].copy()
        ref['ref_gene'] = ref[id_column]
    if id_rules:
        before = ref['ref_gene'].copy()
        ref['ref_gene'] = apply_rewrites(ref['ref_gene'], id_rules)
        log(f"  --id-rewrite changed {int((before != ref['ref_gene']).sum())}/{len(ref)} reference IDs"
            + (f" (e.g. {before[before != ref['ref_gene']].iloc[0]} -> "
               f"{ref['ref_gene'][before != ref['ref_gene']].iloc[0]})" if (before != ref['ref_gene']).any() else ''))
    if ref_strip:
        ref['ref_gene'] = ref['ref_gene'].str.replace(ref_strip, '', regex=True)
    ref['ref_key'] = (ref['ref_gene'].map(unversion) if unversioned else ref['ref_gene']).str.upper()
    n0 = len(ref)
    if tissues:
        # Tissue values can be compound (leaf_stem_phloem, ovule/seed): match on any token.
        want = {t.lower() for t in tissues}
        tok = ref['tissue'].str.lower().map(lambda s: set(re.split(r'[_,;/ ]+', s)) | {s})
        ref = ref[tok.map(lambda t: bool(t & want))]
    ref = ref[ref['confidence'].map(LEVELS).fillna(0) >= LEVELS[min_conf]]
    log(f"  {n0} reference rows; {len(ref)} after tissue/confidence filters")

    if traits is None:
        log('  WARN no --target-traits given: keeping only rows without `requires` tags; '
            '`excludes` tags are not checked')
        keep = ref['requires'].map(lambda s: not tags(s))
    else:
        tt = expand_traits(traits)
        log(f"  target traits: {sorted(tt)}")
        keep = [tags(r) <= tt and not (tags(e) & tt) for r, e in zip(ref['requires'], ref['excludes'])]
        keep = pd.Series(keep, index=ref.index, dtype=bool)
    dropped = ref[~keep]
    if len(dropped):
        uniq = dropped.drop_duplicates(['cell_type', 'symbol'])
        log(f"  {len(dropped)} rows ({len(uniq)} unique cell type x marker) not applicable to this target "
            f"(requires/excludes):")
        for r in uniq.itertuples():
            why = f"requires={r.requires}" if r.requires else f"excludes={r.excludes}"
            log(f"    {r.cell_type:22s} {r.symbol:14s} {why}")
    ref = ref[keep]
    if ref.empty:
        sys.exit('No reference rows left after filtering.')
    return (ref, dropped) if return_dropped else ref


def summarize(out, ref, note):
    print(f"  {len(out)} target marker rows for {out['ref_gene'].nunique()}/{ref['ref_gene'].nunique()} "
          f"reference loci {note}")
    by = out.groupby('cell_type').agg(n_rows=('gene_id', 'size'),
                                     n_function=('evidence', lambda e: int((e == 'function').sum())))
    print('  per cell type (rows / function-evidence rows):')
    for ct, r in by.iterrows():
        print(f"    {ct:24s} {r.n_rows:4d} / {r.n_function}")


ID_HINT = ("Try --match-unversioned (version/transcript suffixes such as .1, .t1, -mRNA-1), "
           "--id-rewrite 'FROM=>TO' (e.g. 'Glyma\\.=>GLYMA_'), or --id-column alt_id.")
QUERY_HINT = ("Check --query-strip-regex, --query-rewrite 'FROM=>TO' (e.g. '_evm=>-evm') or "
              "--match-unversioned; otherwise the markers will be reported as missing from the data.")


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
    p.add_argument('--query-rewrite', action='append', default=[], metavar="'FROM=>TO'",
                   help="regex rewrite of target IDs in the BLAST/orthology input (repeatable, after "
                        "--query-strip-regex), e.g. '_evm=>-evm' when var_names use '-' in merged-locus IDs")
    p.add_argument('--ref-strip-regex', default=None,
                   help=r"regex removed from reference IDs (default '\.\d+$' in BLAST mode, none with --no-blast)")
    p.add_argument('--id-rewrite', action='append', default=[], metavar="'FROM=>TO'",
                   help="regex rewrite of marker-table IDs before matching (repeatable, applied in order, "
                        "before --ref-strip-regex), e.g. 'Glyma\\.=>GLYMA_' for Ensembl-style soybean IDs")
    p.add_argument('--match-unversioned', action='store_true',
                   help='match IDs after stripping version/transcript suffixes (.1 .3.1 .t1 .p .1.p .v2.1 -mRNA-1 '
                        '_T001 -RA) on both sides. With --no-blast and --target-genes/--h5ad, gene_id becomes '
                        'the matching target ID (e.g. Solyc01g005000 -> Solyc01g005000.3)')
    p.add_argument('--target-genes', default=None,
                   help='file with the target gene IDs (var_names), one per line (first column); used to '
                        'report and fix ID mismatches')
    p.add_argument('--h5ad', default=None,
                   help='read the target gene IDs from this h5ad (var and raw/var index only, via h5py)')
    p.add_argument('--ref-annotation', default=None,
                   help='optional TSV: ref_gene<TAB>symbol<TAB>description (overrides BLAST/orthology symbols '
                        'where it has a value)')
    p.add_argument('--max-hits', type=int, default=5, help='distinct reference loci kept per target gene')
    p.add_argument('--max-evalue', type=float, default=1e-5)
    p.add_argument('--min-pident', type=float, default=0.0)
    p.add_argument('--reference', nargs='+', default=None,
                   help='one or more marker tables from references/markers/ (same reference species)')
    p.add_argument('--target-traits', nargs='*', default=None,
                   help='traits of the target species, e.g. eudicot Solanaceae | grass C4 | Sorghum | liverwort | '
                        'moss | gymnosperm | lycophyte | fern (see IMPLIES)')
    p.add_argument('--tissue', action='append', default=None,
                   help="tissue(s) to keep (repeatable, e.g. --tissue leaf --tissue any). Default: all")
    p.add_argument('--min-confidence', choices=list(LEVELS), default='low')
    p.add_argument('--max-marker-rank', type=int, default=1,
                   help='target gene counts as a marker if the marker locus is within its top-N hits (default 1)')
    p.add_argument('--rescue-min-ratio', type=float, default=0.85,
                   help='reverse-best rescue if bitscore(gene, marker) >= this x bitscore(gene, its best hit)')
    p.add_argument('--rescue-min-pident', type=float, default=90.0,
                   help='... or if the identity between gene and marker over aligned residues (indels ignored) '
                        'is >= this (close species; default 90; set >100 to disable)')
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
    p.add_argument('--orth-symbol-col', default=None,
                   help="column with the orthologues' symbols (default: --orth-ref-col with 'orthologues' -> "
                        "'symbols', if that column exists; 'none' to disable)")
    p.add_argument('--orth-desc-col', default=None,
                   help="column with the orthologues' descriptions, ' | '-separated (default: 'orthologues' -> "
                        "'descriptions', if present; 'none' to disable)")
    p.add_argument('--celltype-aliases', default=ALIAS_FILE,
                   help='alias table (alias, canonical) used by the multi-cell-type marker warning '
                        '(default: references/markers/celltype_aliases.tsv, if present)')
    p.add_argument('--out-gene-map', default=None)
    p.add_argument('--out-markers', default=None)
    args = p.parse_args()

    id_rules = parse_rewrites(args.id_rewrite, '--id-rewrite')
    q_rules = parse_rewrites(args.query_rewrite, '--query-rewrite')
    aliases = load_aliases(args.celltype_aliases)
    targets = read_target_genes(args.target_genes, args.h5ad)

    if args.no_blast:
        if not (args.reference and args.out_markers):
            sys.exit('--no-blast needs --reference and --out-markers')
        print('[1] Same-species mode (no homology mapping)')
        ref = load_reference(args.reference, args.tissue, args.min_confidence, args.target_traits,
                             args.ref_strip_regex, args.id_column, id_rules)
        warn_paralog_families(ref)
        out = pd.DataFrame({
            'gene_id': ref['ref_gene'], 'symbol': ref['symbol'], 'cell_type': ref['cell_type'],
            'kind': ref['kind'], 'tissue': ref['tissue'], 'evidence': ref['evidence'],
            'confidence': ref['confidence'], 'ref_species': ref['ref_species'],
            'ref_gene': ref['ref_gene'], 'hit_rank': 0, 'pident': 100.0, 'rbh': '', 'via': 'same_species',
            'basis': ref['basis'], 'source': ref['source'], 'relationship': '',
        })
        if targets is not None:
            mapping, n_amb = match_ids(out['gene_id'], targets, args.match_unversioned)
            report_match('reference IDs', out['gene_id'], mapping, targets, ID_HINT)
            changed = sum(1 for k, v in mapping.items() if v != [k])
            if changed:
                print(f'  {changed} reference IDs rewritten to the target\'s IDs'
                      + (' (unversioned match)' if args.match_unversioned else ' (case)')
                      + (f'; {n_amb} matched several target IDs (all kept)' if n_amb else ''))
            out = explode_ids(out, 'gene_id', mapping)
        else:
            if args.match_unversioned:
                out['gene_id'] = out['gene_id'].map(unversion)
                print('  --match-unversioned without --target-genes/--h5ad: gene_id = unversioned reference ID')
            print('  NOTE pass --h5ad or --target-genes to check that these IDs match the data\'s var_names')
        out = out.drop_duplicates(['gene_id', 'cell_type'])
        out.to_csv(args.out_markers, sep='\t', index=False)
        summarize(out, ref, f'-> {args.out_markers}')
        warn_multi_celltype(out, aliases)
        return

    if not (args.blast or args.orthology) or not args.out_gene_map:
        sys.exit('Homology mode needs --blast (or --orthology) and --out-gene-map (or use --no-blast)')
    ref_strip = r'\.\d+$' if args.ref_strip_regex is None else args.ref_strip_regex

    if args.orthology:
        print('[1] Reading orthology table')
        cols = set(pd.read_csv(args.orthology, sep='\t', nrows=0).columns)

        def derive(opt, word):
            if opt is not None:
                return None if opt.lower() == 'none' else opt
            c = args.orth_ref_col.replace('orthologues', word)
            return c if c != args.orth_ref_col and c in cols else None
        sym_col, desc_col = derive(args.orth_symbol_col, 'symbols'), derive(args.orth_desc_col, 'descriptions')
        fwd = read_orthology(args.orthology, args.orth_query_col, args.orth_ref_col, args.orth_rel_col,
                             args.query_strip_regex, sym_col, desc_col, q_rules)
        rev = None
    else:
        print('[1] Reading forward BLAST')
        fwd = read_blast(args.blast, args.query_strip_regex, ref_strip, args.max_evalue, args.min_pident)
        if fwd.empty:
            sys.exit('No BLAST hits passed filters.')
        if q_rules:
            fwd['query_gene'] = apply_rewrites(fwd['query_gene'], q_rules)
        rev = None
        if args.blast_reverse:
            print('[1b] Reading reverse BLAST for reciprocal best hits')
            # reverse: query = reference, subject = target, so swap the regexes
            rev = read_blast(args.blast_reverse, ref_strip, args.query_strip_regex,
                             args.max_evalue, args.min_pident)
            if q_rules:
                rev['ref_gene'] = apply_rewrites(rev['ref_gene'], q_rules)
    if targets is not None:
        mapping, n_amb = match_ids(fwd['query_gene'], targets, args.match_unversioned)
        report_match('target (query) IDs of the homology input', fwd['query_gene'], mapping, targets, QUERY_HINT)
        if any(v != [k] for k, v in mapping.items()):
            print('  query IDs rewritten to the target\'s var_names'
                  + (f' ({n_amb} matched several, all kept)' if n_amb else ''))
            fwd = explode_ids(fwd, 'query_gene', mapping)
            if rev is not None:
                rev = explode_ids(rev, 'ref_gene', mapping)

    if args.orthology:
        gm = fwd.copy()
        depth = pd.Series([2])  # orthology tables list all orthologues; no depth warning
    else:
        gm = rank_hits(fwd, 'query_gene', 'ref_gene', args.max_hits)
        gm = gm.assign(relationship='')
        depth = fwd.groupby('query_gene')['ref_gene'].nunique()
    if depth.median() <= 1 and (depth > 1).mean() < 0.05:
        print(f'  WARN the BLAST file has ~1 subject per query (median {depth.median():.0f}; '
              f'{(depth > 1).mean():.1%} of queries have >1). It was probably run with -max_target_seqs 1, so '
              f'markers whose target gene best-hits a paralog are lost (often histones, PCNA, cyclins, CDKs) and '
              f'paralog rescue is impossible. Rerun with -max_target_seqs 5 (or more) and add --blast-reverse.')

    # Symbols: fill per-locus from any HSP/orthology row that carried them, then optional file
    sym = (fwd[fwd['ref_symbol'] != ''].drop_duplicates('ref_gene')
           .set_index('ref_gene')[['ref_symbol']])
    dsc = (fwd[fwd['ref_description'] != ''].drop_duplicates('ref_gene')
           .set_index('ref_gene')[['ref_description']])
    gm = gm.drop(columns=['ref_symbol', 'ref_description']).join(sym, on='ref_gene').join(dsc, on='ref_gene')
    gm[['ref_symbol', 'ref_description']] = gm[['ref_symbol', 'ref_description']].fillna('')
    if args.ref_annotation:
        ann = pd.read_csv(args.ref_annotation, sep='\t', header=None, dtype=str,
                          names=['ref_gene', 'ref_symbol', 'ref_description'], usecols=[0, 1, 2]).fillna('')
        ann['ref_symbol'] = ann['ref_symbol'].str.replace(r'^(Symbols:)?\s*no symbol available\s*$', '', regex=True)
        ann['ref_description'] = ann['ref_description'].str.replace(r'^\s*no full name available\s*$', '',
                                                                    regex=True)
        if ref_strip:
            ann['ref_gene'] = ann['ref_gene'].str.replace(ref_strip, '', regex=True)
        ann = ann.drop_duplicates('ref_gene').set_index('ref_gene')
        for c in ('ref_symbol', 'ref_description'):
            new = gm['ref_gene'].map(ann[c]).fillna('')
            gm[c] = new.where(new != '', gm[c])

    if not args.orthology:
        gm['rbh'] = ''
    rev_best = {}
    if rev is not None:
        rev = rank_hits(rev, 'query_gene', 'ref_gene', 1)  # columns: ref locus in query_gene
        rev_best = dict(zip(rev['query_gene'].str.upper(), rev['ref_gene']))
        gm['rbh'] = [
            'yes' if (r == 1 and rev_best.get(ref.upper()) == q) else 'no'
            for q, ref, r in zip(gm['query_gene'], gm['ref_gene'], gm['hit_rank'])
        ]
        print(f"  RBH pairs: {(gm['rbh'] == 'yes').sum():,}")

    cols = ['query_gene', 'hit_rank', 'ref_gene', 'ref_symbol', 'ref_description',
            'pident', 'evalue', 'bitscore', 'rbh', 'relationship']
    gm = gm.sort_values(['query_gene', 'hit_rank'], kind='mergesort')
    gm[cols].to_csv(args.out_gene_map, sep='\t', index=False)
    print(f"  gene map: {gm['query_gene'].nunique():,} target genes -> {args.out_gene_map}"
          + (' (orthology: pident empty, see relationship)' if args.orthology else ''))

    if not args.reference:
        return
    if not args.out_markers:
        sys.exit('--out-markers required with --reference')

    print('[2] Mapping reference markers')
    ref, dropped = load_reference(args.reference, args.tissue, args.min_confidence, args.target_traits, ref_strip,
                                  args.id_column, id_rules, args.match_unversioned, return_dropped=True)
    warn_paralog_families(ref)
    ref_keys = set(ref['ref_key'])

    key = gm['ref_gene'].map(unversion) if args.match_unversioned else gm['ref_gene']
    gm_u = gm.assign(ref_key=key.str.upper())
    in_map = len(ref_keys & set(gm_u['ref_key']))
    print(f"  {in_map}/{len(ref_keys)} reference marker IDs occur in the gene map")
    # Distant targets (Arabidopsis -> liverwort) legitimately miss ~half; < 20% means an ID-format mismatch.
    if ref_keys and in_map / len(ref_keys) < 0.2:
        print(f"  WARN fewer than 20% of the marker-table IDs occur in the gene map (e.g. "
              f"{', '.join(sorted(ref_keys - set(gm_u['ref_key']))[:3])} vs gene-map IDs like "
              f"{', '.join(gm_u['ref_gene'].iloc[:3])}). {ID_HINT}")
    gm_u = gm_u[gm_u['ref_key'].isin(ref_keys)]
    hits = gm_u[gm_u['hit_rank'] <= args.max_marker_rank].assign(via='orthology' if args.orthology else 'forward')
    if rev_best:
        # Rescue paralog misses: the target gene that is the marker locus's own best hit,
        # even if that gene's best hit is a different paralog (e.g. PCNA1 vs PCNA2).
        rb = {(unversion(k) if args.match_unversioned else k).upper(): v
              for k, v in zip(rev['query_gene'], rev['ref_gene'])}
        pairs = pd.DataFrame({'ref_key': list(rb), 'query_gene': list(rb.values())})
        pairs = pairs[pairs['ref_key'].isin(ref_keys)]
        rescue = pairs.merge(gm_u, on=['ref_key', 'query_gene'], how='inner')
        rescue = rescue[rescue['hit_rank'] > args.max_marker_rank].assign(via='reverse_best')
        # Rule (a): near-equivalent paralogs (PCNA1/2, SWEET11/12: ratio ~0.9-1.0). When the target
        # lacks a true ortholog, the marker's best hit is a different subfamily (SUC2 -> grass SUT4-type
        # at 0.78), and the gene's own best hit scores clearly higher.
        # Rule (b): close species. maize C4 PPDK -> sorghum PPDK has ratio 0.84 only because the maize
        # gene model is shorter; over the aligned residues the two are 92% identical. Distant
        # subfamilies (Arabidopsis -> grass) never reach 90%.
        # tied hits share rank 1, so take the max per gene
        best_bits = gm.loc[gm['hit_rank'] == 1].groupby('query_gene')['bitscore'].max()
        rescue = rescue.assign(ratio=rescue['bitscore'] / rescue['query_gene'].map(best_bits))
        ok_ratio = rescue['ratio'] >= args.rescue_min_ratio
        ok_ident = rescue['ident_nogap'] >= args.rescue_min_pident
        low = rescue[~ok_ratio & ~ok_ident]
        if len(low):
            print(f'  NOT rescued (bitscore ratio < {args.rescue_min_ratio} and identity < '
                  f'{args.rescue_min_pident:g}%, likely a different subfamily): '
                  + ', '.join(f'{q}->{r} ({x:.2f}, {i:.0f}%)' for q, r, x, i in
                              zip(low['query_gene'], low['ref_gene'], low['ratio'], low['ident_nogap'])))
        by_ratio = rescue[ok_ratio]
        by_ident = rescue[~ok_ratio & ok_ident]
        if len(by_ratio):
            print(f'  rescued {len(by_ratio)} marker genes via reverse best hit (rule: bitscore ratio >= '
                  f'{args.rescue_min_ratio}): '
                  + ', '.join(f'{q}->{r}' for q, r in zip(by_ratio['query_gene'], by_ratio['ref_gene'])))
        if len(by_ident):
            print(f'  rescued {len(by_ident)} marker genes via reverse best hit (rule: identity >= '
                  f'{args.rescue_min_pident:g}% over aligned residues, ratio below {args.rescue_min_ratio}): '
                  + ', '.join(f'{q}->{r} ({x:.2f}, {i:.0f}%)' for q, r, x, i in
                              zip(by_ident['query_gene'], by_ident['ref_gene'], by_ident['ratio'],
                                  by_ident['ident_nogap'])))
        rescue = rescue[ok_ratio | ok_ident].drop(columns='ratio')
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
        'pident': merged['pident'].round(1),   # empty (NaN) in orthology mode; see relationship
        'rbh': merged['rbh'],
        'via': merged['via'],
        'basis': merged['basis'],
        'source': merged['source'],
        'relationship': merged['relationship'].fillna(''),
    })
    # A target gene can map to a locus listed for two cell types; keep both, drop exact repeats
    out = out.drop_duplicates(['gene_id', 'cell_type', 'ref_gene']).sort_values(
        ['cell_type', 'symbol', 'hit_rank', 'pident'], ascending=[True, True, True, False], kind='mergesort')
    out.to_csv(args.out_markers, sep='\t', index=False)
    summarize(out, ref, f'-> {args.out_markers}')
    if targets is not None:
        found = out['gene_id'].isin(targets).mean() if len(out) else 0
        print(f'  {found:.0%} of mapped marker genes are in the target gene list')

    missing = ref[~ref['ref_key'].isin(set(merged['ref_key']))].drop_duplicates(['ref_key', 'cell_type'])
    dropped_keys = set(dropped['ref_key']) if len(dropped) else set()
    if len(missing):
        print(f"  WARN {missing['ref_key'].nunique()} reference markers have no target gene with "
              f"rank<={args.max_marker_rank} hit, by cell type ('+' = another row of this gene was excluded "
              f"by a lineage tag: the tables disagree on tags):")
        for ct, g in missing.groupby('cell_type'):
            print(f"    {ct:24s} " + ', '.join(f"{r.symbol}({r.ref_gene}, {r.evidence})"
                                               + ('+' if r.ref_key in dropped_keys else '') for r in g.itertuples()))
        empty = sorted(set(ref['cell_type']) - set(out['cell_type']))
        if empty:
            excl = set(dropped['cell_type']) if len(dropped) else set()
            print('  WARN cell types left with NO mapped marker: '
                  + ', '.join(c + (' (other rows excluded by lineage tags)' if c in excl else '') for c in empty)
                  + '. A call of "absent" for these is not supported by the markers.')
    warn_multi_celltype(out, aliases)


if __name__ == '__main__':
    main()
