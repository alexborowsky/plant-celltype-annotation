<!-- Summarized from the maintainers' review of rice_root (Part A review, 2026-10-19) plus the skill test B (2026-10-22). Written directly in the skill: survey/sync_to_skill.py skips rice_root, so this file is not regenerated. Marker table: references/markers/rice_root.tsv (core) -->

# Rice root (Oryza sativa) single-cell datasets

Six datasets were reviewed from the papers (Step 3a). Verdicts are desk review; re-check in data. The marker table built from them is the core `references/markers/rice_root.tsv` (MSU7 `ref_gene`, RAP-DB `alt_id`). Convert IDs with `references/annotation/rice_msu_rap.tsv.gz`.

## Datasets

| Dataset | Material | Protocol | Cells (root) | Gene IDs | Per-cell labels | Label grain |
|---|---|---|---|---|---|---|
| Zhang 2021 *Nat Commun* 12:2053, 10.1038/s41467-021-22352-4 (ZH11) | radicle tip 1 cm, 5 d | protoplast, 10x v2+v3 | 27,469 | RAP-DB | none (re-cluster SRA, or EBI SCEA E-ENAD-52) | 21 clusters |
| Liu 2021 *Mol Plant* 14:384, 10.1016/j.molp.2020.12.014 (Nip, 93-11) | crown root tip 5 mm, 3 d | protoplast, 10x v2, 1 library per cultivar | 10,968 + 12,564 | MSU7 | RCAR (see recipe below); GEO GSE146034 | 8 tissue classes |
| Wang 2021 *J Genet Genomics* 48:881, 10.1016/j.jgg.2021.06.001 (Nip) | primary + crown root tips 2 cm, 14 d; stress series | protoplast, 10x v3 | 8,538 (+8,109 seedling) | MSU7 | Table S13 (mmc2.xlsx); the 41% of root cells in unknown clusters are absent | 9 types, co-clustered with leaf |
| Zhu 2025 *Nature* 642:721, 10.1038/s41586-025-08941-z (Kitaake) | primary root tip ~1 cm, 2-5 d; gel/soil/compaction | protoplast, 10x v3 | 79,743 atlas (includes Zhang reprocessed) | MSU7 | only inside the 35 GB Seurat rds (GSE251706) | 11 types + zone |
| Wang 2025 *Nature* 644:722, 10.1038/s41586-025-09251-0 (Nip) | crown root apex 5 mm, 7-10 d | nuclei multiome | 31,108 | MSU7 (portal: RAP-DB) | portal extract (elabcaas.cn/scmr); full rds 5.1 GB on GEO GSE232863 | 9 labels |
| Yan 2025 *Nat Plants*, 10.1038/s41477-025-02106-6 (Nip) | seminal + crown root tips 2 cm, 14 d | scATAC (+ RNA labels, Slide-seq) | ~9.2k crown-root ATAC nuclei; 17,071 RNA cells | MSU7 | Tables S1 (scATAC cells) and S3 (snRNA cells) | finest: QC, columella, stele initials, proto/metaxylem |

