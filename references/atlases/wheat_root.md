<!-- Collated from the survey review of wheat_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Wheat root single-cell datasets: collated marker resources (group `wheat_root`)

Date: 2026-10-20. Paper-only work (Part A, Steps 1-3a, plus a Step 4 marker table). No in-data check (Step 3b).

Files in this folder:
- `expected_cell_types.tsv`: written from wheat root-tip anatomy before the labels were read. `function_markers` counts the `function` rows in `markers_draft.tsv` (wheat IDs). The `notes` column gives the extra `function` rows available by homology from `arabidopsis_root.tsv` and `rice_root.tsv`, after `grass,C3` trait filtering.
- `markers_draft.tsv`: 47 rows in the skill schema plus `alt_id` (83 rows after the 2026-10-20 update below). `ref_gene` is IWGSC RefSeq **v2.1** (`TraesCS..03G.......`), the ID system of Ke 2025. `alt_id` is **v1.1** (`TraesCS..02G......`), used by Zhang 2023, Ensembl Plants and UniProt. For v1.1 data, run `map_markers.py --id-column alt_id`. Field counts are validated (13 columns on every line). This is a draft and has not been copied into the skill.
- `Ke2025/`: the full review (README, supplements, ID map). I did not change it.
- `Zhang2023_check/`: files I used for the cross-study check: Table S2 (top-100 markers per cluster), Table S14 (in situ probes), Fig 1, the full-text XML, a Ke-vs-Zhang marker overlap matrix, and UniProt checks for the added IDs. Zhang 2023 did **not** get a full Part A review.

## Datasets

| Dataset | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|
| Ke Y ... De Rybel B. 2025 *Cell Reports* 44:115240, doi:10.1016/j.celrep.2025.115240 (GEO GSE270342, GSE271725) | Protoplast scRNA-seq, 10x 3' v3.1 (LeviCell clean-up), plus untargeted Stereo-seq on cell-segmented cross-sections. Chinese Spring, 0.5 cm tips of primary and lateral roots, 15 d, soil | 7,388 cells, 3 reps, 15 clusters | v2.1 (incl. LC) | `large_object`: per-cell labels only in a 557 MB Seurat RDS; cluster-to-label map public | medium (reviewer: medium-high) |
| Zhang L ... Yan W. 2023 *Genome Biol* 24:65, doi:10.1186/s13059-023-02908-x (CNCB GSA CRA008788) | Nuclei snRNA-seq (FACS-sorted, 10x) plus snATAC. AK58, 0.5 cm root tips, 1/2 MS plates | 6,875 nuclei, 22 clusters | v1.1 (v1.0 parts genome) | not checked (cross-check only) | not graded. Used only to check Ke's markers by ID. RNA in situ for 4 probe sets (DAR2, XCP1, WAT1, G-H2AX) |

## Verdict matrix per cell type

Ke verdicts are from the review. Zhang column: the Zhang cluster that shares the most specific Ke DEGs (Ke Table S4 genes with pct.1 > 0.3 and pct.2 < 0.15, converted to v1.1, compared with Zhang Table S2 top-100 lists; counts are in `Zhang2023_check/Ke_specificDEG_vs_Zhang_top100_overlap.tsv`). A = Adopt, R = Revise, X = Reject.

