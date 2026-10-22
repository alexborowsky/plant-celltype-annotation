#!/usr/bin/env python3
"""Regression test for lineage tags and ID matching in map_markers.py.

Checks, on the shipped marker tables (references/markers/**.tsv, except source/):
  1. with --target-traits liverwort (and moss), no angiosperm/seed-plant/vascular-only cell type
     (SAM zones, rib meristem, shoot meristem, primordia, organ boundary, stem-cell niche, pavement,
     trichome, sperm, endothecium, septum, tapetum, flowers, seeds, endosperm, vasculature, roots...)
     from a non-bryophyte reference survives map_markers' trait filter;
  2. Dividing_cells and Epidermis rows (and Protoderm) still survive for liverworts;
  3. Arabidopsis SULTR2;1/SULTR2;2 rows require Brassicaceae;
  4. gymnosperm / fern / lycophyte targets lose flower, endosperm, seed-coat and companion-cell rows
     (and fern/lycophyte lose SAM zonation) but keep xylem and roots;
  5. lineage_tags.py is idempotent on the shipped tables (nothing left to tag);
  6. --match-unversioned / --id-rewrite helpers match Solyc and Glyma style IDs.

Usage: python tests/test_lineage_tags.py [MARKERS_DIR]   (default: the skill's references/markers;
       exit code 1 on failure; < 10 s, no scanpy)
"""
import contextlib
import glob
import io
import os
import re
import sys

import pandas as pd

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, 'scripts'))
import lineage_tags as LT  # noqa: E402
import map_markers as MM  # noqa: E402

MARKERS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SKILL, 'references', 'markers')
TABLES = sorted(p for p in glob.glob(os.path.join(MARKERS, '**', '*.tsv'), recursive=True)
                if os.sep + 'source' + os.sep not in p and not p.endswith('celltype_aliases.tsv'))
BRYO_ONLY_ABSENT = re.compile(
    r'^SAM_|Rib_Meristem|Shoot_Meristem|Shoot_Apical_Meristem|Lateral_Organ_Primordium|Leaf_Primordium|'
    r'Stem_Cell_Niche|Organ_Boundary|Organizing_Center|Meristem_Epidermis|Pavement|Trichome|Sperm_Cell|'
    r'Endothecium|Septum|Tapetum|Petal|Sepal|Stamen|Carpel|Pollen|Ovule|Nucell|Integument|Seed_Coat|'
    r'Endosperm|Aleurone|Embryo|Suspensor|Xylem|Phloem|Procambium|Sieve|Companion|Pericycle|Endodermis|'
    r'Root|Columella|Quiescent|Trichoblast|Guard|Stomat|Bundle_Sheath|Cambium|Periderm|Phellem|Hydathode', re.I)
ANGIO_ONLY = re.compile(r'Petal|Sepal|Stamen|Carpel|Anther|Endothecium|Septum|Endosperm|Aleurone|Seed_Coat|'
                        r'Synergid|Central_Cell|Phloem_Companion|Exocarp|Mesocarp|Endocarp|Lodicule', re.I)
SEED_ONLY = re.compile(r'^SAM_|Rib_Meristem|Organizing_Center|Pollen|Sperm_Cell|Ovule|Embryo|(?<!Pro)Cambium|Periderm',
                       re.I)

failures = []


def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        failures.append(msg)


def surviving(traits):
    """All rows of all shipped tables that pass map_markers' trait filter for these traits."""
    frames = []
    for p in TABLES:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                ref = MM.load_reference([p], None, 'low', traits, None, verbose=False)
        except SystemExit:  # no rows left for this table
            continue
        frames.append(ref.assign(table=os.path.relpath(p, MARKERS)))
    return pd.concat(frames, ignore_index=True)


def lineage(sp):
    return LT.species_lineage(str(sp)) or 'angiosperm'


def bad_rows(df, rx, allowed_lineages):
    hit = df[df['cell_type'].str.contains(rx) & ~df['ref_species'].map(lineage).isin(allowed_lineages)]
    return hit.drop_duplicates(['table', 'cell_type'])


def show(df):
    return '; '.join(f"{r.table}:{r.cell_type}" for r in df.head(12).itertuples())


