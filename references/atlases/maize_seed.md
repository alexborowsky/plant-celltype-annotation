<!-- Collated from the survey review of maize_seed (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Maize seed (kernel): collated review

Date: 2026-10-20. Built from one dataset review in this folder (`Fu2023/`, which has its own README). This is a paper-only review; no in-data check (Step 3b) was run. For cross-study agreement, the draft also uses two independent maize datasets reviewed in sibling groups: Yuan et al. 2024 (`../maize_endosperm/Yuan2024/`, 6-7 DAP endosperm scRNA-seq) and Wu et al. 2025 (`../maize_embryo/`, embryo scRNA-seq plus Xenium). Only genes that the Fu review carried, or that Fu's SD1 independently shows to be compartment-specific, were taken from those reviews.

Files:
- `expected_cell_types.tsv`: expected types for the maize kernel (about 0-24 DAP), written from anatomy, not from the published labels. `function_markers` counts the existing skill tables (`references/markers/`, applicable via homology). The `notes` column gives the count in the draft below. No skill table covers any seed type yet.
- `markers_draft.tsv`: 44 rows in the skill marker schema plus `alt_id`. `ref_gene` holds B73 RefGen_v5 IDs (`Zm00001eb`), as in the maize_leaf and maize_embryo drafts. `alt_id` holds the v4 IDs (`Zm00001d`) used by both source papers. `tissue = seed`, the same as the rice_seed draft; the skill README currently lists only leaf/root/any. Every row has `requires = grass`, because all the types are parts of the grass caryopsis (BETL, ESR, EAS, persistent starchy endosperm, scutellum). Field counts were validated.

## Datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Fu et al. 2023 *Nat Commun* 14:7191, 10.1038/s41467-023-43006-7 (W64A) | whole-kernel longitudinal cryosections, 12, 18 (x2), 24 DAP | 10x Visium (55 um spots) | 10,900 **spots**, not cells; 25 clusters merged into 11 compartments | v4 (`Zm00001d`), v3 in SD1; mapped to v5 with MaizeGDB xref | cluster_only (no per-spot labels, no processed object, no images; the labels came from hand UMAP gates) | medium |
| *Cross-check only:* Yuan et al. 2024 *Nat Commun* 15:34, 10.1038/s41467-023-44369-7 (B73) | dissected endosperm 6-7 DAP | protoplast scRNA-seq, 10x v3 | 17,022 cells, 18 clusters | v4 | cluster_only | medium (reviewed in `maize_endosperm/`) |
| *Cross-check only:* Wu et al. 2025 *Nat Commun*, 10.1038/s41467-024-55803-9 | embryo | scRNA-seq + Xenium | see `maize_embryo/` | v3/v5 | see `maize_embryo/` | see `maize_embryo/` |

## Verdicts by expected cell type

A = Adopt, R = Revise, X = Reject, - = not annotated. Fu 2023 is the only dataset of this group; the Yuan 2024 column is from its own review and is shown for comparison.

| Expected type | Fu 2023 (label, spots %) | Yuan 2024 (for comparison) |
|---|---|---|
| Pericarp | R (maternal-PE, 12.9%; three layer clusters merged, uncharacterized markers) | - (dissected endosperm) |
| Nucellus | - | R (c14, contaminant) |
| Placento_Chalazal | R (maternal-PC, 4.6%; pedicel, vascular terminus and chalaza merged; spot count follows section plane) | - |
| Seed_Coat | - | - |
| Basal_Endosperm_Transfer_Layer | **A** (endosperm-BETL, 2.1%; MN1, BETL4, BETL9 10-12x; BETL4 in situ; SUT1/7 RNAi) | A (c2 outer, c9 inner) |
| Basal_Intermediate_Zone | - | - (maybe in c9 / c8) |
| Conducting_Zone | R (endosperm-CZ, 6.2%; weak markers, a BETL-to-SE gradient) | - |
| Embryo_Surrounding_Region | **A** (endosperm-ESR, 0.17%; 18 spots, 12 DAP, one section) | A (c15) |
| Endosperm_Adjacent_to_Scutellum | **A** (endosperm-EAS, 2.0%; SWEET14a/15a, ZCN11; HMA5 in situ; hand-curated) | R (c11 "progenitors") |
| Aleurone | **A** with caveat (endosperm-AL, 3.7%; LTP2 in situ; spots contain subaleurone) | R (39% of cells) |
| Subaleurone | R (endosperm-VE, 20.7%; zein-rich periphery, not "vitreous" at 12-24 DAP) | - |
| Starchy_Endosperm | R (endosperm-SE, 32.6%; SE vs VE is a gradient; tissue loss in sections) | A (c1 outer, c8 basal) |
| Scutellum | **A** tissue level (embryo-SCU, 10.6%; OLE1 in situ) | - |
| Scutellar_Epithelium | - (inside SCU) | - |
| Embryonic_Axis | R (embryo-EM, 4.6%; whole axis, partly proliferation-driven) | - (c17 whole-embryo contaminant) |
| SAM, coleoptile, coleorhiza, root cap, protoderm, procambium, suspensor | - | - |
| Dividing_cells | - (folded into EM) | R (c10, c12, correctly called a state) |

## Cross-study markers

Agreement is counted by gene ID: validated (in situ, mutant) in one independent study and compartment- or cluster-specific in another. Fu's 55 um Visium spots are counted as enrichment, not as cell-resolution validation; Fu's own RNA in situ hybridizations count as validation. 19 rows were raised (or held at high) by agreement:

| Cell type | Genes (v5 / v4) | Studies |
|---|---|---|
| BETL | MN1/INCW2 Zm00001eb083790 / Zm00001d003776 | Cheng 1996 (mutant, localization); Fu (9.9x) |
| BETL | MRP1 Zm00001eb354390 / Zm00001d010889 | Gomez 2002 (in situ); Yuan (in situ, DE); Fu (6x, low counts) |
| BETL | MEG1 Zm00001eb302080 / Zm00001d019030 | Costa 2012 (function); Yuan (DE); Fu (14x) |
| BETL | MYBR29 Zm00001eb108630 / Zm00001d006791 | Yuan (mutant, DE); Fu (9x) |
| BETL | BETL4 Zm00001eb201370 / Zm00001d000161 | Fu (in situ, 10.9x); Hueros 1995/1999 (BETL family) |
| BETL | BETL9 Zm00001eb138660 / Zm00001d041822 | Fu (in situ, 12x); Yuan (in situ, DE) |
| BETL | BAP2 Zm00001eb172830 / Zm00001d049576 | Serna 2001 and Yuan (in situ); Fu (12.9x) |
| BETL | TCRR1 Zm00001eb178220 / Zm00001d050200 | Muniz 2006 (in situ); Yuan (DE); Fu (8.7x) |
| BETL | pco073740 Zm00001eb198770 / Zm00001d052759 | Yuan (in situ); Fu (9.3x) |
| BETL | gpm875 Zm00001eb207110 / Zm00001d053785 | Yuan (in situ, reduced in *mybr29*); Fu (12.3x) |
| BETL | BETL10 Zm00001eb142290 / Zm00001d042231 | Yuan (DE) and Fu (10.6x): two enrichments, so medium |
| ESR | ESR2 Zm00001eb005200 / Zm00001d027819 | Opsahl-Ferstad 1997 (in situ); Yuan (DE log2FC 8); Fu (5.3x) |
| ESR | ESR6 Zm00001eb201820 / Zm00001d053112 | Balandin 2005 (in situ); Yuan (DE); Fu (ESR top, but BETL 7.6) |
| ESR | Zm00001eb293390 / Zm00001d038758 | Yuan (in situ); Fu (5.5x) |
| EAS | SWEET14a Zm00001eb113080 / Zm00001d007365 | Doll 2020 (in situ); Fu (11x) |
| EAS | SWEET15a Zm00001eb180830 / Zm00001d050577 | Doll 2020 and Yuan (in situ); Fu (12x) |
| EAS | ZCN11 Zm00001eb281410 / Zm00001d037439 | Doll 2020 (in situ); Fu (9.9x) |
| Starchy endosperm | FL3 Zm00001eb341550 / Zm00001d009292 | Li 2017 (mutant); Yuan (in situ, basal SE DE); Fu (endosperm, basal high) |
| Starchy endosperm | gz27 Zm00001eb313800 / Zm00001d020592 | Fu (endosperm-wide); Wu 2025 (endosperm-contaminant DE) |

Agreement that was not used to raise confidence: GLB1 (scutellum; two weak enrichments in Fu and Wu), LTP3 (Fu in situ for the axis; Yuan's cluster is the whole embryo), MS8 (Yuan in situ for EAS precursors, Fu EAS 5.6x, but Yuan's DE puts it in ESR).

## Gaps (expected types with no validated marker)

- No marker at all: Nucellus (in this group), Seed_Coat, Basal_Intermediate_Zone, Subaleurone (a positional state; only zein gradients), Coleorhiza.
- No `function` marker, only enrichment: Embryo_Surrounding_Region, Endosperm_Adjacent_to_Scutellum, Aleurone (LTP2 medium; AL9 conflicted), Conducting_Zone (SDH1 low only), Scutellum, Scutellar_Epithelium, Embryonic_Axis, Placento_Chalazal (in situ noisy or weak), Pericarp (one expression gene).
- Embryo sub-organs (SAM, leaf primordia, coleoptile, radicle, procambium, protoderm, suspensor) are not resolved by Fu; use the maize_embryo draft.
- Dividing_cells: no maize seed-specific rows; the skill's Arabidopsis/rice G2/M rows apply through homology (the maize_embryo draft has KNOLLE, CYCB1-4, CENH3).

## Recommended label reference

None of the labels can be imported per cell: Fu 2023 is cluster_only (no per-spot table, object or images), and so is Yuan 2024. Use **Fu 2023 SD1** (mean expression of 26k genes in 11 kernel compartments) as the compartment reference for whole-kernel data, and its Adopted compartments (BETL, ESR, EAS, Aleurone, Scutellum) as hypotheses. For dissected endosperm at 6-8 DAP, Yuan 2024 is the better reference: cell-resolution, in situ validated, unassignable clusters left unlabeled. For embryo sub-organs use the maize_embryo group.

## Conflicts and corrections

- **Zm00001d000002 is DU1** (starch synthase III; NCBI and SD1 "starch synthase DULL1"), not SS2 as in Fu Fig S12.
- **OLE1 v5 ID:** the review JSON listed `Zm00001eb074950/Zm00001eb074940`. UniProt shows that the oleosin is Zm00001eb074940 (LOC542263); 074950 encodes small uncharacterized/secreted proteins. The draft uses 074940.
- **gz27 v5 ID:** the v4 ID maps to Zm00001eb313810 and 313800. UniProt P04706 (27-kD gamma-zein) carries Zm00001eb313800, as in the maize_embryo draft. The draft uses 313800.
- **AL9 v5 ID:** two v5 models; B4FFB8 (5a2/AL-9, the SD1 accession) is on Zm00001eb369440, which is used here.
- **Zm00001d011340 (EAG1b/acanthoscurrin-2) was dropped.** Fu lists it as an ESR marker (84x over BETL), but in Yuan 2024 it is a top DE gene of the embryo-contaminant cluster c17 (log2FC 9.1; with neighbours Zm00001d011342/011345, an EA1-like gene and PLT3). Fu's 18 ESR spots at 12 DAP probably include embryo-proper cells. It is not a reliable ESR marker.
- **ESR6** is ESR-specific in Yuan 2024 (0.82 vs 0.005) but in Fu it is also high in BETL (7.6 vs 13.6). MaizeGDB describes it as near the BETL.
- **SUT1** is BETL-enriched in Fu (with RNAi function) but DE in a Yuan aleurone cluster and is a leaf companion-cell gene (sorghum_leaf.tsv). It is not BETL-exclusive.
- **AL9** is the classic aleurone marker but is not specific in either dataset (Fu ESR 44 vs AL 62; Yuan pct 0.999 vs 0.931): low.
- **MS8**: Yuan calls it an EAS-progenitor in situ marker, but Yuan's own DE table lists it in ESR only; Fu puts it in EAS.
- **ESR2 symbol:** the NCBI aliases of Zm00001d027819 include "ESR1". ESR1 is a separate locus (Zm00001d027820, no v5 xref).
- **Citations:** MEG1 is Costa et al. 2012 *Curr Biol*, and TCRR1 is Muniz et al. 2006 *Plant J*, checked in Europe PMC.
- Fu Table S3 "in situ" genes that do not peak in their compartment (nac6, KNOX5, Zm00001d037498) were not carried.

## Overlap with existing skill tables

No maize table exists in `references/markers/`, and no table covers seed tissue. Overlap is only by homology. SUT1 is also a `function` row in `sorghum_leaf.tsv` (Phloem_Companion, grass), and OsSUT1 is a row in `rice_root.tsv` (Phloem), so maize SUT1 will map to phloem in other tissues. The Dividing_cells, Procambium, Protoderm (Epidermis) and Root_Cap (Columella) counts in `expected_cell_types.tsv` come from the Arabidopsis and rice tables. Within the resources folder, the draft overlaps the maize_embryo draft for GLB1 (Scutellum vs Scutellum_Parenchyma) and gz27 (Starchy_Endosperm vs Endosperm), with the same v5 IDs. It also overlaps the not-yet-collated maize_endosperm shortlist (Yuan 2024) for the BETL/ESR/EAS/SE genes listed above.

## Could not verify

- Fu's Fig. 2 in situ images and the Source Data file (403 at Springer) were not viewed. In situ claims come from the text, captions and Table S7.
- Per-spot labels, Visium images and the processed object are not deposited, so no spot counts could be recomputed beyond Table S4.
- The original in situ papers (Doll 2020, Hueros 1995/1999, Opsahl-Ferstad 1997, Balandin 2005, Gomez 2002, Serna 2001, Muniz 2006) were identified in Europe PMC but not re-read. The draft takes their localizations as cited by Fu and Yuan.
- Zm00001d038758 (ESR) is not in NCBI Gene or UniProt by name. Its ID comes only from the Yuan and Fu tables.
- SWEET15a has no SWEET symbol in NCBI (alias umc1791). The symbol comes from the papers.
- The v4 to v5 mapping is the MaizeGDB crosswalk plus UniProt for multi-model cases; no BLAST.
- CNCB BioProject PRJCA015607 (listed on the Fu website) was not checked.
