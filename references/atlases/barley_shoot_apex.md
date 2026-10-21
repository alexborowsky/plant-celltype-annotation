<!-- Collated from the survey review of barley_shoot_apex (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Barley vegetative shoot apex (vSAM): collated cell-type resources

Collated 2026-10-20 for the plant-celltype-annotation skill. The input was the one review for this group in
`survey/merged_reviews.json` (Demesa-Arevalo 2026, vSAM part; the review is in `DemesaArevalo2026/README.md`).
I added targeted checks of independent barley in situ papers (Zhong 2021, Walla 2021), Ensembl and UniProt ID checks, and pairwise BLAST of the key proteins. The skill was not edited.

Files here:
- `expected_cell_types.tsv`: the cell types expected in a W0–W0.5 vegetative apex, built from grass SAM anatomy. `function_markers` counts the `function` rows in `markers_draft.tsv`. The notes name skill-table markers that can be used through homology.
- `markers_draft.tsv`: 30 rows in the skill schema plus `alt_id`.
  - `ref_gene` is the Morex V3 ID (`HORVU.MOREX.r3.*`).
  - `alt_id` is the Morex V1 ID (`HORVU*Hr1G*`), from Demesa Supp Table 5, for 13 rows.
  - `tissue = shoot_apex`.
  - Field counts were validated with awk (13 fields on all 31 lines).
- `DemesaArevalo2026/`: the dataset review, downloaded tables and derived per-cell labels. Not modified.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| DemesaArevalo2026 (vSAM part) | Demesa-Arevalo E, Dörpholz H, Vardanega I, ... Usadel B, Simon R. *Nature Plants* (2026). doi:10.1038/s41477-025-02176-6. PMC12830361 | Protoplast scRNA-seq (BD Rhapsody WTA), one GP-vSAM library. Resolve Molecular Cartography (MC) on one vSAM section (D2-1, 76 anchor genes). Seurat integration and imputation | 919 scRNA cells (910 high quality), 543 MC cells, 1,462 integrated | `table`: integrated per-cell labels from two small BARVISTA/ARC files (saved as `DemesaArevalo2026/vSAM_D2-1_res1.3_per_cell_labels.tsv`). The scRNA-only 11-cluster atlas (Supp Fig 10A, Supp Table 7) is cluster-level only. vSAM FASTQs are **not deposited** | low for labels, medium-high for MC-validated markers |

This is the only single-cell dataset for barley vSAM. The `barley_inflorescence` group covers the spike part of the **same paper**. Because it is not an independent study, it was not used to raise confidence.

The survey lists no other barley shoot-apex single-cell dataset. A Europe PMC search on 2026-10-20 also found none. The Brachypodium leaf atlas (Plant Cell 2026) is a different species and tissue.

Large objects were recorded but not downloaded. All are in the DataPLANT ARC: `vSAM.csv` (52 MB), `CPM_normalized_vSAM.tsv` (58 MB) and `CPM_imputation.tsv` (71 MB).

## Per-cell-type verdicts (one dataset)

- A = integrated scRNA+MC labels, resolution 1.3 (BARVISTA curated names).
- B = scRNA-only atlas (Supp Fig 10A, Supp Table 7).
- C = expression gates (Supp Table 10).

| Expected cell type | DemesaArevalo2026 label(s) | Verdict |
|---|---|---|
| Epidermis (SAM L1) | A "tunica (L1 epidermis)" (98 scRNA + 131 MC); B cl4 "Meristem tunica"; C Tun-KN1neg | Adopt |
| Epidermis (primordium protoderm) | A "G2 phase" (119 scRNA, 1 MC); B cl8 "Primordia tunica" | A: Revise (it is epidermis, not G2: HvHDZIV8 0.98 vs 0.17, cuticle genes, no cycling genes). B: Adopt |
| Meristem_Tip_L1 | inside the A tunica cluster (HvLOG1) | missing as a cluster; recover by HvLOG1/HvOCL2 subclustering |
| Shoot_Meristem (corpus) | A "meristem corpus with OC" (49 + 124); B cl0, cl5 "Meristem corpus" | Revise: corpus supported (KN1, OCL2, MADS42, AGO). "with OC" is unsupported. B cl5 looks stress-like |
| Organizing_Center, SAM_Central_Zone | none | missing (no WUS1 or CLV3/FCP1 evidence in vSAM) |
| SAM_Peripheral_Zone | A "intercalary meristem" (35 + 81) | Revise: positional hypothesis (HvMND6, HvFEA5); mostly MC cells |
| Lateral_Organ_Primordium | A "leaf primordia" (80 + 39); B cl2 | Adopt (HvCRC, MC-validated) |
| Ground_Tissue / Rib_Meristem / Procambium / Mesophyll | A "vasculature" (116 + 158); B cl7 "Vascular tissue" | Revise: no vascular markers (HvAPL, HvVND1, HvHB8 ≈ 0). The signature is KN1 + PIN1 + MND1 + GLK1/LHCB, i.e. subapical stem plus green leaf tissue. Split in Part B |
| Xylem, Phloem | none | missing (marker genes barely detected) |
| Axillary_Meristem | B cl3 "Bract, AxM" | Reject: defense/stress signature, no AxM marker |
| Organ_Boundary, Stomatal_lineage | none | missing |
| S_Phase / Dividing_cells | B cl6 S-phase, cl10 M-phase (genuine); cl1 "G2-phase" (actually G1/S); cl9 "Cell cycle exiting" | Reject as types; keep as state flags |
| Protoplasting_stress (state) | A "M phase" (251 scRNA = 27%), A "unkown (process-regulation)" (171) | Reject: stress/wound/LEA signatures, almost no MC cells |

Three A clusters ("M phase", "G2 phase", "unknown") are more than 98% scRNA cells. Together they hold 541 of the 919 scRNA cells (59%), so the spatial anchors did not support them.

## Cross-study markers

Only one dataset exists, so cross-study agreement comes from independent barley in situ papers. Genes were compared by ID: Demesa Supp Table 4 cites Zhong 2021 for the HvKN1 and HvLOG IDs, and Walla 2021 gives the V1 ID itself.

| Cell type | Gene (V3) | Symbol | Studies | Effect |
|---|---|---|---|---|
| Meristem_Tip_L1 | 5HG0502720 | HvLOG1 | Demesa 2026: vSAM tunica DE (lfc 5.0, 0.33 vs 0.02) and spike MC. Zhong et al. 2021 PNAS in situ: L1 of IM/TMM | medium → **high**. Both in situ studies are at the inflorescence stage |
| Shoot_Meristem | 4HG0339120 | HvKN1 (= KNOX3/Hooded) | Demesa 2026 vSAM MC (corpus, off in L1 and primordia). Zhong 2021 in situ: non-L1 IM/TMM | already high; agreement noted |
| Ground_Tissue | 7HG0742750 | HvMND1 | Demesa 2026: "vasculature"/stem cluster. Walla et al. 2021 PLoS Genet in situ: inner-SAM patches and proximal leaf primordia (V1 HORVU7Hr1G113480 in both papers) | **conflict**: not raised. Kept low, and the conflict is in `basis` |

## Gaps

These expected types have no `function` marker:
- SAM_Central_Zone: no barley CLV3/FCP1 ID in any source.
- SAM_Peripheral_Zone: only positional cues. HvMND6 (5HG0498240) is enriched in "intercalary meristem" (lfc 4.5), but it is a low-confidence (LC) model that is missing from Ensembl HC, so I did not carry it.
- Rib_Meristem.
- Organ_Boundary.
- Axillary_Meristem.
- Ground_Tissue: HvMND1 only, and it is in conflict.
- Mesophyll: HvGLK1 only (enriched). The photosynthesis genes are LC models.
- Stomatal_lineage.

Several types rest on weak `function` rows:
- Organizing_Center: HvWUS1 is low. It is not in the vSAM MC panel, appears in about 1% of cells, and rice WUS works in axillary premeristems.
- Procambium, Xylem and Phloem: all ortholog-function rows are low and barely detected in vSAM scRNA.

For these types, the skill's arabidopsis_leaf, arabidopsis_root, rice_root and sorghum_leaf tables can be used through homology. The `expected_cell_types.tsv` notes name them.

## Recommended label reference

Use **DemesaArevalo2026**, since it is the only dataset.
- Import the integrated per-cell labels (`vSAM_D2-1_res1.3_per_cell_labels.tsv`, `edgar_` prefix stripped) only for **tunica → Epidermis** and **leaf primordia → Lateral_Organ_Primordium**.
- Use "meristem corpus" as Shoot_Meristem with care.
- Treat "G2 phase" as primordium epidermis.
- Use "vasculature" and "intercalary meristem" as hypotheses only.
- Drop "M phase" and "unknown" as stress.
- The Supp Table 7 cluster markers are better than the integrated labels for cl4/cl8 (epidermis), cl2 (primordia), cl6/cl10 (cycling) and cl7 (stem), but they have no per-cell labels.
- Re-annotation is limited because the vSAM FASTQs are not public. Users with their own barley apex data should use the markers, not the labels.

## Conflicts and corrections

Corrections to the review:
- **HvKN1 identity resolved.** The review left "is 4HG0339120 the Hooded/BKn3 locus?" unverified. Its protein (UniProt A0A287N5B9) is 100% identical over 364 aa to UniProt Q43484, KNOX3/Hooded. Same-symbol trap: UniProt Q717U9, also named barley "kn1", is a different KNOX (57% identity).
- **HvCRC** (A0A8I6Y321) is 88.5% identical to rice DL (Q76EJ0). **HvLOG1** (M0Y4N4) is 70% identical to rice LOG (Q5ZC82). **HvTOB1** is closest to rice YABBY5/TOB1 (77%). **HvWOX4** is closest to rice WOX4 (69%).
- **HvWUS1** (2HG0201080) is closest to OsWUS/TAB1/MOC3 (47%). UniProt states that rice WUS does not maintain the SAM (Tanaka et al. 2015), so the WUS1 Organizing_Center row is `low`.
- **HvLOG1** was raised to high (see Cross-study).
- **HvMND1** conflicts with independent in situ, and was moved from the "vascular" label to Ground_Tissue at low confidence.
- **HvMND6** is an LC model (Supp Table 7 Confidence = low). It is correctly absent from Ensembl HC, so it was dropped, as in the review.
- **The review's UniProt IDs were spot-checked.** The UniProt free-text search for a Morex V3 ID returns unrelated hits: a search for the HvKN1 ID returned a KRR-R protein first. Use `xref:ensemblplants-<ID>.1` instead. All 30 draft genes have a UniProt entry by that xref, and all 30 are Ensembl Plants MorexV3 HC protein-coding genes (REST lookup, throttled).
- Added beyond the review:
  - LTPG-like 7HG0684200, as `characterized_enriched` low (a cuticular-lipid function), not `expression`.
  - Histone H4 1HG0073050, CYCA3-like 4HG0397970 and HvGLK1 3HG0250220.
  - HvPXY, HvHB8, HvWOX4, HvVND1 and HvAPL, all low, with their vSAM non-detection in `basis`.
- Dropped from the review:
  - nsLTP 3HG0297690: pct.2 0.39–0.42, not specific.
  - The eisosome protein 4HG0411400: an uncharacterized M-phase gene.

Grades follow the sibling barley_inflorescence draft for genes the two drafts share (HDZIV8/OCL7a `function` medium, histones and CDKB2 `function` medium), so the two barley tables can be merged.

Label conflicts (paper vs data):
- "M phase" is a stress cluster and "G2 phase" is epidermis. Neither carries cycling genes in the authors' own fold-change table.
- The B cl1 "G2-phase" cluster is G1/S.
- The paper calls HvMND1 a vascular marker (Supp Table 4).
- The paper names HvWOX3 with two IDs (1HG0010970 in the main text, 5HG0467090 in Supp Table 5), so HvWOX3 was not carried.

Naming: I used `SAM_Central_Zone` and `SAM_Peripheral_Zone` (as in `datasets/arabidopsis_shoot_apex`). The barley_inflorescence draft uses `Meristem_Central_Zone`, so harmonize the two before any merge into the skill.

## Overlap with existing skill tables

- The skill has **no barley table** and no shoot-apex table, so no rows overlap for the same species.
- `tissue = shoot_apex` is a new value; the markers README lists `leaf`, `root`, `any`. `datasets/arabidopsis_shoot_apex` uses the same value.
- Generic cell-type names shared with the skill tables: Epidermis, Mesophyll, Procambium, Xylem, Phloem, S_Phase and Dividing_cells.
  - The barley PDF1-like rows correspond to arabidopsis_leaf PDF1 (`characterized_enriched` medium), and the HD-ZIP IV rows to ATML1.
  - The histones and CDKB2 correspond to the arabidopsis_leaf and rice_root cycling rows.
- The meristem names (Shoot_Meristem, Meristem_Tip_L1, Organizing_Center, Lateral_Organ_Primordium, Ground_Tissue) follow the unpublished barley_inflorescence and arabidopsis_shoot_apex drafts.
- `requires=grass` is set on HvCRC and HvTOB1. The DL midrib and TOB roles are grass-specific, and Arabidopsis CRC is a carpel/nectary gene.

## Could not verify

- I found no vSAM-stage in situ for HvLOG1 or HvKN1. The Zhong 2021 in situ images are of IM/TMM. Müller 1995 and Williams-Carrier 1997 (Hooded) are about awns and lemmas, and I read only their abstracts.
- Demesa shows vSAM MC images only for KN1, the four tunica genes, OCL2 and CRC (Fig 3a,f). For MADS42, PIN1, MND1, MND6 and CYCA3-like, the paper says only that they are in the panel; I read no images.
- HvMND4/HvMND6 naming: Walla 2021 calls the CYP78A PLA1 homolog "MND4", while Demesa uses "HvMND6" for 5HG0498240. I did not check whether these are the same gene (DDBJ LC593237 vs Morex V3).
- I did not verify by sequence that 6HG0615550 is in the PIN1 clade; it rests on the ST5 annotation "PIN1".
- Not accessed (from the review): vSAM FASTQs (not deposited), per-cell labels and cell counts for the scRNA-only atlas, the MC probe-code key, and the authors' code (available on request). No paywall or login was hit, and I contacted no one.