**Liu 2021 label recipe.** RCAR (https://elabcaas.cn/rcar/, the authors' rice root atlas) offers per-cell CSV exports under `downloads/` (barcode, `cluster`). The downloads page returns 403 to scripts; use a browser. Append `-1` to the RCAR barcodes to join the GEO GSE146034 barcodes (100% of 610 Nip cells matched in test B). The survey's export holds only 610 Nip and 643 93-11 cells; whether RCAR gives the full table was not checked. RCAR's class names are finer than the paper's: Liu's "epidermis" is `epidermis_exodermis_sclerenchyma`, and "epidermis near root hair" is a separate class.

## Provisional verdicts by cell type

A = Adopt, R = Revise, X = Reject/relabel, - = not annotated. Desk review; re-check in data.

| Expected type | Zhang 2021 | Liu 2021 | Wang 2021 | Zhu 2025 | Wang 2025 |
|---|---|---|---|---|---|
| Trichoblast | A (CSLD1 reporter) | A (root hair) | R (epidermis unsplit) | A gel only | R ("near root hair") |
| Atrichoblast | A (EXPA8 reporter) | - (in "epidermis") | - | A | - |
| Epidermis (unsplit) | - | R (merged with exodermis + sclerenchyma) | R (merged) | - | A provisional |
| Exodermis | A provisional | - (merged) | - (merged) | A | R |
| Sclerenchyma | R | - (merged) | - (merged) | R | R |
| Cortex | A | R | R (17-19 ok) | A | A provisional (LTPL120 mutant) |
| Endodermis | A (CASP1 cl.13); R (cl.2) | R | R | A provisional | R |
| Pericycle | A | - (in stele) | A provisional | R ("vascular tissue") | - (in vascular) |
| Xylem | A (2 stages, unsplit) | A (metaxylem, few cells) | A (XCP2) | X protoxylem; R metaxylem | - (in vascular) |
| Phloem | R (unsplit) | - (in stele) | A (unsplit) | R (unsplit) | - (in vascular) |
| Procambium | - | - | R | - | - |
| Root cap / columella / LRC | - (R "cap junction") | R (0.3%, unsplit) | - | R/X | X (G2/M markers) |
| QC / stem cell niche | - | - | - | X ("SCN" = meristem zone) | - |
| Cell-cycle states labelled as types | 4 meristem clusters + EMC | - | "Endodermis-cortical initial" | "SCN/Meristem" | "Meristem" (S), "Root cap" (G2/M) |
| Catch-all / unresolved | 2 "vascular cylinder" (stress) + 1 undefined | - | 41% unknown | "Mature root cells" 30-41% | - |

## In-data notes on Liu 2021 (skill test B, 2026-10-22; one run, re-check in data)

- Liu's endodermis is a young, ribosome-high cluster; only a CASP1/MYB36a/SCR1 subcluster of it is endodermis.
- Liu's large "stele" island has no stele function signal (OsSHR1 0%) and carries Zhu 2025 spatial exodermis genes (OsMST1 39-65%, LOC_Os03g02460). It may be exodermis rather than stele; unresolved.
- The `epidermis_exodermis_sclerenchyma` block has a strong secondary-wall programme. OsSWN2+ cells are sclerenchyma. CESA4/7/9, ONAC073/OsSND2 and LOC_Os08g38170 also mark fibres, so they do not establish xylem on their own: a xylem call needs XCP/VND or cell-death genes (XCP2-like LOC_Os01g73980). Expect few xylem cells in a 5 mm tip.
- Clusters with OsHyPRP06 at 58-75% next to cortex are cortex (low) rather than Unknown.
- Benchmarks on Liu with `rice_root.tsv` are partly circular: OsHyPRP06, XCP2-like, RCLEA2 and OsCSLD1 rows cite Liu.

## Markers supported across studies

| Type | Gene (MSU / RAP) | Support |
|---|---|---|
| Trichoblast | OsCSLD1 LOC_Os10g42750 / Os10g0578200 | function; reporter (Zhang, Zhu); marker in Liu, Zhu, Zhang |
| Xylem (TE) | XCP2-like LOC_Os01g73980 / Os01g0971400 | in situ (Liu; Wang 2021); marker in Zhu. Zhang's "XCP2" is a different gene (Os05g0108600 / LOC_Os05g01810) |
| Sclerenchyma | OsSWN2/ONAC029 LOC_Os08g02300 / Os08g0115800 | in situ (Zhang); spatial (Zhu); also xylem |
| Cortex | OsLTPL120 (= OsHyPRP06) LOC_Os04g46810 | in situ (Liu, Wang 2025) + mutant (Wang 2025); marker in Zhu |
| Cortex | RAI1/OsbHLH003 LOC_Os03g04310 / Os03g0135700 | in situ (Zhang); spatial (Zhu); protoplasting-sensitive per Wang 2021 |
| Endodermis | OsCASP1 LOC_Os04g58760 / Os04g0684300 | function; marker in Zhang, Wang 2021, Wang 2025 |
| Endodermis | LOC_Os10g06680 | marker in Zhang, Wang 2021, Wang 2025, Zhu; also top gene of Wang 2021 pericycle |
| Atrichoblast | OsEXPA8 LOC_Os01g14650 / Os01g0248900 | reporter (Zhang); marker in Zhu |
| Exodermis | OsMST1 LOC_Os04g37980 / Os04g0452700 | spatial (Zhu); marker in Zhang |
| Pericycle | Os07g0634400; LOC_Os08g37300 | in situ (Zhang; Wang 2021) |
| Phloem | SUT1 LOC_Os03g07480, PP2-A1 LOC_Os01g06500 | literature function (Wang 2021) |
| G2/M state | CYCB1;1 LOC_Os01g59120; CDKB2;1; KNOLLE LOC_Os03g52650 | function |
| S-phase state | core histones (H2A Os03g0279200 etc.) | function |

## Recommended label reference

- **Crown root tip, cell-level labels:** Liu 2021 via RCAR for root hair, atrichoblast ("near root hair"), cortex and root cap; treat its stele, endodermis and outer-layer classes as hypotheses (see the in-data notes).
- **Finest stele and tip types:** Yan 2025 (QC, columella, stele initials, proto/metaxylem; public cell tables).
- **Spatial validation of layers:** Zhu 2025 (exodermis, sclerenchyma, cortex genes), but its labels are only in a 35 GB object.
- Use Zhang 2021 reporters (CSLD1, EXPA8) and in situ genes as markers; its cluster labels include stress and cell-cycle clusters labelled as types.

## Corrections

- QHB/OsWOX5 is LOC_Os01g63510 / Os01g0854500. LOC_Os04g56780 (given for Wang 2025) is WUS/MOC3.
- OsFRDL1 (LOC_Os03g11734) is a pericycle MATE in Zhang 2021, but Zhu 2025 used it as a root-cap marker.
- LOC_Os04g46810 is OsHyPRP06 in Oryzabase and Zhu 2025, and OsLTPL120 in Wang 2025.
- Zhang 2021's chromatin data is bulk ATAC on sorted nuclei, not scATAC.
