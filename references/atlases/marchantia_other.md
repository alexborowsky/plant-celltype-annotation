<!-- Collated from the survey review of marchantia_other (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Marchantia polymorpha (gemma and vegetative thallus): marker resources

Group collation, 2026-10-20, for the plant-celltype-annotation skill. Inputs are
the two dataset reviews in `Wang2023/` and `Romani2024/` (each has its own
README; both are left as they were). Nothing was re-analysed. Every marker ID in
`markers_draft.tsv` was re-checked against the primary table (Wang 2023 Table S1
`Wang2023/mmc2.xlsx`, sheets "Cluster-enriched genes", "Details of the GFP
reporters", "Primers", "Protoplast-induced genes", or Romani 2024 DS1
`Romani2024/DS1_promoter_list.tsv`), and against UniProt (taxon 3197) where the
gene has an entry.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 19 cell types and states expected in gemmae and the vegetative thallus, from anatomy, with `function`-marker counts from `markers_draft.tsv` |
| `markers_draft.tsv` | 57 rows, skill schema plus `alt_id` (MpTak v3.1 `MARPO_` ORF name from UniProt; empty when there's no UniProt entry or the gene has several copies). `ref_gene` = MpTak v5.1 (`Mp3g07510`), the same IDs as Ensembl Plants MpTak1 v7.1 |

## Datasets

| Dataset | Platform | Cells | Label access | Quality |
|---|---|---|---|---|
| Wang L et al. 2023 *Dev Cell* 58:1429. doi:10.1016/j.devcel.2023.05.014. PRJCA013186 / CRA009114 / OMIX004749 | Protoplast scRNA-seq, 10x 3' v3; Tak-1 male; gemma D0 and thallus D1-D31; one library per time point; 1,190 protoplast-induced genes removed before clustering | 46,136 (21 Louvain clusters; 9 left "Undefined") | `large_object`: only in the 5.51 GB Seurat rds (OMIX004749-01; matrix-only rds 434 MB). Not downloaded; whether named labels are in meta.data is unconfirmed. Cluster-to-type map in Fig. 1A legend | medium |
| Romani F et al. 2024 *Plant Cell* 36:2140. doi:10.1093/plcell/koae053. PMC11132968. Images: mpexpatdb.org | Promoter:mVenus-N7 reporters for ~367 TF genes in gemmae and gemmalings (6-7 lines each); one in situ (MpERF20). No sequencing | none (0/1/2 domain scores for 366 promoters in DS1) | `none` | high (as a marker reference) |

## Verdicts per cell type across datasets

Adopt / Revise / Reject as in the reviews; `-` = not covered. Canonical names
follow the skill's Title_Case_With_Underscores style.

| Cell type | Wang 2023 (scRNA) | Romani 2024 (reporters) | Overall |
|---|---|---|---|
| Oil_Body_Cell | Adopt (c18, ~1%) | Adopt | **Best-supported type.** Three `function` markers agree across studies |
| Air_Pore_Cell | Adopt (c17) | Adopt (thallus, Fig 8A) | Supported. NFYC4 agrees across studies, but only as enrichment in c17 |
| Mucilage_Papilla | Adopt (c21, "mucilage hairs") | Adopt ("mucilage papillae") | Supported. The two studies' markers don't overlap by ID |
| Rhizoid | Revise (c15, mixed with mucilage-hair reporter genes) | Adopt (precursors; proximal/distal split = Revise) | Needs checking in the data |
| Ventral_Scale | Revise (c6; scale reporter genes are protoplast-induced, implausible size) | - | Weak |
| Assimilatory_Filament | Revise (c19, one LHCB reporter) | - | Weak |
| Notch_Meristem | Revise (c11 = proliferation) | Revise (SCZ subapical) | Treat c11 as Dividing_cells; notch identity markers are low |
| Apical_Cell | - | Adopt as a marker only (ERF20) | No scRNA cluster is expected |
| Dividing_cells / S_Phase | (c11) | DDCZ = Revise (dividing/stress state) | State |
| Gemma_Margin | - | Revise (border) | Hypothesis |
| Attachment_Cell | - | Revise | Shared papilla/initial program |
| Gemma_Cup | not resolved | Revise (thallus) | Weak |
| Dorsal_Epidermis | not resolved | - | Gap |
| Storage_Parenchyma, Ventral_Epidermis, Mucilage_Cell, Gemma_Initial | not resolved | (CZ/TZ/PZ = Reject) | Gap |
| Time-point clusters (c2, c5 "mature cells"; c3, c8 "gemma cells"; c4 "differentiating") | Reject | - | Batch/stage states |

## Cross-study markers (same v5.1 ID in both studies)

| Gene | Symbol | Cell type | Wang 2023 | Romani 2024 | Confidence |
|---|---|---|---|---|---|
| Mp3g07510 | MpMYB02 | Oil_Body_Cell | reporter LW881 + c18 DE 0.365 vs 0.001 + mutant | oil-body-only reporter | high (function) |
| Mp6g08690 | MpERF13 | Oil_Body_Cell | c18 feature plot (Fig S2H), not in DE table | oil-body-only reporter | high (function) |
| Mp3g02320 | MpC1HDZ | Oil_Body_Cell | c18 DE 0.67 vs 0.14 (also c17) | oil bodies = 2, all other domains = 1 | medium → high |
| Mp7g06550 | MpWRKY10 | Oil_Body_Cell | c18 DE 0.64 vs 0.13 | oil bodies = 2, rhizoid = 2 | low → medium |
| Mp1g01960 | MpNFYC4 | Air_Pore_Cell | c17 DE 0.68 vs 0.28 (enriched, not specific) | thallus air-pore reporter | low → medium |

Only these five qualify. There are only two studies, and they cover different
stages (Romani mostly gemmae; Wang mostly thalli), so most types rest on one study.

## Gaps (no `function` marker)

Notch_Meristem, Mucilage_Papilla, Rhizoid, Ventral_Scale, Assimilatory_Filament,
Dorsal_Epidermis, Ventral_Epidermis, Storage_Parenchyma, Mucilage_Cell,
Gemma_Initial, Gemma_Margin and Attachment_Cell. Of these, Mucilage_Papilla and
Rhizoid have several medium reporter-validated markers. Storage_Parenchyma,
Ventral_Epidermis, Mucilage_Cell and Gemma_Initial have no marker at all. Possible
`function` candidates that weren't verified here: MpRSL1 (Mp3g17930, rhizoid
development, Proust 2016) and MpFRH1/MpLRL genes for rhizoids; KAR (Mp5g06550,
gemma initials, broad in Wang). MpRSL1 was left out because its Romani gemma
reporter scores SCZ/DDCZ/oil body, not rhizoid.

## Recommended label reference

**Wang 2023** is the only dataset with cells. Use its clusters 18 (oil body), 17
(air pore) and 21 (mucilage papilla) as adoptable labels, and c11 as
Dividing_cells. Re-check c15/c6/c19 in the data. Getting per-cell labels needs
the 5.51 GB OMIX rds read in a job (`obj@meta.data`). The labels are probably
only cluster numbers, mapped with the Fig. 1A legend. **Romani 2024** is the
reference for validating markers (DS1 plus mpexpatdb images), not for labels.
Time point and batch are confounded in Wang (one library per day). Expect
per-sample clusters, and don't adopt c1-c5, c7-c9.

## Conflicts and corrections to the reviews

- **Mp6g16280 (ventral scale):** the Wang text calls it cluster-6-specific, but
  Table S1 DE and reporter LRY340 put it in oil-body cluster 18 (0.391 vs 0.062).
  Kept as Ventral_Scale `low` with the conflict in `basis`.
- **Ventral-scale dirigents Mp3g07430, Mp3g24180:** both are on the
  protoplast-induced list, so they could not have defined cluster 6 (review
  addendum, confirmed).
- **MpERF20/LAXR (apical cell) and GCAM1 (gemma cup)** are also on the Wang
  protoplast-induced list (new finding). ERF20 was lowered from the Romani
  review's `high` to `medium`: it's wound/ablation-induced and detected in 0
  gemma cells.
- **MpAP2L2 (Mp7g13270):** Romani scores it in rhizoid precursors (plus
  SCZ/DDCZ/mucilage), but in Wang it is a specific air-pore c17 DE gene (0.521
  vs 0.011). Kept as Rhizoid `low`, with the conflict noted.
- **MpC4HDZ / MpSBG9 as dorsal-epidermis markers** (Wang's claim, citing a
  phylogeny paper and a MIXTA/cuticle paper): neither study supports them. The
  Wang reporter for C4HDZ gave no signal, and the Romani gemma reporters score
  border/oil body/mucilage (C4HDZ) and SCZ/DDCZ/mucilage (SBG9). Kept `low`.
- **MpBZIP15** was lowered from the Romani review's `medium` to `low`: it's broad
  in Wang (c17 0.911 vs 0.543), and Romani shows it shifting to differentiated
  cells.
- **MpCDC5 (Mp1g10310)** is left out. The Romani review called it a G2/M
  regulator, but Arabidopsis CDC5 is a MAC spliceosome component, so it is
  neither a clean proliferation marker nor an identity marker.
- **Mp5g06510 (air pore)** has no row on the Wang reporter sheet. Its construct
  (LW903, cluster 17) is on the Primers sheet, and the image is Fig. 2A.
- **Protoplast-induced list:** the sheet has 1,251 rows but 1,190 unique genes.
  The Wang review addendum's "1,251" counts duplicate rows.
- Text-versus-table slips in Wang (from the review, confirmed): the cluster-4
  marker is Mp7g05980 (not Mp7g04610). "MpSPY12B" is MpSYP12B. Mp3g11120's
  reporter is listed as "cluster 22".
- **Naming:** Wang "mucilage hairs" and Romani "mucilage papillae" are the same
  slime papillae, merged as `Mucilage_Papilla`. Romani "rhizoid precursors" are
  merged into `Rhizoid`. Mp6g21470 is MpBHLH28 in Romani and "RSL2" in UniProt;
  same gene.

## Table conventions (differences from the skill tables)

- `tissue = thallus` (covers gemmae and thallus); the skill README lists only
  `leaf`/`root`/`any`.
- New trait tag `requires = liverwort` on every identity row. Oil body cells, air
  pores, gemma cups, scales and mucilage papillae are liverwort-specific, and
  most markers are uncharacterized Marchantia genes. Angiosperm targets should
  not receive them by homology. The tag would need adding to `IMPLIES` /
  `--target-traits` in `map_markers.py` (no implications needed). The state rows
  (Dividing_cells, S_Phase) carry no tag.
- New cell-type names: Oil_Body_Cell, Air_Pore_Cell, Mucilage_Papilla, Rhizoid,
  Ventral_Scale, Assimilatory_Filament, Apical_Cell, Notch_Meristem,
  Dorsal_Epidermis, Gemma_Cup, Gemma_Margin, Attachment_Cell. States reuse
  `Dividing_cells` and `S_Phase`.

## Overlap with existing skill tables

None. No table in `references/markers/` covers Marchantia or any bryophyte. The
only shared names are the states `Dividing_cells` and `S_Phase`
(arabidopsis_leaf, rice_root), and `Epidermis` vs `Dorsal_Epidermis`.

## Could not verify

- The Wang OMIX rds (5.51 GB / 434 MB): not downloaded, so the label columns are
  unconfirmed. GSA CRA009114 has a JS bot check, and the Wang web server returns
  404.
- The functional papers were not re-read: Kubo 2018 (MYB02), Kanazawa 2016
  (SYP12B) and 2020 (ERF13), Romani 2020 (C1HDZ), Ishida 2022 (ERF20), Yasui
  2019 (GCAM1), Kato 2020 (ARF2). Their claims are as cited by the two papers
  (marked "as cited" in `basis`). If Kanazawa 2016 shows an oil-body-cell
  reporter, MpSYP12B would rise to `high`.
- IDs absent from UniProt, taken from the primary table only: Mp5g18410 (Wang
  S1), Mp3g04360, Mp7g13270, Mp2g08790 and Mp6g02590 (Romani DS1). Mp2g25500
  (CYCA1;1) and Mp5g19170 (CDKB1;2) are named only in the Wang text; UniProt
  lists them as uncharacterized / Ser-Thr kinase.
- The mpexpatdb.org images were not viewed. DS1 scores are hand-assigned and
  coarse.
- Histone rows (Mp5g22460, Mp7g10730) have no `alt_id`, because UniProt maps
  each to several v3.1 copies.
