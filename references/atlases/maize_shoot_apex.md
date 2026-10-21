<!-- Collated from the survey review of maize_shoot_apex (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Maize shoot apex: collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill from the one review in this group (`Satterlee2020/`, whose own README holds the full desk review). Nothing here has been added to the skill.

Files:
- `expected_cell_types.tsv`: expected types for a seedling vegetative shoot apex (SAM, P1-P6 and ~3 mm of stem), built from anatomy. The function-marker counts combine this draft with the existing leaf tables (Arabidopsis via homology, sorghum), filtered for maize traits (`grass C4 monocot`).
- `markers_draft.tsv`: 33 rows in the skill schema plus `alt_id`. `ref_gene` = B73 v5 (`Zm00001eb`), `alt_id` = B73 v4 (`Zm00001d`), and the paper's v3 ID (`GRMZM`) is at the end of each `basis`. Exceptions: in 2 `REVIEW:` rows (DRM1, HYP1), `ref_gene` is a v4 ID. `tissue` = `shoot_apex`, which is a new value: the skill README only lists `leaf/root/any`.
- `Satterlee2020/maizegdb_B73v4_to_B73v5.tsv` and `maizegdb_B73v5_to_B73v4.tsv` were downloaded today from https://download.maizegdb.org/Pan-genes/B73_gene_xref/ to check the ambiguous v5 IDs.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Satterlee2020 | Satterlee JW, Strable J, Scanlon MJ (2020) PNAS 117:33689. doi:10.1073/pnas.2018788117; SRA PRJNA637882 | Protoplast scRNA-seq. SAM+P2: FDA+ hand-picked cells, CEL-Seq2, 6 replicates. SAM+P6 and Kn1-O/WT: 10x v3 | 327 (SAM+P2); 12,967 (SAM+P6, 2 replicates); 2,761 (Kn1-O/WT) | cluster_only. SAM+P2 names are in Dataset S2. SAM+P6 names are only in the Fig. S5B figure; the cluster-number-to-name mapping was inferred | medium |

This is the only single-cell study of the maize vegetative SAM. There is no processed object and no per-cell label table, so labels have to be re-derived from the SRA reads.

## Verdict matrix (one dataset)

| Canonical type | SAM+P2 label (verdict) | SAM+P6 label (verdict) |
|---|---|---|
| SAM_Tip | Tip (Adopt, 30 cells) | not resolved |
| SAM_Core | none. Defined by UNK+ gene positivity (Dataset S5), not a cluster | none |
| Indeterminate_Meristem / SAM_Periphery | Meristem 2 (Revise: KN1/LG3 periphery-boundary plus heat-stress GO); Meristem 1 (Revise: no marker, GST/TRX stress) | Indeterminate, cl 5 (Revise: KN1+ stem/leaf base, not SAM) |
| Boundary | inside Meristem 2 | Boundary recluster, Fig. S9 (Revise: positional state) |
| Leaf_Primordium | Primordia (Revise: organ, not type) | Leaf primordia, cl 0 (Revise) |
| Procambium | Vasculature (Adopt) | Vasculature, cl 6 (Adopt; may include early xylem/phloem) |
| Epidermis | Epidermis 1 (Adopt) + Epidermis 2 (Revise, merge) | Epidermis, cl 1, 10 (+8 in G2/M) (Adopt) |
| Mesophyll | none | probably the unnamed cl 9 (Reject as labelled "Unknown") |
| S_Phase / Dividing_cells | regressed out | S-phase cl 3, G2/M cl 4 (Reject as types; use as states) |
| Unknown / low quality | none | cl 2 (organelle transcripts), 7, 11 (Reject) |
| Kn1-O vs WT poles | - | Indeterminate/Determinate (Revise: trajectory poles) |

## Recommended label reference

There is no adoptable per-cell reference. For maize shoot-apex data, use Satterlee 2020 as a marker source (in situ-validated tip, core, boundary, epidermis and provascular genes), not as a label source. If labels are needed, reprocess SAM+P6 (PRJNA637882, 10x v3, about 40 Gb per replicate) in a compute job and re-cluster. Use only Epidermis, Vasculature and the KN1+ cluster as anchors. SAM+P2 (327 cells) is too small to train on.

## Cross-study markers (confidence raised one level, or already high and confirmed)

Within this group, all agreement comes from independent literature in situ studies, plus one maize root atlas. There is no second shoot-apex single-cell dataset.

| Gene (v5) | Symbol | Cell type | Studies |
|---|---|---|---|
| Zm00001eb011320 | DYN | SAM_Tip | Satterlee 2020 in situ + Knauer 2019 in situ |
| Zm00001eb055920 | KN1 | Indeterminate_Meristem | Jackson 1994 in situ/mutants + Satterlee cluster DE (already high) |
| Zm00001eb299420 | RS1 | Indeterminate_Meristem | Schneeberger 1995 in situ + Satterlee cl 5 (52% vs 2%) |
| Zm00001eb079890 | FCP1 | Leaf_Primordium | Je 2016 in situ/function + Satterlee in situ |
| Zm00001eb008680 / 400130 | DRL1 / DRL2 | Leaf_Primordium | Strable 2017 + Satterlee cl 0 (low raised to medium) |
| Zm00001eb372180 | PIN1a | Procambium | Carraro 2006 localization + Satterlee cl 6 |
| Zm00001eb026490 | AUX1-like | Procambium | Knauer 2019 in situ + Satterlee Vasculature/cl 6 |
| Zm00001eb235450 | RANBP2-like | Procambium | Takacs 2012 in situ + Satterlee Vasculature/cl 6 |
| Zm00001eb024680 | OCL4 | Epidermis | Vernoud 2009 + Knauer 2019 + Satterlee (already high) |
| Zm00001eb406100 | LTP1 | Epidermis | Takacs 2012 and Knauer 2019 in situ + Satterlee |
| Zm00001eb046050 | KCS | Epidermis | Liu 2021 in situ (as cited in Dataset S2) + Satterlee |
| Zm00001eb352410 | CYC1 | Dividing_cells | Satterlee in situ + Guillotin 2023 maize root G2_M list |

## Gaps (expected types with no validated marker in the draft)

- SAM_Tip has no `function` marker (only DYN and ZNF-LIKE). SAM_Periphery has none of its own.
- No marker at all for Stem_Parenchyma (pith), Axillary_Meristem or Leaf_Base function. Leaf_Base has only the in situ LSH-LIKE genes.
- No maize-specific marker for Mesophyll, Bundle_Sheath, Xylem, Phloem, Stomatal_lineage, Guard or Subsidiary. These rely on the Arabidopsis and sorghum leaf tables (PPDK, NADP-ME, SUT1, CST1 and others). The SAM+P6 photosynthetic cluster was never named.
- No Boundary or Preligule `function` marker. LG1 (in `sorghum_leaf.tsv` as Ligule) is the obvious candidate to add for Preligule.
- L1 vs L2 in the SAM cannot be separated with the current markers.

## Overlap with existing skill tables

- The skill has no maize table. `sorghum_leaf.tsv` and `sorghum_root_Guillotin2023.tsv` use sorghum IDs, but the Guillotin source table (`source/CommonMarkersGrasses_Guillotin2023.tsv`) keeps the maize v5 IDs. Three draft genes appear in it: PIN1a Zm00001eb372180 (root Xylem), AUX1-like Zm00001eb026490 (root Xylem and G2_M) and CYC1 Zm00001eb352410 (G2_M, the agreement used above).
- Symbol collision: maize DRL1 (drooping leaf1, a YABBY) is a different gene from rice `qSOR1/DRL1` in `rice_root.tsv`. Compare them by ID.
- Shared names with existing tables: Epidermis, Procambium, Xylem, Phloem, Mesophyll, Bundle_Sheath, Dividing_cells, S_Phase. New names introduced: SAM_Tip, SAM_Core, SAM_Periphery, Boundary, Indeterminate_Meristem, Leaf_Primordium, Leaf_Base, Preligule, Stem_Parenchyma, Axillary_Meristem. Preligule may be merged with sorghum `Ligule`.

## Conflicts and corrections to the review

- **CUC2 (GRMZM2G393433)**: the review lists it under Meristem 2, but in Dataset S2 it is a **Tip** DE gene (43% vs 7%). It is kept as Boundary (Fig. S9B, Johnston 2014), with the conflict written in `basis`.
- **GA2OX1 (GRMZM2G051619)**: it is not in Dataset S2, and in SAM+P6 it is not cluster-specific (~90% of cells in clusters 6, 7 and 10). Its support is the Bolduc & Hake 2009 in situ. Kept at medium, not raised.
- **GRMZM2G094353**: the review graded it `expression`. It is the "RANBP2" vascular marker of Fig. S7B (UniProt: RanBP2-type zinc finger), with a cited Takacs 2012 in situ and specificity in both datasets. Regraded to characterized_enriched, high.
- **HYP1 (GRMZM2G304378)**: the paper's v3 annotation is "hybrid proline-rich protein1" (Dataset S2/S7). Both the v3->v5 and v4->v5 crosswalks give Zm00001eb375490, which UniProt names ribonucleoside-diphosphate reductase. The v5 ID is unreliable, so the row uses the v4 ID and is marked `REVIEW:`. In SAM+P6, HYP1 is enriched in the KN1+ cluster 5 (70% vs 19%), not in leaf primordia.
- **DRM1 (GRMZM2G123896)**: v4 gives two loci (032422/032423), and neither maps to v5. It is broadly expressed in SAM+P6. Marked `REVIEW:`, low.
- **ZNF-LIKE (GRMZM2G318296)**: the paper's annotation is a C3HC4 RING finger, but UniProt calls the v5 product a VWFA-domain protein. A possible model change between versions; noted in `basis`.
- **PIN1a**: v4 Zm00001d044812 maps to two v5 genes. Zm00001eb372180 (UniProt Q0MWY2, auxin efflux carrier) is used. Zm00001eb372190 is uncharacterized.
- **LSH-LIKE (sheath)**: the main text ID GRMZM2G816289 is a typo for GRMZM5G816289 (primer table). Of its two v5 genes, Zm00001eb274030 (ALOG domain) is used rather than Zm00001eb306950.
- **YAB15 and FPF1-LIKE** are graded down to low: YAB15 is spread over 7 SAM+P6 clusters, and FPF1-LIKE is mainly epidermal in SAM+P2 despite the provascular in situ.
- **FEA3** is enriched in the unnamed photosynthetic cluster 9 in SAM+P6.

## What could not be verified

- I did not open the cited in situ papers (Knauer 2019, Takacs 2012, Johnston 2014, Liu 2021, Je 2016, Strable 2017, Schneeberger 1995, Carraro 2006, Jackson 1994, Vernoud 2009). The raised confidences rely on Dataset S2's statement that its citations are in situ evidence, and on the known content of those papers. DOIs were confirmed in Europe PMC, except Jackson 1994 (10.1242/dev.120.2.405, which was not found by search).
- In particular, DRL1/2 in situ in Strable 2017 is not confirmed, which is why those rows stop at medium.
- The UniProt REST API does not index v4 (`Zm00001d`) IDs. Names were checked with v5 IDs only, and UNK, FCP1, DYN and WOX9C come back uncharacterized or unnamed there.
- No v5 ID for DRM1, and no trustworthy one for HYP1. Both need BLAST against the v5 proteome.
- The SAM+P6 cluster-number-to-name mapping (from Fig. S5B) is inferred, not published.
- I did not check whether scPlantDB or the Plant Cell Atlas hosts processed data or labels for PRJNA637882.

## Update 2026-10-20: gap-fill reviews

One new review was merged: `Dong2026/` (its README has the full desk review). `markers_draft.tsv` now has 55 rows (33 before): 22 rows added, 3 raised, 2 corrected, and Dong 2026 evidence written into the `basis` of 13 more. `expected_cell_types.tsv` gains a `Rib_Zone` row, and its notes and counts were updated (Epidermis function markers 6 -> 7, from FDL1).

### New dataset

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Dong2026 | Dong L, Sun Y, Kang L, Li Z, Liang Y, Sheng H, Tian F, Jackson D, Yang F (2026) Genome Biology. doi:10.1186/s13059-026-04033-x (Europe PMC PMC13112620); GEO GSE309101, SRA PRJNA1398575 | Protoplast scRNA-seq, BD Rhapsody; Seurat 4.3 + Harmony; protoplasting and cell-cycle genes regressed out | 17,563 cells, SAM+P1/P2 at 14/22/26 DAS, **one sample per stage, no replicates** | cluster_only (GEO count matrix, 71 MB, has no labels) | medium |

It uses v4 IDs, mapped to v5 here with the MaizeGDB crosswalk in `Satterlee2020/`. It also runs RNA in situs for KN1, UB3, NAC67, GST41, IDD7 and Zm00001d000506, and projects its clusters onto Satterlee 2020 (Figs S8 and S11).

### Verdicts (Dong 2026)

| Published label (clusters) | Verdict | Canonical |
|---|---|---|
| CMC central meristem (C3, C4) | Revise: KN1+ corpus, not tip; C3/C4 is a stage/sample split, so merge | Indeterminate_Meristem |
| LMC lateral meristem (C7) | Revise (weak): phosphate-starvation/ABA stress signature | SAM_Periphery candidate, no marker |
| RZC rib zone (C6, C9) | Revise: KN1+RS1+UB3 SAM base | Rib_Zone (new) |
| BC boundary (C15) | **Adopt** | Boundary |
| LPC leaf primordia (C2) | Revise: organ-level | Leaf_Primordium |
| VC vasculature (C1) | Revise | Procambium |
| VC vasculature (C11) | Reject: histone-driven S-phase | S_Phase state |
| Xylem (C17) | Revise: no secondary-wall genes | protoxylem precursor (Procambium/Xylem) |
| Phloem (C18) | **Adopt** | Phloem (protophloem/SE precursor) |
| EC epidermis (C8, C10, C12, C16) | **Adopt**: merge, C16 = G2/M epidermis, C12 = wax-rich | Epidermis |
| CC G2/M (C5, C13), S-phase (C14) | Reject as types | Dividing_cells / S_Phase states |

### Markers raised (cross-study rule: validated in one study and cluster-specific in another)

| Gene (v5) | Symbol | Cell type | Change | Studies |
|---|---|---|---|---|
| Zm00001eb264380 | CUC2 | Boundary | medium -> high | Satterlee 2020 boundary recluster + Johnston 2014; Dong C15 (52% vs 6%) |
| Zm00001eb043940 | YAB10 | Leaf_Primordium | medium -> high | Satterlee 2020 in situ; Dong C2 (35% vs 12%) |
| Zm00001eb171720 | OCL5 | Epidermis | medium -> high | Satterlee 2020 Epidermis clusters; Dong C8/C10/C12/C16 (57-85% vs 8-10%) |

Confirmed and already high: KN1, RS1, PIN1a, AUX1-like (aic1), RANBP2-like, OCL4, KCS, CYC1. Checked in Dong Table S7 but not raised (broad or absent): LG3, GA2OX1, YAB15, WAT1-LIKE, LSH-LIKE. Absent from Table S7: DYN, ZNF-LIKE, UNK, GRAS33, DRM1, FCP1, FEA3, WOX9C, DRL1, DRL2, YAB14, ZOS2-LIKE, LSH-LIKE2, LTP1, H3.

### Markers added (22, all `source` = Dong 2026)

- SAM_Tip: NAC67 (in situ in the upper dome, but also epidermal in scRNA; low).
- Rib_Zone: UB3 (in situ at the SAM base; broad and stage-induced; low).
- Boundary: GST41 (in situ, medium) and CUC3 (low).
- Leaf_Primordium: IDD7 (in situ, medium).
- Epidermis: FDL1 (function, medium); Zm00001d000506 (in situ, medium, v4-only `REVIEW:`); OCL8/HB91, HDZIV-like, LTP3 (low); FPF1-LIKE as Epidermis (expression, medium for two-study agreement).
- Procambium: IAA15 (low). Xylem (protoxylem precursor): WAT1, bHLH TMO5-like (low).
- Phloem: CALS7, KAN-FEATHERED, GST11, CRSP, NAC28/NAC57 (all low, single study).
- States: CYCB1-4 (Dividing_cells), PCNA2 and CYCA3-1 (S_Phase), all medium.

Expression-only rows were set to `low` following the skill README default. The review had graded several of them `medium`.

### Corrections to existing rows

- **HYP1 (`Zm00001d045192`, Leaf_Primordium)**: Dong Table S7 annotates this v4 ID as ribonucleoside-diphosphate reductase large subunit, and UniProt names the v5 model RNRL1. It is enriched in S-phase C14 (90% vs 49%). So the v3->v4 mapping of GRMZM2G304378 probably points to the wrong gene. The row is kept (low, `REVIEW:`), but its basis now says not to use it until the gene is found by BLAST.
- **FPF1-LIKE (`Zm00001eb142230`)**: Dong 2026 finds it only in epidermal clusters. The Procambium row stays at low with a "do not use" note, because the Satterlee in situ is provascular. A separate Epidermis row was added.

### Gaps closed

- **Boundary**: there is now an adopted boundary cluster and a high-confidence marker (CUC2), plus an in situ gene (GST41). There is still no `function` marker.
- **Phloem**: first maize-specific candidates (C18), all low.
- **Rib_Zone** was added as an expected type and has one low marker.

### Gaps remaining

- SAM_Tip has no `function` marker, and Dong 2026 resolves no tip cluster. SAM_Periphery still has no marker.
- Stem_Parenchyma, Axillary_Meristem, Leaf_Base function, Preligule function, Mesophyll, Bundle_Sheath, Stomatal_lineage, Guard, Subsidiary and Trichome are unchanged. Dong 2026 sampled only SAM+P1/P2.
- Xylem has only precursor genes, with no secondary-wall genes.
- Candidates from the characterized-marker survey (`survey/characterization/characterized_markers.tsv`), not yet added because no review in this group tested them: LG1 `Zm00001eb067740` for Preligule (function, high) and BA1 `Zm00001eb148990` for Axillary_Meristem (function, high, in situ). Their IDs do not match any draft row, so they gave no independent support. The Arabidopsis CUC2/LOB, CLV3 and ANT rows in that table support Boundary, SAM_Tip and SAM_Periphery only by homology.

### Conflicts

- Dong's "CMC" is not the Satterlee tip. Their Sankey (Fig S11a) maps Satterlee's Unknown group onto LPC/CMC.
- The new RS1 data place the gene highest in the rib zone (C9) rather than the corpus. The row stays Indeterminate_Meristem, with a note in its basis.
- RANBP2-like is strongest in phloem C18 (80%) as well as procambial C1. It is a provascular-plus-early-phloem marker.
- With no replicates, the stage-enriched clusters (C3, C4, C6, C7) are confounded with sample.

### Recommended label reference (revised)

There is still no per-cell label set. For labels, Dong 2026 is now the better re-clustering target: its post-QC count matrix is public on GEO (GSE309101, 17,563 cells), whereas Satterlee 2020 has only raw SRA reads. Re-derive clusters in a compute job and anchor only on the adopted Boundary (CUC2+CUC3+GST41), Epidermis (OCL4/OCL5), Phloem (C18 genes) and the KN1+ corpus. Satterlee 2020 remains the main source for tip and core markers.

### Could not verify (this update)

- No v5 ID for Zm00001d000506. PIN1a v4 still maps to two v5 models. The DOF11, APL, TMO5, LTP2, CYC3, CYC18 and UMC1283 genes used by Dong have no IDs in the paper's tables.
- Population fractions are read off the Fig S11a Sankey and are approximate.
- The cited in situ papers for RS1 (Becraft & Freeling 1994) and FDL1 (La Rocca 2015) were not opened.
