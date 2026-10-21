<!-- Collated from the survey review of soybean_nodule (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Soybean (*Glycine max*) nodule: group summary of cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill. Inputs: the one review for this group in
`survey/merged_reviews.json` (`CervantesPerez2024/`), plus a cross-check I added against the nodule part
of Zhang et al. 2025 *Cell*, done from that paper's supplementary tables and GEO pseudobulk
(`Zhang2025_crosscheck/`). Zhang 2025 is **not** a full Part A review. Its root part was reviewed in
`../soybean_root/Zhang2025/`. The skill was not edited.

Files written here:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Expected types for a mature (3-4 week) determinate soybean nodule, from anatomy. `function_markers` is counted from `markers_draft.tsv` |
| `markers_draft.tsv` | 78 rows (77 genes) after the 2026-10-20 update below (was 47), skill schema + `alt_id`. `ref_gene` = `Glyma.xxGxxxxxx` (Wm82.a2 Phytozome style, the style used by most soybean count matrices); `alt_id` = Ensembl Plants `GLYMA_xxGxxxxxx` (same locus) |
| `Zhang2025_crosscheck/` | Zhang 2025 nodule tables extracted for the cross-check (see below) |

## Datasets

| Dataset | Platform | Cells | Label access | Quality | Role here |
|---|---|---|---|---|---|
| **Cervantes-Pérez et al. 2024** *Plant Commun* 5:100984, doi 10.1016/j.xplc.2024.100984; GEO GSE226149 | snRNA-seq (10x 3' v3.1, FACS nuclei) of 28-dpi Williams 82 nodules + Resolve Molecular Cartography (28 soybean + 9 *Bradyrhizobium* probes, one section) | 7,830 nuclei, 2 replicates, 11 clusters (~1,060 UMI/nucleus) | `table`: per-nucleus cluster IDs from the public Tabula Glycine portal (`CervantesPerez2024/labels.tsv`) | medium (full review in `CervantesPerez2024/README.md`) | **Label reference**; source of all spatially validated markers |
| **Zhang et al. 2025** *Cell* 188:550, doi 10.1016/j.cell.2024.10.050; GEO GSE270392 (nodule part, cross-check only) | snRNA-seq + scATAC-seq (10x); no Visium for nodule | 12,609 snRNA nuclei from 15-dpi roots carrying ~1 mm nodules (*B. japonicum* USDA110), root tips removed; 2 replicates; median 1,238 UMI | `table`: per-nucleus labels in Table S1 (`mmc1.xlsx`, 41.8 MB, in `../soybean_root/Zhang2025/`); nodule rows extracted to `Zhang2025_crosscheck/TableS1_snRNA_early_nodule_labels.tsv.gz` | low-medium for nodule (my assessment, not a full review): 67% of nuclei are `Cortex_Epidermis` (mostly attached root), labels are forced, and several nodule labels were assigned with Cervantes-Pérez markers | Independent second dataset for cross-study agreement. Young nodules |
| Liu et al. 2023 *Nat Plants* 9:515, doi 10.1038/s41477-023-01387-z (snRNA-seq + spatial, soybean nodule development) | not accessed | - | not checked | not assessed | Paywalled, and the bioRxiv preprint (10.1101/2022.06.30.498286) returned Cloudflare error 1015. Its marker IDs were used only as Zhang 2025 Table S2 cites them (secondary source) |

GEO nodule objects from Zhang 2025 were not downloaded (sizes in `Zhang2025_crosscheck/GEO_nodule_file_sizes.tsv`):
`GSE270392_Gm_atlas_Early_nodule.rna.seurat.obj.rds.gz` (516 MB), `..._Early_nodule_metav3_gene_sparse.rds.gz`
(208 MB), `GSE270392_Early_nodule.soc.processed.rds.gz` (609 MB), `..._ACR_sparse.rds.gz` (169 MB). The small
pseudobulk table `GSE270392_Gm_atlas_Early_nodule_RNA_gene_cellstate_counts.txt.gz` (0.46 MB) was downloaded,
and CPMs for the draft genes are in `zhang_nodule_pseudobulk_cpm_markers.tsv`.

### How the Zhang 2025 cross-check was done
- Table S2 (`mmc2.xlsx`, already downloaded with the root review) has the de novo snRNA markers for the nodule
  (top 50 per cluster: infected, uninfected, meristem, endodermis, pericycle, procambium, phloem, xylem,
  cortex/epidermis) and the literature markers used to label each nodule cluster. Extracted to
  `TableS2_snRNA_denovo_markers_nodule.tsv` and `TableS2_literature_markers_early_nodule.tsv`.
- Cluster correspondence (best-matching Cervantes cluster for each of Zhang's top-50 marker genes,
  from Cervantes Table S1): Zhang infected → F/G (40/50); uninfected → K (16/50, diffuse); Xylem → D (36/50);
  Endodermis → C (20/50); Procambium/Pericycle/Phloem → E (37, 21 and 26 of 50); Cortex_Epidermis → A;
  "Nodule meristem" → A/I (low expression in mature nodules). The two atlases agree on compartments.
- **Circularity rule:** Zhang labeled some nodule clusters using Cervantes-Pérez markers (their Table S2
  `Early_nodule` column: 16G106800/14G218700 → Endodermis, 02G003700/18G062100 → Pericycle, the
  CesA genes → Xylem, Liu 2023 genes → infected/uninfected). A gene that Zhang used to label a cluster
  does not count as independent agreement for that cluster. Agreement counts when the gene is a de novo Zhang
  marker that Zhang did not use for that tissue's label.

## Per-cell-type verdict matrix

Verdicts for Cervantes-Pérez come from its review (Adopt/Revise). For Zhang 2025 they are my
cross-check assessments, not a full review.

| Expected type | Cervantes-Pérez 2024 (28 dpi) | Zhang 2025 (15 dpi, with root) | Liu 2023 |
|---|---|---|---|
| Infected_Cell | F + G **Adopt** (RIM by Molecular Cartography (MC), 97%); H Revise (N-fixing state; may be mixed with uninfected nuclei, uricase 72%) | `Nodule_infected_cell` 854 (6.8%): consistent (Rj2, CYCLOPS, RPG, SYMREM1 de novo; maps to F/G) | infected subtypes (not checked) |
| Uninfected_Cell | K **Adopt** (TAT/MLO by MC, uricase 71%); J Revise (no specific gene, replicate-skewed) | `Nodule_uninfected_cell` 856 (6.8%): plausible (INR2), diffuse | uninfected subgroups (not checked) |
| Cortex / Nodule_Parenchyma | A, B Revise (MC cortex markers; inner, outer and parenchyma merged; A is replicate-skewed) | `Cortex_Epidermis` 8,469 (67%): Reject as a nodule label (root-dominated, merged) | - |
| Epidermis | not resolved (inside A?) | merged in `Cortex_Epidermis` | - |
| Sclerenchyma | D Revise (21 nuclei; secondary-wall CesA/UXS by MC in the sclereid layer) | `Xylem` 93 (0.7%): same program, labeled xylem | - |
| Endodermis | C Revise (115; MC markers sparse; Table S8 calls it nodule parenchyma) | `Endodermis` 104 (0.8%): consistent (label partly circular) | - |
| Stele / Pericycle / Phloem / Xylem | E Revise (509; all vascular merged) | `Procambium` 1,331, `Pericycle` 439, `Phloem` 201: split, but labels partly circular | - |
| Senescing (state) | I Revise (236; stress/defense genes, three different labels, cited NAC genes not enriched) | none | - |
| Dividing_cells (state) | none (H4/PCNA ≤2.5%) | `Nodule_meritem` 262 (2.1%): unverified (markers include Cervantes root "niche" genes and PLT2) | - |

## Recommended label reference

**Cervantes-Pérez 2024** is the reference for mature nodules, because it has MC spatial validation in the
same tissue, small per-nucleus label tables, and Table S1 with % expressing per gene and cluster. Adopt
F+G (and H with caution) as `Infected_Cell` and K as `Uninfected_Cell`. Treat A/B, C, D and E as
lineage-level hypotheses to split in Part B, and I as a state. For **young (≤2-3 week) nodules**, use
Zhang 2025 labels for infected and uninfected cells only. Check its vascular labels against this draft, and
remove its root-dominated `Cortex_Epidermis` bin. Liu 2023 may be the better reference for nodule
development stages, but it could not be accessed.

## Markers (`markers_draft.tsv`)

47 rows. Evidence tiers: 10 `function`, 32 `characterized_enriched`, 5 `expression`. Confidence: 5 high,
32 medium, 10 low. By type: Infected_Cell 17, Cortex 7, Stele 6, Sclerenchyma 6, Uninfected_Cell 5,
Endodermis 4, Phloem 2. 46 genes: TPS (Glyma.15G210100) has deliberate rows in both Infected_Cell and Phloem,
because the two studies conflict.

Grading choices:
- MC (cell-resolution spatial) counts as in situ, so MC markers are `characterized_enriched` medium unless
  they are sparse (≤15% of their cluster's nuclei) or broad (then low).
- The `function` rows are characterized symbiosis/transport genes. Rows whose function was shown only in a
  Medicago/Lotus ortholog are medium.
- Single-study DE-only genes were left out (invertase 04G005700, the cluster I genes metallothionein
  18G180800, γ-thionin 16G100400 and CAP/PR-1 13G252600, and 05G203100). `expression` rows are kept only when
  the gene is lineage-specific in **both** independent atlases (medium by the lineage clause).
- New vocabulary that the skill would need: `tissue=nodule`, and the trait tag `Fabaceae` (should imply
  `eudicot` in `IMPLIES`). The symbiosis rows carry `requires=Fabaceae`.

### Cross-study markers (same gene ID, ≥2 independent studies, same compartment): 23 rows

**Formal confidence raises** (validated by MC in one study and cluster-specific in an independent, non-circular
cluster in another), 3 rows:

| Gene | Type | Evidence |
|---|---|---|
| Glyma.16G106800 (Ser/Thr kinase) | Endodermis | MC nodule vascular endodermis (Cervantes) + Zhang hypocotyl endodermis de novo 54% vs 1% → **high** |
| Glyma.14G218700 (C2H2 ZnF) | Endodermis | MC (sparse, 6%) + Zhang root endodermis de novo 18% vs 1% → **high** |
| Glyma.07G231500 (HPAT) | Stele | MC vascular bundle + Zhang nodule procambium de novo 14% vs 2% → **high** |

**Expression-level agreement** (no MC validation in either study, or the label conflicts), 20 rows:
Infected_Cell: Rj2 16G212300, SYMREM1.1 08G012800 (also Liu 2023), RPG 10G198700 (also Liu 2023), CYCLOPS
01G149500, 10G047800, 12G027100, 11G128800. Uninfected_Cell: INR2 06G109200 (Liu 2023 + Cervantes K 51% +
Zhang), UPS 02G116300 (Liu 2023 + Cervantes). Endodermis: 04G227200, 18G291000. Stele: PHO1-H1 02G003700
(already high by function), PHO1-H5 10G183300, SWEET14 06G125800. Phloem: 05G216000. Sclerenchyma/xylem:
CesA 06G065000, 04G063800, 09G051100, UXS 15G040000, laccase 14G062300.

## Gaps (expected types without a validated soybean marker)

- **Uninfected_Cell**: there is no clean `function` marker. Uricase reaches the N-fixing cluster (H 72%), and
  TAT/MLO are not supported in Zhang 2025.
- **Nodule_Parenchyma** (inner cortex / O2 barrier) and **Epidermis**: no marker at all. Neither atlas
  resolves them.
- **Cortex**: spatial markers only (best: 06G259400, 20G061300 medium). None are cortex-specific in Zhang 2025.
- **Pericycle, Xylem, Phloem (companion cells)**: no soybean nodule `function` marker. Use arabidopsis_root/leaf
  by homology (SUC2, CASP, PHO1) and the Stele rows here.
- **Sclerenchyma vs Xylem**: the secondary-wall genes cannot tell them apart.
- **Senescing and Dividing_cells** states: no validated nodule markers. Use the generic cell-cycle and
  senescence rows in the Arabidopsis tables.

## Conflicts and corrections to the review

- **TPS Glyma.15G210100**: MC infected cells (Cervantes) vs Zhang nodule phloem de novo (26% vs 4%; 705 vs
  ≤64 CPM). Graded low in both rows.
- **Glyma.05G216000**: used by Cervantes MC for a subset of infected cells (H 8%), but it is their root phloem
  marker and Zhang's nodule phloem marker (359 vs ≤25 CPM). Placed in Phloem, not Infected_Cell.
- **Cluster D "sclereid layer"**: Zhang labels the same transcriptional program `Xylem` (36 of its 50 xylem
  markers peak in D). Kept as Sclerenchyma, because MC places the genes in the sclereid layer, with xylem
  noted in `basis`.
- **Cluster C vascular endodermis vs nodule parenchyma** (Cervantes Methods vs Table S8): Zhang endodermis
  data favor Endodermis.
- **Glyma.02G116300**: UniProt names it "ureide permease A3", Liu 2023 (via Zhang) names it GmUPS2-2, and the
  review called it UPS1-like. Compare by ID. The GmUPS1 function (Collier & Tegeder 2012) belongs to other
  paralogs.
- **Glyma.20G061300** is not "uncharacterized" as the review says. UniProt names it ADP-ribosyl
  cyclase/cyclic ADP-ribose hydrolase (TIR-like).
- **Glyma.19G120400** is the "FEN1 ortholog" only per Table S7. UniProt calls it 2-isopropylmalate synthase
  (the same family as homocitrate synthase).
- **Glyma.14G218700**: the review graded it `expression` (6% of C). It is upgraded to MC-validated
  `characterized_enriched` high, because the Zhang root independently gives it as an endodermis marker.
- **TAT 06G235500 / MLO 06G002000** (Cervantes uninfected-cell MC markers) are not enriched in Zhang's 15-dpi
  uninfected cells. TAT is also a root/hypocotyl cortex marker. TAT stays medium with a caution, and MLO is low.
- **Lb genes**: Zhang's filtered pseudobulk lacks Lba/Lbc1 (and RIM, NOD26, DNF2, FEN1, uricase), so these
  could not be cross-checked. Lbc2 is only weakly infected-enriched there.
- I re-checked all 46 IDs in UniProt (free-text `GLYMA_<id> AND organism_id:3847`). The 36 IDs taken from
  the review were also checked in Ensembl REST `lookup/id`. Every ID resolves to the product given in the review or in this draft, apart from the two
  naming corrections above. Table S1 percentages were recomputed for every row.

## Overlap with existing skill tables

There is no soybean table in `references/markers/` (arabidopsis_leaf/root, rice_root, sorghum_leaf,
sorghum_root_Guillotin2023), so no rows overlap. By homology, `arabidopsis_root.tsv` contributes function
markers for Endodermis (7), Xylem (2), Phloem (2), Procambium (2), Pericycle (1) and Stele (1), and
`arabidopsis_leaf.tsv` contributes Dividing_cells (2), Senescing (1) and Phloem_Companion/SUC2 (1). These are
the fallback for the nodule's vascular and state gaps. No skill table covers nodule-specific types (infected
or uninfected cells). A related draft exists at `../medicago_root/markers_draft.tsv` (root only), and
`../lotus_nodule/Ye2024/` has a review but no group draft yet. Lotus and Medicago nodule markers would map
here only by homology, and Medicago is indeterminate, so its zones do not match soybean anatomy.

## Could not verify / access

- Liu et al. 2023 *Nat Plants*: paywalled. The bioRxiv preprint PDF and XML returned Cloudflare error 1015
  (rate-limited), and I did not try to get around it. Its marker IDs (SYMREM1.1, RPG, INR2, UPS, CBS1)
  are taken from Zhang 2025 Table S2 citations, not from Liu's own tables. Please download Liu 2023's
  supplementary marker table if you need these confirmed.
- europepmc.org article/PDF pages sit behind a Cloudflare challenge (not bypassed). The Zhang 2025 text came
  from the PMC OA S3 bucket, and its supplements were already local.
- Zhang 2025 nodule: no Visium for the nodule, and the large Seurat/ArchR objects were not downloaded. The
  per-cell checks use pseudobulk CPMs and Table S2 de novo `pct.1/pct.2` only.
- The Wm82.a2 → a4 ID identity was confirmed only for genes that appear in Zhang's a4 tables. For the others
  (RIM, NOD26, Lba, Lbc1, DNF2-like, FEN1-like, APX, UXS 13G334500, uricase `U032500` on an unanchored a2
  scaffold) it is assumed. **Check the uricase ID before use in a4-based data.**
- Cervantes MC images (Fig. S6/S8 PDFs) were not rendered, as noted in the review. Validation is taken from
  the main text, Fig. 2 and the Methods.
- Function claims for orthologs (DNF2, FEN1, IPD3/CYCLOPS, SYMREM1, RPG, CBS1) rely on the cited
  Medicago/Lotus papers. I checked the titles and DOIs in Europe PMC but did not re-read the papers.

## Update 2026-10-20: gap-fill reviews

One new review: **Liu et al. 2023** *Nat Plants* 9:515-524, doi 10.1038/s41477-023-01387-z (`Liu2023/`; full
review in `Liu2023/README.md`, verdicts in `Liu2023/evaluation.tsv`, reviewer rows in `Liu2023/markers_liu2023.tsv`).
This replaces the "not accessed" row in the datasets table above: the supplementary tables, source data, figures
and the authors' GitHub notebook were read; the main text and Methods stay paywalled.

| Dataset | Platform | Cells | Label access | Quality |
|---|---|---|---|---|
| Liu 2023 | 10x snRNA-seq of root, 12-dpi and 21-dpi nodules (one library each) + Stereo-seq (bin-level, DestVI deconvolution); Wm82.a2.v1 | 26,712 nuclei, 15 clusters; IC cluster 12 = 12-0 (492) + 12-1 (38) | `large_object` (per-nucleus cluster/UMAP from Source Data without barcodes in `Liu2023/nucleus_clusters_from_SourceDataFig1.tsv.gz`; processed data OMIX002290) | medium |

### Verdicts (Liu 2023)

| Liu label | Verdict | Maps to |
|---|---|---|
| Infected cells, cluster 12 / 12-0 (530 / 492) | Adopt | Infected_Cell (ISH of 02G098200 and 11G203900; strongly under-recovered, 2.6% of nodule nuclei) |
| IC subcluster 12-1 (38, 97% 12 dpi) | Revise | Infection_Thread_Cell (kind=state), not a type |
| Uninfected cells 0 / 7 | Adopt | Uninfected_Cell (labels from Stereo-seq deconvolution + Lotus ortholog AUC) |
| Uninfected cells 11 (21 dpi only) | Revise | Uninfected_Cell starch-mobilization state (BMY2/3) |
| Inner cortex 1 | Adopt | Nodule_Parenchyma |
| Outer cortex 2, 4 | Revise | Cortex (Stereo-seq-transferred labels; 9-11% root nuclei) |
| Vascular bundle 9 | Adopt | Stele (promoter-GUS 10G044800) |
| Vascular bundle 3 (77% root) | Revise | root stele; split by sample |
| Epidermis 5 (55% root) | Revise | Epidermis, mixed with root epidermis |
| Stele subclusters vb-0..6 | Revise | named by Arabidopsis label transfer, root-dominated |
| Unknown 6, 8, 10, 13, 14 | Reject | cluster 8 carries the draft's endodermis genes (16G106800 41%, 14G218700 36%, 18G291000 43% vs 1-2%), so it is probably nodule/root endodermis, but Liu left it Unknown |

### Markers added (31 rows; IDs as `Glyma.` with `GLYMA_` in `alt_id`)

- **Infected_Cell (5):** LHT-like 02G098200 (high: ISH + Cervantes F/G 63-68% vs 0), LRAT-like 11G203900 (high: ISH +
  Cervantes F/G), EGF-like 03G139300 (medium), 18G173300 (medium), ENOD55 02G204500 (medium; see conflicts).
- **Infection_Thread_Cell (8, kind=state):** VPY 05G088400, NNL1 02G076900, NPL 11G244800, SPK1 13G093600, RINRK1
  06G184400, 02G004800 (CRISPR: more but white nodules) (all `function` medium), SPL9d 19G146000 (`function` low),
  QWRF3 13G300600 (ISH 12 dpi only, medium).
- **Uninfected_Cell (4):** AAT 14G111800 (medium), uricase UR2 20G072400 (`function` low; broad), BMY3 05G068000
  (medium; Cervantes K 38%), BMY2 17G150100 (low).
- **Nodule_Parenchyma (4):** ENOD2/early nodulin-75 20G203800 (`characterized_enriched` medium; the review's
  `function` was lowered because the 1990 in situ cannot be tied to this paralog), CA1 06G182700 (medium; Cervantes
  B/C 36%), PEBP-like 19G194300 (ISH faint, low), CSLH1 12G096900 (low).
- **Stele (5):** WAT1-related 10G044800 (high: promoter-GUS + Cervantes E 36% vs 0), 13G240400, PER47-like 20G214200,
  ANN14 13G191200, LRP1 11G155400 (all `expression` medium, two-atlas agreement).
- **Cortex (2):** CYP716A-like 05G220500, SALI5-4A 12G217300 (low). **Epidermis (1):** 16G161100 (ISH outer layer, low).
- **Phloem (1):** AAP3 04G246400 (low). **Pericycle (1):** SWEET16 06G166900 (low). Both from label-transferred,
  root-dominated stele subclusters.
- Not added: MIP1-like 11G057600 (promoter-GUS over the whole central zone, but 9% of UC nuclei and ~0 in
  Cervantes-Perez; no single type). The review's `id_checked` column was dropped to keep the existing column set;
  all added IDs except ENOD2 (partial) were checked in UniProt (`Liu2023/uniprot_checks.tsv`).

### Existing rows raised or changed (Liu 2023 Supp. Data 3/8 read directly; independent of the other two atlases)

| Gene | Type | Change | Liu evidence |
|---|---|---|---|
| RIM 17G195900 | Infected_Cell | medium -> high | cl12 86% vs 11% |
| DNF2-like 02G102700 | Infected_Cell | medium -> high | 60% vs 3% |
| FEN1-like 19G120400 | Infected_Cell | medium -> high | 58% vs 3% |
| Rj2 16G212300 | Infected_Cell | medium -> high | 17% vs 0.3% |
| SYMREM1.1 08G012800 | Infected_Cell | medium -> high | 66% vs 3% (before: Liu only via Zhang's citation) |
| CYCLOPS 01G149500 | Infected_Cell | medium -> high | 32% vs 3% |
| 10G047800, 12G027100, 11G128800 | Infected_Cell | medium -> high | 84/59/29% vs 7/6/0.7% (expression-only, three atlases) |
| RPG 10G198700 | Infected_Cell | characterized_enriched medium -> function high | 12-1 79% vs <=1% |
| CBS1 16G177500 | Infected_Cell | characterized_enriched low -> function medium | 12-1 84% vs 0.4%; young nodules only |
| TAT 06G235500 | Uninfected_Cell | medium -> high | 21-dpi UC cl11 65% vs 6%; cortex caution kept |
| PHO1-H5 10G183300 | Stele | medium -> high | cl9 95% vs 13% |
| SWEET14 06G125800 | Stele | medium -> high | cl9 28% vs 1% |
| PILS3 01G156200 | Cortex | low -> medium | outer cortex cl4 45% vs 15% |

Agreement noted without a raise: NOD26, PHO1-H1, HPAT (already high), INR2 (Liu 66-78% vs 21-26%, weak), the three
endodermis genes (Liu cluster 8 is unlabeled), UPS 02G116300 (conflict below).

After the update: 78 rows (77 genes; TPS still in two rows). Evidence: 20 `function`, 42 `characterized_enriched`,
16 `expression`. Confidence: 21 high, 39 medium, 18 low. By type: Infected_Cell 22, Stele 11, Cortex 9,
Uninfected_Cell 9, Infection_Thread_Cell 8, Sclerenchyma 6, Endodermis 4, Nodule_Parenchyma 4, Phloem 3,
Epidermis 1, Pericycle 1. `expected_cell_types.tsv` gained an `Infection_Thread_Cell` state row and recounted
`function_markers` (Infected_Cell 10, Infection_Thread_Cell 7, Uninfected_Cell 2, Stele 1).

### Gaps closed

- **Nodule_Parenchyma**: now has 4 rows from a resolved inner-cortex cluster (ENOD2 and CA1 medium). Still no
  `function` marker.
- **Epidermis**: first row (16G161100, ISH, low), but the Liu cluster is mixed with root epidermis.
- **Infection state** (young nodules): 8 rows, 7 `function`.
- **Stele**: a second high-confidence reporter-validated marker (WAT1-related 10G044800).

### Gaps remaining

- Uninfected_Cell: no clean `function` marker (both uricases are broad in nuclei).
- Nodule_Parenchyma, Cortex, Epidermis: no `function` marker; Cortex rows are spatial-only.
- Pericycle, Phloem, Xylem: only label-transferred, root-dominated rows (low); use arabidopsis_root by homology.
- Sclerenchyma vs Xylem: unchanged. Endodermis: no soybean `function` marker (characterized survey has only Lotus
  FAR3.1 and GmUPS1, which also marks cortex).
- Senescing and Dividing_cells: unchanged (the characterized survey's GmNAC039/GmNAC018 have no localization; not added).

### Conflicts

- **UPS Glyma.02G116300**: the characterized-marker survey maps this ID (NCBI LOC100801814, XP_003518768) to GmUPS1-2,
  which Collier and Tegeder 2012 *Plant J* localized to nodule **cortex and vascular endodermis**; both atlases (Liu
  cl0 70% vs 20%, Cervantes J/K) put it in uninfected cells. The row stays Uninfected_Cell medium (not raised) with the
  conflict in `basis`. This corrects the earlier note above that the GmUPS1 function belongs to other paralogs.
- **ENOD55**: Liu Supp. Data 5 lists GLYMA_13G024700, which UniProt names a pyruvate carboxyltransferase. The
  authors' notebook uses 02G204500 (phytocyanin), which is the row kept.
- **ENOD2**: Liu's 20G203800 (NCBI "early nodulin-75", LOC100791125) is not the characterized survey's GmENOD2B
  (Glyma.08G131925, Wm82.a4). The two are different loci; neither ID is independently localized.
- **Uricase paralogs**: the draft's U032500 (Cervantes J/K) and Liu's UR2 20G072400 (broad in Liu, <=5% in
  Cervantes) disagree; compare by ID and treat both as weak.
- Liu stage and batch are confounded (one library per stage), and its UC/cortex labels come from bin-level
  Stereo-seq deconvolution, not single-cell spatial data.

### Recommended label reference (revised)

- **Mature nodules (3-4 weeks):** still **Cervantes-Perez 2024** (cell-resolution Molecular Cartography, small
  per-nucleus label table).
- **Young/maturing nodules (12-21 dpi):** **Liu 2023** is now the better reference for infected-cell infection
  states, Nodule_Parenchyma (inner cortex) and nodule vascular bundle (cluster 9), with Zhang 2025 as a cross-check.
  Remove root nuclei first (clusters 3 and 5 are root-dominated), and do not reuse Liu's Unknown clusters or
  label-transferred stele subclusters. Per-nucleus labels need the large OMIX002290 object (not downloaded).

### Could not verify (this update)

- Liu main text and Methods are paywalled (not bypassed); the GUS/ISH claims are from figures and legends.
- The paralog identity of ENOD2 20G203800 and the UPS 02G116300 naming (UPS1-2 vs UPS2-2) were not resolved
  beyond NCBI/UniProt names.
