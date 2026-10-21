<!-- Collated from the survey review of rice_ovule (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Rice pistil/ovule (1 day before anthesis): marker resources

Group collation for the plant-celltype-annotation skill, written 2026-10-20. It is based on one dataset review (`Li2023/README.md`, left unchanged). Nothing in the skill was edited.

Files in this folder:

- `expected_cell_types.tsv`: written from rice pistil anatomy, not from the published labels. `function_markers` counts the skill tables' `function` rows that apply to a rice pistil (tissue `any`, traits grass/C3). The draft's counts are in `notes`.
- `markers_draft.tsv`: 33 rows. It uses the skill schema plus `alt_id`, with the same ID convention as `rice_root.tsv` and the `rice_seed` draft: `ref_gene` = MSU7 `LOC_Os` (or `-`), `alt_id` = RAP-DB. The dataset itself uses RAP IDs, so map with `map_markers.py --id-column alt_id`. 9 rows have no MSU ID (8 uncharacterized genes and one ncRNA), but every row has a RAP ID. `tissue` = `pistil`, except the two cell-cycle `function` rows, which are `any`.
- `marker_table/uniprot_id_check_2026-10-20.tsv`: a UniProt (taxon 39947) lookup for all 33 RAP IDs.

## Datasets

| Dataset | Citation | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Li2023 | Li C, Zhang S, Yan X, Cheng P, Yu H. *Dev Cell* 58:694-708.e4 (2023), doi:10.1016/j.devcel.2023.03.004; GEO GSE208432 | Nuclei: PI-stained, FANS-sorted, 10x 3' v3.1 (2N) and 3' LT v3.1 (1N); Cell Ranger 6.1.2 with `--include-introns` | 8,173 2N nuclei (2 replicates; median ~700 genes per nucleus), plus 989 putative 1N nuclei that have no per-cell table | RAP-DB IRGSP-1.0 | `table` (Table S2, `Li2023/labels_Li2023_TableS2.tsv`) | medium |

These are whole unfertilized pistils (stigma, style, ovary wall, ovule), with some stamen carry-over. The tissue name is `pistil`, even though the group folder is called `rice_ovule`.

## Verdict matrix (published label to canonical type)

A = Adopt, R = Revise, X = Reject. Only one dataset exists, so this is one column.

| Expected type | Li2023 (cluster, n, %) |
|---|---|
| Stigma | A: sti (cl5, 667, 8.2%) |
| Style | R: inside "ow" (cl4, 681) |
| Basal_Style | R: inside "ow" (cl6, 649) |
| Ovary_Wall | R: inside "ow" (cl7, 622; young-carpel state) |
| Carpel_Epidermis (outer) | R: inside "ep" (cl1 1,060 + cl2 1,052) |
| Carpel_Inner_Epidermis | R: inside "ep" (cl9, 461; mixed with outer integument) |
| Inner/Outer_Integument | R: inside "ov" (cl3, 864; integuments not split) |
| Ovule (young stage) | R: inside "ov" (cl10, 167) |
| Chalaza | A: ch (cl8, 504, 6.2%; probably includes the ovular vascular region) |
| Nucellus | R: nu (cl0, 1,237, 15.1%; provisional, weak markers, also absorbed the 1N nuclei) |
| Ovular_Vascular_Trace | R: C12 (66, 0.8%; unassigned by the authors; candidate) |
| Dividing_cells (state) | X as a type: C13 (47, 0.6%; G2/M) |
| Stamen (contaminant) | X as a pistil type: sta (cl11, 96); keep the label to remove these nuclei |
| Transmitting_Tract, Nucellar_Epidermis, Xylem, Phloem, Egg_Cell, Synergid, Central_Cell, Antipodal | not annotated |

## Cross-study markers (by gene ID)

This group has no second pistil dataset. "Cross-study" here means agreement between Li 2023 and an independent dataset in another resource group (or the characterizing paper) for the same cell type.

| Gene (RAP / MSU) | Type | Support | Confidence effect |
|---|---|---|---|
| DL Os03g0215200 / LOC_Os03g11600 | Carpel | carpel-identity mutant + in situ (Yamaguchi 2004); Li cl7; Wang 2025 Nature "Stigmata" (= carpel/pistil) cluster DE (`rice_inflorescence/Wang2025`) | raised medium to high |
| SPW1/OsMADS16 Os06g0712700 / LOC_Os06g49840 | Petal_Stamen_Organ | B-class mutant (Nagasawa 2003); Li cl11 (stamen residue); Wang 2025 lodicule/stamen clusters | raised medium to high |
| OsMADS13 Os12g0207000 / LOC_Os12g10540 | Ovule | ovule-identity mutant + in situ (Dreni 2007); in situ Li cl10; Wang 2025 in situ probe for a pistil cluster labeled "stigma" | already high |
| CycB1;1 Os01g0805600, KNOLLE/SYP111 Os03g0736500 | Dividing_cells | Li C13 DE; same rows in `rice_root.tsv`, the `rice_seed` draft and the `rice_embryo` draft | already high |
| OsMADS29 Os02g0170300 / LOC_Os02g07430 | Nucellus | function (Yin and Xue 2012); Li Fig. 5E feature plot; Liu 2026 JIPB nucellus panel (`rice_seed` draft) | not raised (medium): Li gives only a feature plot, and the gene is also in the ovular vascular trace |
| OsMADS58 Os05g0203800 | Stamen_Carpel_Organ | Li cl2; Wang 2025 carpel cluster | not raised: different compartments, organ-level gene |

There are 6 cross-study genes (DL, SPW1, OsMADS13, CycB1;1, KNOLLE, OsMADS29). Of these, 2 had their confidence raised by this collation.

## Marker draft summary

The draft has 33 rows: 8 `function`, 16 `characterized_enriched`, 9 `expression`. Most Li 2023 markers are uncharacterized or functionally unrelated genes, but almost all have in situ validation in the paper. Uncharacterized genes with in situ support are `expression`. They are `medium` when highly specific (Os01g0837700, Os03g0773300, Os05g0130600) and `low` when specificity is weak. `requires=grass` is set on DL (carpel specification is a grass DL role; Arabidopsis CRC is not a carpel-identity gene) and on OsMADS29 (the grass B-sister nucellus role; Arabidopsis ABS/TT16 acts in the endothelium). No `function` marker is stigma-, style-, epidermis-, integument- or chalaza-specific. Those types rest on in situ `characterized_enriched` rows only.

## Gaps (no validated `function` marker)

- Stigma, Style, Basal_Style, Carpel_Epidermis, Carpel_Inner_Epidermis, Ovary_Wall, Integument (inner and outer), Chalaza: in situ markers only, from one study.
- Transmitting_Tract, Nucellar_Epidermis: no marker at all.
- Embryo sac (Egg_Cell, Synergid, Central_Cell, Antipodal): no marker. These nuclei are mostly haploid and fall outside the 2N gate. Li's 1N library was only projected onto cl0. These types are Step 4 search targets: known rice genes include egg- and synergid-expressed genes from laser-capture studies, which were not curated here.
- Xylem, Phloem, Phloem_Companion, Ovular_Vascular_Trace: only skill rows with tissue `any` (via Arabidopsis homology) or one uncharacterized in situ gene (Os05g0130600).
- Nucellus: one `function` row (OsMADS29, post-anthesis peak) and two weak `expression` rows.

## Recommended label reference

Li2023 Table S2 (`Li2023/labels_Li2023_TableS2.tsv`; barcodes `rep1_`/`rep2_` + GEO barcode). It is the only dataset, and its labels are small and public. Adopt `sti` → Stigma and `ch` → Chalaza. Split `ow` into cl4 Style, cl6 Basal_Style and cl7 Ovary_Wall (young). Split `ep` into cl1/cl2 Carpel_Epidermis and cl9 (mixed inner epidermis/outer integument). Split `ov` into cl3 Integument and cl10 Ovule (young). Treat `nu` as provisional Nucellus, `C12` as a candidate Ovular_Vascular_Trace, `C13` as Dividing_cells (state), and `sta` as contaminant. Use the Table S1 cluster numbers. Table S5's cluster column is wrong.

## Conflicts and corrections to the review

- **"OsMTP11" is a symbol error in the paper.** The probe and Table S1 row are Os01g0837700, an unnamed gene (UniProt Q943N0; "Hypothetical genes" in Table S1). Oryzabase gives OsMTP11/CS1 as the adjacent locus Os01g0837800 (LOC_Os01g62070). The draft keeps the RAP ID from the paper's tables, sets the symbol to `- (paper: 'OsMTP11')`, and leaves the MSU ID empty. The review's symbol "OsMTP11" should not be used.
- **OsWDA1 is not stigma-specific outside pistil samples.** Wang 2025 Nature (rice_inflorescence) shows it by in situ in the anther/hull epidermis, and its characterized role is anther cuticle (Jung 2006). It is a stigma marker only when the sample is a pistil.
- **OsCP1 (Os11g0255300 / LOC_Os11g14900, UniProt name RepA)** marks stamen residue in Li, but in Wang 2025 it is the in situ palea marker (SP3-4) and the top gene of the SP8 "ovary wall" cluster. Its confidence was lowered to `low`.
- **OsMADS6/MFO1** is also expressed in palea, lodicule and floral meristem (Ohmori 2009; Zong 2022 floret cluster), so it is integument-specific only within pistil samples.
- **Evidence grading changed from the review.** KNOLLE and CycB1;1 were changed from `characterized_enriched` to `function` (state), to match `rice_root.tsv`. OsYAB7 was changed from `expression` to `characterized_enriched` (low), because it is a named, characterized gene with enrichment only.
- **Synonyms.** Oryzabase lists OsHyPRP18 (Os06g0643500) as OsHyPRP18/OsHyPRP19. OsATL32 (Os02g0686100) is also OsRING329. OsCEL9A is also OsGLU5.
- **Supplement problems** (from the review): Table S5's cluster column disagrees with Table S1, and Table S4's 1N/2N percentages and symbols (MEL2, DLC1) are unreliable. OsMADS29's ID came from Table S4 and was confirmed in UniProt (Q6H711, LOC_Os02g07430).

## Overlap with existing skill tables (rice)

- `rice_root.tsv`: shares only CycB1;1 (LOC_Os01g59120) and KNOLLE/SYP111 (LOC_Os03g52650) under Dividing_cells. None of the root cell types occur in the pistil, and the root rows have tissue `root`.
- No rice flower, pistil or ovule table exists in the skill. Related drafts in the resources folder: `rice_seed` (OsMADS29 Nucellus; Ovular_Vascular_Trace rows for the post-fertilization trace) and `rice_inflorescence` (Wang 2025, Zong 2022; DL, OsMADS13, OsMADS58, SPW1, WDA1, OsCP1, OsMADS6 appear there).
- Cell-type names follow the existing tables and drafts: Chalaza, Nucellus, Ovule, Transmitting_Tract, Carpel, Carpel_Epidermis, Stamen_Carpel_Organ, Petal_Stamen_Organ, Ovular_Vascular_Trace, Dividing_cells. These names are new: Stigma, Style, Basal_Style, Ovary_Wall, Carpel_Inner_Epidermis, Integument, Stamen, Antipodal.

## Could not verify

- MSU IDs for 9 genes (Os01g0837700, Os03g0773300, Os08g0485400, Os09g0517000, Os03g0803066, Os05g0454500, Os05g0366900, Os05g0130600, Os04g0496300). They are absent from UniProt, Oryzabase and Ensembl xrefs, and RAP-DB conversion files were not fetched (scripted access refused).
- Os03g0803066 (ncRNA) is not in UniProt or Oryzabase. Its ID comes only from the paper's Tables S1 and S5.
- In situ images and dot plots were not viewed. Specificity values come from Table S1 (`Li2023/insitu_validated_markers_TableS1.tsv`).
- The Wang 2025 and Liu 2026 support was taken from the existing reviews in `rice_inflorescence/Wang2025` and `rice_seed`. Those papers were not re-read here. The OsMADS29 original (Yin and Xue 2012) and Dreni 2007 were checked only for their citations (Europe PMC), not re-read.
- No in-data check (Step 3b) was done. Nothing large was downloaded.
