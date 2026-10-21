<!-- Collated from the survey review of arabidopsis_inflorescence (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis inflorescence / flower: collated marker resources

Collated 2026-10-20 from the one review in `survey/merged_reviews.json` for group
`arabidopsis_inflorescence` (Lee et al. 2025, flower part). The per-dataset review is in
`Lee2025/README.md` and is unchanged. This folder adds:

- `expected_cell_types.tsv`: expected types for whole flowers, stages 6-15 (from anatomy, not from the
  published labels), with the number of `function` markers per type counted from `markers_draft.tsv`.
- `markers_draft.tsv`: 77 rows in the skill marker-table schema plus `alt_id` (UniProt accession).
  `tissue` = `flower`, which is a new value (`map_markers.py --tissue flower` filters on it as free text).

Nothing in the skill was edited.

## Datasets

| Dataset | Platform | Cells | Label access | Quality |
|---|---|---|---|---|
| Lee TA, ... Ecker JR 2025 *Nat Plants* 11:1960 "A single-cell, spatial transcriptomic atlas of the Arabidopsis life cycle", flower part. DOI 10.1038/s41477-025-02072-z; GEO GSE226097 | 10x 3' HT v3.1 snRNA-seq (nuclei; pollen grains spun out), plus MERSCOPE MERFISH on 3 flowers with non-flower panels (1,000-gene seedling, 140-gene silique) | 11,888 nuclei, 13 clusters, 6 runs; whole flowers stages 6-15, Col-0 | `table`: per-cell labels from the public cellxgene portal API (`Lee2025/flower_labels_from_portal.tsv`); also inside the 1.1 GB GEO rds | medium |

Only one dataset was reviewed for this group, so cross-dataset agreement between single-cell studies
is not possible yet. Agreement here means a gene validated in an independent earlier study (reporter, in
situ, mutant) that is also specific to a Lee 2025 cluster which the paper did **not** label with that
gene (see below).

## Verdict matrix (cell type x dataset)

Only one column exists. A = Adopt, R = Revise, X = Reject, - = not present.

| Canonical type | Lee 2025 flower | Note |
|---|---|---|
| Tapetum | A (c8 secretory; c3 late) | sporopollenin genes in c8; GRP17/oleosin program in c3 |
| Pollen (vegetative / microspore) | R (c7 "Anther") | AGP6/AGP11/PPME1 at 0.83-0.97; label should be Pollen |
| Sperm_Cell (germline) | A (c11 "Pollen") | GEX1, MGH3, CYCD7;1; 52 nuclei |
| Meiocyte | R (c9) | MSH5 weak; CYCB1;1/CYCB1;2/CDC20 DE; DMC1/ASY1/ZYP1/SPO11 not DE |
| Guard | R (c5 "Unknown") | FAMA 0.78 vs 0.04; paper left it unlabeled |
| Myrosin_Idioblast | R (inside c5) | TGG2 and DREB2F (vascular in MERFISH) in c5; KAT1/SLAC1/MYB60 not DE in c5 |
| Epidermis | R (c2, c4, c10 subclusters) | merged with mesophyll (c2), proliferation (c4), flavonoid state (c10) |
| Mesophyll | R (inside c2) | RBCS/LHCB/CA1 in c2 |
| Xylem | R (c12 "Vascular") | CESA4/7/8, VND2, XCP2 |
| Phloem / companion cells | - | no snRNA cluster; MERFISH only (AHA3, FT, UMAMIT20) |
| Dividing_cells | R (c4 "Developing ovule") | TOPII, KNOLLE, CDC20; no ovule-identity gene |
| Flavonoid_producing (state) | R (c10 "Gynoecium and developing ovule") | TT3/TT4/LDOX; subclusters = tapetum, epidermis, female gametophyte |
| Filament / unresolved | X (c6 "Anther, filament junction") | label rests on KNAT2 (pct 0.14); KAN1, ABCB19, MYO5 program |
| Low quality | X (c0, c1) | c0 = 99% run 1, lowest depth; c1 has no identity signal (43% of nuclei together) |
| Endothecium, middle layer, carpel valve, valve margin, replum, septum, transmitting tract, stigma, style, ovule integuments, nucellus, female gametophyte, nectary, trichome, floral meristem | - | not resolved at 13 clusters |

## Cross-study markers (independent validation + Lee 2025 cluster specificity)

| Gene | AGI | Type | Independent evidence | Lee 2025 |
|---|---|---|---|---|
| FAMA | AT3G24140 | Guard | reporter + mutant (Ohashi-Ito & Bergmann 2006) | c5 0.78 vs 0.04 (cluster unlabeled by paper) |
| AGP6 | AT5G14380 | Pollen | reporter + mutant (Levitin 2008) | c7 0.89 vs 0.13 (labeled "Anther" from other genes) |
| AGP11 | AT3G01700 | Pollen | reporter + mutant (Levitin 2008) | c7 0.87 vs 0.10 |
| PPME1 | AT1G69940 | Pollen | pollen-specific, mutant (Tian 2006) | c7 0.46 vs 0.05 |
| CESA4/IRX5 | AT5G44030 | Xylem | irx5 mutant (Taylor 2003) | c12 0.44 vs 0.03 (labeled from HB8/ACL5 etc.) |
| CESA7/IRX3 | AT5G17420 | Xylem | irx3 mutant (Taylor 1999) | c12 0.15 vs 0.007; stem MERFISH |
| CESA8/IRX1 | AT4G18780 | Xylem | irx1 mutant (Taylor 2000) | c12 0.29 vs 0.015 |
| XCP2 | AT1G20850 | Xylem | xylem protease (Funk 2002) | c12 0.17 vs 0.014; stem MERFISH |
| FUL | AT5G60910 | Carpel_Valve | valve in situ (Gu 1998) | carpel MERFISH (Ext. Data Fig. 5h); not DE in snRNA |

FUL is the only row whose confidence was raised by this agreement (medium to high); the others were
already `high` from their function. Tapetum sporopollenin genes and GEX1/MGH3 are not counted: the paper
labeled c8 and c11 with those genes (circular). AHA3 had two validations (DeWitt 1995 reporter; Lee 2025
MERFISH) but was kept `medium` because the snRNA puts it in c10/c8 rather than in a phloem cluster.

## Gaps (expected types with no `function` marker in the draft)

Stomatal_lineage, Trichome, Mesophyll, Phloem_Companion, Phloem_Parenchyma and Sieve_Element have
function markers only in `arabidopsis_leaf.tsv` (tissue `leaf`). With no flower-specific marker at all:
Filament, Middle_Layer, Replum, Septum, Stigma_Papillae, Style, Inner_Integument, Nucellus,
Floral_Meristem, and petal conical epidermis. These are Step 4 search targets. Vascular rows (7) are all
`low` MERFISH-only genes.

## Recommended label reference

Lee 2025 is the only reviewed flower dataset. Use its per-cell portal labels only for Tapetum (c3, c8)
and Sperm_Cell (c11, renamed from "Pollen"), plus c5 as Guard (with myrosin cells split off) and c12 as
Xylem. Do not use c0, c1, c6, and treat c4 and c10 as states. Drop run 1 before re-clustering. A second
independent flower or anther atlas is needed before any label is treated as ground truth.

## Conflicts and corrections

- **c7 "Anther" is pollen.** AGP6/AGP11/PPME1 are pollen genes; the paper's label came from bulk
  Nakayama 2005 anther genes.
- **c11 "Pollen" is the male germline** (generative/sperm), not the vegetative cell.
- **c5 is guard cells and probably myrosin idioblasts.** FAMA specifies both; TGG2 (myrosin cells, not
  guard cells per Barth & Jander 2006) is DE (0.89 vs 0.31), the MERFISH "vascular" gene DREB2F is DE only
  here, and KAT1/SLAC1/MYB60 are not DE in c5. KAT1 is instead DE in c3 (tapetum, 0.10 vs 0.03).
- **CA1 (AT3G01500)**: the paper's ST1 (via Nakayama 2005) calls it "epidermis specific in petals and
  stamens"; it is a chloroplast carbonic anhydrase and is DE in c2 with photosynthesis genes. Graded as
  Mesophyll (low).
- **AT2G37540**: the text/Extended Data Fig. 5b say sepal/petal outer epidermis; Supp. Table 3 lists it as
  silique mesocarp. Kept as Epidermis, `low`.
- **MERFISH vascular genes vs snRNA**: AHA3 (c10/c8), GRP5/AT3G20470 (c10, 0.79), AT1G67870 (c8, c2),
  PARCL/AT1G64370 (c2, c7) are DE in non-vascular clusters. All `low` except AHA3.
- **ID hygiene**: Supp. Table 2 IDs carry `make.unique` suffixes (`AT5G075301`); truncated to 9
  characters before matching. Supp. Table 3 gives symbols only for 8 flower rows. UMAMIT20 = AT4G08290 is
  taken from the Extended Data Fig. 5c legend. SULTR3;1, FBH3, EMB3103, BBX15, SPL9, SPL11 (ST3 flower
  rows without AGIs) were **not** added, since their IDs would have to be inferred from symbols. FMA in
  ST3 = FAMA.
- **Correction to the review's marker list**: AT1G64570 (ST1 "pollen", Brownfield 2009) is DE in c5, c8
  and c12, not specific; not carried. KNAT2/ATK1 (c6 label) not carried.

## IDs checked

Every AGI in `markers_draft.tsv` was confirmed with the UniProt REST API (taxon 3702); the accession is in
`alt_id`. The Lee 2025 genes were also matched to ST1/ST2/ST3 or the full-text figure legends. The two
review-made check files are `Lee2025/uniprot_id_check*.tsv`.

## Classic rows not from the review

15 rows (`source` starts `classic:`) were added from the literature to cover expected types the dataset
does not resolve: MS1, DYT1, MYB26, DMC1, ASY1, DUO1, HAP2, AP1, IND, MYB98, EC1.1, FIS2, NTT, SWEET9,
CRC. None is DE in Lee 2025. INO is cited in Lee ST1 but not DE.

## Overlap with existing skill tables (same species)

`arabidopsis_leaf.tsv` has the same gene and cell type for ATML1, FDH, PDF1, LTP1 (Epidermis), FAMA
(Guard), CA1 (Mesophyll), IRX3, XCP2 (Xylem), ATHB8 (Procambium), CYCB1;1, KNOLLE (Dividing_cells). The
flower rows add the Lee 2025 flower evidence but use `tissue=flower`. LTP1 and PDF1 have the same
confidence. CA1 is `medium` in the leaf table and `low` here because the flower evidence conflicts.
`arabidopsis_root.tsv` shares no gene/cell-type pair. All reproductive, organ-identity, nectary and
myrosin rows are new to the skill.

## Could not verify

- Literature citations for the classic and characterized genes (author, year, journal) come from
  knowledge, not from fetching each paper. Gene IDs were checked; the cited expression patterns were
  not re-read. No DOIs are given for them, to avoid wrong DOIs.
- The flower dot plots in the SI PDF were not checked visually. The basis for the post-spatial relabel of
  c4 as "developing ovule" is not documented in the paper.
- The GitHub repo `travandlee/arabidopsis_lifecycle_atlas` returned 404. Large objects (flower rds
  1.1 GB, h5ad 455 MB, relaxed rds 65 MB, ST5-6) were not downloaded.
- Not reviewed, possible further datasets for this group: other Arabidopsis flower, anther or
  inflorescence single-cell atlases (for example the Long et al. 2021 source of the paper's tapetum list).
  A second dataset is needed for real cross-study agreement.
