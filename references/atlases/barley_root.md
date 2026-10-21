<!-- Collated from the survey review of barley_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Barley root single-cell datasets: collated marker resources (group `barley_root`)

Date: 2026-10-20. New group, built from one gap-fill review. This is paper-only work (Part A, Steps 1-3a, plus a Step 4 marker table). There was no in-data check (Step 3b).

Files in this folder:
- `expected_cell_types.tsv`: written from barley root-tip anatomy before the labels were read (sources: Kirschner et al. 2017 *Front Plant Sci* 8:1240, doi:10.3389/fpls.2017.01240, PMC5519606, and the grass-root list in the skill). `function_markers` counts the `function` rows in `markers_draft.tsv`, which use barley MorexV3 IDs. The `notes` column gives the extra `function` rows available by homology from `arabidopsis_root.tsv` and `rice_root.tsv` after `grass,C3` trait filtering.
- `markers_draft.tsv`: 15 rows. The columns are the skill schema plus `alt_id` and `other_ids`.
  - `ref_gene` is MorexV3 (`HORVU.MOREX.r3.*`).
  - `alt_id` is the Morex V1 ID (`HORVU*Hr1G*`) where Demesa-Arevalo 2026 Supp Table 5 lists it. Otherwise it is the MorexV2 ID from UniProt, prefixed `MorexV2:`. A mixed alt_id column cannot be used directly with `--id-column alt_id`: strip the prefix and use only rows of one system.
  - `other_ids` holds UniProt accessions.
  - Every line has 14 fields (checked). This is a draft and has not been copied into the skill.
- `Dolata2026/`: the full review (README, evaluation.tsv, markers.tsv, full text, Fig 2 and Fig 3, atlas landing page). I did not change it.

## Datasets

| Dataset | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|
| Dolata A ... Stahl Y. 2026 bioRxiv, doi:10.64898/2026.06.15.732315 (v1, posted 2026-06-16; Europe PMC PPR1253367) | Protoplast scRNA-seq on BD Rhapsody WTA (microwell; cells over 60 um are lost). Golden Promise, 1-2 mm primary root tips, 6 DAG, 3 replicates. 1,308 protoplast-induced genes removed. Validated by HCR RNA-FISH and Molecular Cartography (MC). | about 5,000 cells, 24 clusters (32-494 cells each) | MorexV3 | `cluster_only`. There is no accession; the Seurat object and matrix links on the Shiny atlas are placeholders. | medium |

No other barley root single-cell atlas was in the survey. The skill's characterized table (`characterized/barley.tsv`) has three barley root genes: HvLsi1 (epidermis + cortex), HvLsi2 (endodermis) and HvEXPB1 (root hair). They are keyed by UniProt accession only, and UniProt cross-references them to barley pan-genome projections (e.g. Golden Promise) but not to MorexV3 IDs. None of them is in Dolata's marker list, so none can count as independent support. `survey/characterization/characterized_markers.tsv` has no rows with `barley_root:` in `gaps_filled`.

## Verdicts (Dolata 2026)

| Published label | Clusters | Verdict | Canonical name |
|---|---|---|---|
| QC/Niche | 2 | Revise | Quiescent_Center + Stem_Cell_Niche (split in Part B; barley QC is about 30 cells) |
| CSC | 21 | Revise (weak) | Columella (stem cells) |
| Metaxylem | 10 | Adopt | Metaxylem |
| Vasculature | 5 | Revise | Procambium / Stele (pericycle not resolved) |
| Xylem | 23 | Adopt | Xylem (proto/meta not stated) |
| Phloem | 19 | Adopt | Phloem (SE/CC not split) |
| Endodermis | 1, 20 | Adopt | Endodermis |
| Cortex | 3, 7, 9, 12, 13, 17 | Revise | Cortex (outer vs inner not labeled; cl7 is "vascular" in the text but Cortex in Fig 3) |
| Cortex/Epidermis | 4 | Revise | resolve in Part B |
| LRC/Epidermis | 0, 16 | Revise | Lateral_Root_Cap / Epidermis (cross-species transfer only) |
| Epidermis | 15 | Revise | Epidermis (cross-species transfer only) |
| Epidermis/Stele | 8 | Reject | - |
| Cell cycle, Cell cycle (Initials), Cell cycle (Epidermis) | 6, 11, 14, 18 | Reject as types | state: Dividing_cells / S_Phase |
| NA | 22 | Reject | Unknown (the authors left it unlabeled) |

About 40% of cells (the "unidentified" block in Fig 2H) got their labels only from cross-species transfer.

## Markers

