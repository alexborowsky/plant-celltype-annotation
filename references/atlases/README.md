# Atlas notes by species x organ

One file per group, from the survey collations (2026-10-19/20, updated with gap-fill reviews). Each covers the datasets reviewed, per-cell-type verdicts, the recommended label reference, cross-study markers, gaps, conflicts, and (for updated groups) an "Update 2026-10-20: gap-fill reviews" section. The marker table is `references/markers/<tier>/<group>.tsv`.

- Full dataset list (all datasets found, including unreviewed ones): `references/atlas_catalog.tsv`.
- Source files (supplements, label extracts, per-dataset reviews) are kept in the maintainers' resources folder (`datasets/<group>/`), not in this repository.

**Status: drafts.** IDs were checked by the review and collation agents against paper tables and UniProt or organism databases, but rows were not independently re-verified. Cross-study confidence raises were judged per agent.

| Group | Tier | Datasets | Markers | High conf. | Function | Cell types |
|---|---|---|---|---|---|---|
| [wheat_inflorescence](wheat_inflorescence.md) | primary | 3 | 223 | 88 | 105 | 24 |
| [arabidopsis_root](arabidopsis_root.md) | primary | 7 | 167 | 65 | 69 | 23 |
| [arabidopsis_shoot_apex](arabidopsis_shoot_apex.md) | primary | 2 | 82 | 47 | 49 | 19 |
| [arabidopsis_seed](arabidopsis_seed.md) | primary | 4 | 121 | 46 | 43 | 32 |
| [arabidopsis_stem](arabidopsis_stem.md) | primary | 2 | 84 | 41 | 44 | 16 |
| [maize_endosperm](maize_endosperm.md) | primary | 3 | 83 | 38 | 15 | 13 |
| [arabidopsis_leaf](arabidopsis_leaf.md) | primary | 6 | 125 | 34 | 41 | 22 |
| [arabidopsis_seedling](arabidopsis_seedling.md) | primary | 1 | 58 | 34 | 41 | 15 |
| [populus_stem](populus_stem.md) | primary | 6 | 96 | 34 | 43 | 16 |
| [arabidopsis_fruit](arabidopsis_fruit.md) | primary | 1 | 103 | 28 | 46 | 36 |
| [arabidopsis_inflorescence](arabidopsis_inflorescence.md) | primary | 1 | 77 | 27 | 49 | 27 |
| [maize_inflorescence](maize_inflorescence.md) | primary | 2 | 73 | 24 | 15 | 21 |
| [soybean_nodule](soybean_nodule.md) | primary | 2 | 78 | 21 | 20 | 11 |
| [arabidopsis_endosperm](arabidopsis_endosperm.md) | primary | 2 | 58 | 20 | 23 | 13 |
| [brassicaceae_root](brassicaceae_root.md) | primary | 1 | 35 | 19 | 18 | 12 |
| [maize_seed](maize_seed.md) | primary | 1 | 44 | 18 | 13 | 10 |
| [rice_inflorescence](rice_inflorescence.md) | primary | 3 | 72 | 18 | 39 | 32 |
| [soybean_root](soybean_root.md) | primary | 2 | 61 | 16 | 24 | 12 |
| [maize_embryo](maize_embryo.md) | primary | 1 | 50 | 15 | 16 | 14 |
| [tomato_other](tomato_other.md) | primary | 2 | 53 | 15 | 36 | 18 |
| [maize_shoot_apex](maize_shoot_apex.md) | primary | 2 | 55 | 14 | 7 | 14 |
| [medicago_nodule](medicago_nodule.md) | primary | 2 | 60 | 12 | 18 | 12 |
| [soybean_seed](soybean_seed.md) | primary | 2 | 70 | 12 | 22 | 25 |
| [tomato_root](tomato_root.md) | primary | 3 | 73 | 12 | 19 | 16 |
| [cotton_ovule](cotton_ovule.md) | primary | 4 | 68 | 11 | 19 | 9 |
| [maize_leaf](maize_leaf.md) | primary | 4 | 76 | 11 | 35 | 18 |
| [wheat_root](wheat_root.md) | primary | 2 | 83 | 11 | 18 | 15 |
| [lotus_root](lotus_root.md) | primary | 2 | 45 | 9 | 31 | 12 |
| [maize_root](maize_root.md) | primary | 4 | 65 | 9 | 16 | 14 |
| [rice_seed](rice_seed.md) | primary | 3 | 64 | 9 | 20 | 14 |
| [rice_root](rice_root.md) | core (`markers/rice_root.tsv`) | 6 | 46 | 12 | 19 | 16 |
| [lotus_nodule](lotus_nodule.md) | secondary | 1 | 24 | 14 | 17 | 5 |
| [catharanthus_leaf](catharanthus_leaf.md) | secondary | 1 | 39 | 13 | 14 | 11 |
| [barley_inflorescence](barley_inflorescence.md) | secondary | 1 | 42 | 7 | 31 | 23 |
| [tomato_seedling](tomato_seedling.md) | secondary | 1 | 27 | 7 | 11 | 9 |
| [rice_embryo](rice_embryo.md) | secondary | 1 | 30 | 6 | 11 | 16 |
| [sorghum_leaf](sorghum_leaf.md) | secondary | 1 | 39 | 6 | 16 | 7 |
| [arabidopsis_ovule](arabidopsis_ovule.md) | secondary | 1 | 27 | 5 | 18 | 9 |
| [marchantia_other](marchantia_other.md) | secondary | 2 | 57 | 5 | 10 | 14 |
| [rice_ovule](rice_ovule.md) | secondary | 1 | 33 | 5 | 8 | 16 |
| [selaginella_root](selaginella_root.md) | secondary | 2 | 27 | 5 | 10 | 8 |
| [brachypodium_leaf](brachypodium_leaf.md) | secondary | 1 | 36 | 4 | 15 | 14 |
| [cotton_anther](cotton_anther.md) | secondary | 1 | 55 | 3 | 32 | 12 |
| [cucumber_inflorescence](cucumber_inflorescence.md) | secondary | 1 | 40 | 3 | 15 | 18 |
| [sorghum_root](sorghum_root.md) | secondary | 2 | 40 | 3 | 11 | 14 |
| [barley_shoot_apex](barley_shoot_apex.md) | secondary | 1 | 30 | 2 | 15 | 12 |
| [pepper_fruit](pepper_fruit.md) | secondary | 1 | 39 | 2 | 2 | 13 |
| [pine_shoot_apex](pine_shoot_apex.md) | secondary | 1 | 11 | 2 | 2 | 6 |
| [rice_leaf](rice_leaf.md) | secondary | 2 | 52 | 1 | 5 | 13 |
| [strawberry_fruit](strawberry_fruit.md) | secondary | 1 | 45 | 1 | 9 | 19 |
| [barley_root](barley_root.md) | secondary | 1 | 15 | 0 | 7 | 9 |
| [cassava_leaf](cassava_leaf.md) | secondary | 1 | 49 | 0 | 25 | 13 |
| [medicago_root](medicago_root.md) | secondary | 1 | 47 | 0 | 11 | 13 |
| [peanut_fruit](peanut_fruit.md) | secondary | 1 | 29 | 0 | 1 | 11 |
| [physcomitrium_other](physcomitrium_other.md) | secondary | 1 | 37 | 0 | 0 | 6 |
| [populus_root](populus_root.md) | secondary | 2 | 15 | 0 | 1 | 8 |
