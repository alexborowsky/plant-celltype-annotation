<!-- Collated from the survey review of maize_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Maize root single-cell datasets: group summary (Part A, Steps 1-3a)

Date: 2026-10-20. This collates four paper-only reviews (one per subfolder, each with its own README) into one marker table and one expected-cell-type list. No in-data check (Step 3b) has been run.

Files in this folder:
- `expected_cell_types.tsv`: expected types for a maize primary/seminal root tip (0-5 mm), written from anatomy. `function_markers` counts `function` rows in `markers_draft.tsv`.
- `markers_draft.tsv`: 65 rows in the skill marker-table schema plus `alt_id`. `ref_gene` holds B73 RefGen_v4 IDs (`Zm00001d`) and `alt_id` holds B73 v5 IDs (`Zm00001eb`). For v5 data, use `map_markers.py --id-column alt_id`. Field counts were validated with awk.
- `OrtizRamirez2021/`, `Guillotin2023/`, `Wang2025/`, `Cao2023/`: the per-dataset reviews, supplements and extracted tables.

The skill has no maize marker table, and this draft does not edit the skill.

## Datasets

| Dataset | Material | Platform | Cells (maize) | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Ortiz-Ramirez et al. 2021 *Science* 374:1247 (10.1126/science.abj2327), GEO GSE172302 | B73 seminal root tips, 7 DAG | protoplast scRNA, 10x v2/v3; labels by ICI against reporter/dye-sorted bulk | 14,733 (22 GEO clusters) | v4 | Small table: GSE173087 per-cell cluster IDs; names only in Fig 2B (merged in `OrtizRamirez2021/labels_from_GEO_cluster_plus_Fig2B.tsv`). Sorted-tissue bulk GSE172280 downloaded | medium |
| Guillotin et al. 2023 *Nature* 617:785 (10.1038/s41586-023-06053-0), GEO GSE225118 | B73 primary+seminal tips 0.5 cm | the same 3 protoplast libraries as 2021 (v2) + 4 nuclei libraries (v3); pan-grass SCT integration | 7,615 (4,324 cells + 3,291 nuclei), 19 clusters | v4 | Table: GEO metadata with cluster numbers; names inferred from ST4 order (`Guillotin2023/labels_maize_inferred.tsv`). Authoritative names are only in the 3.7 GB RData | medium |
| Wang et al. 2025 *Nat Commun* 16:177 (10.1038/s41467-024-55485-3), GSA CRA015077 | B73 primary root tip 4 mm, 4 d; control and 42 °C | protoplast scRNA, 10x v2 | 35,103 (CK 16,742) | v4 | Cluster only: Supp Data 2 markers by type, no per-cell labels | medium |
| Cao et al. 2023 *Plant Biotechnol J* 21:1839 (10.1111/pbi.14097), SRA PRJNA865791 | Qi319 and B104 tips 0-5 mm, mock and *Fusarium* | protoplast scRNA, 10x v3, no integration | 29,217 (21 clusters into 7 types) | v4 | Cluster only: Table S2/S3, raw FASTQ only (~125 GB) | low |

Independence: Guillotin 2023 reuses the 2021 protoplast libraries and comes from the same lab. Agreement between Ortiz-Ramirez 2021 and Guillotin 2023 was therefore **not** counted as cross-study agreement. The 2021 sorted-tissue bulk (GSE172280) was used as tissue-level support, not as a second study.

## Verdicts by expected cell type

A = Adopt, R = Revise, X = Reject, - = not annotated. Verdicts are taken from the reviews, with the corrections described below.

| Expected type | Ortiz-Ramirez 2021 | Guillotin 2023 | Wang 2025 | Cao 2023 |
|---|---|---|---|---|
| Columella | - | A (nuclei only) | R ("Columella" 20%, whole cap) | - |
| Lateral root cap | R (merged "Epidermis/LRC") | R ("LRC" is a stress state; Epidermis_2 is cap-like) | - (in Columella) | X ("RC" markers are the phloem/endodermis module) |
| QC / initials | R (QC, 115 cells; marker is a snoRNP gene); X ("Initials") | - | X ("Initials" = G2/M) | - (wox5b reporter only) |
| Epidermis | R (merged with LRC; one library) | R (Epidermis_1/2/3 batch- or nuclei-driven) | A | R (weak markers) |
| Trichoblast | - | R ("Trichoblast", no hair genes, one library) | - | - |
| Exodermis/hypodermis | - | - | - | - |
| Cortex | R (4 subtypes, collapse) | A Cortex_1; R Cortex_2-4 (states) | A | A (9 clusters) |
| Endodermis | A cl6 / R cl12,16 (**contested, see below**) | R ("Endodermis" = 2021 Pith) | A (**contested**) | R (early/merged) |
| Pericycle | R | R (stress genes) | R (GST/peroxidase) | - (in stele) |
| Xylem | A | A | A | A (metaxylem) |
| Phloem | R | A (**contested**) | R (markers are cap genes in bulk) | - (in stele) |
| Procambium / stele bins | R (3 stele clusters) | R/X (Stele_1, Stele_2, Young_Stele_2) | R ("Stele") | R ("Stele") |
| Pith / stele parenchyma | R ("Pith") | - (labelled Endodermis) | - | R (cluster 14, central pith in situ) |
| Proliferation states labelled as types | "Cortex II (E)" (histone H4), "Initials" | handled as G2_M (A) | "Initials" (G2/M) | "RAM" (S-phase histones) |

