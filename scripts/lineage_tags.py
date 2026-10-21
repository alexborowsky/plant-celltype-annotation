#!/usr/bin/env python3
"""Add lineage tags to marker tables so markers only apply where the cell type exists.

`excludes` is used rather than `requires` so rows still apply when no --target-traits are given.
  excludes=bryophyte          : vascular, root, stomatal, hydathode, periderm, axillary/shoot-apical meristem,
                                nodule, flower, seed and fruit cell types
  excludes=monocot,gymnosperm : eudicot-only types (palisade/spongy mesophyll, adaxial/abaxial epidermis)
                                and GL1/GL2/TTG1/TTG2/WRKY44 trichome/root-hair patterning rows
  requires=Brassicaceae       : Arabidopsis SULTR2;1 / SULTR2;2 rows (their XP vs BS split does not transfer;
                                see plant_pitfalls.md)
Rows from bryophyte reference species and rows that already carry a lineage tag are left alone.
Trait implications live in map_markers.py IMPLIES (liverwort/moss/hornwort -> bryophyte).

Usage: python lineage_tags.py table.tsv [...]   (edits in place; prints a summary)
"""
import re
import sys

import pandas as pd

LINEAGE_TAGS = {'eudicot', 'monocot', 'grass', 'C3', 'C4', 'angiosperm', 'tracheophyte', 'gymnosperm', 'conifer',
                'lycophyte', 'bryophyte', 'liverwort', 'moss', 'hornwort', 'Brassicales', 'Brassicaceae', 'Solanaceae',
                'Capsicum', 'Fabaceae', 'Gossypium', 'Rosaceae', 'Apocynaceae', 'Cucurbitaceae', 'Sorghum', 'Oryza'}
BRYO_SPECIES = {'marchantia', 'physcomitrium', 'physcomitrella'}
VASCULAR = re.compile(r'xylem|phloem|procambi|cambium|sieve|companion|pericycle|stele|vascul|bundle_sheath|mestome|'
                      r'tracheid|vessel|ray_parenchyma|endoderm|guard|stomat|subsidiary|root_cap|columella|'
                      r'lateral_root|quiescent|trichoblast|atrichoblast|root_hair|exoderm|metaxylem|protoxylem|root|hydathode|'
                      r'phellem|phelloderm|periderm|cork|lenticel|axillary|shoot_apical_meristem|nodule', re.I)
FLOWER = re.compile(r'petal|sepal|stamen|carpel|anther|tapetum|pollen|microspore|ovule|integument|endosperm|nucell|'
                    r'synergid|egg_cell|central_cell|stigma|style|transmitting|exocarp|mesocarp|endocarp|seed_coat|'
                    r'endotheli|suspensor|chalaz|funicul|aleurone|scutell|lodicule|glume|palea|lemma|nectary|'
                    r'floral|inflorescence|spikelet', re.I)
EUDICOT_TYPES = re.compile(r'palisade|spongy|abaxial_epiderm|adaxial_epiderm', re.I)
EUDICOT_SYMBOLS = {'GL1', 'GL2', 'TTG2', 'WRKY44', 'TTG1'}
EUDICOT_SPECIES = {'arabidopsis', 'brassicaceae', 'tomato', 'nbenthamiana', 'soybean', 'medicago', 'lotus',
                   'populus', 'poplar', 'cotton', 'cassava', 'catharanthus', 'strawberry', 'peanut', 'pepper',
                   'cucumber', 'tobacco', 'potato'}


def tags(s):
    return [t.strip() for t in str(s).split(',') if t.strip()]


def add(val, tag):
    t = tags(val)
    return ','.join(t + [tag]) if tag not in t else ','.join(t)


def tag_table(df):
    n = {'excl_bryophyte': 0, 'eudicot_only': 0, 'SULTR2_Brassicaceae': 0}
    for c in ('requires', 'excludes'):
        if c not in df.columns:
            df[c] = ''
    for i, r in df.iterrows():
        sp = str(r.get('ref_species', '')).lower()
        ct = str(r.get('cell_type', ''))
        sym = str(r.get('symbol', '')).upper()
        req, exc = r['requires'], r['excludes']
        if sp in BRYO_SPECIES:
            continue
        if sym.startswith('SULTR2;') and sp in {'arabidopsis', 'brassicaceae'} and 'Brassicaceae' not in tags(req):
            req = add(req, 'Brassicaceae'); n['SULTR2_Brassicaceae'] += 1
        lineage = (set(tags(req)) | set(tags(exc))) & LINEAGE_TAGS
        if (VASCULAR.search(ct) or FLOWER.search(ct)) and 'bryophyte' not in tags(exc) and not lineage:
            exc = add(exc, 'bryophyte'); n['excl_bryophyte'] += 1
        if sp in EUDICOT_SPECIES and (EUDICOT_TYPES.search(ct) or sym in EUDICOT_SYMBOLS) and not lineage:
            exc = add(add(add(exc, 'monocot'), 'gymnosperm'), 'bryophyte'); n['eudicot_only'] += 1
        df.at[i, 'requires'] = req
        df.at[i, 'excludes'] = exc
    return df, n


if __name__ == '__main__':
    for path in sys.argv[1:]:
        df = pd.read_csv(path, sep='\t', dtype=str).fillna('')
        df, n = tag_table(df)
        df.to_csv(path, sep='\t', index=False, lineterminator='\n')
        print(f'{path}: added {n}')
