#!/usr/bin/env python3
"""Add lineage tags to marker tables so markers only apply where the cell type exists.

`excludes` is used rather than `requires` so rows still apply when no --target-traits are given.
Each cell-type name is matched (case-insensitive) against the groups below, in order; the first group
that matches decides the tags. The lineage traits are those of map_markers.py --target-traits:
bryophyte (liverwort, moss, hornwort), lycophyte, fern, gymnosperm (conifer); angiosperms are the default.

  group        excludes                                    cell types (regex in GROUPS below)
  angiosperm   bryophyte,lycophyte,fern,gymnosperm         flower organs and floral/inflorescence/spikelet meristems,
                                                           anther wall (endothecium, middle layer, connective),
                                                           carpel/fruit (septum, replum, valve, pericarp...),
                                                           endosperm (incl. aleurone, BETL, ESR), double-fertilization
                                                           female gametophyte (egg, central cell, synergid),
                                                           bitegmic integument layers and seed coat, funiculus,
                                                           grass embryo organs (scutellum, coleoptile), companion cells
  seed_plant   bryophyte,lycophyte,fern                    SAM zonation (CZ, PZ, rib meristem/zone, organizing centre,
                                                           SAM L1/meristem epidermis), axillary meristem,
                                                           cambium/periderm/ray (secondary growth), ovule/nucellus/
                                                           megaspore, pollen and sperm cells, seed embryo/suspensor/
                                                           radicle/cotyledon/seedling hook, seed maturation
  tracheophyte bryophyte                                   vascular tissue, root types, stomata, hydathode, nodule,
                                                           shoot meristem (generic), primordia, organ boundaries,
                                                           stem-cell niche, pavement cells, trichomes, tapetum,
                                                           microspores, pith
  eudicot      monocot,gymnosperm,bryophyte,lycophyte,fern palisade/spongy mesophyll, adaxial/abaxial epidermis, and
                                                           GL1/GL2/TTG1/TTG2/WRKY44 rows (eudicot-species tables only)
  requires=Brassicaceae  Arabidopsis SULTR2;1 / SULTR2;2 rows (their XP vs BS split does not transfer;
                         see plant_pitfalls.md)

Deliberately NOT tagged (generic or conserved): Epidermis, Protoderm/Protodermal, Dividing_cells, S_Phase and
other states, Mesophyll, Meristem, Meiocyte (meiosis genes are conserved; bryophyte sporophytes have
meiocytes), Sclerenchyma, Ground_Tissue. Bryophyte gametophyte epidermis is not homologous to the angiosperm protoderm, but the ATML1/
HD-ZIP IV family exists in bryophytes, so these rows stay and are judged on the data.

A tag is not added when the row already blocks that lineage: the tag is already in `excludes`, or a
`requires` tag is not implied by the lineage (requires=grass already excludes bryophytes), or the row comes
from a species of that lineage (Marchantia/Physcomitrium rows are left alone entirely; Selaginella rows never
get lycophyte, pine rows never get gymnosperm). Tags are only added, never removed, so the script is
idempotent and safe to re-run.

Usage: python lineage_tags.py table.tsv [...]   (edits requires/excludes in place; prints a summary)
       python lineage_tags.py --dry-run table.tsv [...]   (report only)
"""
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from map_markers import expand_traits  # noqa: E402

LINEAGE_TAGS = {'eudicot', 'monocot', 'grass', 'C3', 'C4', 'angiosperm', 'tracheophyte', 'gymnosperm', 'conifer',
                'lycophyte', 'fern', 'bryophyte', 'liverwort', 'moss', 'hornwort', 'Brassicales', 'Brassicaceae',
                'Solanaceae', 'Capsicum', 'Fabaceae', 'Gossypium', 'Rosaceae', 'Apocynaceae', 'Cucurbitaceae',
                'Sorghum', 'Oryza'}
# Reference species -> its lineage (rows are never tagged against their own lineage).
SPECIES_LINEAGE = {
    'marchantia': 'bryophyte', 'physcomitrium': 'bryophyte', 'physcomitrella': 'bryophyte',
    'ceratodon': 'bryophyte', 'anthoceros': 'bryophyte',
    'selaginella': 'lycophyte', 'lycopodium': 'lycophyte', 'isoetes': 'lycophyte',
    'ceratopteris': 'fern', 'azolla': 'fern', 'marsilea': 'fern', 'adiantum': 'fern',
    'pine': 'gymnosperm', 'pinus': 'gymnosperm', 'picea': 'gymnosperm', 'spruce': 'gymnosperm',
    'ginkgo': 'gymnosperm', 'cycas': 'gymnosperm', 'taxus': 'gymnosperm', 'gnetum': 'gymnosperm',
}
BRYO_SPECIES = {s for s, lin in SPECIES_LINEAGE.items() if lin == 'bryophyte'}

