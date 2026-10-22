<!-- Collated from the survey review of physcomitrium_other (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Physcomitrium patens (protonema and gametophore): marker resources

Group collation, 2026-10-20, for the plant-celltype-annotation skill. This is a new
group. The only input is the dataset review in `Chen2024/` (it has its own README
and is left as it was). Nothing was re-analysed.

All 37 marker IDs in `markers_draft.tsv` were re-checked here against the raw
supplementary tables: Table S4 (`Chen2024/supp/...-mmc5.xlsx`, log2FC/pct per
cluster) and Table S5 (`...-mmc6.xlsx`, symbols and v1.6 aliases). The 9 reporter
genes were also re-checked in UniProt (EnsemblPlants xref = the same v3.3 locus).
The DOI was confirmed in Europe PMC (PMID 39046878). The characterization survey
table (`survey/characterization/characterized_markers.tsv`) has no
`physcomitrium_other:` rows and no P. patens genes, so it adds no independent
support.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 15 cell types and states expected in protonema and vegetative gametophores, from anatomy, with `function`-marker counts from `markers_draft.tsv` (all 0) |
| `markers_draft.tsv` | 37 rows: skill schema plus `alt_id` and `other_ids`. `ref_gene` = Phytozome *P. patens* v3.3 locus (`Pp3c16_25600`). `alt_id` = v1.6 alias from Table S5 (`Pp1s4_308V6`), empty for the 9 reporter genes, which are not in S5. `other_ids` = NCBI LOC / PHYPADRAFT and UniProt accession, for reference only |

Conventions:
- `ref_species` = `physcomitrium`. `tissue` = `protonema` or `gametophore`.
- `requires` = `moss`. The tag is in the skill vocabulary (`moss` -> `bryophyte`);
  rows apply only when `moss` is passed in `--target-traits`.
- Gene IDs: data mapped to v3.3 should match `ref_gene` directly. For v1.6 data use
  `--id-column alt_id` (reporter genes will not match). Check whether the dataset uses
  the bare locus (`Pp3c16_25600`) or the transcript (`Pp3c16_25600V3.1`).

## Datasets

| Dataset | Platform | Cells | Label access | Quality |
|---|---|---|---|---|
| Chen Z et al. 2024 *Cell Rep* 43:114524. doi:10.1016/j.celrep.2024.114524. PMID 39046878. CNCB PRJCA020730 / GSA CRA013145 (fastq only) | Protoplast scRNA-seq (10x Chromium inferred from Table S2), 3 replicates; Gransden, 14-day protonema plus gametophores | 17,849 in 7 Seurat clusters | `cluster_only` (Tables S4/S5; no per-cell labels or processed object found) | medium |

## Verdicts per cell type

| Cluster | Paper label | n (%) | Verdict | Canonical name | Reason |
|---|---|---|---|---|---|
| 0 | Chloronemal cells | 6,263 (35.1%) | Adopt | Chloronema | JMJD5-homolog reporter in branched chloronema; specific DE; tissue-microarray cross-check |
| 1 | Chloronemal cells | 4,528 (25.4%) | Revise | Chloronema (merge or subcluster) | Most markers have pct.1 < pct.2 (CRPK1 reporter gene 0.33 vs 0.64); defined weakly or by absence; may be a state or quality bin |
| 2 | Gametophore cells | 3,148 (17.6%) | Revise | Gametophore_Leaf + Gametophore_Stress | EYA reporter; top GO heat/H2O2/ROS, DREB/DEAR/ASR1 markers: stress state of leaf cells |
| 3 | Gametophore cells | 2,953 (16.5%) | Revise | Gametophore_Leaf | OST1/SnRK2A reporter; tissue-level label (lamina, midrib, stem, apical cell not resolved) |
| 4 | Caulonemal cells | 470 (2.6%) | Adopt (medium) | Caulonema | KUP3 reporter (low coverage); cell-wall/phenylpropanoid markers |
| 5 | Tip cells | 422 (2.4%) | Revise | Protonemal_Apical_Cell (tentative) | Defined by photosynthesis genes; called from LCM bulk data; chloronemal vs caulonemal tip unclear |
| 6 | Bud cells | 65 (0.36%) | Adopt (medium) | Bud | Very specific markers; PHT2;1 reporter in buds, absent from chloronema; no cell-cycle markers; small n |
| - | Rhizoids | 0 | Reject | Rhizoid | Rhizoid markers almost not detected in any cluster (Fig S11); lost in protoplast capture |

No cluster is a proliferation state (no cell-cycle GO, no histone/cyclin markers).

## Markers (37 rows)

| Cell type | Rows | Best markers |
|---|---|---|
| Chloronema | 8 | Pp3c2_7150 "JMJD5" (reporter, medium); OPR2, Sec14p, POQR, ERF1A-1 (expression, low); CRPK1 is a weak cluster-1 reporter gene (low, pct.1 < pct.2) |
| Caulonema | 4 | Pp3c22_12740 KUP3 (reporter, low); Pp3c18_17700 (log2FC 3.0), CSLA09 (also in bud), FAH |
| Protonemal_Apical_Cell | 6 | all low and tentative: PSBO2-1 (reporter), betaCA6, betaCA2 (fusions; betaCA2 also cluster 3), Pp3c3_25110 (pct 0.26 vs 0.008), SBPASE, AAS |
| Bud | 8 | Pp3c16_25600 PHT2;1 (reporter, medium); BGLC1 Pp3c26_8580 and PGP2 Pp3c1_34680 (expression, medium: pct.2 <= 0.01); WR3, XTH9-1, XT1-1, EXL5, GLR3.5 (low) |
| Gametophore_Leaf | 8 | EYA, OST1/SnRK2A (reporters, low: localization not seen, enriched not specific); SHS1, Pp3c14_11840, Pp3c16_23250 and others (low) |
| Gametophore_Stress (state) | 3 | ASR1, DEAR5-1, DREB26 (low) |

Grading notes:
- No row reaches `function`. The reporter genes are `characterized_enriched`: the
  reporter supports localization, but the gene's function does not define the cell type.
- Reporter rows are `medium` only where the localization was confirmed in text
  (JMJD5 in branched chloronema, PHT2;1 in buds). The main text and Fig 2 were blocked,
  so the other 7 reporter localizations are inferred, and those rows are `low`.
- No confidence was raised: there is only one study, and the characterization survey
  has no P. patens rows.
- Compare by ID: "JMJD5" is the paper's homology name for Pp3c2_7150, which UniProt
  calls a DM8 domain-containing protein.

## Gaps

No cell type has a `function` marker. With nothing at all: Side_Branch_Initial,
Gametophore_Apical_Cell, Leaf_Midrib, Stem, Hydroid, Leptoid, Axillary_Hair, Rhizoid,
Dividing_cells. Protonemal_Apical_Cell and Gametophore_Leaf have only low markers.
Candidates that were not checked here (IDs not verified, do not use until taken from
a primary table): RSL1/RSL2 and RHS genes for rhizoids; VNS (NAC) genes for hydroids
and stereids; APB, CLE/CLV1, DEK1 and NOG1 for buds and the gametophore apical cell;
cell-cycle genes (CYCB, CDKB, histone H4) for Dividing_cells. Hata et al. 2025
*Dev Cell* (gametophore apical stem cell snRNA-seq) was named in the Chen review but
not reviewed.

## Recommended label reference

**Chen 2024** is the only dataset. Its labels are cluster-level only, so they can be
used as hypotheses for re-clustering, not as a per-cell benchmark. Adopt clusters 0
(Chloronema), 4 (Caulonema) and 6 (Bud). Merge 1 into 0 or subcluster it, treat 2+3
as Gametophore_Leaf (with a Gametophore_Stress state in 2), and check cluster 5 with
tip-growth markers before naming it.

## Conflicts

- CSLA09 (Pp3c14_12270) is enriched in caulonema (cluster 4) and bud (cluster 6).
  It is listed under Caulonema only.
- betaCA2 (Pp3c1_19190) is enriched in clusters 5 and 3 (tip and gametophore). It is
  listed under Protonemal_Apical_Cell, with the overlap noted in `basis`.
- Cluster 1 markers (CRPK1, GINT1, RBOHF, HEXO2) overlap with bud cluster 6 and are
  lower in cluster 1 than elsewhere. Only CRPK1 is kept, as low.

## Could not verify

- Main text and Figs 1-6 (cell.com / ScienceDirect returned HTTP 403; no PMC copy).
  Needed: the Fig 2 reporter images and legends (GFP localization of CRPK1, EYA, OST1,
  KUP3, PSBO2-1, betaCA2/6), and the Methods (10x chemistry, clustering resolution).
- The JMJD5 and PHT2;1 localizations come from text snippets, not the figures.
- Per-cell labels: none public. Raw reads only (CNCB CRA013145, not downloaded).
