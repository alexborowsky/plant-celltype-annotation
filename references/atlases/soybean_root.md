<!-- Collated from the survey review of soybean_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Soybean root: collated cell-type marker resources

Group `soybean_root`, collated 2026-10-20 for the plant-celltype-annotation skill.
The per-dataset reviews are in `CervantesPerez2024/README.md` and `Zhang2025/README.md`.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Cell types expected from the anatomy of a 6-7 day whole primary root (nuclei data), with marker coverage counted from `markers_draft.tsv` |
| `markers_draft.tsv` | 61 rows in the skill marker-table schema plus `alt_id` |
| `README.md` | This file |

## Gene IDs

- `ref_gene` uses the Wm82.a2.v1 locus in Phytozome/LIS format (`Glyma.02G003700`).
  - Ensembl Plants and UniProt write the same locus as `GLYMA_02G003700`. Cervantes-Pérez 2024 tables use that form.
  - Zhang 2025 uses Wm82.a4.v1 (`Glyma.02G003700`). All 61 loci keep the same name in a4. No a4-only IDs (such as `Glyma.20G183866`) are used.
- `alt_id` is the Wm82.a1 (Glyma1.1) locus (`Glyma02g00640`). All 61 were checked against the LIS synonym file `glyma.Wm82.gnm2.ann1.RVB6.synonym.txt.gz`. One draft alt_id was wrong (`Glyma20g06810`) and was corrected to `Glyma20g06820`.
- Every `ref_gene` appears in the Cervantes-Pérez Table S1 all-genes matrix.
- Each ID was checked by the per-dataset reviews (Ensembl xrefs plus UniProt REST). I re-checked these IDs in UniProt: `GLYMA_10G183300` (PHO1-H5), `06G259400`, `10G070200`, `15G274200`, `11G042000`, `05G023700`, `07G130800`, `15G245800` and `08G125800`.
- Arabidopsis best hits come from the LIS `info_annot` file.

## Datasets

| Study | Platform | Cells | Label access | Quality |
|---|---|---|---|---|
| Cervantes-Pérez et al. 2024 *Plant Commun* 5:100984, doi 10.1016/j.xplc.2024.100984 (GEO GSE226149; root atlas only) | snRNA-seq, 10x 3' v3.1, FACS nuclei; Resolve Molecular Cartography (MC) on one mature-zone cross-section; soybean promoter reporters for root hair | 14,369 nuclei, 3 replicates, 16 clusters; 6-day Williams 82 primary root, N-free, uninoculated | Table: a portal barcode→cluster export (`portal_root_cell_labels.tsv`) covers 9,082 of 14,369 nuclei (63%), because 6 clusters are downsampled. Full per-cluster expression is in Table S1 | Medium (the folder README says medium-high). The best-validated root dataset |
| Zhang et al. 2025 *Cell* 188:550-567, doi 10.1016/j.cell.2024.10.050 (GEO GSE270392; root part only) | 10x snRNA-seq (2 replicates) + scATAC-seq (5 replicates) + Visium (55 µm spots) | snRNA: 7,496 root nuclei, 12 sub-clusters → 8 labels. scATAC: 35,586 nuclei. 7-day Williams 82 whole roots on 1/2 MS, uninoculated | Table: per-nucleus labels in Table S1 (`mmc1.xlsx`, extracted to `Zhang2025/TableS1_snRNA_root_labels.tsv`) | Medium (second-pass review). Forced assignment; validation is spot-level only. Its root literature markers are mostly taken from the Cervantes-Pérez preprint |

## Verdict matrix

Canonical names follow the skill tables. "-" means the type is not labeled in that dataset.

| Canonical type | Cervantes-Pérez 2024 (snRNA) | Zhang 2025 snRNA | Zhang 2025 scATAC |
|---|---|---|---|
| Trichoblast | Adopt (C3 root hair; 73% from replicate 3) | Adopt (Root_hair.6) | Root_hair |
| Epidermis (non-hair) | Adopt (C1, C2) | Revise (Epidermis.2/.3 merged; .3 may be a defense state) | Epidermis |
| Root_Cap | Adopt, low-medium (C4; columella and LRC merged; no in situ) | - | Root_cap (2.2%) |
| QC / Stem_Cell_Niche | Reject the SCN label on C6 (G2/M) | - | RAM (7.4%, batch-skewed) |
| Dividing_cells / S_Phase (states) | Revise: C5 = S-phase/meristematic, C6 = G2/M | - (probably inside Procambium.1_0) | absent |
| Cortex | Adopt (C7, C8, C9) | Revise (Cortex.0 is a sink; Cortex.5 is LR-emergence-like; Cortex.7 is PR1-high and was rejected as a state) | Cortex |
| Endodermis | Adopt (C10 Casparian stage; C11 suberized) | Adopt (Endodermis.4) | Endodermis |
| Pericycle | Adopt (C13; poles not split) | Adopt (Pericycle.1_1; poles not split) | Pericycle |
| Procambium / Stele_Parenchyma | Revise (C12 "cambium", 14.7%, weak) | Revise (Procambium.1_0, catch-all) | Procambium |
| Xylem | Adopt (C14, differentiating) | Revise (Xylem.8_1, weak) | Xylem |
| Phloem_Companion | Adopt (C16) | Reject Phloem.8_0 (no phloem markers per nucleus; see below). The CC phloem sits inside Procambium.1_0. Reject 8_2 as a stress state | Phloem |
| Phloem_Sieve_Element | Revise: C15 "phloem fiber" → developing SE | - | - |