## Markers supported across independent studies

These are the 18 rows whose `confidence` was raised for agreement on the same v4 ID. The full basis is in `markers_draft.tsv`.

| Type | v4 / v5 | Symbol | Studies |
|---|---|---|---|
| Xylem | Zm00001d035689 / Zm00001eb267050 | ccp5 (XCP2-like) | in situ Cao; DE in Wang, Ortiz-Ramirez, Guillotin |
| Xylem | Zm00001d032672 / Zm00001eb045580 | - | in situ Wang; Guillotin Xylem |
| Xylem | Zm00001d002828 / Zm00001eb075510 | nactf131 | Cao + Guillotin DE |
| Xylem | Zm00001d017936 / - | IDP737 | Wang + Guillotin DE |
| Cortex | Zm00001d029859 / Zm00001eb023070 | LTP | in situ Cao; DE in Wang, Guillotin |
| Epidermis | Zm00001d032822 / Zm00001eb046900 | Gly-rich | in situ Wang; Guillotin epidermis |
| Epidermis | Zm00001d040090 / Zm00001eb126140 | ocl1 | Wang + Guillotin DE |
| Epidermis | Zm00001d032823 / Zm00001eb046910 | GRP-like | Wang + Guillotin DE |
| Columella | Zm00001d004089 / Zm00001eb086310 | PRP18 (SCP) | in situ Wang; Guillotin Columella; cap bulk |
| Columella | Zm00001d049129 / Zm00001eb169090 | umc2696 | Wang + Guillotin; cap bulk |
| Columella | Zm00001d044652, Zm00001d014603 | - | Wang + Guillotin DE |
| Quiescent_Center | Zm00001d042821 / Zm00001eb147630 | wox5b | reporter and in situ in Cao; QC-sorted bulk in Ortiz-Ramirez |
| Pericycle | Zm00001d043361 / Zm00001eb152300 | X8-domain | Wang Pericycle + Guillotin Young_Phloem (holds only if Young_Phloem is pericycle) |
| Dividing_cells | Zm00001d026129, Zm00001d027589, Zm00001d023810, Zm00001d033112 | cyc23, umc1948, csld1, krp13 | Guillotin G2_M + Wang "Initials" (umc1948 HCR) |

Several genes agree across studies but were **not** raised, because their specificity is weak: Zm00001d017508 (cortex; 4 studies), rc109 Zm00001d004725, and Zm00001d051419 (stele/pericycle).

## Conflicts and corrections to the reviews

1. **Endodermis vs phloem module (main conflict).** The same co-expressed genes appear under different labels in different studies:
   - Genes: Zm00001d049606, 050168, 023477, 021674, 020794, 019069.
   - Ortiz-Ramirez 2021 and Wang 2025 call them **endodermis**. Guillotin 2023 calls them **phloem**. Cao 2023 calls them **root cap**.
   - New finding: Wang's endodermis in situ gene (050168) is specific to the Guillotin *Phloem* cluster (11.4 vs ≤0.75).
   - Evidence for phloem:
     - Guillotin's two-colour HCR shows the sorghum ortholog as spots inside the green endodermal ring.
     - ZmSCR1 is not enriched in that cluster in Guillotin, and is not a Wang endodermis DE gene.
     - The 2021 "SCR1-sorted endodermis" bulk is as high as stele for the phloem genes sut1 (4,347 vs 4,644) and sweet13a (134 vs 20). That suggests the sorted pool contains phloem cells.
   - Evidence for endodermis: the 2021 sorted bulk is 4.5x higher than stele for 049606, and Wang shows a low-resolution ring.
   - Decision: the module is filed under **Phloem** at `low` confidence, with "CONFLICT" in `basis`. Test it in the data: does it co-express with SCR1/SHR1/2 or with SUT1? Is it one cluster at the stele periphery or several poles?
   - Consequences:
     - The Adopt verdicts for Ortiz-Ramirez "Endodermis (M)" and Wang "Endodermis" become Revise.
     - The Guillotin Phloem Adopt stays provisional.
     - No maize dataset has an undisputed endodermis cluster. Endodermis markers are limited to SCR1/SHR genes, which are poorly detected.