ANGIO = ['bryophyte', 'lycophyte', 'fern', 'gymnosperm']
SEED = ['bryophyte', 'lycophyte', 'fern']
TRACH = ['bryophyte']


def _rx(*parts):
    return re.compile('|'.join(parts), re.I)


# (name, excludes, regex). Order matters: first match wins (Embryo_Surrounding_Region is endosperm,
# Seed_Coat_* is angiosperm-only while plain Seed is seed-plant, Procambium is vascular, not cambium).
GROUPS = [
    ('angiosperm', ANGIO, _rx(
        # flowers, inflorescences and their meristems
        r'petal', r'sepal', r'stamen', r'carpel', r'anther', r'stigma', r'style', r'transmitting', r'nectar',
        r'floral', r'flower', r'inflorescence', r'spikelet', r'floret', r'glume', r'palea', r'lemma', r'lodicule',
        r'bract', r'rachilla', r'receptacle',
        # anther wall (not tapetum: sporangium tapetum exists in all vascular plants)
        r'endotheci', r'middle_layer', r'connective',
        # carpel / fruit
        r'septum', r'replum', r'(^|_)valve', r'ovary', r'placent', r'pericarp', r'exocarp', r'mesocarp',
        r'endocarp', r'fruit',
        # endosperm and the angiosperm female gametophyte (double fertilization)
        r'endosperm', r'aleurone', r'embryo_surrounding', r'central_cell', r'synergid', r'antipodal',
        r'egg_cell',
        # bitegmic integuments, seed coat, funiculus, angiosperm seed structures
        r'inner_integument', r'outer_integument', r'seed_coat', r'endotheli', r'chalaz', r'funicul',
        r'hilum', r'hourglass', r'pigment_layer', r'seed_abscission', r'nucellar_projection',
        # grass embryo organs
        r'scutell', r'coleopt', r'coleorhiz', r'epiblast',
        # companion cells (gymnosperms have Strasburger cells; pine rows that require gymnosperm are skipped)
        r'companion',
    )),
    ('seed_plant', SEED, _rx(
        # SAM zonation (fern/lycophyte shoots grow from apical cells; no CLV3/WUS zonation)
        r'(^|_)sam(_|$)', r'central_zone', r'peripheral_zone', r'rib_meristem', r'rib_zone', r'organizing_cent',
        r'meristem_epidermis', r'meristem_tip_l1', r'shoot_apical_meristem', r'axillary',
        # secondary growth (procambium is vascular, handled by the tracheophyte group)
        r'(?<!pro)cambium', r'phellem', r'phellogen', r'phelloderm', r'periderm', r'cork', r'lenticel',
        r'ray_parenchyma', r'xylem_mother',
        # ovule, pollen, sperm
        r'ovul', r'(^|_)integument', r'nucell', r'megaspore', r'pollen', r'sperm', r'generative_cell',
        r'vegetative_cell',
        # seed embryo and seedling
        r'embryo', r'suspensor', r'radicle', r'plumule', r'cotyledon', r'hypocotyl', r'apical_hook',
        r'(^|_)seed(_|$)',
    )),
    ('tracheophyte', TRACH, _rx(
        # vascular tissue
        r'xylem', r'phloem', r'procambi', r'sieve', r'pericycle', r'stele', r'vascul', r'bundle_sheath',
        r'mestome', r'tracheid', r'vessel', r'endoderm', r'interfascicular', r'pith',
        # roots
        r'root', r'columella', r'quiescent', r'trichoblast', r'atrichoblast', r'exoderm', r'border_cell',
        r'shoot_borne',
        # stomata, hydathodes, nodules
        r'guard', r'stomat', r'subsidiary', r'hydathode', r'nodule',
        # angiosperm-type shoot development without bryophyte homologues
        r'shoot_meristem', r'primordi', r'boundary', r'lateral_organ', r'stem_cell_niche',
        r'intercalary_meristem', r'ground_meristem',
        # leaf epidermal cell types of vascular plants
        r'pavement', r'trichome',
        # sporangium: bryophyte sporangia have no tapetum of this kind
        r'tapetum', r'microspore',
    )),
]
EUDICOT_TYPES = re.compile(r'palisade|spongy|abaxial_epiderm|adaxial_epiderm', re.I)
EUDICOT_SYMBOLS = {'GL1', 'GL2', 'TTG2', 'WRKY44', 'TTG1'}
EUDICOT_EXCLUDES = ['monocot', 'gymnosperm', 'bryophyte', 'lycophyte', 'fern']
EUDICOT_SPECIES = {'arabidopsis', 'brassicaceae', 'tomato', 'nbenthamiana', 'soybean', 'medicago', 'lotus',
                   'populus', 'poplar', 'cotton', 'cassava', 'catharanthus', 'strawberry', 'peanut', 'pepper',
                   'cucumber', 'tobacco', 'potato'}