| Expected type | Ke 2025 cluster: verdict | Zhang 2023 best-matching cluster (shared genes) | Collated call |
|---|---|---|---|
| Epidermis (non-hair) | 7: A; 1: R | 7 -> 0 epidermis/cortex I (20); 1 -> mixed: 0 (11), 12 epi/cortex II (8), 6 root hair (4) | cl7 = Epidermis; cl1 unresolved epidermis lineage |
| Trichoblast | 8: A | 6 root hair (40) | Adopt |
| Exodermis/hypodermis | absent | absent | gap |
| Cortex | 2: A | none (only 25 specific Ke DEGs; Zhang has no pure cortex cluster) | Adopt (spatial only) |
| Endodermis | 9: A | 10 endodermis I (16) + 17 endodermis II (22) | Adopt, confirmed |
| "Endodermis/Phloem" | 11: R | 14 immature sieve elements (21), 16 protophloem (8), 11 metaxylem (7); 0 endodermis | **Re-read as immature sieve element / developing phloem** (Part B) |
| Pericycle | 6 "Pericycle*": R | 21 companion cell (22) + 16 protophloem (12); 0 shared with Zhang pericycle clusters 1/4/9 | **Probably companion cell / phloem-pole, not pericycle** (Part B) |
| Procambium/provascular | 4: R | weak: 5 provascular (4), 11 (4), 13/14/16 (3 each) | hypothesis only |
| Xylem | 10: A | 13 protoxylem (24) + 11 metaxylem (7) | Adopt; proto/meta merged |
| Phloem | 13: A | 16 protophloem (11) | Adopt; SE/CC merged |
| Root cap | 14: A | 15 root cap (31) | Adopt; columella/LRC merged |
| QC / stem-cell niche | absent | 18 SCN (not checked) | gap |
| G1/S (state) | 3: A | 3 "proximal meristem" (29) | state |
| G2/M (state) | 12: A | 7 "meristem II" (45) | state |
| Unknown | 0: X; 5: X (heat-shock) | 5 -> no clear match | keep Unknown / stress |

## Cross-study markers (same gene ID in both atlases)

27 rows of `markers_draft.tsv` cite both studies. In 26 of them the same gene ID is a marker in both; the histone H4 row cites Zhang only for the S-phase state. Confidence was raised one level only where at least one study validated the gene (Ke Stereo-seq or Zhang RNA in situ) and the other study found it specific to the same type:

| Type | v2.1 / v1.1 | Gene | Ke 2025 | Zhang 2023 | Confidence |
|---|---|---|---|---|---|
| Xylem | TraesCS5D03G0377000 / TraesCS5D02G152400 (+5A, 5B homeologs) | XCP1-like | cl10 DE, Stereo-seq | protoxylem marker, RNA in situ (joint homeolog probe) | function, high |
| Endodermis | TraesCS3D03G0402600 / TraesCS3D02G185100 | peroxidase 72-like | Stereo-seq | endodermis I+II | high |
| Endodermis | TraesCS5D03G0492700 / TraesCS5D02G209900 | VIT2-like | Stereo-seq | endodermis I | high |
| Epidermis | TraesCS2D03G0324500, TraesCS2D03G0324400 | glycine-rich cell wall proteins | Stereo-seq | epidermis/cortex I (merged) | high |
| Root cap | TraesCS3D03G0697200 / TraesCS3D02G306100 | LEA-like (At5g60530-like) | Stereo-seq | root cap | high |
| Dividing (G2/M) | TraesCS3A03G0796600 / TraesCS3A02G333000 | CycB1-like | G2/M | "meristem II" | high (function) |
| Procambium | TraesCS3D03G0013700 / TraesCS3D02G003600 | WAT1-like | DE cl4 | provascular, RNA in situ | medium (raise withheld: endodermal in both) |

Cluster-specific in both atlases but validated in neither, so not raised: EXPA17-like and CSLD1-like (Trichoblast); TaCASP1 2A/2D (Endodermis, cluster-specific in Ke cl9 and Zhang endodermis II); VND1-like 4B/4D (Xylem); APL-like 7A (Phloem); SUT1-like 4A and ANN5-like 3A/3B (Phloem_Companion); PP2-B12-like 6A/6D and callose synthase-like 6A (Sieve_Element); WAT1-like 3A and the A/B-barrel protein (Procambium).

## Gaps (no validated wheat marker)

- **No `function` marker:** Columella, Lateral_Root_Cap (only merged Root_Cap rows), Quiescent_Center, Stem_Cell_Niche, Atrichoblast, Exodermis, Cortex, Pericycle, Procambium, Metaxylem (vs protoxylem), Sieve_Element, Stele_Parenchyma, Lateral_Root_Primordium.
- **No marker at all:** Atrichoblast, Exodermis, Pericycle, QC/SCN, Metaxylem, and Lateral_Root_Primordium. The two former pericycle rows were moved to Phloem.
- The Phloem_Companion `function` row (SUT1-like) is detected in only about 20% of cells.

## Recommended label reference