Verdicts are desk review (Table S1/S2, GEO pseudobulk); re-check in data. **Correction from the per-nucleus check (skill test L5, 2026-10-22):** Zhang's Phloem.8_0 is not phloem. In the Seurat object, MT3-like `Glyma.12G154300` is in 4.8% of 8_0 nuclei vs 49% of a ~106-nucleus cluster that lies 72% inside Procambium.1_0, together with PP2-A1-like, SUC/SUT1-like and AHA; PP2-A1/SUC are <=2% in 8_0. 8_0's own top genes (`Glyma.15G228200`/`228300`, the paper's Visium vasculature markers) suggest an unresolved vascular (precursor?) population. The GEO pseudobulk columns (MT3-like 540 counts in 8_0 vs 259 in 1_0) disagree with the Table S1 sub-cluster labels for this gene, so do not use the pseudobulk to place genes in 8_0/1_0. Xylem.8_1 is also unsupported per nucleus (secondary-wall genes have zero counts; see the filtering note below).

## Cross-study markers

`markers_draft.tsv` has 61 rows: 24 `function`, 35 `characterized_enriched` and 2 `expression`. Confidence: 16 high, 31 medium, 14 low. 32 rows cite both studies.

Cross-study agreement raised 12 rows to `high`. Each was validated by MC in situ in Cervantes-Pérez 2024 and is also cluster-specific in Zhang 2025 (de novo DE or pseudobulk top state):

| Cell type | Gene | Symbol | Zhang 2025 evidence | Independent of Zhang's input list? |
|---|---|---|---|---|
| Epidermis | Glyma.19G255500 | CNGC1-like | Epidermis.3 pseudobulk 3.7x | yes |
| Epidermis | Glyma.06G259400 | TIR-NBS-LRR | Epidermis.3 pseudobulk 2.2x | yes |
| Epidermis | Glyma.09G099900 | LRR-RLK | Epidermis.2 2.7x; Visium epidermis+cortex | no (input marker) |
| Epidermis | Glyma.01G156200 | PILS3-like | Epidermis.2 4.4x | no |
| Endodermis | Glyma.14G218700 | C2H2 ZF | de novo 0.18 vs 0.01 | yes |
| Endodermis | Glyma.16G106800 | PBL15-like | de novo 0.41 vs 0.02 | no |
| Pericycle | Glyma.02G003700 | GmPHO1-H1 (function) | de novo 0.56 vs 0.05 | no |
| Pericycle | Glyma.11G078300 | AHK1-like | de novo 0.57 vs 0.04 | no |
| Xylem | Glyma.13G334500 | UXS | pseudobulk 5x | no |
| Xylem | Glyma.15G040000 | UXS5-like | pseudobulk 7x | no |
| Phloem | Glyma.05G216000 | uncharacterized | Phloem.8_0 top (but 8_0 is not phloem, L5); Visium vasculature | no |
| Phloem | Glyma.12G154300 | MT3-like | ~~Phloem.8_0 3.5x~~ (GEO pseudobulk only; per nucleus it is in the CC cluster inside Procambium.1_0, L5); Visium vasculature | no |

Circularity note: Zhang 2025 labeled its clusters partly with markers taken from the Cervantes-Pérez preprint. I still counted those genes, because each Zhang cluster's identity also has independent support:
- Pericycle: PHO1-H5, FRD3a and NRT1.5 in the de novo DE.
- Endodermis: two MYB39 orthologs.
- Epidermis: the independent CNGC1-like and TIR-NBS-LRR genes.

The circularity is flagged in each row's `basis`.

Some markers are specific in both snRNA datasets but have no in situ validation, so they were not raised (the rule requires validation in at least one study):
- Endodermis: MYB39-like `Glyma.01G016600` and `09G206200`; peroxidase `04G227200`.
- Pericycle: PHO1-H5 `10G183300`, GmFRD3a `15G274600`, NRT1.5-like `11G042000`, PHO1-H4 `10G004800`.

## Gaps

Expected types with no validated (`function`, or in situ/reporter) marker:
- Columella, Lateral_Root_Cap: the Root_Cap rows rest on snRNA only. The cap is not on the MC section.
- Quiescent_Center and Stem_Cell_Niche: no marker. WOX5 and PLT orthologs are not usable in these nuclei data.
- Atrichoblast: no non-hair-specific gene. Use the Epidermis rows minus the Trichoblast rows.
- Cortex: no `function` marker, and two of three MC rows conflict in Zhang.
- Procambium and Stele_Parenchyma: only a weak WOX4-like row.
- Phloem_Companion: GmSUT1 is snRNA-only and not phloem-specific in Zhang. The MC "Phloem" rows cannot separate CC from SE.
- Lateral_Root_Primordium and S_Phase: no rows.
- Protoxylem and Metaxylem: not split.

## Recommended label reference

Use **Cervantes-Pérez 2024** as the primary reference. It has three replicates, MC in situ for six layers, root-hair reporters, and separate root cap, SE and suberized-endodermis clusters. Apply these corrections:
- C15 → Phloem_Sieve_Element.
- C6 → Dividing_cells (G2/M).
- C5 → S_Phase/meristematic.
- Keep C12 as a procambium/stele-parenchyma hypothesis.

Its portal labels cover only 63% of nuclei, and C3 is batch-skewed.
- Source: the Dash app http://soybeancellatlas.org/tissue-scatter/root (URL checked 2026-10-22). POST to `/django_plotly_dash/app/SoybeanTissueScatter/_dash-update-component` with tissue-type `root`, as the page itself does; the response holds barcode, ClusterID, ClusterName and UMAP. Barcode suffix `-k` = sample k: GSM7065807/08/09 matched 88% vs <=33% for other permutations (skill test C, 2026-10-22).
- Table S1/S2 on PMC (`/bin/mmc7.xls`, `mmc8.xlsx`) show a bot check to scripts.

Use **Zhang 2025** as a second, complete per-nucleus reference (Table S1) for the epidermis, endodermis, pericycle and root-hair labels. Before using it, drop Cortex.7, Phloem.8_0, Xylem.8_1 and Phloem.8_2 via `Seurat_clusters`, and do not trust Procambium.1_0 (it contains the CC phloem).
- Source: Table S1, https://ars.els-cdn.com/content/image/1-s2.0-S009286742401273X-mmc1.xlsx (41.8 MB, all tissues; URL checked 2026-10-22; cell.com and PMC block scripts). Root snRNA nuclei: `Tissue`=Root with cellID `rt3_<16mer>` (rep1) or `rt4_<16mer>` (rep2); columns Replicate, Seurat_clusters, Celltype (7,496 nuclei).
- `Seurat_clusters` -> Celltype: 0, 5, 7 Cortex; 1_0 Procambium; 1_1 Pericycle; 2, 3 Epidermis; 4 Endodermis; 6 Root_hair; 8_0 Phloem; 8_1 Xylem; 8_2 Phloem.
- GEO `GSE270392_Gm_atlas_Root.rna.seurat.obj.rds.gz` is gzipped twice (`readRDS` fails with "unknown input format"; `zcat` it to a `.rds` first, then `readRDS`), and its counts are gene-filtered: 16,352 of 40,127 genes are zero in every nucleus, including all root-hair, root-cap, xylem secondary-wall, CASP/SCR/MYB36 and many G2/M markers. Treat those as not measurable, not absent (L5). Its scATAC Root_cap and RAM labels are the only root-cap/RAM labels in the group, but they are ATAC-only and batch-skewed.

## Conflicts and corrections

- **Earlier summary (`survey/merged_reviews.json`, Zhang2025) is superseded by the folder's second-pass README.**
  - Table S1 and S2 were later obtained from the Elsevier CDN, so label access is "table", not "large_object", and quality is medium, not low.
  - GmPLT2 (`Glyma.12G056300`) spatial evidence is from **seed** and was not used as a root marker. The `RAM / stem cell niche` marker row in the earlier JSON should be dropped (Cervantes-Pérez pct 0.02).
  - In the earlier JSON, the Zhang IDs carry `id_checked: false`; the second pass checked them in UniProt.
- **New review JSON vs the folder README (Cervantes-Pérez):** both use the same 41 markers. The JSON omits RSL2-like `GLYMA_04G045300`, which is included here.
- **Cervantes-Pérez Table S3 ortholog errors** (from that review, verified there):
  - `GLYMA_17G030700` is labeled "CBL9" but is COBL7-like.
  - `GLYMA_02G261600` is labeled "GPAT6" but is LAC5-like.
  - `GLYMA_13G234700` is labeled "IRX9" but is SND2-like.
  - Hyphenated IDs (`GLYMA-05G215500`) appear.
  - Zhang 2025 used `Glyma.17G030700` as a Root_hair marker. It is not specific in either dataset and is not used here.
- **Zhang Table S2 symbol error:** "PHO1_H8" is `Glyma.20G032500`, which UniProt names PHO1-H10. PHO1-H8 is `Glyma.20G206900`. Not used as a marker.
- **MC probes that disagree with the snRNA data:**
  - `Glyma.15G245800` (an MC "xylem" probe) peaks in pericycle in both datasets. It is kept as a low-confidence Pericycle row.
  - `Glyma.15G179500` ("xylem") peaks in endodermis C10. Not used.
  - `Glyma.11G221200` ("cortex") peaks in suberized endodermis C11 and in Zhang Epidermis.2. Not used.
  - `Glyma.20G061300` ("epidermis") peaks in root hair C3 in Cervantes-Pérez and is non-specific in Zhang. Not used.
- **Cortex rows that conflict between studies:**
  - GmXET1 `15G169100` is phloem-high in Zhang's pseudobulk, so it was lowered to low.
  - PAE `09G216800`: Zhang's pseudobulk gives Cortex.0 ≈ Epidermis.2.
  - TAT `06G235500` marks one cortex sub-cluster in both studies (Cervantes C7; Zhang Cortex.7, PR1-high). It was not raised. Zhang's "Cortex.7 is a defense state" call may instead be a real cortex subpopulation.
- **Other cross-study conflicts:**
  - `Glyma.04G102700` (MFS) is a Zhang de novo Epidermis marker but peaks in root cap C4 in Cervantes-Pérez. This suggests Zhang Epidermis.2 contains cap/LRC nuclei. Not used.
  - GmCAPRICE `Glyma.01G224900` is a Zhang Root_hair input marker but peaks in C4 (root cap) in Cervantes-Pérez. CPC is transcribed in atrichoblasts in Arabidopsis. Not used.
  - GmSUT1 and PP2-A1-like peak in Zhang's Xylem/Procambium, not its Phloem cluster.
  - CalS7-like peaks in Zhang Procambium.1_0. This fits SE precursors inside that cluster.
- **GmCASP1 naming:** the Ensembl xref is "casparian strip membrane protein 2", while UniProt C6T2E7 is GmCASP1. The LIS best hit is AT2G36100 (CASP1).
- **Possible typos in the Cervantes-Pérez nodule MC list:** "Glyma.04G218700" and "Glyma.14G227200" (vascular endodermis) are probably root endodermis markers `14G218700` and `04G227200` with the chromosome numbers swapped. Not verified.

## Overlap with existing skill tables

This table is the skill's `primary/soybean_root.tsv`. Every row cites Cervantes-Pérez 2024 (some also Zhang 2025), so benchmarking on either dataset with it is circular. No other skill table has soybean rows.

Several rows here are soybean orthologs of `function` genes in `arabidopsis_root.tsv`: EXPA7, CASP1, SMB, and the SCR/PLT/WOX5 family. Through `map_markers.py` homology, the Arabidopsis table would also cover:
- Quiescent_Center (WOX5)
- Stem_Cell_Niche (PLT1)
- Columella and Lateral_Root_Cap

In these nuclei data, the PLT/WOX5 orthologs are barely detected. The EXPA7 hit should map to `Glyma.17G133100` (LIS best hit AT1G12560), but paralogs exist, so check the mapping.

Trait tags: GmSUT1 (SUC2 clade, type I SUTs) and GmSEOa (SEO forisome family) have `requires=eudicot`. The vocabulary has no legume tag, and the skill was not edited.

## Could not verify

- Fig S3 (the MC panels in `mmc2.pdf`) was not inspected page by page. The MC layer assignments come from the Methods probe lists.
- I did not open Qiao et al. 2017, the source for the root-hair genes `03G188300` and `15G020700`. Those rows rely on Cervantes-Pérez's statement.
- The Zhang GEO pseudobulk table is gene-filtered. Many Cervantes-Pérez markers are absent from it, including all root-hair reporters, the CASPs, the CESA8s, LAC4, SEOa, KNOLLE and SULTR3;4. So no cross-study check was possible for them. A full check needs the 284 MB Zhang Seurat object (`GSE270392_Gm_atlas_Root.rna.seurat.obj.rds.gz`), which was not downloaded.
- Zhang Supplementary Figures S1-S4 (root heatmaps, Visium plots) were not viewed.
- The Cervantes-Pérez portal covers 63% of nuclei. The mapping from barcode suffix to GSM is unverified.
- Function citations in `basis` are given by author and year and were not re-opened here: Hamburger 2002 (PHO1), Durrett 2007 (FRD3), Lin 2008 (NRT1.5) and Cohen 2020 (SUBERMAN). Their DOIs are not in `source`.
- No in-data check (Step 3b) was done.
