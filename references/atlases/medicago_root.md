<!-- Collated from the survey review of medicago_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Medicago truncatula root: cell-type marker resources (group review)

Collated 2026-10-20 for the plant-celltype-annotation skill. Inputs: the one review for this group in
`survey/merged_reviews.json` (Cervantes-Pérez 2022) and its folder `CervantesPerez2022/` (its README is
unchanged). I re-checked every gene ID used here (see "ID checks"). Nothing in the skill was edited.

## Files

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Cell types expected from root anatomy (tip to root-hair zone), with marker counts from `markers_draft.tsv` |
| `markers_draft.tsv` | 47 rows in the skill schema plus `alt_id`. `ref_gene` = MtrunA17r5.0 ann1_6 IDs, `alt_id` = Mt4.0 `Medtr` IDs (NCBI/UniProt spell these `MTR_`) |
| `id_check/` | ann1_6 and Mt4.0 proteomes from LIS, UniProt query sequences, DIAMOND hit tables (`hits.tsv`, `at_hits.tsv`, `sel_mt4.tsv`), PMC full texts used for IDs, and `build_markers_draft.py`, which writes the table |
| `CervantesPerez2022/` | Dataset review (unchanged) |

## Datasets

| Dataset | Platform | Cells | Label access | Quality | Status |
|---|---|---|---|---|---|
| Cervantes-Pérez et al. 2022 *Mol Plant* 15:1868, doi:10.1016/j.molp.2022.10.021; GEO GSE210881 | Nuclei (FACS), 10x 3' v3.1; A17, 6 d, root tip to root-hair zone, mock and *E. meliloti* 48 h | 28,375 nuclei, 25 clusters, 3+3 libraries | large_object: per-cell labels only in the 832 MB RDS (GEO) and ShinyCell; cluster→type only in Fig. 2A (transcribed to `CervantesPerez2022/cluster_to_celltype.tsv`) | medium | reviewed |
| Pereira et al. 2024 *Cell Rep* 43:113747, doi:10.1016/j.celrep.2024.113747 | scRNA-seq of nodule development in roots (Mt) | ? | ? | ? | **not reviewed** (found in Europe PMC; no PMC full text) |
| Serrano et al. 2024 *Nat Plants*, doi:10.1038/s41477-024-01666-3 (PMC11035146) | Spatial co-transcriptomics, AM-colonized roots | – | – | ? | not reviewed; possible source of spatial validation |
| Jhu et al. 2025 bioRxiv 10.1101/2025.07.22.663073 (Xenium, roots and nodules); Venado et al. 2026 bioRxiv 10.64898/2026.09.29.755433 | spatial / single-cell | – | – | ? | not reviewed |

Only one single-cell dataset was reviewed. So there is no atlas-to-atlas cross-study agreement for this group.
The "cross-study" evidence below is agreement between a published Medicago reporter study and the
Cervantes-Pérez (CP) cluster profile. Reviewing Pereira 2024 is the obvious next step.

## Per-cell-type verdicts (CP 2022 is the only dataset)

| Cell type (canonical) | CP clusters | Verdict | Best marker evidence |
|---|---|---|---|
| Trichoblast (root hair) | 3 (plus part of 1, 2) | Adopt (cl3) | MtRbohF (Marino 2011 GUS), MtEXP7 75x, Prx100 57x, RSL4-like |
| Atrichoblast | 1, 2 (unsplit) | Revise | none; GL2 ortholog peaks in cortex cl7 |
| Root_Cap | 4, 5 (labelled epidermis) | Revise → Root_Cap | BFN1-like 9-13x in cl4; SMB-like and a PME in cl5 |
| Quiescent_Center | – (in cl9) | Missing | MtWOX5 barely detected |
| Stem_Cell_Niche | 9 (labelled stem cell niche) | Revise → Dividing_cells | cl9 is G2/M (CycB1-1 20x); PLT1-4 peak there |
| Cortex | 6, 7, 10-14 | Adopt 7 (lineage); 14 Revise (library skew); 6, 10-13 Revise (correlation only) | MtIFS1 (cortex promoter) only in inoculated cl14 |
| Endodermis | 15-19 | Adopt 17, 19; Revise 15, 16; Reject 18 | CASP-likes 40-230x and MtSCR, MYB36-like top in cl19; cl17 has SCR 1.4x but no CASP signal (younger endodermis or not endodermis) |
| Pericycle | 20 | Adopt | MtPHO1.1/1.3 6-9x, SWEET 5-6x |
| Stele / procambium | 21, 23 | Revise | SMXL5-like in cl21; T5L1b in cl23 |
| Xylem | 22-24 | Adopt 24 (differentiating xylem) | IRX3/CESA8-like 24x, VND7-like |
| Phloem | 25 | Adopt (CC/phloem parenchyma; nuclei, so no sieve elements) | MtSUNN 33-209x, SUT1-1 17x, NaKR1-like, metacaspase |
| Lateral root primordium | – | Missing | LBD16 not enriched |