| Cell type | MorexV3 | Gene | Evidence, confidence | Validation in barley |
|---|---|---|---|---|
| Quiescent_Center | 3HG0301330 | HvWOX5 | function, medium | MC (stronger in metaxylem than in QC); CRISPR mutant has a QC phenotype |
| Metaxylem | 3HG0301330 | HvWOX5 | function, medium (requires grass) | MC central metaxylem file; mutant metaxylem phenotype |
| Endodermis | 2HG0133890 | HvSCR (paper) / SCL23-like (UniProt) | function, medium | HCR |
| Cortex [outer] | 1HG0004290 | CI-2A-like protease inhibitor | characterized_enriched, medium | HCR outer cortex only |
| Cortex | 2HG0206040 | LTP-like | characterized_enriched, low | HCR (Suppl, not seen) |
| Cortex | 5HG0517260 | HvMND8 | characterized_enriched, low | MC (Suppl, not seen); ID from Demesa 2026 |
| Procambium | 5HG0508470 | HD-ZIP III | function, medium | MC central stele |
| Procambium | 7HG0666250 | TCP | characterized_enriched, medium | MC stele above QC |
| Procambium | 3HG0233930 | HvRA2/VRS4 | characterized_enriched, low | MC (Suppl, not seen); ID from Demesa 2026 |
| Procambium | 7HG0742750 | HvMND1 | expression, low | MC (Suppl, not seen); ID from Demesa 2026 |
| Stele | 2HG0130150 | HvSHR | function, medium | scRNA and pseudotime only |
| Xylem | 2HG0216570 | HvVND7 | function, medium | scRNA and pseudotime only |
| Xylem | 5HG0462580 | XCP-like | characterized_enriched, low | "expression" in Suppl Fig 2E (not seen) |
| Phloem | 7HG0738570 | HvAPL (paper) | function, low | scRNA and pseudotime only; paralog conflict |
| Columella | 7HG0662370 | Bet v I/MLP (UniProt) | expression, low (REVIEW) | HCR in CSC, metaxylem and phloem: not specific |

Where my grading departs from the review:
- **HvWOX5 QC row, high to medium.** The text says the MC signal is in metaxylem "and, to a lesser extent, in the QC". The cluster it marks (cl2) also holds niche cells.
- **XCP-like, medium to low.** The text only says xylem was assigned "based on expression of" this gene. Whether Suppl Fig 2E is MC or scRNA is not known.
- **HvAPL, medium to low.** Two MYB-CC paralogs are called HvAPL in two papers (see Conflicts).

No confidence was raised: there is only one barley root single-cell study, and no characterized barley root marker shares a gene ID with it.

## Gaps

- **No `function` marker in barley IDs:** Columella, Lateral_Root_Cap, Root_Cap, Stem_Cell_Niche, Epidermis, Trichoblast, Atrichoblast, Exodermis, Cortex, Pericycle, Stele_Parenchyma, Protoxylem, Sieve_Element, Phloem_Companion, Dividing_cells, S_Phase.
- **No barley marker at all:** Lateral_Root_Cap, Root_Cap, Stem_Cell_Niche (the JKD and BRAVO orthologs are named, but their IDs are only in the inaccessible Suppl), Epidermis, Trichoblast, Atrichoblast, Exodermis, Pericycle, Stele_Parenchyma, Protoxylem, Sieve_Element, Phloem_Companion and the cell-cycle states. The Histone H4 in situ probe of Kirschner 2017 (EST AK357536) has not been mapped to MorexV3.
- **Partly filled by this review:** Quiescent_Center, Metaxylem, Cortex (outer cortex) and Procambium.
- **Next steps:**
  - BLAST HvLsi1, HvLsi2 and HvEXPB1 (UniProt B9X078, C6KYS0, Q6V4S0) against MorexV3 to turn the characterized rows into usable IDs.
  - Read Dolata Suppl Tables 2-3 when the user can download them.

## Recommended label reference

Dolata 2026 is the only barley root atlas. Use its in situ-backed calls (Endodermis cl1/20, Metaxylem cl10, Xylem cl23, Phloem cl19, Vasculature cl5 as Procambium/Stele, Cortex clusters) as hypotheses keyed by cluster. Its labels are cluster-level only and the data are not public, so it cannot be a per-cell benchmark. For epidermis, root cap and pericycle, use homology from `rice_root.tsv` and the `wheat_root` draft instead of Dolata's cross-species labels.

## Conflicts

- **HvSCR.** Dolata's HvSCR (2HG0133890) is "Scarecrow-like protein 23" in UniProt (449 aa). It is a different gene from Demesa-Arevalo 2026's HvSCR2 (5HG0463700, "Protein SCARECROW", 585 aa). The endodermis pattern holds whichever name is right.
- **HvAPL.** Dolata uses 7HG0738570; Demesa-Arevalo 2026 uses its paralog 6HG0570890 (barley_shoot_apex draft). The barley shoot apex draft and this draft therefore key HvAPL to different genes.
- **HvWOX5 / HvWOX9.** Demesa-Arevalo 2026 calls 3HG0301330 "HvWOX9". It is the same gene.
- **CSC marker.** 7HG0662370 is a 160 aa Bet v I/MLP protein in UniProt, not the "LRR-XI kinase" the paper describes.
- **HvMND1.** Dolata calls it vascular in the root. In the barley shoot apex and spike it marks ground/pith tissue (barley_shoot_apex draft).
- **Cluster 7.** It is listed among the vascular clusters in the text but labeled Cortex in Fig 3.
- **Kirschner 2017 in situ.** Dolata says its HvSCR and HvSHR patterns are "consistent with" Kirschner 2017 in situ data. The Kirschner et al. 2017 *Front Plant Sci* full text (PMC5519606) has only a Histone H4 in situ, so I could not confirm this. Dolata may mean another paper.

## Could not verify

- Dolata supplementary material (Suppl Tables 1-3, Suppl Figs 1-4). bioRxiv returned Cloudflare 1015 (rate limit), and I did not try to get around it. The user can download these from https://www.biorxiv.org/content/10.64898/2026.06.15.732315v1.supplementary-material.
- Raw data and the Seurat object: not released.
- IDs for HvMND8, HvRA2 and HvMND1 come from Demesa-Arevalo 2026 tables (same MC probeset), not from Dolata. Their images were not seen.
- UniProt entries were re-queried on 2026-10-20 for 3HG0301330, 2HG0133890, 7HG0662370 and 5HG0462580, and agreed with the review.