**Ke 2025, at cluster level**, for epidermis (cl7), root hair (8), cortex (2), endodermis (9), xylem (10), phloem (13), root cap (14) and the two cell-cycle states. It is the only atlas with spatial validation, it has no forced assignment, and its tables are complete. Labels have to come from the 557 MB RDS (run the export in a job) or be re-derived from the public cluster map. Do not reuse its labels for clusters 1, 4, 6 and 11. The Zhang 2023 overlap points to companion cells for cl6 and immature sieve elements for cl11; check both in Part B with the Phloem_Companion and Sieve_Element rows. Zhang 2023 is the better source for finer stele and tip types (XPP/PPP pericycle, protoxylem vs metaxylem, SE vs CC, columella, border cells, SCN) because it has 22 clusters, but it is nuclei data with 6.9k nuclei. Give it a full Part A review before using its labels.

## Conflicts and corrections

- **Ke cl6 "Pericycle*" (manual call):** its specific DEGs share 22 genes with Zhang's companion-cell cluster and 12 with protophloem, and none with Zhang's three pericycle clusters. They include SUT1-like, annexin D5-like, APL-like MYB, polyol transporters and trehalose-6-P synthases. This supports the Ke pipeline's original "phloem" call over the manual override. The two Ke "pericycle" markers are not pericycle-specific in Ke's own Table S4. PERK2-like is higher in phloem cl13 (0.84) than in cl6 (0.73), and the PDF2.3-like defensin is equal in cl6, cl11 and cl13 and is a Zhang protophloem marker. Both rows are now `Phloem`, `low`, with the conflict noted in `basis`.
- **Ke cl11 "Endodermis/Phloem":** it matches Zhang immature sieve elements (PP2-B12 F-box homeologs, callose synthase-like, CASP-like 4B1), not endodermis.
- **Zhang 2023 state clusters:** "meristem II" (cl7) shares 45 genes with Ke G2/M, and "proximal meristem" (cl3) shares 29 with Ke G1/S. These are cell-cycle states labelled as zones, the recurring problem noted in the rice review.
- **Review corrections and regrading:**
  - Uncharacterized genes with Ke Stereo-seq support (the phloem LOC119361884 triad) are `characterized_enriched` medium, not `expression`, matching the convention in `rice_root.tsv`.
  - Weak or partial spatial support (PERK2-like, the A/B-barrel protein) stays `expression` low.
  - Endodermis TaCASP1 homeologs, Trichoblast CSLD1-like, Xylem VND1-like, Phloem APL-like, Phloem_Companion SUT1-like and ANN5-like, and Sieve_Element PP2-B12 6D and callose synthase-like were added. They come from the Ke/Zhang overlap and were not in the review.
  - Ke's "chitinase CLP-like" (TraesCS3D03G1015700) is a peptidase A1 (xylanase-inhibitor/nepenthesin-like) protein in UniProt. The NCBI name is a homology transfer.
  - The IWGSC record for TaCASP1 (TraesCS2A02G383000) is UniProt E6Y2A0 "TaCASP1/TaSTG". The PubMed ID attached there (24920445) is the CASP-family paper by Roppolo 2014, not a wheat functional study.
  - The SUT1-like 4A gene is UniProt Q8S4W1, NCBI LOC542881. UniProt's automatic name is "SUT3", so the TaSUT1-4A identity is likely but not confirmed.
- **XCP1-like** is also DE in Ke root cap (pct 0.89). Use it for xylem only together with root-cap markers.
- **ID checks:** every v2.1 ID maps 1:1 to its v1.1 alt_id in the IWGSC correspondence table (`Ke2025/idmap/iwgsc_refseq_all_correspondances.zip`; repeated rows are v1.0 duplicates). The cluster and pct of every Ke row were re-read from Table S4 (`Ke2025/mmc5.xlsx`). Each Zhang cluster assignment comes from Zhang Table S2, and in situ probe IDs come from Table S14. The added v1.1 IDs were checked in UniProt (`Zhang2023_check/uniprot_added_markers.tsv`).

## Overlap with existing skill tables