## Cross-study markers (reporter study + CP cluster, same lineage)

No row was raised one confidence level. These are the candidates and why each one stayed at its level:

| Gene | Reporter study | CP | Why not raised |
|---|---|---|---|
| MtRbohF MtrunA17Chr7g0238371 | Marino 2011 New Phytol: GUS in developing root hairs | cl3 4.2x | Marino's ID is Mt3.5 Medtr7g067680. In Mt4.0 that ID is now an F-box gene, so the link rests only on CP Table S2. The ann1_6 gene is the Rboh Medtr7g060540 |
| MtIFS1 MtrunA17Chr4g0046351 | Biala 2017 J Exp Bot: promoter mainly in cortex | cl14 6.4x in inoculated nuclei only (not in mock); cl14 is 54% one library | condition-dependent and library-skewed |
| MtPHO1.1 / MtPHO1.3 | Nguyen 2021 Plant Physiol: GUS in root vascular cylinder | cl20 pericycle 5-9x | reporter not resolved to pericycle |
| MtSUNN | Schnabel 2012 Plant Signal Behav: GUS confined to vascular tissue | cl25 phloem 33-209x | reporter not resolved to phloem |
| MtABCG20, MtRDN1 | Pawela 2019; Schnabel 2011: vascular reporters | cl25 3.8x; cl24 2.7x | weak enrichment |

The most reliable rows for Medicago are ordered by data support rather than by tier. MtSUNN, the CASP-like trio, MtEXP7,
MtPrx100, IRX3/CESA8-like, MtSUT1-1, MtPHO1.1 and the cyclins are both highly specific in CP and
biologically coherent.

## Gaps (no validated Medicago marker)

Atrichoblast; Columella (and LRC vs columella split); Quiescent_Center (WOX5 not detected); Cortex (no
specific constitutive marker; IFS1 is inducible); Procambium; protoxylem vs metaxylem; companion cell vs
phloem parenchyma; lateral root primordium. Cell types with no `function` row: all except Stem_Cell_Niche,
QC, Endodermis (SCR), Stele (SHR) and Dividing_cells.

## Recommended label reference

Use CP 2022 at **lineage level only**, with these clusters: 3 (Trichoblast), 4+5 (Root_Cap, our revision), 7 (Cortex),
9 (Dividing_cells), 17 and 19 (Endodermis), 20 (Pericycle), 24 (Xylem), 25 (Phloem). Do not reuse 6, 8,
10-13, 15, 16, 18, 21-23 as types. The per-cell labels need the 832 MB RDS (export `meta.data` in a job), and the
clusters were built on annotation v1.8. For per-cell benchmarking, Pereira 2024 should be reviewed first.

## Conflicts and corrections to the dataset review

- **Dong et al. 2021 is *Nature* 589:586** (doi:10.1038/s41586-020-3016-z), not *Science*.
- **SUNN reporter is vascular, not phloem.** Schnabel 2012 reports SUNN promoter-GUS "confined to the
  vascular tissue". The phloem call comes from CP cl25 alone.
- **MtIFS1 is not "nearly specific to cl14" in mock** (top is cl24 0.34 vs cl14 0.24). It is specific only in
  inoculated nuclei (6.4x).
- **MtPT1 is not cluster-specific** (1.0-1.1x). Paralogs 97-99% identical sit beside it (Chr1g0167731/0167761),
  so expect multimapping. UniProt "PT1" for *M. truncatula* also returns an unrelated leaf gene (PINNATE PENTAFOLIATA).
