<!-- Collated from the survey review of rice_leaf (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Rice leaf: group collation (Part A, Steps 1-4)

Date: 2026-10-20. Desk collation of two dataset reviews (`Swift2024/`, `Jing2026/`); no in-data check (Step 3b).
New group: there was no `markers_draft.tsv` before this run.

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Expected types from C3 grass leaf anatomy (written from anatomy first); `function_markers` = `function` rows in this draft plus rice leaf rows of the skill's `characterized/rice.tsv` (OsLG1, GLR1) |
| `markers_draft.tsv` | 52 rows (52 genes), skill schema + `alt_id` + `other_ids`. `ref_gene` = MSU7 `LOC_Os`, `alt_id` = RAP-DB (same convention as `rice_root.tsv`), `other_ids` = ZH11 T2T IDs for Jing rows. Field counts validated (14 columns) |
| `Swift2024/`, `Jing2026/` | The dataset reviews (README, supplements, graded tables, label exports). Left as written |

## Datasets

| Dataset | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|
| Swift J et al. 2024 *Nature* 636:143, doi:10.1038/s41586-024-08204-3 (rice part; Kitaake) | 10x snRNA + sci-RNA-seq3 (190,569 nuclei, 0-48 h de-etiolation), 10x Multiome (22,154 nuclei), FACS-sorted ZjPCK::H2B-mTurquoise2 BS nuclei | 19 clusters, 11 named, 8 left unknown; per-label counts not obtained | MSU7 (Nipponbare) | `large_object`: GSE248919 `L1_rice_combined.RData.gz` (1.3 GB) + Script 09 cluster map | medium |
| Jing Y et al. 2026 *Cell*, doi:10.1016/j.cell.2026.09.023 (leaf portion; ZH11) | Stereo-seq cell-boundary bins (~116 genes/bin), 3 leaf blade sections; snRNA (DNBelab C4) 12 leaf samples | 6,842 bins: Mesophyll 3918, Vascular_cell 1740, Lower_epidermis 605, Upper_epidermis 579 | ZH11 T2T (mapped to MSU/RAP here) | `table` (spatial h5ads 2-13 MB, exported to TSV); snRNA labels only in 0.5 GB h5ads, unchecked | low |

Swift samples whole etiolated/de-etiolating shoots (coleoptile, sheaths, emerging leaves), not mature blade; Jing samples mature blade cross-sections. Neither study validates subtypes beyond the Swift BS reporter and one Jing in situ (OsGDCH, figure not seen).

## Verdicts per expected type

A = Adopt, R = Revise, X = Reject, - = not annotated.

| Expected type | Swift 2024 | Jing 2026 | Note |
|---|---|---|---|
| Mesophyll | R (cl0, cl5) | A (positional) | Swift cl0 driven by plastid-like chr10 loci, cl5 weak; Jing on position, markers not specific |
| Bundle_Sheath | A, medium (cl10) | - (inside Vascular_cell) | reporter-sorted nuclei; only 6% marker overlap with atlas cl10, shared with phloem |
| Mestome_Sheath | R (cl16, candidate) | - | coherent suberin/Casparian program, unvalidated |
| Xylem | R (cl12) | R (marker table, Lsi6 only) | Swift cl12 = developing TEs, may include SCW sclerenchyma |
| Phloem / Phloem_Companion | R (cl6, merged) | R (marker table) | SUT1 common to both |
| Vascular (merged) | - | R (Vascular_cell, 25% of bins) | includes BS, mestome sheath, bundle-cap sclerenchyma by inference |
| Sclerenchyma | - (unlabeled cl9 = BC1, CESA4/7/9) | - | Swift "fiber" cl4 rejected (cuticle genes) |
| Epidermis | A (cl3, cl14); X (cl4 "fiber" = epidermal subtype) | R (Upper/Lower_epidermis, merged) | pavement, bulliform, silica, stomata not split |
| Guard | R (cl15, unconfirmed) | R (marker table, DE + ALMT ortholog) | no canonical guard gene in either |
| Stomatal_Lineage / S_Phase | R (cl7 "epidermis" = S phase + SCR2) | - | proliferation state labelled as a type |
| Subsidiary, Bulliform, Silica, Trichome, Ligule, Procambium, Sieve_Element, Dividing_cells | - | - | not annotated |
| (unknown) | cl1, 2, 8, 9, 11, 13, 17, 18 left unknown (good) | forced assignment (no unknown class) | Swift code labels cl13 "fiber", Supp Table 1 leaves it unnamed |

## Markers

52 rows: 5 `function` (CESA4, CESA7, CESA9 Xylem; BC1 Sclerenchyma; OsSUT1 Phloem_Companion), 23 `characterized_enriched`, 24 `expression`. High: 1 (OsSUT1). Medium: 8 (CESA4/7/9, BC1, XCP2-like LOC_Os01g73980, OPT7, AAP11C, DX1). Two rows start `REVIEW:` (ZH11-to-MSU mapping unconfirmed: OsALMT2 Guard, OsASR2/6 Phloem).

### Cross-study markers (by gene ID)

| Type | Gene (MSU / RAP) | Support | Result |
|---|---|---|---|
| Phloem_Companion | OsSUT1 LOC_Os03g07480 / Os03g0170900 | Swift phloem cl6 only (6.2x); Jing Vascular_cell-restricted in cell-boundary Stereo-seq; characterized companion-cell sucrose loader (Scofield 2007 *J Exp Bot*, skill `characterized/rice.tsv`) | `function` high (Swift alone: characterized_enriched low) |
| Xylem | XCP2-like LOC_Os01g73980 / Os01g0971400 | Swift cl12 only; root xylem in situ (Liu 2021, Wang 2021; `rice_root.tsv`) | raised low -> medium |
| Xylem_Parenchyma | Lsi6 LOC_Os06g12310 / Os06g0228200 | Swift BS cluster 3.7x vs Jing literature xylem parenchyma (barely detected) | not raised: cell types disagree, no in-data validation |

Not raised: CESA4 (root xylem in situ, but in leaf it marks all secondary-wall clusters), OsLTP1 (shoot-apex epidermis in situ in the rice_inflorescence table, but leaf contrast 0.15 vs 0.12), RCN1/ABCG5 (root exodermis suberin function; leaf cell type differs).

The survey's `characterized_markers.tsv` has no rows with `rice_leaf:` in `gaps_filled`, so it gave no independent support beyond the skill's rice table rows used above.

## Gaps

No `function` marker: Mesophyll, Bundle_Sheath, Mestome_Sheath, Xylem_Parenchyma, Phloem (parenchyma), Sieve_Element, Procambium, Epidermis (pavement), Guard, Subsidiary, Bulliform, Silica, Stomatal_Lineage, Dividing_cells/S_Phase (use `rice_root.tsv` state rows).
Survey gaps for this group: Mesophyll filled only as a spatial anchor (Jing) and with low rows; Bundle_Sheath filled at medium/low (Swift reporter-sorted); Bulliform not filled; Sclerenchyma a candidate only (BC1 in unlabeled cl9).

## Recommended label reference

Swift 2024 atlas clusters for BS/M partitioning (cl10 BS, cl0 M) and the vascular/epidermal lineages, after relabelling cl4 as epidermis, cl7 as S-phase/stomatal lineage, and treating cl9 as sclerenchyma; requires the 1.3 GB RData in an R job. Jing 2026 Stereo-seq sections are a coarse positional benchmark only (Mesophyll vs Vascular vs adaxial/abaxial epidermis). Neither gives per-cell labels for mature-blade subtypes.

## Conflicts and corrections

- **Swift "fiber" cl4** carries cuticle genes (HTH5/ONI3, BDG, CYP86A7, GPAT3, CUT5), not secondary-wall genes; rows put ONI3/BDG under Epidermis. Swift code labels cl13 "fiber", Supp Table 1 does not.
- **Swift "epidermis" cl7** is an S-phase state (MCM6, histones, RPA1B, RNR, POLA1) with SCR2/ICE1; MCM6 is `kind=state`.
- **XCP2 symbol swap.** Swift "XCP2" = LOC_Os01g73980; Zhang 2021 "XCP2" = LOC_Os05g01810 (Os05g0108600). Rows keyed by ID.
- **Lsi6 cell type.** Swift puts it in BS (and phloem); Jing and the literature in xylem parenchyma. Kept as Xylem_Parenchyma, low.
- **OsGDCH.** Jing's portal says in situ-validated for mesophyll, but in the Stereo-seq bins it is as high in Upper_epidermis; graded characterized_enriched low, not Jing's `function` medium.
- **OsSUT1 cell type.** Jing calls it Phloem_Companion, Swift Phloem; the draft uses Phloem_Companion from the characterized companion-cell function, with the atlas evidence at merged-phloem level.
- **ID ambiguity (Jing).** OsASR6 portal symbol fits several Oryzabase ASR loci (ASR2 Os01g0963600, ASR4 Os01g0959200 and two chr4 loci); OsALMT ZH10G23490 mapped by position only (Oryzabase LOC_Os10g42180 = Os10g0572100 = OsALMT2). Both rows flagged `REVIEW:`.
- Not carried from Jing: "OsrbcL1" ZH06G22680 (chloroplast-like insert), RBCS ZH12G11550 (locus ambiguous), unnamed chr10 Lower_epidermis DEGs.

## Could not verify

- Swift per-label cell counts and per-cell labels (1.3 GB RData not downloaded); ED Fig. 2g / 3e images.
- Jing *Cell* full text, STAR Methods and supplements (paywalled, 403); the OsGDCH in situ image; snRNA leaf labels (0.5 GB h5ads).
- Hua et al. 2021 *Plant J* (doi:10.1111/tpj.15292; rice LCM BS vs M vs vein) is not open access in Europe PMC; its BS gene lists would be the best independent check of the Swift BS rows (same lab as Swift, so only partly independent). A bioRxiv version exists (10.1101/2021.04.16.440137).
- Literature claims recalled in the reviews and not checked here: ONI2/ONI3 epidermal localization, FTIP1 companion cells, SCR2 stomatal lineage, Lsi6 leaf localization (Yamaji 2015 *PNAS* is a node paper).
- DOIs checked in Europe PMC this run: Swift 2024, Jing 2026, Li 2003 *Plant Cell* (BC1), Tanaka 2003 *Plant Physiol* (CESA4/7/9), Wang 2021 *J Exp Bot* (SUT1 phloem loading), Yamaji 2015 *PNAS*.