There is no wheat table in `references/markers/`. The closest relatives are `rice_root.tsv` (Oryzeae, a different tribe from Triticeae, so the full search was warranted) and `sorghum_root_Guillotin2023.tsv` (grass-conserved, maize-derived). Ke's own ortholog notes put several wheat rows next to rice rows: HyPRP DC2.15-like 1B with rice OsHyPRP06 (cortex in both), EXPA17-like with OsEXPA17 (trichoblast), and CLP-like with rice CLP (epidermis). Wheat TaCASP1 matches rice OsCASP1 (endodermis), and CSLD1-like matches OsCSLD1. These pairings are by homology and were not checked with BLAST. Running `map_markers.py` from `rice_root.tsv` onto wheat will give a second, independent set for comparison.

## Not verified or not accessed

- Per-cell labels for both atlases: Ke's are in the 557 MB RDS, not downloaded. Zhang's were not looked for (GSA CRA008788, a supplementary 3D UMAP HTML).
- Zhang 2023 has no full review: no proportions, replicate or QC assessment. Its Supplementary Note (`.doc`) could not be parsed as text here. Only Fig 1, Tables S2 and S14 and the main text were used.
- Zhang in situ images (Fig 2f-g) were not inspected. Only the text and legend were used, so the XCP1 "protoxylem" and WAT1 "provascular" readings are the authors' claims.
- Orthology of the added genes (CSLD1, VND1, APL, SUT1, CalS7) to the characterized genes was taken from NCBI, UniProt and Zhang Table S14 names. It was not checked by BLAST or phylogeny.
- No in situ, reporter or spatial validation exists in either study for Columella, LRC, QC, Pericycle, Exodermis, Metaxylem, SE or CC as separate types.

## Update 2026-10-20: gap-fill reviews

One new review: the full Part A review of **Zhang et al. 2023** (`Zhang2023/README.md`, `Zhang2023/markers_Zhang2023.tsv`). Before this, Zhang 2023 was used only as a cross-check (`Zhang2023_check/`). I also checked the characterized-markers survey (`survey/characterization/characterized_markers.tsv`) for `wheat_root:` rows. The only wheat gene there is TaSUT1 (Aoki et al. 2004 *Planta*, doi:10.1007/s00425-004-1232-7, PMID 15014993, checked in Europe PMC). Its ID, TraesCS4A02G016400, matches the existing SUT1-like row. The other `wheat_root:` survey rows are Arabidopsis, rice, maize or barley genes, which apply only by homology and were not added here.

### New dataset

| Dataset | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|
| Zhang L ... Yan W. 2023 *Genome Biol* 24:65, doi:10.1186/s13059-023-02908-x, PMID 37016448 (CNCB GSA CRA008788; GitHub hcph/wheat_singlecellAtlas, Zenodo 7761965) | FACS-sorted nuclei, 10x 3' (one library) plus snATAC; no RNA doublet removal. AK58, 0.5 cm tips, 1/2 MS plates | 6,875 nuclei, 22 clusters (per-cluster counts not reported; estimated from Fig 1d) | v1.1 (`alt_id`); converted to v2.1 for `ref_gene` (all 39 pairs re-checked 1:1 in the IWGSC correspondence table) | `cluster_only` (no barcode table anywhere) | medium as a marker source, medium-low as a label source |

### Verdicts (Zhang 2023)

- **Adopt (8):** cl6 root hair (Trichoblast), cl10 and cl17 endodermis I/II, cl13 protoxylem (Xylem), cl14 immature sieve elements (Sieve_Element), cl15 root cap (Root_Cap, columella and LRC merged), cl16 protophloem (Phloem), cl21 companion cell (Phloem_Companion).
- **Revise (9):**
  - cl0 and cl12: epidermis and cortex merged.
  - cl2: a meristem zone.
  - cl3: S_Phase.
  - cl5: Procambium (medium).
  - cl7: Dividing_cells.
  - cl11: Metaxylem (hypothesis).
  - cl18: Stem_Cell_Niche (hypothesis, about 20 nuclei).
  - cl19: Border_Cell, a Root_Cap sub-state (JA/wound signature).
- **Reject (5):** the "pericycle" clusters cl1 (IPC), cl4 (XPP) and cl9 (PPP), which were called without a pericycle marker; cl8, which has no specific genes; and cl20 "columella", called from BAM3 alone plus a sugar-starvation/hypoxia set.