def tags(s):
    return [t.strip() for t in str(s).split(',') if t.strip()]


def add(val, tag):
    t = tags(val)
    return ','.join(t + [tag]) if tag not in t else ','.join(t)


def species_lineage(sp):
    sp = sp.lower()
    for k, lin in SPECIES_LINEAGE.items():
        if sp.startswith(k):
            return lin
    return None


def blocked(lineage, req, exc, sp_lin):
    """True if the row already does not apply to a target of this lineage (or must not be tagged)."""
    if lineage in tags(exc) or lineage == sp_lin:
        return True
    implied = expand_traits({lineage})
    return any(r not in implied for r in tags(req))


def group_of(cell_type):
    for name, excl, rx in GROUPS:
        if rx.search(cell_type):
            return name, excl
    return None, []


def tag_table(df):
    n = {'angiosperm': 0, 'seed_plant': 0, 'tracheophyte': 0, 'eudicot_only': 0, 'SULTR2_Brassicaceae': 0}
    for c in ('requires', 'excludes'):
        if c not in df.columns:
            df[c] = ''
    for i, r in df.iterrows():
        sp = str(r.get('ref_species', '')).lower()
        ct = str(r.get('cell_type', ''))
        sym = str(r.get('symbol', '')).upper()
        req, exc = str(r['requires']), str(r['excludes'])
        if sp in BRYO_SPECIES or species_lineage(sp) == 'bryophyte':
            continue
        sp_lin = species_lineage(sp)
        if sym.startswith('SULTR2;') and sp in {'arabidopsis', 'brassicaceae'} and 'Brassicaceae' not in tags(req):
            req = add(req, 'Brassicaceae'); n['SULTR2_Brassicaceae'] += 1
        name, excl = group_of(ct)
        if sp in EUDICOT_SPECIES and (EUDICOT_TYPES.search(ct) or sym in EUDICOT_SYMBOLS):
            name, excl = 'eudicot_only', EUDICOT_EXCLUDES
        changed = False
        for lin in excl:
            if not blocked(lin, req, exc, sp_lin):
                exc = add(exc, lin); changed = True
        if changed:
            n[name] += 1
        df.at[i, 'requires'] = req
        df.at[i, 'excludes'] = exc
    return df, n


def main(argv):
    dry = '--dry-run' in argv
    paths = [a for a in argv if a != '--dry-run']
    if not paths:
        sys.exit(__doc__)
    for path in paths:
        df = pd.read_csv(path, sep='\t', dtype=str).fillna('')
        if 'cell_type' not in df.columns:
            print(f'{path}: no cell_type column, skipped')
            continue
        before = df[['requires', 'excludes']].copy() if {'requires', 'excludes'} <= set(df.columns) else None
        df, n = tag_table(df)
        n_rows = int((df[['requires', 'excludes']] != before).any(axis=1).sum()) if before is not None else len(df)
        if not dry and n_rows:
            # Re-read right before writing and only replace requires/excludes, so edits made to other
            # columns by someone else in the meantime survive (rows must still line up).
            cur = pd.read_csv(path, sep='\t', dtype=str).fillna('')
            same = (len(cur) == len(df) and (cur['cell_type'].values == df['cell_type'].values).all()
                    and (cur.get('ref_gene', cur['cell_type']).values == df.get('ref_gene', df['cell_type']).values).all())
            if not same:
                print(f'{path}: changed on disk while tagging; re-tagging the current version')
                cur, n = tag_table(cur)
            else:
                cur['requires'] = df['requires'].values
                cur['excludes'] = df['excludes'].values
            cur.to_csv(path, sep='\t', index=False, lineterminator='\n')
        print(f'{path}: {n_rows} rows changed {"(dry run) " if dry else ""}{ {k: v for k, v in n.items() if v} }')


if __name__ == '__main__':
    main(sys.argv[1:])