- **"Cluster 17 = endodermis" is weak.** The CASP-like genes are 40-230x in cl19 and ~0 in cl17. SCR is only 1.4x in cl17.
- **MtSMB is not a clean root-cap marker.** It is only 1.3x over xylem cl24 in mock, and it shares a PANTHER subfamily with VND4.
- **Symbol conflicts.** CP's "MtSWEET12" (Chr8g0386011) is not the best hit of AtSWEET12. CP's "MtVND4" is
  only the third hit of AtVND4. CP's "LjIPN2-like" (Chr8g0356501) is the best hit of AtAPL. CP's MtMYB070 is the
  MYB36 ortholog. LIS describes both SHR genes as "PAT1-like", but Chr5g0401131 is the reciprocal best hit of AtSHR.
- **Root-cap vs atrichoblast.** The cl5 gene Chr4g0011771 is the ortholog of the Arabidopsis atrichoblast
  marker AT2G45220. CP Table S4 lists several genes as "Root cap/Atrichoblast".
- **ID format errors in CP Table S2.** PHO1.3 is written `\tMtrunA17_Chr8g0368741` (a tab and an underscore). SUNN's v1.8 ID
  `MtrunA17Chr4g0035464` is absent from ann1_6 (`MtrunA17Chr4g0035451`). MtSHR2's ann1_6 model is
  truncated (244 aa vs 504 aa for Medtr4g097080).
- **The review cites validation it did not re-read.** WOX5's Medicago reporter (Osipova 2011) is about the nodule meristem
  (abstract only), so the row is `low`.

## ID checks

- **Literature IDs.** Taken from the primary papers (Franssen 2017 table for PLT1-4; Nguyen 2021 for PHO1.1-1.3;
  Pawela 2019 for ABCG20; Schnabel 2011 for RDN1; UniProt for SUNN G7JIK2, RDN1 E9KID2, IFS1 Q49BZ0, MtPT1
  O22301). I fetched the UniProt sequences and matched them with DIAMOND to the ann1_6 proteome. Every one hit the
  CP v1.8 ID at 99-100% identity, except SUNN (ann1_6 ID differs; see above).
- **SCR, SHR, WOX5 and other Arabidopsis-named genes.** Checked by DIAMOND best hit of the reviewed Arabidopsis protein against ann1_6
  (`id_check/at_hits.tsv`) and by CP Table S3 synteny orthologs.
- **alt_id.** Mt4.0 `Medtr` by DIAMOND of the ann1_6 protein against the Mt4.0 primary proteome (≥96.8% identity,
  full length). Left empty for LAT52/POE-6 and APL-like (best Mt4.0 hit only 63-75%).
- **Not verifiable by sequence.** MtRbohF (Marino's Mt3.5 ID) and MtWOX5 (Osipova's gene ID).

## Overlap with existing skill tables

There is no Medicago table in `references/markers/`. Through Arabidopsis homology, `arabidopsis_root.tsv` rows
map onto these Medicago genes: SCR, SHR, WOX5, PLT1, SMB, EXPA7, COBL9, CASP1/2/4, MYB36, APL. Their behaviour
in CP: EXPA7/COBL9 orthologs → cl3 (good); CASPs/MYB36 → cl19 (good); SMB → cl5 but also xylem; APL → cl25 (weak);
WOX5 → undetected; PLT1 → G2/M cl9; GL2 (eudicot-only atrichoblast row) → cortex cl7. That last one is a reason not to use the
`requires=eudicot` GL2/WRKY44 rows for Medicago. If this table is added to the skill, it would be
`references/markers/medicago_root.tsv` (`ref_gene` = MtrunA17 ann1_6; use `--id-column alt_id` for Mt4.0 data).

## Could not access or verify

- ScienceDirect/cell.com pages (403 bot check; not bypassed). Pereira 2024 Cell Rep has no PMC copy, so it was not reviewed.
- Dong 2021 *Nature* full text (not open). SCR/SHR expression is cited from CP Table S2.
- Chiou 2001 (MtPT1) and Marino 2011 figures were not re-examined. Osipova 2011 was read as abstract only.
- The 832 MB CP RDS was not downloaded. All specificity ratios are from CP Table S9 per-cluster averages
  (top cluster / second cluster, mock and inoculated), not per-cell statistics.
- The epidermal patterning claim (Medicago hairs not position-patterned) and the cortex layer count come from the review,
  not re-checked.
