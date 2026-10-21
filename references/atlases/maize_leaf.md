<!-- Collated from the survey review of maize_leaf (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Maize leaf single-cell datasets: group collation

Date: 2026-10-20. Paper-only review (Steps 1-3a); no in-data check yet.
Inputs: the four dataset reviews in `survey/merged_reviews.json` (group `maize_leaf`) and their folders here.

Files in this folder:

- `expected_cell_types.tsv`: written from grass/C4 leaf anatomy, not from the published labels. `function_markers` counts the `function` rows in `markers_draft.tsv` (all rows apply to maize, which is `grass,C4`).
- `markers_draft.tsv`: 76 rows (74 genes; SWEET13a and SWEET13c appear under two cell types), skill schema plus `alt_id`. **`ref_gene` = B73 v5 (`Zm00001eb`), `alt_id` = B73 v4 (`Zm00001d`).** v5 is the current reference and Zhao 2024 uses it. Three of the four papers use v4: for data aligned to v4, run `map_markers.py --id-column alt_id`. Every v4/v5 pair was checked against MaizeGDB `B73v4_to_B73v5.tsv`, and every v5 symbol against the MaizeGDB v5 `fulldata` table (copies in `Sun2022/id_check/`).
- Per-dataset folders (`Bezrutczyk2021/`, `Yi2026/`, `Sun2022/`, `Zhao2024/`) keep their own README, supplements and ID checks. I left them unchanged.

## Datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Bezrutczyk et al. 2021 *Plant Cell* 33:531, 10.1093/plcell/koaa055 (GSE157757) | B73 leaf 2, distal 6 cm, V2 | protoplast scRNA, 10x 3' | 3,763 (rep A) + 3,242 (rep B) | v4 | cluster only (GEO matrices 71/45 MB; mapping in Supp Table S1/S2, Data Set 1) | medium: ≥98% mesophyll; 53 BS cells; no epidermis or vasculature |
| Yi et al. 2026 *Plant Cell* 38:koag035, 10.1093/plcell/koag035 (SRA PRJNA1051680) | B73 P4 primordia, 3-4 mm, ~200 pooled | nuclei, 10x 3' v3.1 | 7,476 nuclei in 14 clusters, 1 library | v4 | cluster only (raw FASTQ 32 GB; cluster table in text and Supp Fig S2) | medium: 22 in situ probes, PIN1a-YFP and mutants; no replicate |
| Sun et al. 2022 *Plant Cell* 34:1890, 10.1093/plcell/koac047 (PRJNA740934) | B73 abaxial epidermal peels (leaves 1-2) + basal 1 cm of leaf 2 | FANS nuclei, 10x 3' v2/v3 | 24,131 peel + 8,967 leaf-base nuclei | v4 | cluster only (raw SRA; Shiny portal plots only) | medium: GC/SC reporters, but 44 GC nuclei; supplementary zip not accessible |
| Zhao et al. 2024 bioRxiv, 10.1101/2024.10.28.620769 (STOmics STT0000093, CNP0005465) | B73 shoot base, 12 d (SAM, P1-P6, sheath) | cell-segmented Stereo-seq + nuclei (DNBelab C4) | 14,037 spatial cells; 33,309 nuclei | v5 | cluster only (STOmics objects 3.73 GB, file list not checked) | medium: manual anatomical BS/MC labels on one section; snRNA labels partly by label transfer; preprint |

None of the four has public per-cell labels. All four are cluster-only, so labels must be re-derived after re-clustering.

## Verdicts by expected cell type

A = Adopt, R = Revise, X = Reject, - = not annotated. From the dataset reviews.

| Expected type | Bezrutczyk 2021 | Yi 2026 (P4) | Sun 2022 (epidermis + base) | Zhao 2024 (spatial / sn) |
|---|---|---|---|---|
| Mesophyll | A (MS1); R (MS2-4 stress/ribosomal); X (MS5 iron, 1 rep) | R (c10 "palisade" → Mesophyll); R (c8 merged with midrib parenchyma) | R (peel contamination) | A (spatial manual; sn C5) |
| Bundle_Sheath | A (abaxial BS, 21 cells); R ("adaxial BS" = all non-abaxial BS) | - (c13 possible precursor, unresolved) | R ("BS-related", may hold vasculature) | A (spatial manual, vein rank; sn C25); R (sn early BSC, circular) |
| Epidermis / pavement | - | A (c0, c6; subtype unresolved) | R (PCs-N merged; PCs-A anthocyanin state) | A spatial; R (sn 8 stage clusters) |
| Guard | - | - | A (44 nuclei, under-recovered) | R (merged with SC) |
| Subsidiary | - | - | A (1,513) | R (merged with GC) |
| Stomatal_lineage | - | - | A (GMC, YGC, YSC); R (SMC) | R (sn C22, markers not given) |
| Bulliform, Silica, Cork, Trichome | - | - | - (probably inside PCs-N) | - |
| Sclerenchyma | - | - | - | R (spatial C11 sheath, position only) |
| Xylem | - | A (c12 primary xylem) | R (leaf base vasculature, transferred) | A (spatial C13); R (sn C16, C27) |
| Phloem (incl. SE, CC, PP) | - (SUT1 in situ only) | A (c11 primary phloem, unsplit) | R (as above) | A (spatial C7, unsplit); R (sn 7 of 29 clusters) |
| Procambium | - | A (c5, best supported) | - | A (spatial C12; sn C12) |
| Ground_Meristem | - | A (c1 mGM) | - | R (spatial mGM, position only) |
| Ground_Parenchyma | - | R (c8) | - | - |
| Ligule | - | - | R (C10, LG1 only) | - |
| Shoot_Meristem (KNOX) | - | - | X (C1 "leaf primordia" zone) | R (sn C18) |
| Dividing_cells / S_Phase (states) | - | A as states (c2, c7 G2/M; c3 S) | X (C7 typed as a cluster) | X (left unlabelled: correct) |
| Unassigned / low quality | - | X (c4 ribosomal; c9 unknown) | - | X (sn C4, C6, C17, C24) |

## Cross-study markers (same gene ID, two or more independent studies)

| Cell type | Gene (v5 / v4) | Studies | Confidence |
|---|---|---|---|
| Mesophyll | PEPC1 Zm00001eb383680 / Zm00001d046170 | Bezrutczyk (DE), Zhao (sn dotplot) | high |
| Mesophyll | CAH1 Zm00001eb158810 / Zm00001d044099 | Bezrutczyk (DE), Zhao (sn), Sun (Fig 3C, MC and SC) | high |
| Mesophyll | NADP-MDH Zm00001eb038930 / Zm00001d031899 | Bezrutczyk, Zhao | high |
| Bundle_Sheath | NADP-ME Zm00001eb121470 / Zm00001d000316 | Bezrutczyk, Zhao | high |
| Bundle_Sheath | RBCS1 Zm00001eb197410 / Zm00001d052595 | Bezrutczyk (in situ), Zhao (Stereo-seq) | high |
| Bundle_Sheath | RBCS2 Zm00001eb092540 / Zm00001d004894 | Bezrutczyk (DE), Zhao (module M7) | medium |
| Phloem_Companion | SUT1 Zm00001eb005460 / Zm00001d027854 | Bezrutczyk (in situ CC), Zhao (Fig 5D, as PP) | high |
| Procambium | PIN1a Zm00001eb372180 / Zm00001d044812 | Yi (YFP reporter), Zhao (Stereo-seq) | high |
| Epidermis | PLT3/LTP3 Zm00001eb149490 / Zm00001d043049 | Zhao (Stereo-seq), Yi (epidermal DE, Table S5) | high (raised from medium) |
| Subsidiary | CST1 Zm00001eb288410 / Zm00001d038226 | Wang 2019 *Plant Cell* (reporters, mutant), Sun (native eYFP) | high |

That is 10 cross-study genes. Caveat: Zhao 2024 gives symbols or enzyme names only, and its ID tables (S9, S13) could not be opened. Its IDs are therefore inferred from MaizeGDB symbols. They agree with the IDs in the other papers' tables, but the paralog choice is not confirmed. The C4 enzymes are already `high` from in situ and proteomics literature, so the raise only changed PLT3. RBCS2 stays `medium` because Zhao supports it only through module membership.

## Gaps (expected types with no `function` marker)

- **Bulliform, Silica, Cork, Trichome:** no dataset annotated them. Sun 2022 "PCs-N" probably contains them. For Silica, use sorghum `SLP1` via homology. All four are Step 4 search targets.
- **Sclerenchyma:** only Zhao's position-only spatial cluster. Yi's ZmWRKY98 "sclerenchymatous cell" in Table S5 has no probe in Table S1, so I excluded it.
- **Phloem (unsplit), Ground_Parenchyma, Shoot_Meristem:** only `characterized_enriched` rows.
- **Thin.** Subsidiary, Ligule, Xylem, Sieve_Element, Phloem_Companion and Ground_Meristem each have a single `function` marker.
- **Mature-blade vasculature:** the vascular markers come from P4 primordia (Yi) or the shoot base (Zhao). No mature-blade dataset resolves xylem, phloem or PP, and Bezrutczyk captured no vascular cells.

## Recommended label reference

There is no single reference. Use the one that matches the sample:

- **Mature blade, MS vs BS:** Bezrutczyk 2021 markers. Its C4 enzyme split and the in situ/GUS-validated abaxial-BS SWEET13 set are the strongest. Its labels cover only MS and BS.
- **Epidermis and stomata:** Sun 2022 markers (GC, SC and GMC reporters). Do not use its proportions: GCs are under-recovered.
- **Primordia / leaf base (mGM, procambium, protophloem, protoxylem):** Yi 2026 is the best-validated (22 in situ probes). Zhao 2024 Stereo-seq adds spatial ground truth for Kranz BS/MC and vein tissues, but it is a preprint with inaccessible ID tables.

Because no per-cell labels are public, these serve as marker sources and cluster-level hypotheses, not as benchmarks.

## Conflicts and corrections

- **ZmSHR1/ZmSHR2 swap (Yi 2026).** Table S5 calls Zm00001d021973 (gras19) "ZmSHR1" and Zm00001d029607 (gras58) "ZmSHR2". The paper's own ZmSHR1 overexpression primers (Table S1) use Zm00001d029607. Per the Yi review (Slewinski 2014 naming), ZmSHR1 = Zm00001d029607 and ZmSHR2 = Zm00001d021973. Zhao 2024's SHR pair (Zm00001eb108090 = gras85 / Zm00001d006721, and Zm00001eb020850 = gras58) is also unresolved. Neither SHR gene is detected in nuclei, so I left SHR out of the table.
- **SWEET13a/b/c: abaxial BS or phloem parenchyma.** In situ puts most of the signal in abaxial BS of rank-2 veins and the rest in PP (Bezrutczyk). They are kept as Bundle_Sheath rows (abaxial subtype only) and as Phloem_Parenchyma rows. In the Bezrutczyk scRNA they mark only abaxial BS, because PP was not captured.
- **SUT1.** Bezrutczyk's in situ puts it in companion cells (plus vascular parenchyma of major veins); Zhao 2024 calls it a phloem-parenchyma marker. Kept as Phloem_Companion; the conflict is in `basis`.
- **CAH1** is also expressed in subsidiary cells (Sun Fig 3C). Do not use it alone for mesophyll in epidermis-enriched data.
- **Yi "palisade mesophyll" (c10)** is relabelled Mesophyll: grasses have no palisade layer.
- **Bezrutczyk "adaxial BS"** means all BS cells without SWEET13, not adaxial BS.
- **KAN1 vs RL9.** The symbol for Zm00001d032249 differs between Bezrutczyk and UniProt. It is expression-only, so I excluded it.
- **Golden2 ID.** An NCBI text search for "golden2" returns glk1 (Zm00001d044785). The correct G2 is Zm00001eb118900 / Zm00001d039260 (MaizeGDB symbol g2).
- **Probe claims without probes (Yi 2026).** Table S5 lists in situ for INCW5, AIC1, C2H2-46 and WRKY98, but Table S1 has no probe for them. I excluded all four.
- **v4 genes split in v5.** Each of these v4 genes maps to two v5 models. `ref_gene` holds the symbol-bearing model and `basis` names the other:
  - PIN1a (eb372180/eb372190)
  - AIC3 (eb010460/eb010470)
  - TMO5-LIKE3 (eb099390/eb099400)
  - KZM2 (eb120180/eb120190)
  - NRT1.2 (eb385450/eb385460)
  - MUM2 (eb146100/eb146110)
  - MPK12 (eb415930/eb415940)

## Excluded on purpose

- **Expression-only DE genes (skill rule: no data-picked rows):** UmamiT21a, STP3, AAP45, AAP56, Zm00001d016625, KAN1/RL9, CC3 (Bezrutczyk); INCW5, DEF4 (Yi); GELP3 (Sun); MAD2 (Zhao).
- **Low or no detection in nuclei:** AAS2, SHR1/2.
- **NKD1:** GRN only.

## Overlap with existing skill tables

There is no maize table in `references/markers/`. The closest is `sorghum_leaf.tsv` (17 rows, Sobic v5.1 IDs). Its PPDK, NADP-ME, SUT1, SWEET13, CHX20, CST1 and LG1 rows have maize counterparts here with the same function and cell type (PPDK, NADP-ME, SUT1, SWEET13a/b/c, CHX20, CST1, LG1). I matched these by name and function only, not by BLAST. sorghum_leaf rows with no maize row here: CCR1 (BS/Sclerenchyma), FTL12 and PEAR2 (Phloem), IRX1, XCP1 and CESA7 (Xylem), WBC11 (Epidermis), SLP1 (Silica), CYP79A1 (sorghum Trichome). The maize table would add Guard (8), Subsidiary (6), Stomatal_lineage (5), Procambium/Ground_Meristem (9) and BS/MS depth that the sorghum table lacks.

## Could not verify

- **Sun 2022 supplement** (`koac047_supplementary_data.zip`, 3.7 MB) was blocked by reCAPTCHA or 403 at PMC, Europe PMC and OUP. Its IDs come from the figure legends, and the v5 annotations match the gene names. I did not try to get around the blocks; the user can download it from https://doi.org/10.1093/plcell/koac047.
- **Three Sun 2022 markers named only in the text.** I took their IDs from NCBI Gene aliases, not from the paper:
  - KZM2 (Zm00001d039386)
  - ZMK1 (Zm00001d011473)
  - FAMA-like (Zm00001d009715, NCBI RefSeq description only)

  Confirm them against Supp Data Set 2.
- **Zhao 2024 Tables S9/S13 and the STOmics file list** were not reachable (bioRxiv Cloudflare rate limit; JavaScript-rendered page). So I could not resolve the IDs for ZmLAX2, ZmAPL, ZmXCP1 or ZmMPa, and they are not in the table. Its GLP1, PLT3, IDD7, IDDP1, SSU1/2, CYC23 and C4-enzyme IDs are symbol-inferred.
- **UniProt does not index v4 IDs.** I checked v5 IDs instead (e.g., COMT Q06509 lists Zm00001d049541; LTP3 B6SIF2; RNRS1; Cyclin-B2-1). Uncharacterized genes (GRP6, LecRLK1, GELP2, MUM2) have no UniProt name to confirm.
- **No per-cell labels** exist for any dataset, so no Step 3b in-data check was possible.
