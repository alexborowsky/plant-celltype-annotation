<!-- Collated from the survey review of maize_endosperm (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Maize endosperm: collated cell-type marker resources

Date: 2026-10-20. This collates the one reviewed endosperm dataset (Yuan et al. 2024) into a draft marker table. Each marker was cross-checked against an independent maize kernel spatial dataset (Fu et al. 2023, reviewed under `../maize_seed/Fu2023/`), the sibling maize drafts (`maize_seed`, `maize_embryo`, `maize_leaf`) and the published in situ literature. Nothing was re-analysed. All statistics come from the papers' supplementary tables: Yuan Supp Data 4 (DE) and 27 (symbols), and Fu SD1 (compartment mean UMI index) and SD4.

Files in this folder:
- `expected_cell_types.tsv`: written from the anatomy of B73 endosperm at 6-8 DAP (plus the contaminants expected from hand dissection), not from the published labels. `function_markers` counts the `function` rows in `markers_draft.tsv`. The skill has no maize table, so the skill count is 0 for every endosperm type.
- `markers_draft.tsv`: 47 rows covering 10 types and 2 states, in the skill schema plus `alt_id`. `ref_gene` = **B73 v5** (`Zm00001eb`) and `alt_id` = **B73 v4** (`Zm00001d`, the IDs Yuan and Fu used), matching the other maize drafts. `tissue` = `endosperm`. Endosperm-type rows have `requires=grass`. Field counts were validated (13 fields on every line).
- `Yuan2024/`: the per-dataset review (README, supplementary files, ID crosswalk, UniProt checks). Its README was left unchanged.

## Datasets

| Dataset | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|
| Yuan Y, Huo Q, Zhang Z, ... Song R, Ma Z (2024) Decoding the gene regulatory network of endosperm differentiation in maize. *Nat Commun* 15:34. doi:10.1038/s41467-023-44369-7. GEO GSE201640 | Protoplast scRNA-seq, 10x 3' v3; B73 endosperm 6 DAP (1 library) + 7 DAP (3 libraries); Seurat + Harmony, cell-cycle regressed | 17,022 cells; 18 clusters, 12 assigned to 5 endosperm types | B73 v4 | `cluster_only`: no per-cell labels anywhere, and the GitHub code labels a different 22-cluster run | medium |
| *Cross-check only:* Fu Y, ... Wu Y, Wang W (2023) *Nat Commun* 14:7191. doi:10.1038/s41467-023-43006-7 | 10x Visium, 55 um spots; W64A kernels at 12, 18 and 24 DAP | 10,900 spots, 11 compartments | B73 v4 | `cluster_only` (graded in `maize_seed`) | medium (markers) |

Fu 2023 comes from a different lab, inbred line, platform and stage range (12-24 DAP vs 6-7 DAP), so it counts as independent. A row was counted as agreeing when the same v4 ID was in situ-validated or compartment-specific for the same type in both studies. The stage gap works in both directions. Early genes (SBT1, TPS11) are absent from Fu, and late genes (MN1, BETL4, LTP2, zeins, SWEET14a, ZCN11) are absent from Yuan's DE table.

## Per-cell-type verdicts

There is one endosperm dataset, so the matrix has one verdict column. The Fu column says whether Fu's compartment, taken at the region level, supports the same type.

| Expected type | Yuan 2024 cluster(s), n (%) | Yuan verdict | Fu 2023 compartment | Note |
|---|---|---|---|---|
| Aleurone | 0, 3, 4, 7: 6670 (39.2%) | Revise | AL (Adopt with caveat) | 39% is implausible for one layer. The cells probably include subaleurone, dividing peripheral cells and stress states (c7 shares DHN/EFCB1 with stress c13). AL9 is not specific in either dataset |
| Subaleurone | inside "AL" and undefined c6 | not resolved | VE (peripheral SE) | Treat as a position/state |
| Starchy_Endosperm | 1, 8: 2964 (17.4%) | Adopt | SE + VE (Revise) | c1 = outer/hypoxic (PDC1), c8 = basal (CNGT1, PDK1): positions within one type |
| Basal_Endosperm_Transfer_Layer | 2, 9: 3033 (17.8%) | Adopt | BETL (Adopt) | Best-supported type in both. c2 = outer transfer cells, c9 = inner layers (may hold BIZ) |
| Basal_Intermediate_Zone | none | missing | none | Gap |
| Conducting_Zone | none | missing | CZ (Revise; weak markers) | The Yuan survey note claiming a validated CZ is wrong: only the LCM CZ profile was used |
| Embryo_Surrounding_Region | 15: 159 (0.9%) | Adopt | ESR (Adopt, 18 spots) | Markers very specific in both |
| Endosperm_Adjacent_to_Scutellum | 11: 370 (2.2%) | Revise | EAS (Adopt) | Yuan c11's DE genes are SE genes, and the named EAS markers are not DE for c11. EAS forms after 7 DAP. Treat as EAS precursor / embryo-adjacent SE |
| Dividing_cells (state) | 10, 12: 866 (5.1%) | Revise (state, correctly named) | (EM partly) | G2/M cyclins, KNOLLE, CENH3 |
| Protoplasting_stress (state) | 13: 278 (1.6%), removed | Reject as type | n/a | HSP-dominated |
| (low quality) | 16: 90 (0.5%), removed | Reject | n/a | Mitochondrial-high |
| (undefined) | 5: 1013 (6.0%) | Reject | n/a | No specific markers; SE-like |
| (undefined) | 6: 1387 (8.1%) | Reject | n/a | AL-like, stress-gene overlap |
| Nucellus (contaminant) | 14: 110 (0.6%), removed | Revise (flag) | not resolved (PC) | Pericarp not excluded |
| Embryo (contaminant) | 17: 82 (0.5%), removed | Adopt (flag) | SCU/EM | Exclude from endosperm analyses |
| Pericarp, Placento_Chalazal | none | absent (dissected endosperm) | PE, PC | Use the maize_seed rows if present |

## Cross-study markers

29 rows have agreement from a second independent source: a second dataset (Fu 2023, Wu 2025/Satterlee 2020, Guillotin 2023) or an independent in situ/mutant study. "Fu" = fold over the next compartment in Fu SD1.

| Cell type | Symbol | v5 | v4 | Evidence | Agreement |
|---|---|---|---|---|---|
| BETL | MRP1 | Zm00001eb354390 | Zm00001d010889 | function, high | Gomez 2002 in situ; Yuan c2 0.45 vs 0.015; Fu 6.3x (low counts) |
| BETL | MEG1 | Zm00001eb302080 | Zm00001d019030 | function, high | Costa 2012; Yuan 0.59 vs 0.07; Fu 14x |
| BETL | MYBR29 | Zm00001eb108630 | Zm00001d006791 | function, high | Yuan mutant + c2 0.77 vs 0.04; Fu 9.3x |
| BETL | SWEET4C | Zm00001eb236810 | Zm00001d015912 | function, high | Sosso 2015 mutant; Yuan 0.60 vs 0.19; Fu 4.5x |
| BETL | MN1/INCW2 | Zm00001eb083790 | Zm00001d003776 | function, high | Cheng 1996; Fu 9.9x; not DE in Yuan (stage) |
| BETL | BETL9 | Zm00001eb138660 | Zm00001d041822 | char_enriched, high | in situ in both; Fu 12.2x |
| BETL | BAP2 | Zm00001eb172830 | Zm00001d049576 | char_enriched, high | Serna 2001 + Yuan in situ; Fu 12.9x |
| BETL | TCRR1 | Zm00001eb178220 | Zm00001d050200 | char_enriched, high | Muniz 2006 in situ; Yuan c2 only; Fu 8.7x |
| BETL | BETL10 | Zm00001eb142290 | Zm00001d042231 | char_enriched, medium | Yuan 0.85 vs 0.09; Fu 10.6x |
| BETL | pco073740 | Zm00001eb198770 | Zm00001d052759 | char_enriched, high | Yuan in situ; Fu 9.3x (top BETL gene) |
| BETL | gpm875 (1d053785) | Zm00001eb207110 | Zm00001d053785 | char_enriched, high | Yuan in situ + reduced in mybr29; Fu 12.3x |
| BETL | gpm481 (1d053108) | Zm00001eb201800 | Zm00001d053108 | char_enriched, high | Yuan in situ (outer BETL); Fu 14.2x |
| BETL | gpm832 | Zm00001eb416640 | Zm00001d024659 | expression, medium | Yuan c2 0.97 vs 0.10; Fu 6.3x |
| BETL | BETL4 | Zm00001eb201370 | Zm00001d000161 | char_enriched, high | Hueros 1999 + Fu in situ; not DE in Yuan (stage) |
| ESR | ESR1 | (none in v5) | Zm00001d027820 | char_enriched, high | Opsahl-Ferstad 1997; Yuan 0.88 vs 0.01; Fu 14.8x |
| ESR | ESR2 | Zm00001eb005200 | Zm00001d027819 | char_enriched, high | Opsahl-Ferstad 1997; Yuan 0.92 vs 0.02; Fu 5.3x |
| ESR | ESR6 | Zm00001eb201820 | Zm00001d053112 | char_enriched, high | Balandin 2005; Yuan 0.82 vs 0.005; Fu 1.8x (BETL second) |
| ESR | MEG14 | (none in v5) | Zm00001d019033 | char_enriched, high | Yuan in situ, 0.94 vs 0.06; Fu 3.7x |
| ESR | 1d038758 | Zm00001eb293390 | Zm00001d038758 | char_enriched, high | Yuan in situ; Fu 5.6x |
| EAS | SWEET15A | Zm00001eb180830 | Zm00001d050577 | char_enriched, high | Doll 2020 + Yuan in situ; Fu 12x |
| EAS | ZCN11 | Zm00001eb281410 | Zm00001d037439 | char_enriched, high | Doll 2020 in situ; Fu 9.9x |
| EAS | SWEET14a | Zm00001eb113080 | Zm00001d007365 | char_enriched, high | Doll 2020 in situ; Fu 11x |
| EAS | MS8 | Zm00001eb366340 | Zm00001d012234 | char_enriched, medium | Yuan in situ; Fu EAS 5.6x; conflict (below) |
| Starchy_Endosperm | FL3 | Zm00001eb341550 | Zm00001d009292 | function, high | Li 2017 mutant; Yuan in situ; Fu weak 1.3x |
| Dividing_cells | CYCB1-4 | Zm00001eb150450 | Zm00001d043164 | function, high | Yuan c10/c12; Wu 2025; Satterlee 2020 |
| Dividing_cells | KNOLLE | Zm00001eb215350 | Zm00001d013323 | function, high | Yuan c12 0.35 vs 0.04; Wu 2025; Satterlee 2020 |
| Dividing_cells | CENH3 | Zm00001eb291210 | Zm00001d038533 | function, high | Yuan c12 0.64 vs 0.28; Wu 2025; Satterlee 2020 |
| Dividing_cells | CYC3 | Zm00001eb272010 | Zm00001d036360 | char_enriched, medium | Yuan c10/c12; Guillotin 2023 Dividing_cells |
| Embryo (contaminant) | LTP3 | Zm00001eb149490 | Zm00001d043049 | char_enriched, medium | Yuan c17; Fu in situ embryo; an epidermis gene (maize_leaf) |

## Gaps

- **Basal_Intermediate_Zone, Conducting_Zone, Subaleurone:** no validated marker in either dataset. Yuan did not annotate them. Fu's CZ marker (SDH1) is weak and not specific in Yuan (0.96 vs 0.93). These are Step 4 search targets (Leroux 2014 LCM BIZ genes; Zhan 2015 LCM CZ genes).
- **Aleurone:** no `function` marker and no gene that is specific in scRNA at 6-7 DAP. SBT1 (in situ, modest DE) is the best early marker, and LTP2 is a later one.
- **Starchy_Endosperm:** FL3 is the only `function` row. Zeins and starch genes (in the maize_seed draft) are endosperm-wide, appear after ~8-10 DAP, and are a high ambient-RNA risk.
- **ESR and EAS:** no `function` markers (all `characterized_enriched`, high).
- **Pericarp, Placento_Chalazal:** not captured in dissected endosperm. Only maize_seed rows exist.

## Recommended label reference

There is only one endosperm single-cell dataset, so **Yuan 2024 at the cluster level** is the reference for 6-8 DAP data. Re-cluster and re-derive labels using:
- Adopt BETL (c2/c9), ESR (c15) and SE (c1/c8), plus the removed contaminant clusters (embryo c17, nucellus c14) as flags.
- Re-call aleurone and peripheral cells, EAS precursors (c11) and the undefined clusters c5/c6 de novo.
- Leave G2/M (c10/c12) as `Dividing_cells`.

For later stages (≥ 10 DAP), use Fu 2023's compartments only as **region-level** priors. Its spots mix cells, and its labels were hand-gated.

## Conflicts and corrections

- **MS8 (Zm00001d012234):** Yuan's text and in situ call it an EAS-progenitor marker, but Yuan SD4 has it DE only in ESR c15 (0.37 vs 0.015). Fu places it in EAS (5.6x). It is kept under EAS at medium confidence. It may mark the embryo-facing endosperm generally.
- **EAG1b / acanthoscurrin-2 (Zm00001d011340):** Fu calls it an ESR marker (84x). In Yuan it is the second-highest gene of the **embryo** contaminant cluster c17 (0.99 vs 0.003), with tandem paralogs 1d011342 and 1d011345, and it is not DE in ESR c15. Fu's 55 um ESR spots border the embryo. It is kept as an `Embryo` row at low confidence. Do not use it as an ESR marker until it is checked against ESR1/ESR2 in the data.
- **ESR6:** ESR-specific in Yuan (0.82 vs 0.005), but Fu shows substantial BETL signal (7.6 vs 13.6).
- **SUT1 (Zm00001d027854):** Fu's BETL function marker (RNAi) is DE in Yuan **aleurone** c4/c7 (0.31-0.36 vs 0.15), not in BETL, at 6-7 DAP. It is left out of this draft; the maize_seed draft carries it at medium confidence.
- **nsLTP2P (Zm00001d013907):** Fu's aleurone gate gene is also a top DE gene of Yuan's nucellus cluster c14. It is `expression`, low.
- **AL9:** not specific in Yuan (0.999 vs 0.931) and nearly as high in ESR as in AL in Fu. It is kept at low confidence for continuity only.
- **DE18/YUC1:** graded `characterized_enriched` (the review said `function`). Endosperm auxin synthesis does not define SE identity.
- **Symbols:** Yuan SD27 gives MEG1 the full name "maternally expressed gene6" (UniProt Q6JB15 confirms MEG1). It calls Zm00001d015569 "VPP7", which NCBI names vpp1 (the row symbol is VPP1). Zm00001d043164 is "CYC7" in Yuan and CYCB1-4 (cyclin IaZm) elsewhere. LTP3 is "PLT3" in Yuan. Zm00001d008403 "NAC130" is NCBI "NAC domain-containing protein 100" (nac4). FL3's v5 model is named PLTZ2 in UniProt. The NCBI ESR2 locus (Zm00001d027819) carries ESR1 aliases.
- **IDs with no v5 gene model:** ESR1 (Zm00001d027820) and MEG14 (Zm00001d019033) have no MaizeGDB crosswalk entry and no Ensembl v5 gene at their NCBI v5 loci. In those two rows `ref_gene` holds the v4 ID, so they will not match v5-annotated data (the RefSeq LOC100037781 and LOC103632061 models exist).
- **SWEET4C v5 ID added:** the review had no v5 ID. Zm00001eb236810 is the Ensembl v5 gene overlapping NCBI LOC100273706 (chr5:130,301,473-130,304,291). The same method reproduced MN1 → Zm00001eb083790, which matches the crosswalk.
- **Corrections to the review:** none to the IDs it checked. The review's `id_checked=false` IDs were confirmed through NCBI Gene aliases (ZEAMMB73_v4 + v3 + symbol) for MRP1, BETL9, BETL10, BAP2, SWEET4C, gpm832, gpm481, pco073740, gpm875, FL3, CNGT1, umc1698, ESR1, ESR2, PEBP11/ZCN11 and si606045f03. AL9 and 1d038758 have no NCBI Gene record. They are confirmed only by Yuan SD27 and the UniProt v5 entries (B4FFB8 5a2; knottin).

## Overlap with the skill's marker tables

- The skill has no maize table (`references/markers/` holds Arabidopsis leaf/root, rice root, sorghum leaf and sorghum root Guillotin 2023).
- Two draft genes appear, by v5 ID, in `sorghum_root_Guillotin2023.tsv` (where maize v5 IDs sit in the `symbol` column), both as `Dividing_cells`: CYC3 (Zm00001eb272010) and HMG9 (Zm00001eb238060). This is consistent with the state assignment here.
- No endosperm, aleurone, BETL, ESR or EAS row exists in any skill table.
- The sibling drafts overlap heavily:
  - 24 of the 47 rows share an ID with `maize_seed/markers_draft.tsv`. 23 have the same cell type, evidence and confidence; LTP3 is Embryonic_Axis there (medium) and Embryo here.
  - CYCB1-4, KNOLLE and CENH3 match `maize_embryo`.
  - PDK1 is a `maize_leaf` Mesophyll function marker (C4 PPDK): do not use it outside endosperm.
  - LTP3 is a `maize_leaf` Epidermis marker.

## Could not verify

- No per-cell labels exist for Yuan 2024. The Seurat object is not deposited, and the ShinyCell portals were not scraped.
- In situ images were not inspected. "In situ" is as stated in the papers' text and legends (Yuan Supp Figs 6, 7, 11; Fu Fig 2, Table S3).
- Literature validations (Gomez 2002, Muniz 2006, Serna 2001, Opsahl-Ferstad 1997, Balandin 2005, Costa 2012, Sosso 2015, Hueros 1999, Doll 2020, Li 2017) are as cited by Yuan, Fu and the maize_seed collation. I did not reread the primary papers, and those DOIs were not individually re-resolved.
- The v4→v5 mapping uses the MaizeGDB crosswalk (plus Ensembl overlap for SWEET4C), with no BLAST. For multi-model maps (TPS11, AL9, KNOLLE, CENH3), the first model or the model checked in the sibling review was used.
- Zm00001d038758 and Zm00001d012572 (AL9) have no NCBI Gene record.
- Doll et al. 2020 (EAS) and the BIZ/CZ LCM studies (Leroux 2014, Zhan 2015) were not mined for additional markers. That is the next Step 4 search for the gaps.

## Update 2026-10-20: gap-fill reviews

Two characterization studies from the Yadegari lab were reviewed to fill the BIZ, CZ, aleurone, ESR and maternal-tissue gaps: `Zhan2015/` and `Li2014/`. Their markers were merged into `markers_draft.tsv` by v5 gene ID, not by symbol. The table now has **83 rows** (47 before, 36 added; 13 fields on every line, validated). The same ID conventions are kept: `ref_gene` = v5, `alt_id` = v4, and the v4 ID stays in `ref_gene` where no v5 model exists. Five new rows have **no v4 model**, so their `alt_id` is empty: BAP1A, MEG2, GRMZM2G027472, GRMZM2G072219 and GRMZM2G120008. They will not match v4-annotated data such as Yuan's or Fu's. Every added gene was cross-checked by v4 ID against Yuan SD4 and Fu SD1 (results are in the `basis` lines). The `characterized_markers.tsv` rows tagged `maize_endosperm:` were used as well. `expected_cell_types.tsv` counts and notes were updated. Pre-update copies of the three group files are kept as dot-files (`.markers_draft.pre_2026-10-20_update.tsv` and so on).

### New datasets

| Dataset | Type | Samples | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|
| Zhan J, Thakare D, ... Drews GN, Yadegari R (2015) *Plant Cell* 27:513-531. doi:10.1105/tpc.114.135657 (DOI confirmed in Europe PMC) | LCM + Illumina RNA-seq, B73 8 DAP | 10 compartments: AL, BETL, CSE, CZ, ESR, EMB (3 reps each); NU, PE, PC, PED (1 rep each) | v3 GRMZM, mapped to v5/v4 through the MaizeGDB xref | population_level | medium |
| Li G, Wang D, ... Drews GN, Wang X, Yadegari R (2014) *PNAS* 111:7582-7587. doi:10.1073/pnas.1406383111 (DOI confirmed in Europe PMC) | SOLiD bulk time course 0-12 DAP + in situ of 23 genes | 8 bulk stages; in situ compartment map | v2/v3, mapped to v5/v4 | population_level | medium |

**Independence.** Both studies come from the same lab, and Zhan cites Li's in situ results. A Li in situ result plus Zhan LCM enrichment was therefore *not* counted as cross-study agreement; those rows say "same lab". To raise a confidence level, a row needed agreement with Yuan 2024, Fu 2023 or a study from another lab.

### Verdicts

| Compartment | Zhan 2015 | Li 2014 | Maps to |
|---|---|---|---|
| BETL | Adopt (30 in situ genes; MRP1 module confirmed by Y1H) | Adopt (3 BETL-only + 6 BETL+BIZ in situ genes) | Basal_Endosperm_Transfer_Layer |
| BIZ | (no capture) | Revise: rests on one exclusive gene | Basal_Intermediate_Zone |
| CZ | Revise: weak; looks like a BETL-to-CSE transition | Revise: one gene (FL3), diffuse, only at 7 DAP | Conducting_Zone |
| ESR | Adopt (100-200x) | Adopt (4 ESR-only genes) | Embryo_Surrounding_Region |
| AL | Adopt with caveats (thin layer, impure captures) | Revise (AL9 only) | Aleurone |
| CSE / SE | Adopt (Sh1, Sh2, gamma-zein in situ; subaleurone not separated) | Adopt (TF genes; modest specificity) | Starchy_Endosperm |
| EMB | Revise: whole embryo + suspensor | n/a | Embryo (contaminant flag) |
| NU | Adopt, low confidence (1 rep, no in situ) | n/a | Nucellus |
| PE | Adopt, low confidence (merged layers, 1 rep) | n/a | Pericarp |
| PC | Revise: worst sample (25 ng, RIN 2.9) | n/a | Placento_Chalazal |
| PED | Reject (out of scope) | n/a | none |
| Whole-kernel / endosperm stages | n/a | Reject (stages, not cell types) | none |

### Markers raised (existing rows)

| Row | Change | New support |
|---|---|---|
| BETL10 (Zm00001eb142290) | medium -> high | Li 2014 in situ BETL+BIZ, independent of Yuan/Fu |
| gpm832 (Zm00001eb416640) | medium -> high; expression -> characterized_enriched | Zhan 2015 in situ BETL |
| SBT1 (Zm00001eb408980) | medium -> high | Zhan 2015 in situ aleurone (second in situ after Yuan's) |
| VPP1 (Zm00001eb234390) | low -> medium | Wisniewski and Rogowsky 2004 in situ (doi:10.1007/s11103-004-3414-x, confirmed in Europe PMC) + Zhan LCM |
| NAC130 (Zm00001eb334180) | low -> medium | Li 2014 in situ SE. Only to medium, because enrichment is about 2x everywhere. The symbol is now confirmed by Zhan DS3 (ZmNAC130) |
| si606045f03 (Zm00001eb388330) | medium -> high | Zhan LCM nucellus 19x (a single replicate, from a different lab than Yuan) |

Basis lines of 16 other existing rows gained Zhan/Li support without a confidence change, because they were already high or still conflict: MRP1, MEG1, MYBR29, SWEET4C, MN1, BETL9, BAP2, TCRR1, gpm481, BETL4, ESR1, ESR2, ESR6, AL9, FL3, TAR1. In MN1's and BETL4's rows, "later-stage" is now qualified: both are strongly BETL-specific by 8 DAP in the LCM data.

### Markers added (36)

- **BETL (8):** MEG13, GRMZM2G132162, BURP3, LTP-like GRMZM2G009854 and BAP1A at high (BAP1A from Serna 2001 + Zhan in situ). MEG2, GRMZM2G027472 and LTP-like GRMZM2G072219 at medium (Li + Zhan only, same lab).
- **Basal_Intermediate_Zone (1):** BURP GRMZM2G406170 (Zm00001eb300370), characterized_enriched, medium. This is the first BIZ row.
- **Conducting_Zone (3):** FL3 (low; CZ-only by in situ at 7 DAP), plus CC10 and CIP8-like RING (LCM only, low).
- **ESR (2):** GRMZM2G149869 (high: Zhan in situ + Yuan c15 + Fu ESR) and GRMZM2G120008 (medium).
- **EAS (2, from the characterized survey):** KIL1 and KIL2, both `function`. They are raised medium -> high because Fu's EAS compartment is the top compartment for both (low counts).
- **Aleurone (2):** GRMZM2G091774 (high: Zhan in situ + Yuan AL DE) and PEAMT (medium; conflicts with Fu, see below).
- **Starchy_Endosperm (6):** 27kD gamma-zein (function, high), SH1 and SH2 (function, medium), GRAS20 and MYB127 (medium), NAC128 (low).
- **Embryo (3):** LEC1 (function, medium), extensin-like (medium: Zhan EMB + Yuan c17), YAB1 (low).
- **Nucellus (3), Pericarp (3), Placento_Chalazal (3):** all from Zhan's single-replicate LCM, so all low, except ZmDL1, which was raised to medium by agreement with Fu PE.

**Not added:**
- GRMZM2G080263: its v3 ID splits into 2 v4 and 2 v5 models.
- GRMZM2G128832 (ESR+BETL+BIZ) and the GRMZM2G046532 defensin-like gene (BETL+BIZ+CZ+ESR; near-ubiquitous in Yuan): neither is type-specific.
- The two strongest Zhan CZ genes: they have no v4/v5 model.
- Zhan PED genes.
- Characterized-survey rows C1, NKD1, NKD2 and CR4 (maturation-stage or not aleurone-restricted), P1 (v5 not verified, multi-copy, allele-dependent pericarp expression), and the rice/barley homology-only rows (OsMADS29, NF-YB1, barley LTP2).

### Gaps closed

- **Basal_Intermediate_Zone:** now has one in situ-validated marker (no `function` marker). Call BIZ as BURP+ cells that express BETL+BIZ genes (BETL10, BURP3, BAP1A, MEG2) and lack the outer-BETL genes (MRP1, TCRR1, MYBR29, gpm481).
- **Conducting_Zone:** has rows now, but all low confidence.
- **Aleurone:** two high early markers (SBT1, GRMZM2G091774), each validated in situ plus a second study.
- **ESR:** a sixth high marker (GRMZM2G149869).
- **Starchy_Endosperm:** three more `function` rows (gamma-zein, SH1, SH2).
- **EAS:** its first `function` rows (KIL1, KIL2).
- **Nucellus, Pericarp, Placento_Chalazal, Embryo:** have contamination-flag rows.

### Gaps remaining

- No `function` marker for Aleurone, ESR, BIZ, CZ, Subaleurone, Nucellus, Pericarp or Placento_Chalazal.
- BIZ rests on one low-expression gene that is not DE in Yuan 2024. Leroux 2014 (BIZ LCM) is still unmined.
- CZ markers are weak. Zhan's CZ looks like a transition zone, so Conducting_Zone may not be a separable cluster at 6-8 DAP.
- Subaleurone is still unresolved. GRAS20 (peripheral in situ; AL/VE-high in Fu) is a candidate only.
- All maternal rows rest on single-replicate LCM with no in situ.
- The 27kD gamma-zein, SH1 and SH2 rows are endosperm-wide by 10+ DAP and carry an ambient-RNA risk.

### Conflicts

- **FL3 (Zm00001eb341550):** Li's in situ shows it CZ-only at 7 DAP. Zhan's LCM has it highest in CZ, but high in CSE and ESR too, and Zhan's single "CZ" in situ gene is FL3 itself. Later stages show broad SE expression (fl3 function). It is kept as a Starchy_Endosperm function row (high) and added as a Conducting_Zone row (low).
- **PEAMT (Zm00001eb294690):** in situ aleurone and LCM AL 15.6x over ESR (Zhan). But Fu 12-24 DAP puts it in ESR (24.1) and near zero in AL, and Yuan DE is weak (AL c3/c4 plus embryo c17). Kept at medium, not raised.
- **AL9:** Li's in situ shows it AL-only, but Zhan LCM is only 2x and Yuan/Fu are non-specific. It stays low.
- **B12D (Placento_Chalazal):** Yuan has it DE in aleurone c0.
- **Extensin-like (Embryo):** Fu ESR spots, the same embryo-border pattern as EAG1b.
- **CIP8-like (CZ):** Yuan DE in the stress cluster c13.
- **Symbols to compare by ID:**
  - GRMZM2G088896 is MEG2 in UniProt (Q6JB14) but MEG9 in Zhan DS3.
  - BURP3 is named BURP7 in UniProt.
  - GRMZM2G369799 is ZmMYB127 in Zhan DS3. Li 2014 assigned that name by elimination, and UniProt calls the gene MYB44.
  - GRAS20 is SCL1 in Zhan DS3.
- **BETL gradient:** BETL9 (3.9x) and BURP3 (2.3x) are only weakly BETL-over-CZ in the LCM data, and Li shows six BETL genes also in the BIZ. Expect basal clusters to grade into one another.

### Recommended label reference (revised)

Neither new study has per-cell labels, so **Yuan 2024 at the cluster level stays the single-cell reference** for 6-8 DAP. Use the two new studies as follows:
- **Zhan 2015** as the 8-DAP compartment reference for marker grading. Its BETL, ESR, AL and CSE captures are triplicated and backed by in situ. Its CZ, EMB and maternal compartments are context only.
- **Li 2014** as the in situ map for splitting basal clusters into BETL (outer: MRP1, TCRR1, gpm481), BETL+BIZ and BIZ (BURP).

For ≥ 10 DAP, Fu 2023 remains the region-level prior.

### Could not verify

- **Zhan 2015 main text:** the PMC page returned a reCAPTCHA and there is no Europe PMC full text. The review used the abstract and the full supplement (DS1-DS6, Supp Table 6).
- **Li 2014 SI PDF (Fig S5) and Datasets S1-S4:** PMC and PNAS returned a bot-check page, which was not bypassed. Li in situ results were read from main-text Figs 4-5.
- **Missing gene models:** ESR1 and the two strongest Zhan CZ genes have no v5 model. Five added genes have no v4 model.
- **SWEET4C's v5 ID** still comes from the earlier Ensembl overlap; there is no MaizeGDB v5 xref.
- **Literature DOIs:** confirmed in Europe PMC for Zhan 2015, Li 2014, Wisniewski 2004, Royo 2014 (doi:10.3389/fpls.2014.00180), Gutierrez-Marcos 2004 (doi:10.1105/tpc.019778) and Woo 2001 (doi:10.1105/tpc.010240). Gomez 2009 (AL9 promoter) was not found and is not cited in `source`. The in situ claims attributed to these papers are as cited by Zhan/Li, not reread.
- **Fu values** are compartment mean UMI (SD1). Values below about 1 are low counts and were treated as weak support only.