# 1-2. bryophytes
for trait in ('liverwort', 'moss'):
    s = surviving([trait])
    b = bad_rows(s, BRYO_ONLY_ABSENT, {'bryophyte'})
    check(b.empty, f'{trait}: no angiosperm/vascular-only cell types survive' + (f' (got {show(b)})' if len(b) else ''))
    for ct in ('Dividing_cells', 'Epidermis', 'Protoderm'):
        n = int(((s['cell_type'] == ct) & (s['ref_species'] == 'arabidopsis')).sum())
        check(n > 0, f'{trait}: Arabidopsis {ct} rows survive ({n})')

# 3. SULTR2
allrows = pd.concat([pd.read_csv(p, sep='\t', dtype=str).fillna('') for p in TABLES], ignore_index=True)
sul = allrows[allrows['symbol'].str.upper().str.startswith('SULTR2;')
              & allrows['ref_species'].str.lower().isin(['arabidopsis', 'brassicaceae'])]
check(len(sul) > 0 and sul['requires'].map(lambda r: 'Brassicaceae' in MM.tags(r)).all(),
      f'SULTR2;1/2 Arabidopsis rows ({len(sul)}) require Brassicaceae')
s = surviving(['Sorghum'])
check(not s['symbol'].str.upper().str.startswith('SULTR2;').any() or
      not s[s['symbol'].str.upper().str.startswith('SULTR2;')]['ref_species'].eq('arabidopsis').any(),
      'Sorghum target: no Arabidopsis SULTR2 rows survive')

# 4. gymnosperm / fern / lycophyte
for traits, lin in ((['conifer'], 'gymnosperm'), (['fern'], 'fern'), (['lycophyte'], 'lycophyte')):
    s = surviving(traits)
    b = bad_rows(s, ANGIO_ONLY, {lin})
    check(b.empty, f'{traits[0]}: no angiosperm-only cell types survive' + (f' (got {show(b)})' if len(b) else ''))
    if lin != 'gymnosperm':
        b = bad_rows(s, SEED_ONLY, {lin, 'gymnosperm'})
        check(b.empty, f'{traits[0]}: no seed-plant-only cell types survive' + (f' (got {show(b)})' if len(b) else ''))
    for ct in ('Xylem', 'Epidermis'):
        check(int((s['cell_type'] == ct).sum()) > 0, f'{traits[0]}: {ct} rows survive')
    check(int(s['cell_type'].str.contains('Root|Endodermis').sum()) > 0, f'{traits[0]}: root rows survive')

# 5. idempotent: the shipped tables are fully tagged
changed = []
for p in TABLES:
    d = pd.read_csv(p, sep='\t', dtype=str).fillna('')
    before = d[['requires', 'excludes']].copy()
    d, _ = LT.tag_table(d)
    n = int((d[['requires', 'excludes']] != before).any(axis=1).sum())
    if n:
        changed.append(f'{os.path.relpath(p, MARKERS)}({n})')
check(not changed, 'lineage_tags.py has nothing left to tag' + (f' (run it on: {", ".join(changed)})' if changed else ''))

# 6. ID helpers
m, _ = MM.match_ids(['Solyc01g005000', 'Solyc02g000010'], {'Solyc01g005000.3', 'Solyc02g000010.1'}, True)
check(m == {'Solyc01g005000': ['Solyc01g005000.3'], 'Solyc02g000010': ['Solyc02g000010.1']},
      '--match-unversioned maps Solyc IDs to versioned var_names')
m, _ = MM.match_ids(['Solyc01g005000'], {'Solyc01g005000.3'}, False)
check(m == {}, 'without --match-unversioned, versioned IDs do not match')
for a, b in (('AT1G01010.1', 'AT1G01010'), ('Sobic.001G000100.1.p', 'Sobic.001G000100'), ('g12.t1', 'g12'),
             ('Zm00001eb000010_T001', 'Zm00001eb000010'), ('Glyma.17G133100', 'Glyma.17G133100'),
             ('Nbe01g00010-mRNA-1', 'Nbe01g00010'), ('LOC_Os01g01010.1', 'LOC_Os01g01010')):
    check(MM.unversion(a) == b, f'unversion({a}) == {b}')
r = MM.parse_rewrites([r'Glyma\.=>GLYMA_'], '--id-rewrite')
check(MM.apply_rewrites(pd.Series(['Glyma.17G133100']), r).iloc[0] == 'GLYMA_17G133100', "--id-rewrite 'Glyma\\.=>GLYMA_'")

print()
if failures:
    print(f'{len(failures)} FAILED')
    sys.exit(1)
print('ALL PASS')
