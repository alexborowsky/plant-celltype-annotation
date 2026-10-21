<!-- Collated from the survey review of maize_embryo (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Maize embryo: collated cell-type marker resources

Date: 2026-10-20. This collates the one reviewed dataset for this group (Wu et al. 2025) into a draft marker table, cross-checking it against an independent maize shoot-apex scRNA-seq dataset (Satterlee et al. 2020, reviewed under `../maize_shoot_apex/Satterlee2020/`) and against published in situ studies. Nothing was re-analysed; all statistics come from the papers' supplementary tables.

Files in this folder:
- `expected_cell_types.tsv`: written from the anatomy of a Stage 1 (leaf-1, 12-13 DAP) B73 embryo, not from the published labels. The `function_markers` column counts `function` rows in `markers_draft.tsv`. The skill has no maize embryo table yet.
- `markers_draft.tsv`: 50 rows, 18 cell types plus 1 state. It uses the skill schema with an added `alt_id` column. `ref_gene` holds **B73 v5** (`Zm00001eb`) IDs and `alt_id` holds the **B73 v3** (`GRMZM2G`) IDs used by Wu 2025. `tissue` = `embryo`. Field counts were validated.
- `Wu2025/`: the per-dataset review (README, supplementary files, ID crosswalks). That README was left unchanged.

## Datasets

| Dataset | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|
| Wu H, Zhang R, Niklas KJ, Scanlon MJ (2025) *Nat Commun* 16:802, doi:10.1038/s41467-024-55803-9 | Protoplast scRNA-seq (10x 3'), with 10x Visium (8 sections), LM-RNA-seq (5 organs) and a 10x Xenium 99-gene panel on three stages | 11,459 cells from 2 batches of about 200 Stage 1 embryos; 22 clusters; per-cluster counts not reported | B73 v3 | `cluster_only`: Supp Data 2 cluster table and Supp Data 1 DE. Raw reads are at SRA PRJNA1045558. No per-cell labels or processed object | medium |
| *Cross-check only:* Satterlee JW, Strable J, Scanlon MJ (2020) *PNAS* 117:33689, doi:10.1073/pnas.2018788117 | Protoplast scRNA-seq of the seedling shoot apex (SAM+P2, SAM+P6) | see `../maize_shoot_apex/` | B73 v3 | Dataset S2/S7 DE tables | not graded here (different organ) |

Satterlee 2020 is a separate experiment on a different organ (the seedling shoot apex), so it counts as an independent study for marker agreement. It comes from the same lab as Wu 2025. Agreement was counted only when the same v3 ID was cluster-specific for the same cell type. Satterlee's SAM+P2 cluster names (Meristem 2, Tip, Epidermis 1, Vasculature) come from Dataset S2. The SAM+P6 identities used below (KN1 cluster, epidermis, dividing, vascular, primordium) were inferred from each cluster's DE genes, because the names are only in SI Fig S5B, which I did not read.

## Per-cell-type verdicts (Wu 2025 is the only embryo dataset)

| Expected type | Wu 2025 cluster(s) | Verdict | Note |
|---|---|---|---|
| Shoot_Apical_Meristem | 5 "SAM and hypocotyl" | Revise | Merged with the embryonic stem (KN1/LG3/RS1). Split with WUS1/LOG7 |
| Embryonic_Stem | 5 (merged) | Revise | No specific marker |
| Organ_Boundary | 16 "possible boundary" | Reject | Weak DE, and the cluster lacks CUC2 |
| Leaf_Primordium | 20 "Leaf" | Adopt | DRL1 0.39 vs 0.002. Tiny island |
| Lateral_Organ_Margin | (inside 9) | – | NS1 is in cl9 at 0.06 |
| Coleoptile | 9 "coleoptile epidermis", 13 "coleoptile internal" | Adopt (as coleoptile) | Epidermis vs internal is not shown for 13 |
| Epidermis (shoot protoderm) | 9 (partly) | Revise | OCL4 is weak in the Wu scRNA data |
| Procambium | 14 "Vasculature" | Adopt | SHR, PIN1a, BHLH40. Cluster 15 "possible vasculature" rejected |
| Scutellum_Adaxial_Epidermis | 6 | Adopt | LOG7, GRMZM2G140968 |
| Scutellar_Epithelium | 1 (Adopt); 2, 3 (Revise: HSP state / mixed) | Adopt/Revise | Merge 1-3 |
| Scutellum_Parenchyma | 0, 4 (Adopt); 7, 8 (Revise); 10 (Reject) | Adopt/Revise | 8 is ribosomal/PCNA; 10 is mitochondrial/ribosomal |
| Radicle / Root_Cap | none | missing | Xenium "pre-root" signal exists (SCR, SBP18, GRMZM2G079883). Cluster 15 may hold these cells |
| Coleorhiza | 11 "embryo-endosperm boundary" | Reject (candidate) | Its Xenium gene was placed at the "pre-coleorhiza area?" |
| Suspensor | 21 "suspensor residue" | Revise | Its top genes MYB73/FLS1 are endosperm by Xenium, and WOX9B is DE in cl5 instead |
| Endosperm (contaminant) | 19 | Adopt | Zeins. Exclude from analysis |
| Dividing_cells | 12 "abaxial scutellum epidermis" | Revise → state | CENH3/KNOLLE/CYCB |
| Protoplasting_stress | 2, 17, 18 | Reject as types | HSP, PR10/chitinase, AOS1/JAZ |

## Cross-study markers (confidence raised or confirmed)

14 rows have agreement from a second, independent source:

| Cell type | Symbol | v5 | v3 | Second source |
|---|---|---|---|---|
| Shoot_Apical_Meristem | KN1 | Zm00001eb055920 | GRMZM2G017087 | in situ (Zhang 2002 Planta); Satterlee Meristem 2 / KN1 cluster |
| Shoot_Apical_Meristem | LG3 | Zm00001eb130180 | GRMZM2G087741 | Satterlee Meristem 2 / KN1 cluster (0.68 vs 0.03) |
| Shoot_Apical_Meristem | RS1 | Zm00001eb299420 | GRMZM2G028041 | Satterlee KN1 cluster (0.52 vs 0.02) |
| Shoot_Apical_Meristem | LOG7 | Zm00001eb160700 | GRMZM2G059392 | Satterlee Tip (0.40 vs 0.007); in situ cited (Knauer 2019) |
| Leaf_Primordium | DRL1 | Zm00001eb008680 | GRMZM2G088309 | in situ primordia (Strable 2017 Plant Cell); Satterlee primordium cluster |
| Lateral_Organ_Margin | NS1 | Zm00001eb092480 | GRMZM2G069028 | in situ margins (Nardmann 2004 Development) |
| Epidermis | OCL4 | Zm00001eb024680 | GRMZM2G123140 | in situ embryo protoderm (Ingram 2000 Plant J); Satterlee Epidermis 1 |
| Epidermis | ABCG11 | Zm00001eb221130 | GRMZM2G177314 | Satterlee SAM+P6 epidermis (0.66 vs 0.11) |
| Epidermis | PRP2 | Zm00001eb080380 | GRMZM2G102356 | Satterlee Epidermis 1 and SAM+P6 epidermis |
| Procambium | SHR | Zm00001eb326020 | GRMZM2G172657 | Satterlee Vasculature (0.14 vs 0.01) |
| Radicle | SCR | Zm00001eb195650 | GRMZM2G131516 | in situ endodermis + QC (Lim 2000 Plant Cell) |
| Dividing_cells | KNOLLE | Zm00001eb215350 | GRMZM2G100478 | Satterlee dividing cluster |
| Dividing_cells | CYCB1-4 | Zm00001eb150450 | GRMZM2G073003 | Satterlee dividing cluster |
| Dividing_cells | CENH3 | Zm00001eb291210 | GRMZM2G158526 | Satterlee dividing cluster |

v4 IDs (MaizeGDB crosswalk) for these rows, for v4 data: KN1 Zm00001d033859, LG3 Zm00001d040611, RS1 Zm00001d018742, LOG7 Zm00001d044327, DRL1 Zm00001d028216, NS1 Zm00001d004889, OCL4 Zm00001d030069, ABCG11 Zm00001d013960, PRP2 Zm00001d003379, SHR Zm00001d021973, SCR Zm00001d052380, KNOLLE Zm00001d013323, CYCB1-4 Zm00001d043164, CENH3 Zm00001d038533. All other rows have their v4 ID in `Wu2025/idmap/B73v3_to_B73v4.tsv`.

## Gaps (expected types without a `function` marker)

Embryonic_Stem, Scutellum_Adaxial_Epidermis, Scutellar_Epithelium, Scutellum_Parenchyma, Root_Cap, Coleorhiza, Suspensor and Protoplasting_stress have none. The scutellum types and Suspensor have only Xenium-validated `characterized_enriched` rows. Root_Cap and Coleorhiza have no marker at all, and Radicle rests on SCR alone. The rice embryo review (`../rice_embryo/Yao2024`) has scutellar-epithelium and coleorhiza markers (OsSAG12-1, RAmy1A, qLTG3-1) that could be carried over by homology. That was not done here.

## Recommended label reference

Wu 2025 is the only maize embryo single-cell dataset reviewed, and it is the reference by default. However:
- Use its **markers** (especially the Xenium Supp Data 7 observed locations), not its labels.
- Adopt only clusters 0, 1, 4, 6, 9, 13, 14, 19 and 20, at region level.
- Per-cell labels are not public. Reuse would mean reprocessing SRR27013101/2 against v3 or v5 and re-deriving labels from `markers_draft.tsv`.
- For the shoot-apex types (SAM, epidermis, provasculature, dividing cells), Satterlee 2020 gives supporting cluster-level evidence.

## Conflicts and corrections to the review

ID corrections. In each case the MaizeGDB v3→v5 crosswalk lists several models; the corrected ID was confirmed with UniProt and NCBI Gene:
- **PIN1a** = Zm00001eb372180 (Q0MWY2, NCBI LOC103637824 alias PIN1a), not Zm00001eb372190 as in the review JSON. The review README already had this.
- **ZP27** = Zm00001eb313800 (P04706, gz27), not Zm00001eb313810. The review README already had this.
- **PRP2** = Zm00001eb080380 (Q19VG6 = NCBI LOC542195, alias prp2), not Zm00001eb080390. This is new.
- **KNOLLE** = Zm00001eb215350 (A0A1D6GI53 t-SNARE, NCBI LOC103625904 "syntaxin-related protein KNOLLE"), not Zm00001eb215340 (a 116-aa uncharacterized model). This is new.
- **CENH3** = Zm00001eb291210 (Q8LK76), not Zm00001eb291200 (an ARF GTPase). This is new.
- **GRMZM2G048793** maps to Zm00001eb083660 or Zm00001eb083650 and is unresolved. The row keeps 083660; use the v3 `alt_id` when in doubt.

Symbol conflicts (compare by ID):
- GRMZM2G122537 is "WOX3A" in the paper and NCBI. UniProt also names NS1 (GRMZM2G069028) "WOX3A".
- GRMZM2G133972 (WOX9A) also has the NCBI alias wox9b; the real WOX9B is GRMZM2G031882.
- GRMZM2G102161 is "MADS8" in the paper, but NCBI calls it MADS14 (aliases zmm8/M8).
- GRMZM2G314064 is "WOX11" in the paper, but NCBI calls it "WUSCHEL-related homeobox 6".
- GRMZM2G021406 is "LOG8" in the paper, but NCBI calls it "LOGL7".

Biological conflicts (also in the `basis` of each row):
- LOG7 is at the SAM tip by in situ, yet its strongest scRNA cluster is the adaxial scutellum epidermis (cl6). It has two rows.
- LEC1 is "adaxial scutellum" by Xenium, but in situ shows it across the early embryo proper, fading in the scutellum (Zhang 2002).
- WOX9B is suspensor by Xenium but DE in the SAM+stem cluster 5.
- WOX11 is basal scutellum by Xenium but DE in cluster 5.
- The peroxidase GRMZM2G029479 is abaxial epidermis by Xenium but DE in the G2/M cluster 12.
- MYB73, the top gene of the "suspensor" cluster 21, is endosperm by Xenium.
- The main text and Supp Data 2 of Wu 2025 give different cluster numbers. Supp Data 2 is used here.

## Overlap with the skill's existing tables

There is no maize table in `references/markers/`. `sorghum_root_Guillotin2023.tsv` lists maize v5 IDs in its `symbol` column, and two draft genes appear there:
- PIN1a (Zm00001eb372180) as root Xylem, which fits a vascular identity.
- GRMZM2G079883 (Zm00001eb154390) across root epidermis/trichoblast/dividing lineages, which fits its "pre-root" Xenium signal. Its confidence was not raised because the cell type differs and the gene marks several lineages.

`sorghum_leaf.tsv` cites maize only through orthologs (CST1, SUT1, SWEET13), and none of those are in this draft.

## What I could not verify

- Per-cell labels, per-cluster cell counts and batch composition for Wu 2025 are not public. The Xenium bundle (Science Data Bank) and the raw reads (56-61 GB per run) were not downloaded.
- Several in situ papers were read only as abstracts (Europe PMC): Zhang 2002, Lim 2000, Nardmann 2004, Strable 2017, Ingram 2000, Vernoud 2009, Suzuki 2015, Forestan 2010.
- The CUC2 in situ (Johnston 2014) and the LOG7/KN1/OCL4 in situ (Knauer 2019) were taken from Satterlee 2020 Dataset S2's citation column and not re-read. CUC2 was therefore left at `medium`.
- Uncharacterized genes (GRMZM2G140968, GRMZM2G122276, GRMZM2G048793, GRMZM2G051752, GRMZM2G079883) were checked only through the paper table, the MaizeGDB crosswalk and NCBI Gene aliases. UniProt has no names for them.
- I did not check whether Nardmann 2007 (*Mol Biol Evol*) localizes WOX9B/C to the suspensor, so the WOX9 rows were not raised.
- The other maize single-cell groups (maize_seed Fu2023, maize_endosperm Yuan2024) had no marker lists in `merged_reviews.json` and were not mined for agreement.