### Markers added (36 rows; 47 -> 83)

From the Zhang review there are 34 new gene IDs. Five of the review's 39 markers were already in the draft (XCP1-like 5A/5B/5D, callose synthase-like 6A, PP2-B F-box 6A). Two TaSUT1 homeologs come from the characterized survey row.

| Cell type | Added | Evidence / confidence |
|---|---|---|
| Xylem (protoxylem) | TMO5-like 5A, 4D | characterized_enriched low (5A also Ke xylem DE, but also in root cap) |
| Metaxylem (new type in the table) | IRX9-like 4A, LAC5-like 5A, VRLK1-like 4B | characterized_enriched low; use only inside Xylem-marked cells |
| Sieve_Element | PP2-B12-like F-box 6B | characterized_enriched low (Ke cl11 0.44 vs 0.05; graded like the 6A/6D homeologs, not the review's expression medium) |
| Phloem (protophloem) | APL-like 7B, PEAR2-like Dof 3D, BAM1-like 4A | characterized_enriched low |
| Phloem_Companion | DAR-like LIM 4A/4B/4D (in situ, medium); LOL3-like 1D (expression low); **TaSUT1-4B, TaSUT1-4D** (function medium) | see basis |
| Procambium | PNH1/AGO10-like 7B, 7D | characterized_enriched low |
| Endodermis | MYB36-like 5A, 5B | characterized_enriched low; also specific in Ke cl9, but neither study validated them, so not raised (same rule as TaCASP1) |
| Stem_Cell_Niche (new type in the table) | PLT1-like x4, RGF1-like x2, RGF3-like | characterized_enriched low; hypothesis only |
| Root_Cap | BRN2-like NAC 2D (low); **LEA At3g19430-like 3A (high)** | see below |
| Border_Cell (new type; review name Root_Border_Cell) | JAZ10-like x3, PDR8/PEN3-like, PRN2-like x2, coiled-coil 90B-like | characterized_enriched / expression low (qPCR on collected border cells) |
| S_Phase | G-H2AX-like 2B | characterized_enriched medium (state; in situ), not raised (Ke G1/S 0.91 vs 0.57, not specific) |

Cell-type naming:
- The review's `Root_Border_Cell` was renamed `Border_Cell` to match the existing skill tables.
- The review's `requires=Xylem` / `requires=Root_Cap` entries were dropped, because `requires` holds trait tags only. The pairing is now written in `basis`.

### Confidence raised or regraded

- **TaSUT1-4A** (TraesCS4A03G0027400 / TraesCS4A02G016400), Phloem_Companion: function, **medium -> high**.
  - The characterized-markers survey confirms the TaSUT1 identity. The earlier draft said it was "likely, not confirmed".
  - Aoki et al. 2004 localized its mRNA to companion cells by in situ in leaf, sheath and internode. That is an independent study, and the gene is cluster-specific in both root atlases.
  - Caveat: the in situ was not done in root.
  - Symbol changed to TaSUT1-4A.
- **LEA At3g19430-like 3A** (TraesCS3A03G0756500), Root_Cap: the review graded it expression medium. It is now characterized_enriched **high**.
  - Ke Table S5 lists it as a root-cap Stereo-seq gene with the expected pattern (Ke cl14 0.71 vs 0.00), which makes it characterized_enriched medium.
  - It is also specific in Zhang cl15, which raises it one level.
- **Not raised:**
  - XCP1-like 5A/5B stay high. The Zhang review rated them medium because the joint probe cannot resolve homeologs, but Ke Table S5 lists both homeologs among the Stereo-seq-patterned xylem genes.
  - The remaining Zhang Adopt clusters had already been used in the earlier cross-check, so no other existing row was raised.

### Existing rows edited

- **TaSUT1-4A:** symbol, confidence, basis and source, as above.
- **PP2-B F-box 6A/6D:** a note in `basis` that Zhang's Arabidopsis homolog names (PP2-B11, PP2-B10) differ from the NCBI name, PP2-B12. Matching is by ID.
- **XCP1-like 5A/5B:** a note on why they stay high.
- **VRLK1-like 4D:** a pointer to the 4B metaxylem row.
- No existing row was found to be wrong.

### Gaps closed (partly)

- **Sieve_Element:** 4 rows, from two atlases that agree (Zhang cl14 matches Ke cl11). Still no `function` marker, and no in situ.
- **Metaxylem:** 3 rows, from one unvalidated cluster.
- **Stem_Cell_Niche:** 7 rows, from a cluster of about 20 nuclei.
- **Procambium:** PNH1/AGO10-like added.
- **Root_Cap:** a second high row (LEA 3A) and BRN2-like.
- **Border_Cell:** added as a type.
- **Phloem_Companion:** now has 3 `function` rows (the TaSUT1 triad) plus the in situ DAR-like triad.

`expected_cell_types.tsv` was updated with the new counts and notes, and gained a `Border_Cell` row.

### Gaps remaining

- **No `function` marker:** Columella, Lateral_Root_Cap, Root_Cap (merged), Border_Cell, Quiescent_Center, Stem_Cell_Niche, Atrichoblast, Epidermis, Exodermis, Cortex, Pericycle, Procambium, Metaxylem, Sieve_Element, Stele_Parenchyma, Lateral_Root_Primordium.
- **No wheat marker at all:** Columella (cl20 rejected), Lateral_Root_Cap, Quiescent_Center (Zhang cl18 has no WOX5/QHB in its top 100), Atrichoblast, Exodermis, Pericycle (all three Zhang pericycle clusters rejected), Stele_Parenchyma, Lateral_Root_Primordium.

### Recommended label reference

- **Ke 2025 stays the label reference**, at cluster level and for the same clusters as above. It has spatial validation and 3 replicates; Zhang has one nuclei library and no per-cell labels.
- **Zhang 2023 is the better source for finer stele subtypes,** but only as marker evidence. Its labels are `cluster_only` and would have to be re-derived from raw reads. Use its adopted subtypes as Part B hypotheses inside Ke's merged clusters: protoxylem cl13 vs metaxylem cl11, immature SE cl14, protophloem cl16 and companion cells cl21.
- Do not reuse Zhang's pericycle (cl1/4/9), columella (cl20), meristem (cl2/3/7) or cl8 labels.

### Conflicts

- **"DAR2" probe (Zhang Fig 2e):** Zhang Table S2 gives the homolog as DA1 (AT1G19270), and UniProt names the 4B gene DA2 (A0A1L6K401). The symbol is kept as "DAR-like LIM (paper: DAR2)".
- **Two MYB36-like pairs in the endodermis:** 6A/6D (Ke regulon, function medium) and 5A/5B (Zhang cl10 and Ke cl9, characterized_enriched low). It is unresolved which pair is the MYB36 ortholog.
- **LAC5-like 5A:** Zhang calls it metaxylem (cl11), but in Ke it is DE only in cl11 "Endodermis/Phloem", which this draft reads as immature SE. Ke cl11 also shares 7 genes with Zhang metaxylem, so it may contain early metaxylem cells.
- **TaSUT1-4A outside companion cells:** it is a top marker of Zhang cl4 "XPP" (rejected) as well as cl21. This supports reading cl4 as phloem-adjacent rather than pericycle.
- **Border-cell genes:** in Ke, JAZ10-like 2D/2B are DE in the heat-shock/stress cl5, not in root cap. JAZ10-like 2A and PRN2-like 1B/1D are root cap plus stress or cortex. This fits the review's caution that cl19 may be a wound or JA state. Use these genes only inside Root_Cap-marked cells.
- **XCP1-like and TMO5-like 5A:** both are also DE in Ke root cap cl14.

### Could not verify (this update)

- **Zhang review gaps:** per-cluster nuclei counts, Additional files 1 and 3, the in situ images for the cl0/cl12 genes, and the authors' Arabidopsis orthology calls. The BRN2-like ID comes from a figure caption. Details are in `Zhang2023/README.md`.
- **TaSUT1 homeologs:** whether the Aoki 2004 in situ probe distinguishes 4A, 4B and 4D is not stated in the survey row. I did not re-read the paper.
- **No orthology checks:** none of the added genes was checked by BLAST or phylogeny.