2. **Guillotin "Endodermis" is pith or stele parenchyma.** Its cells were Pith in 2021. Its top gene, 049683, is a Cao stele in situ gene, and 003707 (Cao stele/central-pith in situ) also peaks there. Both are filed under `Stele_Parenchyma`.
3. **Guillotin "Young_Phloem" is probably pericycle.** Its top genes are pericycle DE genes in Wang (043361; 051419), and its HCR gene 011156 marks a ring at the stele periphery. Wang's pericycle genes (dirigent 005472, gst12/13) peak in Guillotin Stele_2. Neither call is settled.
4. **Wang 2025 "Phloem" markers are root-cap genes in the bulk.** The in situ gene Zm00001d037032 (TBL) is 12,284 in dissected cap vs 1 in stele, and nactf116 (037029) is 1,358 vs 0. Both peak in Guillotin Columella. They are excluded from the table.
5. **Cao 2023 "Epidermis" in situ genes are contradicted by the bulk.** 033711 peaks in Guillotin Pericycle, and 025614 is cap-high. Both are excluded. Cao's "RC" genes belong to the module in item 1.
6. **Misnomers.**
   - Wang's cortex "PLT29" (012081) is an LTP, not PLETHORA.
   - "Cortical cell-delineating protein" (017508) is an LTP-domain gene that maps to two v5 models.
   - Ortiz-Ramirez's QC marker 052952 is an H/ACA snoRNP (ribosome biogenesis) gene and was excluded.
7. **ID notes.**
   - ZmSHR2 = gras19 (Zm00001d021973) and ZmSHR2-h = gras85 (Zm00001d006721) were inferred by matching bulk values to the figure. The paper's tables were inaccessible and UniProt names neither gene, so both rows are `low`.
   - ZmSHR1 = gras58 (Gramene synonym shr1), and SCR1 = UniProt Q9FUZ7.
   - wox5a/wox5b were confirmed in the MaizeGDB/Gramene v4 gene table, and wox5b in UniProt (A8Y7W0).
   - IDP737 (017936) has no v5 ID.
   - These v4 IDs map to more than one v5 model: 017508, 022228, 029607, 038533, 032776 (cesa10 also maps to an eIF-iso4F model) and 040390.
8. **Additions not in the reviews**, taken from the paper tables and the MaizeGDB gene table (ID checked in UniProt): cesa10 and cesa11 (Xylem), sut1 (Phloem companion cells) and pcna2 (S phase). Their literature function claims were not re-verified.

## Gaps

These expected types have no validated marker (`function` or in situ `characterized_enriched` at medium or above):
- Exodermis/hypodermis: no dataset annotates it.
- Trichoblast: not expected in tip samples.
- Stem-cell initials: not separable from the meristem.
- Procambium.
- Phloem sieve elements and companion cells: SUT1 is weak, and the phloem module is contested.
- Proto- vs metaxylem split.
- Lateral root cap as distinct from columella: only grp4, which also marks epidermis.
- Endodermis in scRNA: SCR1/SHR are function markers but barely detected.
- Pericycle function markers.

The rice and Arabidopsis root tables can add, via homology: CASP1 and MYB36 (endodermis), the SMB ortholog (LRC), APL (phloem) and trichoblast genes.

## Recommended label reference

**Guillotin 2023** is the best reference to work from. It has a public per-cell cluster table, includes nuclei (so it captures columella), labels G2/M as a state, has HCR validation and full marker and average-expression tables. Adopt only Columella, Xylem, merged Cortex and G2_M. Treat its Phloem/Endodermis/Young_Phloem/Stele labels as hypotheses (see Conflicts). Confirm the cluster-number-to-name mapping from the 3.7 GB RData on a compute node first.

For tissue-level checks, use the **Ortiz-Ramirez 2021 sorted-tissue bulk** (GSE172280, already downloaded). Its endodermis sort may include phloem.

Wang 2025 is the largest independent protoplast dataset, but its labels are cluster-only. Use its markers, not its labels. Cao 2023 is low quality, so use only its in situ genes.

## Overlap with existing skill tables

The skill has no maize table. `sorghum_root_Guillotin2023.tsv` stores the maize v5 ID in its `symbol` column. 14 of the 65 draft genes appear there:
- Agreeing: ccp5, nactf131 and IDP669 (Xylem); 014603 (Columella); csld1 and krp13 (Dividing_cells); ocl1 and IDP7964 (epidermal subclusters); rcph2 (Root_Cap here, Columella there); 020794 (Phloem).
- Disagreeing: 021850 and 046778 are Endodermis here but Pericycle/Stele_2/Xylem there; 011156 and 043361 are Pericycle here but Young_Phloem there.

The Arabidopsis and rice root tables were not compared by homology.

## Could not verify

- Ortiz-Ramirez 2021 Tables S1-S3 and the supplementary figures are behind a reCAPTCHA/Cloudflare check and a 403. The SHR2/SHR2-h IDs and the per-cluster marker statistics could not be checked. The user can download them from the PMC article page.
- The Guillotin cluster-name mapping is inferred. The authoritative names are in the 3.7 GB RData, which was not downloaded.
- Wang 2025: the GSA pages are behind a bot check, no per-cell labels exist, and the full-resolution in situ images are in a 163 MB Source Data zip that was not kept.
- Cao 2023: no processed data. The in situ images have no sense controls.
- Literature functions marked "not re-verified" in `basis` were not checked against the original papers: rcph1/2 cap periphery, zrp2 cortex, ocl1 L1, csld1 division, CesA10-12 secondary wall and SUT1 companion cell.
- The SI PDFs were not parsed.
