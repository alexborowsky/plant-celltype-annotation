<!-- Collated from the survey review of soybean_seed (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Soybean developing seed: collated single-cell review

Date: 2026-10-20. Built from one dataset review (`Zhang2025/`, which has its own README, `selected_markers.tsv` and `uniprot_id_check.txt`). This is a paper-only review: no in-data check (Step 3b) was run.

Files:
- `expected_cell_types.tsv`: 29 expected types (31 after the update below adds the Hilum and Seed_Coat_Vasculature umbrellas) for the whole seed (seed coat + endosperm + embryo), globular to mid-maturation. Written from soybean seed anatomy, not from the published labels. `function_markers` counts `function` rows in the existing skill tables (`references/markers/`) that would reach a eudicot target via homology (almost all from the Arabidopsis tables). `notes` gives the counts in the draft below.
- `markers_draft.tsv`: 35 rows in the skill marker schema plus `alt_id` (70 rows after the 2026-10-20 update below). `ref_species = soybean`, `tissue = seed` (a new value; the skill README lists only leaf/root/any). `ref_gene` holds Wm82.a4.v1 `Glyma.` IDs, `alt_id` the UniProt accession (and the Wm82.a1 ID for Gy4). Field counts were checked (13 per line); there are no duplicate gene IDs.
- `requires=Fabaceae` is used on 6 rows: legume storage-protein genes (KTi3, KTi1, CG-1, Gy4), hourglass cells (Ep) and hilum (F3'H). The tag is in the skill vocabulary (`Fabaceae` -> `eudicot` in `map_markers.py` IMPLIES). `requires=eudicot` is on the 4 seed-coat parenchyma and epidermis rows.

## Datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Zhang X, Luo Z, Marand AP, Yan H, ... Schmitz RJ. *Cell* 188:550-567 (2025), 10.1016/j.cell.2024.10.050; GEO GSE270392 | Williams 82 whole seeds: globular (GS), heart (HS), cotyledon (CS), early maturation (EMS); mid-maturation (MMS) is scATAC only | 10x snRNA-seq (2 reps/stage) + scATAC-seq + 10x Visium (HS, CS, EMS) | snRNA 86,850 nuclei (GS 21,565; HS 26,059; CS 18,388; EMS 20,838); scATAC 93,359 | Wm82.a4.v1 (Phytozome Gmax_508) `Glyma.XXGXXXXXX` | table: per-nucleus labels in Table S1 (mmc1, 41.8 MB xlsx; extracted to `Zhang2025/TableS1_*.tsv`), plus endosperm sub-region and embryo-lineage integration labels | high |

Only one seed dataset was reviewed. The same paper's root part (`../soybean_root/Zhang2025/`) is the same study, and `../soybean_root/` and `../soybean_nodule/` (Cervantes-Perez 2024) are other organs, so none of them counts as independent support for seed cell types.

## Verdicts by expected cell type

A = Adopt, R = Revise, X = Reject, - = not annotated. Zhang 2025 labels in brackets.

| Expected type | Zhang 2025 |
|---|---|
| Seed_Coat_Epidermis | A (SC_epidermis; TT8, CHS7, PRP1; LCM + Visium) |
| Hourglass_Cell | - (probably merged into SC_vascular_parenchyma / SC_vasculature, where Ep peroxidase is DE) |
| Seed_Coat_Parenchyma | A (SC_parenchyma; SWEET10b by Visium; inner/outer parenchyma merged) |
| Inner_Integument | R (SC_inner_integument; LCM correlation only, no marker) |
| Endothelium | R (SC_endothelium; LCM correlation only; its "markers" are SUC2/PHO1/trichome genes) |
| Hilum_Parenchyma | R (SC_hillum_parenchyma; F3'H/CHS enrichment, LCM hilum, Visium hilum parenchyma at CS) |
| Tracheid_Bar | - in snRNA (Visium only); SC_xylem probably includes it |
| Phloem / Phloem_Parenchyma / Phloem_Companion | A (SC_phloem; SWEET11, bZIP9, SMXL3, CLE25; CC and PP not split) |
| Sieve_Element | - (absent from nuclei, as expected) |
| Xylem | R (SC_xylem = secondary-wall cells incl. tracheid bar; EMS replicate imbalance); R (SC_vasculature at EMS: merged vascular class) |
| Procambium | A embryo (Em_vasculature, EMS); R seed coat (SC_vascular_parenchyma; SC_hillum_vasculature is oversized at 12.4% at HS, low UMI, few DE genes) |
| Endosperm (umbrella) | A (Endosperm; SWEET15a/b, LCM, replicate-balanced) |
| Micropylar / Peripheral / Chalazal_Endosperm | R (integrated sub-region labels from 55 um Visium spots projected by iNMF; ZOU, the expected ESR gene, is spatially peripheral) |
| Aleurone | - |
| Suspensor | - (not called) |
| Embryo (embryo proper, GS/HS) | R (Em_innitials = whole embryo proper, not initials) |
| Protoderm | A (Em_epidermis, CS/EMS; PDF1, LTPG1, SPCH; CS replicate imbalance) |
| Stomatal_lineage | - (inside Em_epidermis) |
| Cotyledon_Parenchyma / Embryonic_Axis | R (Em_proper_innitials at CS: axis + cotyledon merged, Visium splits 442/1,307; Em_parenchyma at EMS: merged; embryo-integration Embryo_parenchyma.1-3 / *_initial_cells are pseudotime branches) |
| Shoot_Apical_Meristem / Stem_Cell_Niche | R (embryo-integration SAM:RAM, 623 nuclei; real STM/KNAT1/PLT2 signal, SAM and RAM merged) |
| Quiescent_Center / Root_Cap | - |
| Dividing_cells | R (Dividing_cell; G2/M state with CDC20, lineage must be reassigned) |
| (contamination / bins) | X (embryo-integration Seed_coat, 545; SC_unknown GS 213; Unknown EMS 318) |

## Cross-study markers

None. With a single seed dataset, no gene can be supported by two independent single-cell datasets. Confidence was raised once, on literature agreement, under the "validated in one study, cluster-specific in another" rule:

| Type | Gene | Support | Draft |
|---|---|---|---|
| Embryo | KTi3 Glyma.08G341500 | in situ, embryo region then axis (Perez-Grau & Goldberg 1989 *Plant Cell*) + Zhang 2025 Visium and snRNA DE | characterized_enriched, high |

SWEET15a (endosperm) and SWEET10b (seed-coat parenchyma) are `high` on their own, as `function` markers with a knockout or domestication phenotype (Wang 2019 *Plant Physiol*; Wang 2020 *Natl Sci Rev*) plus Visium localization in Zhang 2025. The two CDC20 paralogs are `high` as conserved G2/M state markers that are DE at all four stages.

## Gaps (expected types with no validated marker in the draft)

- Seed coat: Inner_Integument, Endothelium, Tracheid_Bar (CESA8 is shared with Xylem), and Hourglass_Cell (Ep is literature-localized but not a single-cell label).
- Endosperm: Micropylar, Peripheral and Chalazal endosperm have only `expression` rows; Aleurone has nothing.
- Embryo: Suspensor, Embryonic_Axis ground tissue, Quiescent_Center and Root_Cap have no soybean marker. Cotyledon_Parenchyma has only storage-protein rows (stage-restricted, ambient-mRNA risk). Phloem_Companion and Sieve_Element: none in soybean (SE absent from nuclei anyway).
- Step 4 search targets: soybean suspensor genes (Goldberg/Harada LCM, e.g. G564-like suspensor-specific genes), endothelium/inner-integument genes, and hourglass-cell genes other than Ep.

## Recommended label reference

Zhang 2025, as the only dataset, and acceptable: per-nucleus labels in a small table, two balanced replicates per stage, and Visium at three stages. Adopt Endosperm, SC_epidermis, SC_parenchyma, SC_phloem, Em_epidermis and Em_vasculature. Treat the inner seed-coat layers (inner integument, endothelium, hilum vasculature, vascular parenchyma) and the endosperm sub-regions as hypotheses. Re-derive the embryo lineages from `TableS1_embryo_integrated_labels.tsv` plus STM, PLT2, PDF1 and PXY. Re-assign Dividing_cell nuclei to a lineage. Barcodes are `cs1_AAACCCACAACTAGAA` (library prefix = stage + replicate).

## Corrections to the review and conflicts

- **GmSTM paralog Glyma.15G111900:** the review JSON says "spatial de novo HS". In Table S2 it is a snRNA de novo marker of HS Em_initials only, not a spatial marker. Fixed in `basis`.
- **Gy4 Glyma.10G037100:** the review gives "in situ 1989" as validation. Perez-Grau & Goldberg 1989 (abstract) localized KTi3, KTi1/2 and beta-conglycinin, not glycinin, and Table S2 cites only a CRISPR mutagenesis paper (Li et al. 2019 *BMC Res Notes*) for Gy4. Downgraded to `low`.
- **KTi1:** in situ marks the outer cotyledon perimeter in early maturation and is absent from the axis (filed as Cotyledon_Parenchyma, not "Embryo").
- **CG-1:** the 1989 in situ used a beta-conglycinin probe. The CG-1 (alpha') locus assignment rests on Table S2.
- **SWEET naming:** paper names and UniProt names differ (paper GmSWEET15a = UniProt SWEET10; GmSWEET10b = SWEET24; GmSWEET10a = SWEET39; GmSWEET11 = SWEET21). Compare by Glyma ID only. The main text writes SWEET15a as "Glyma05G12200" (typo); Table S2 has Glyma.05G122200.
- **GmSWEET10a Glyma.15G049200:** seed-coat parenchyma in the literature, but the CS Visium 'End micropylar' cluster and late peripheral endosperm in Zhang 2025 (`low`).
- **GmPLT2:** embryo root pole (Fig 2D), but also a Visium de novo marker of the EMS 'SC tracheid bar' spot cluster.
- **GmSWEET11:** SC_phloem in snRNA, but Visium 'SC outer parenchyma' at CS. Ortholog type is "O", not LDO, to AtSWEET11.
- **GmCESA8 Glyma.06G065000:** appears twice in Table S2 under two names. snRNA SC_xylem, but spatially the tracheid bar.
- **GmAPL Glyma.15G263700:** UniProt names it PHR27 (MYB-CC). APL orthology rests on the PANTHER LDO call in Table S2 (`low`).
- **GmZOU:** expected micropylar/ESR from Arabidopsis, but spatially peripheral in soybean.
- **Grading changes vs the review's `selected_markers.tsv`:** TT8 medium -> low (snRNA enrichment only); ZPR3 medium -> low (55 um spot-level, sub-region is a hypothesis); KTi3 kept high (cross-study rule).

## Overlap with existing skill tables

There is no soybean (or other legume) table in `references/markers/`, so no row duplicates an existing one. Homology overlap with the Arabidopsis tables: GmSPCH (Stomatal_lineage, SPCH), GmAPL (Phloem, APL), GmXCP2 (Xylem, XCP2), GmSWEET11 (Phloem_Parenchyma, SWEET11), GmPLT2 (Stem_Cell_Niche, Arabidopsis has PLT1 only), CDC20 (Dividing_cells; Arabidopsis has CYCB1;1/KNOLLE), and GmPDF1 (Arabidopsis leaf Epidermis has ATML1, not PDF1). Seed-coat, endosperm, storage-parenchyma and hilum types have no rows in any skill table.

## Could not verify

- Glyma.17G232205 (GmKNAT1) is a Wm82.a4-only locus: absent from UniProt (taxonomy 3847) and NCBI Gene. Kept as `low`; check it exists in the dataset's annotation.
- Wm82.a2 vs a4 ID identity is assumed for the other loci (UniProt matches a2-style `GLYMA_` names); not checked against the Phytozome a2-a4 crosswalk.
- Primary papers were not re-read beyond Crossref/Europe PMC metadata and abstracts: Wyatt et al. 1992 (PRP1 localization), Gijzen et al. 1997 (Ep in hourglass cells), Wang 2019 and 2020 (SWEETs), Pelletier 2017 (LEC1). Their claims come from the review and Zhang 2025 Table S2.
- Zhang 2025 figures (Fig 2C-F, S4) were not viewed; spatial claims come from the text and Table S2 de novo lists. PMC supplementary links are behind a reCAPTCHA (not bypassed); mmc1/mmc2 came from the Elsevier CDN: https://ars.els-cdn.com/content/image/1-s2.0-S009286742401273X-mmc1.xlsx (Table S1, 41.8 MB, all tissues; URL checked 2026-10-22) and `...-mmc2.xlsx` (PII from `api.crossref.org/works/10.1016/j.cell.2024.10.050`). Table S1 places blocks side by side: snRNA per-nucleus metadata in columns 18-30, endosperm integration in 32-42, embryo integration in 43-67 (skill test H3, 2026-10-22).
- Large objects were not downloaded (per-stage Seurat rds 0.9-1.3 GB, Visium rds 132-381 MB, endosperm iNMF 272 MB, embryo uiNMF 379 MB; listed in `Zhang2025/README.md`).

## Update 2026-10-20: gap-fill reviews

One new review, `Pelletier2025/` (its own README, `selected_markers.tsv`, `uniprot_id_check.txt`, flattened Dataset S4). Paper-only review: no in-data check was run.

### New dataset

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Pelletier JM, Chen M, Lin JY, ... Goldberg RB, Harada JJ. *PNAS* 122:e2416987121 (2025), 10.1073/pnas.2416987121 (Europe PMC confirmed; PMC11725896); GEO GSE243174 (snMultiome), GSE116036 (LCM) | Williams 82: one pooled library of ~50 cotyledon-stage seeds; LCM of 41 subregions (globular, heart, cotyledon, early maturation) | 10x Multiome v1 (only snRNA analysed) + LCM RNA-seq + HCR RNA-FISH | 8,636 nuclei, 23 clusters (embryo 1,055, endosperm 1,053, seed coat 5,988, unassigned 496) | Wm82.a2.v1 (Gmax_275) | cluster_only (no per-nucleus labels; one library, no replicate) | medium |

**Independence from Zhang 2025.** The two studies come from different labs (Harada/Goldberg vs Schmitz) and have separate nuclei libraries, so gene-level agreement counts as cross-study support. One caveat: Zhang 2025 named its SC_inner_integument and SC_endothelium clusters only by correlation with the Goldberg/Harada LCM data (GSE57349/57350/57606/46906), and Pelletier names sn14 and sn9 from the same lab's LCM. The two endothelium and inner-integument labels therefore share their reference. Agreement on these two layers was used to raise confidence only for genes that are themselves LCM subregion-specific (the per-gene "Subregion Specifics" flags in Dataset S4 or the TF lists in Fig S6).

**Gene IDs.** Pelletier IDs are Wm82.a2.v1. The same ID strings were found in the Zhang 2025 Wm82.a4 count tables (checked during collation against the gene lists of the CS and GS count tables, 32,180 IDs) for 42 of the 43 selected genes (the review reported 39 of 43). The exception is GmWOX9 Glyma.11G210800, which is flagged in `alt_id` and `basis`. Finding the same string does not prove that the a2 and a4 gene models match. This was not checked against a Phytozome crosswalk.

### Verdicts (Pelletier 2025, mapped to the expected types)

| Expected type | Pelletier 2025 | Zhang 2025 (from above) |
|---|---|---|
| Seed_Coat_Epidermis | A (sn3/sn7/sn13/sn20 as one type; LCM SC-EPD, GL2, MYB5, TTG2, PRP1; sub-identities type vs state unresolved, sn20 maybe a maturing state) | A |
| Hourglass_Cell | R (sn5b, 34 markers, weak LCM em SC-HG; hypothesis) | - |
| Seed_Coat_Parenchyma | A (sn0 thick-walled parenchyma, SCS1); R (sn1, unresolved); R (sn5a/sn19 transitional, not a type) | A |
| Inner_Integument | A (sn14; LCM SC-II; no in situ) | R |
| Endothelium | A (sn9; LCM SC-ENT, TT16 highest; no in situ) | R |
| Hilum (umbrella, new row) / Hilum_Parenchyma | R (sn16 = mixed hilum: TGA10/bZIP65, LRP1, auxin genes; not parenchyma-specific) | R |
| Phloem | R (sn6a, SE/CC-like: GSL7/GSL4 callose synthases, bZIP9) | A |
| Phloem_Parenchyma / Seed_Coat_Vasculature (new umbrella row) | R (sn6b: bZIP9, SWEET11/13, vascular GRP; the 6a/6b split is a subcluster call) | A |
| Endosperm | R (sn12: no unique markers; transitional or chalazal, test in data) | A |
| Aleurone | **A (sn10, HCR-validated)**. First label for this type; marker IDs are expression-level because the HCR probe IDs are not published | - |
| Peripheral_Endosperm (+ Micropylar/ESR) | R (sn11, HCR; ESR and peripheral merged) | R |
| Chalazal_Endosperm | - (not addressed; LCM ES not split) | R |
| Suspensor | LCM SUS adopted as a population reference (no snRNA cluster) | - |
| Embryo | R (sn2, 39 markers; axis and cotyledon merged) | R |
| Protoderm | A (sn18; includes the suspensor outer layer) | A |
| Dividing_cells | **R: sn15 is labeled "embryo proper" in the paper but is a G2/M state** (CYCB1;2/1;4, CDC20.1, TPX2, CDKB2;2) | R |
| (mixed / unassigned) | X (sn4 mixed/doublet-like; sn17 unclear; sn8 unassigned, ambient) | X |
| LCM ES | R (one population per stage: does not fill the endosperm sub-region gaps) | |

### Markers added and raised

`markers_draft.tsv` now has 70 rows (35 new; 22 function, 33 characterized_enriched, 15 expression; 12 high, 33 medium, 25 low). No gene ID appears twice. All 43 Pelletier markers are now in the draft: 35 as new rows and 8 merged into existing rows by gene ID.

New rows by type: Aleurone 3 (2S albumin/LTP-like, knottin/defensin-like, AIL7); Peripheral_Endosperm 3 (SCPL51, WAT1-related, galactosyltransferase); Endosperm 2 (HDG11, AGL62); Suspensor 3 (WOX9, ERF019-like, WOX9 paralog); Protoderm 3 (PDF1-2, CER1, LTP1); Stomatal_lineage 1 (SPCH1 Glyma.04G238400, Danzer 2015 RNAi); Cotyledon_Parenchyma 1 (YAB1, abaxial domain only); Dividing_cells 1 (CYCB1;4); Seed_Coat_Parenchyma 2 (SCS1, SCB1); Phloem 2 (GSL7, bZIP9-2); Seed_Coat_Vasculature 1 (GRP); Inner_Integument 3 (BGAL6/MUM2, O-FucT, ANAC087); Endothelium 5 (TT16, AGL6, CYP86B1, LOX, JKD); Hilum 1 (TGA10/bZIP65); Hourglass_Cell 1 (KAN2); Seed_Coat_Epidermis 3 (TTG2, MYB5, GL2).

Confidence raised one level on existing rows. In each case the second study is Pelletier 2025 and the first is Zhang 2025 or the literature already cited in the row:

| Gene | Type | Change | Why |
|---|---|---|---|
| GmSWEET15b Glyma.08G077200 | Endosperm | medium -> high | Wang 2019 + Pelletier sn11 (pct 0.85 vs 0.10) |
| GmCYP78A57 Glyma.02G119600 | Embryo | medium -> high | Zhang Visium + snRNA; Pelletier sn2/sn18 |
| GmPDF1 Glyma.18G106400 | Protoderm | medium -> high | Zhang Visium; Pelletier sn18 |
| GmLTPG1 Glyma.18G005800 | Protoderm | low -> medium | Zhang snRNA; Pelletier sn18 + LCM SUS |
| GmBZIP9 Glyma.17G188500 | Phloem | low -> medium | Zhang SC_phloem; Pelletier sn6a/6b |
| GmSWEET11 Glyma.08G010000 | Phloem_Parenchyma | medium -> high | Zhang snRNA + Visium; Pelletier sn6b (the Zhang CS Visium outer-parenchyma conflict is kept in basis) |
| GmPRP1 Glyma.09G092700 | Seed_Coat_Epidermis | medium -> high | Wyatt 1992 + Pelletier top sn7 marker + LCM SC-EPD |
| GmTT8 Glyma.10G026000 | Seed_Coat_Epidermis | low -> medium | Zhang SC_epidermis; Pelletier sn3/7/13/20 (broad background in both) |

**Corrected row:** GmZOU Glyma.02G103200 moved from Endosperm (characterized_enriched, low) to Peripheral_Endosperm (function, medium). Zhang Visium (peripheral) and Pelletier sn11 (HCR-validated embryo-surrounding + peripheral endosperm) agree. Arabidopsis function: Yang et al. 2008 *Development*.

**Notes added without a grade change:** SWEET15a and KTi3 (already high; Pelletier sn11 and sn2 support); CDC20 x2 (sn15); SWEET10b (Dataset S4 lists only sn17); Glyma.19G062000 (Pelletier calls it MYB98, LCM ES-specific but ES not split, so chalazal still unsupported); and three conflicts listed below (F3'H, Ep, CESA8).

**Collation grades that differ from the review's `selected_markers.tsv`:** SCS1 high -> medium (broad in Zhang SC parenchyma, pct2 0.68-0.89); SCB1 medium -> low (broad in both, pct2 0.55 and 0.88); CYP86B1 medium -> low (no LCM SC-ENT flag, and the endothelium labels share the LCM reference); JKD low -> medium (LCM ENT-specific plus the endothelium cluster in both datasets); PDF1-2 medium -> high (Zhang Visium pct 0.86 + Pelletier sn18). `requires=eudicot` was added to the new seed-coat epidermis and parenchyma rows, and `requires=Fabaceae` to the hilum and hourglass rows, matching the existing rows.

**Characterized-marker table:** `survey/characterization/characterized_markers.tsv` has 11 rows tagged `soybean_seed:`. All are Arabidopsis or maize genes mapped by homology (TT16, BAN, TT12, ATS, ZOU, FH5, AGL62, WOX8, LEC1, STM, KN1), so none matches a soybean ID directly. Three are orthologs of draft genes and are cited as homology support in `basis`: AtTT16 for GmTT16, AtAGL62 for GmAGL62, and AtWOX8/9 for GmWOX9. ZOU, LEC1 and STM were already cited. No confidence was raised on homology alone.

### Gaps closed

- **Aleurone:** a validated label now exists (Pelletier sn10, HCR), but the markers are expression-level only.
- **Inner_Integument** and **Endothelium:** 3 and 5 markers at medium (low for CYP86B1), from two snRNA datasets plus LCM. TT16 is a function marker. The caveat is that both labels rest on the same LCM reference.
- **Peripheral_Endosperm:** ZOU (function, medium) plus 3 cross-study expression markers at medium.
- **Suspensor:** partly closed. There are 3 low LCM-only rows; one of them (WOX9) has an a4 ID that could not be confirmed, and one (the WOX9 paralog) conflicts with Zhang.
- **Seed_Coat_Parenchyma, Seed_Coat_Epidermis, Protoderm, Phloem, Endosperm, Embryo:** reinforced.

### Gaps remaining

- **Micropylar_Endosperm** and **Chalazal_Endosperm:** still only low expression rows. Pelletier merges ESR into sn11 and its LCM endosperm is not split.
- **Hourglass_Cell:** Ep (literature) and KAN2 (weak sn5b) only. **Hilum_Parenchyma:** F3'H, which now conflicts. **Tracheid_Bar:** none (CESA8 under Xylem).
- **Aleurone:** no function or characterized marker, and the HCR probe genes are unknown.
- **Embryonic_Axis, Quiescent_Center, Root_Cap:** none. **Cotyledon_Parenchyma:** storage-protein rows plus YAB1 (abaxial only). **Phloem_Companion, Sieve_Element:** none.
- **Next search target:** Pelletier Dataset S2 (subregion-specific mRNAs for SUS, em AX-SAM/PL/RT, SC-HG, SC-HI and the other subregions, 15.1 MB xlsx inside the 95 MB Europe PMC supplement zip). It was not read and should cover axis, SAM, hourglass and hilum.

### Conflicts

- **Glyma.10G069700 (WOX9 paralog):** LCM suspensor-specific in Pelletier, but SC hilum vasculature (snRNA, GS) and tracheid bar (Visium, EMS) in Zhang. Kept low; do not use it in seed-coat data.
- **Glyma.02G179500 (AIL7):** Pelletier sn10 aleurone vs Zhang End micropylar (CS) / Endosperm (EMS).
- **BGAL6, O-FucT, ANAC087:** SC inner integument in Zhang at GS/HS, but DE in Zhang **Emb epidermis** at CS. Pelletier puts them in sn14 (inner integument) at CS. Either Zhang's CS label is wrong or the genes are shared with the embryo epidermis; check in data.
- **F3'H Glyma.06G202300 (Hilum_Parenchyma row):** Pelletier puts it in the seed-coat epidermis clusters (sn3/4/7/13, pct 0.82-0.94 vs 0.27), not the hilum cluster sn16.
- **Ep peroxidase Glyma.09G022300 (Hourglass_Cell row):** Pelletier sn1/sn6b (LCM cotSC-OI), not sn5b ("hourglass"). Its hourglass placement rests only on Gijzen 1997.
- **GmSPCH:** Pelletier uses Glyma.04G238400 (UniProt SPCH1, Zhang Visium Emb epidermis EMS); the draft also has Glyma.06G125500 (SPCH2). Both are kept.
- **Names:** Glyma.08G010000 = GmSWEET11 (Zhang) = SWEET13 (Pelletier TAIR hit) = SWEET21 (UniProt). Glyma.19G062000 = "AT5G40430-like" (Zhang) = MYB98 (Pelletier). Compare by ID.
- **Paper labels to correct when reusing Pelletier:** sn15 "embryo proper" is Dividing_cells (a state); sn11 is ESR + peripheral endosperm, not one region; sn16 is not hilum parenchyma.

### Recommended label reference (revised)

Zhang 2025 stays the main label reference: it has per-nucleus labels, four stages and replicates, and Pelletier has no per-nucleus labels. Use Pelletier 2025 as the second reference where it is stronger:
- **Aleurone** (sn10) and **embryo-surrounding + peripheral endosperm** (sn11): HCR-validated. To transfer them, re-cluster the GSE243174 SoupX matrix (92 MB, not downloaded) or score sn10/sn11 markers in the target data.
- **Inner_Integument** (sn14) and **Endothelium** (sn9) at cotyledon stage. Together with Zhang, these layers can move from hypothesis to Revise/Adopt, with the shared-LCM caveat.
- **LCM subregion profiles** (SUS, SC-II, SC-ENT, SC-HI, SC-EPD, em SC-HG/PY/PS, em AX/COT subregions) as population-level references for correlation.

### Could not verify (this update)

- HCR probe Glyma IDs (sn10_08G, sn11_02G, sn11_12G) are not published. The three candidate genes are named INFERRED in `basis`.
- Wm82.a2-to-a4 identity is inferred from matching ID strings. Glyma.11G210800 is absent from the Zhang a4 tables.
- Pelletier Datasets S1, S2 and S5 were not read. The Europe PMC supplement zip is 95 MB, and the PNAS supplement page is behind a Cloudflare challenge, which was not bypassed. Large GEO objects were not downloaded: GSE243174 h5 (128 MB), the SoupX matrix (92 MB), ATAC fragments (1.3 GB) and GSE116036_RAW.tar (35 MB).
- Batchelor 2000/2002, Ye & Varner 1991, Danzer 2015, Nesi 2002, Kang 2008 and Yang 2008: DOIs confirmed in Europe PMC; localization claims come from the review and Pelletier, not from re-reading the papers.
