<!-- Collated from the survey review of rice_embryo (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Rice germinating embryo: group collation (Part A, Steps 1-4)

Date: 2026-10-20. Desk collation only; no in-data check (Step 3b).
Inputs: one dataset review (`Yao2024/`, from `survey/merged_reviews.json`) plus a literature check of the markers it carries and of classic rice embryo in situ markers.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Expected types from germinating-embryo anatomy (6-48 HAI), written before reading the labels; `function_markers` counted after the draft table was built |
| `markers_draft.tsv` | 30 rows, skill schema plus `alt_id`. `ref_gene` = **RAP-DB** IDs (`Os..g.......`, as in Yao 2024); `alt_id` = MSU7 `LOC_Os` (empty for 5 uncharacterized genes with no MSU mapping in Oryzabase/UniProt). This is the **reverse** of `rice_root.tsv` (MSU in `ref_gene`); use `map_markers.py --id-column alt_id` for MSU-ID data. `tissue` = `embryo`, a value not yet in the skill's vocabulary (`leaf`, `root`, `any`) |
| `Yao2024/` | The dataset review (README, supplements, per-bin labels, UniProt check). Left as written |

## Datasets

| Dataset | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|
| Yao J et al. 2024 *Dev Cell* 59:2320, doi:10.1016/j.devcel.2024.05.016 (Nipponbare, stripped embryos, 6/24/36/48 HAI) | Stereo-seq at Bin50 (~25 um bins; one chip per time point), plus BD Rhapsody protoplast scRNA-seq | 38,678 labelled bins in 14 sections (not cells; a plumule bin holds ~9 cells); 27,070 scRNA cells, unlabelled | RAP-DB / IRGSP-1.0 | `table`: per-bin label TSVs for all 14 sections (STOmicsDB STT0000049), merged in `Yao2024/`. No scRNA labels, no segmented-cell labels, no DE table | medium |

This is the only dataset reviewed for this group. A broad Europe PMC search (2026-10-20) found no second single-cell or spatial atlas of the **germinating** rice embryo. Related, not reviewed:
- Liu Y et al. 2026 *J Integr Plant Biol*, doi:10.1111/jipb.70373: snRNA-seq of **developing** rice caryopses (67,922 nuclei), with ISH and promoter-GUS validation and an embryo-endosperm interface population. A candidate second dataset for embryo and scutellum markers at an earlier stage.
- Peirats-Llobet M et al. 2026 *Plant Cell*, doi:10.1093/plcell/koag120: 4-D spatial atlas of barley grain development and germination (a different species; not usable for ID-level agreement).

## Verdicts per expected type

A = Adopt, R = Revise, X = Reject, - = not annotated. Only one dataset, so this is one column.

| Expected type | Yao 2024 label | Verdict | Note |
|---|---|---|---|
| Scutellar_Epithelium | SCL1 | A | REP1 ISH, AMY1A |
| Scutellar_Parenchyma | SCL2 (+ BESCL2) | A (SCL2); R (BESCL2, positional/stress subset) | OsMFT2 FISH + KO, early stage only |
| Scutellar_Subepithelium | SCL1-2 | R (hypothesis) | metallothioneins, OsCYS9 ISH; histone-high |
| Procambium (scutellum) | SCL3 | R | position-based; pan-vascular markers; SRZ1 ID conflict |
| Epiblast | EP-CR (merged) | R | qLTG3-1, OsHyPRP14 FISH |
| Coleorhiza | EP-CR (merged) | R | merged with epiblast |
| Coleorhiza_Epidermis | EP-CRL1 | R (hypothesis) | absent at 6 HAI; OC1 is seed-wide |
| Coleoptile_Epidermis | COL1 | A | outer and inner epidermis merged |
| Coleoptile_Parenchyma | COL2 | A | Os02g0587000 ISH; vascular bundles not split |
| Shoot_Apical_Meristem, Leaf_Primordium, shoot Epidermis | PL | R (region) | split de novo |
| Guard, Mesocotyl | - | - | not annotated |
| Radicle types (Epidermis, Exodermis, Cortex, Endodermis, Pericycle) | RA | R (region) | whole radicle merged |
| Stele / Xylem / Phloem | RAL3 | X | 24 HAI chip only |
| Columella / Lateral_Root_Cap | RC | R | position only, no cap marker |
| Quiescent_Center | - | - | not annotated |
| Dividing_cells / S_Phase | - (PL chromatin GO; SCL1-2 histone-high) | - | not separated |
| (no expected type) | LS "lateral scale" | R | not a standard rice embryo type; PR10/defense markers suggest a state |

## Cross-study markers

Agreement here means the same gene ID localized in Yao 2024 and in an independent earlier study (no second single-cell dataset exists).

| Type | Gene (RAP / MSU) | Support | Confidence |
|---|---|---|---|
| Scutellar_Epithelium | AMY1A Os02g0765600 / LOC_Os02g52710 | promoter-GUS first in scutellar epithelium (Itoh 1995 *Plant Physiol*); embryo L1-epithelium in situ marker (Kamiya 2003 *Plant Cell Physiol*); SCL1 in Yao 2024 | function, high |
| Epiblast | qLTG3-1 Os03g0103300 / LOC_Os03g01320 | promoter-GUS in the epiblast covering the coleoptile, plus a germination function (Fujino 2008 *PNAS*); EP-CR in Yao 2024 | function, high |
| Epidermis (shoot) | ONI1 Os03g0181500 / LOC_Os03g08360 | in situ in the outermost layer of SAM and lateral organs, and the mutant has an aberrant epidermis (Ito 2011 *Plant J*); COL1 in Yao 2024 | function, high |

ROC1 (Ito 2002, Kamiya 2003) is not counted: both papers are from the same group, and Yao 2024 did not show it.

Grading of the other rows: the six Yao ISH/FISH genes (REP1, OsCYS9, OsMFT2, Os02g0587000, OsLTP1.2, OsHyPRP14) are `characterized_enriched` medium, except REP1 (`function` medium: reserve-mobilizing protease, but known mainly from aleurone). The spatial-only characterized genes are `characterized_enriched` low, and uncharacterized spatial genes are `expression` low. Five literature genes (OSH1, ROC1, OsPNH1, QHB, OsSCR1) were added to fill gaps, from embryo in situ papers; their IDs come from UniProt and Oryzabase (both list RAP and MSU IDs for these entries). CycB1;1 and OsPCNA state rows are copied from `rice_root.tsv`.

## Gaps (no `function` marker in the draft or in `rice_root.tsv`)

Scutellar_Parenchyma, Scutellar_Subepithelium, Coleorhiza, Coleorhiza_Epidermis, Coleoptile_Epidermis as a type distinct from shoot epidermis (outer vs inner), Coleoptile_Parenchyma, Guard (coleoptile stomata), Leaf_Primordium ground tissue, Mesocotyl, Lateral_Root_Cap, Cortex, Aleurone (contamination check). The radicle types rely on root-tip markers from `rice_root.tsv` that were not validated in embryos.

## Recommended label reference

Yao 2024 bin labels, used as **spatial region priors** only: adopt SCL1, SCL2, COL1, COL2. Use PL, RA and EP-CR as organ regions to split de novo. Do not use RAL3 (chip-specific), and treat SCL1-2, BESCL2, EP-CRL1, LS and RC as hypotheses. The labels are 25 um bins, so they cannot be used as a per-cell benchmark. The scRNA set has no labels.

## Conflicts and corrections

- **Citations in the Yao review.** The qLTG3-1 cloning paper is Fujino et al. 2008 *PNAS* 105:12623 (doi:10.1073/pnas.0805303105), not *Nat Genet*. ONI1 is Ito et al. 2011 *Plant J* 66:680 (doi:10.1111/j.1365-313X.2011.04530.x), not *Plant Cell*. Both corrected in the draft.
- **qLTG3-1 location.** Fujino 2008 puts its GUS signal in the epiblast and in the aleurone over the embryo, not in the coleorhiza. The row is therefore `Epiblast`, while Yao's merged EP-CR markers (OsHyPRP14/20) are `Epiblast_Coleorhiza`.
- **ID and symbol errors in Yao 2024** (kept from the review, re-checked in UniProt/Oryzabase): OsSAG12-1/REP1 is printed as Os10g0907600 in Fig 3 (no such gene; Os01g0907600 is correct). SRZ1: text gives Os03g0836200 (Oryzabase OsRZ1), Fig 3A gives Os02g0203700 (Oryzabase LS1/OsSRZ1), so the row was **left out**. Dotplot "OsHyPRP17" is OsHyPRP20 by ID. Paper "LTP1" Os11g0115400 is Oryzabase LTP5. Paper "OsCYS9" Os04g0350100 is OsCPIP10 / Oryzacystatin X. OsMT2b Os05g0111300 is MT2C in UniProt. Paper "SAMDC1" is Oryzabase SAMDC4. The Discussion calls OsMFT2 a mannitol transporter, contradicting its PEBP identity.
- **REP1 and AMY1A are aleurone genes too.** In stripped-embryo data they mark the scutellar epithelium, but adhering aleurone would also express them.
- **OsSCR1** marks the radicle endodermis but also stomatal and ligule lineages in leaf primordia (Kamiya 2003 *Plant J*), so in plumule cells it does not mean endodermis.
- **Name clash.** `Epidermis` rows here are shoot epidermis (ONI1, ROC1); `Epidermis` rows in `rice_root.tsv` are root epidermis. Separate by organ (plumule/coleoptile vs radicle) before using them.
- **Review markers not carried into the draft:** Os02g0203700 (SRZ1 ID conflict); Os01g0914000 (RAL3, chip-specific label); OC1 Os01g0803200 (seed-wide cystatin); Os03g0734100 (EP-CRL1 hypothesis, uncharacterized); RPR10b/PBZ1 Os12g0555200 (LS, defense gene for an undefined label); Os07g0120650 (shown for both EP-CRL1 and LS).

## Overlap with existing skill tables

`rice_root.tsv` is the only other rice table. Four genes are shared by ID: QHB (Quiescent_Center), OsSCR1 (Endodermis), CycB1;1 (Dividing_cells), OsPCNA (S_Phase), all with the same cell type. The radicle types in `expected_cell_types.tsv` count `rice_root.tsv` function markers (qSOR1, OsCASP1, OsFRDL1, OsSHR1, OsCESA4, OsSUT1, CDKB2;1, H2A); these were validated in root tips, not in embryos. No overlap with the sorghum or Arabidopsis tables, which are in other ID systems.

## Could not verify

- The Yao figure gene panels (dotplot Fig 2C, S2C) were read from rendered images in the review; there is no DE table, so marker specificity values could not be checked.
- RAP-to-MSU mapping for the uncharacterized genes Os11g0496500, Os09g0272600, Os10g0361300 and Os02g0587000 (no MSU ID in Oryzabase or UniProt; RAP-DB download refuses scripted access).
- Embryo-specific localization of REP1 outside Yao 2024: the abstracts found (Shintani 1997, Ho 2000, Sutoh 2003) describe aleurone and whole-seed expression only.
- The full texts of the literature papers were not read; the evidence above is from their PubMed abstracts.
- The ScienceDirect/cell.com HTML of Yao 2024 (bot check) and the REGSTA portal (HTTP 404), as recorded in the review. Large objects (bin50 GEMs 60-147 MB, scRNA FASTQ) were not downloaded.
