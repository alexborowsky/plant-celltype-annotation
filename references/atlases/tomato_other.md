<!-- Collated from the survey review of tomato_other (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# tomato_other: tomato callus (shoot regeneration) marker collation

Collated 2026-10-20 for the plant-celltype-annotation skill (Part A + Step 4). One dataset is in this group, Song et al. 2023 (tomato cotyledon callus). Its review is in `Song2023/README.md` and was left unchanged. To check agreement across studies, markers were compared by gene ID with the other tomato reviews in this resources folder (`tomato_seedling/Huang2026`, `tomato_root/CantoPastor2024`, `tomato_root/Kajala2021`).

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 27 cell types/states expected in cotyledon callus at 16 d on shoot-induction medium. Built from callus and regeneration anatomy; marker counts were filled in after the table was built. |
| `markers_draft.tsv` | 53 rows (45 before the 2026-10-20 update, see the end of this file) in the skill schema plus `alt_id`. `ref_species=tomato` and `tissue=callus` (`callus` is not yet in the skill's tissue vocabulary). The IDs are SL4.0/ITAG4.x `Solyc` loci with no version suffix. `alt_id` holds the UniProt accession and, where known, the Arabidopsis homolog. |
| `Song2023/` | The dataset review, supplementary files and full text, all from the earlier review. |

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Song2023 (this group) | Song X, ... Deng XW, Li B (2023) *PNAS* 120:e2310163120, doi:10.1073/pnas.2310163120. Raw data: CNGB CNP0003986 | Micro-Tom cotyledon callus, 16 d SIM. (i) Stereo-seq cell bins; (ii) BMK S1000 50 µm spots; (iii) 10x Visium; (iv) 10x 3' v3.1 snRNA. One callus per platform (n=1). | i: 28,036 or 6,759 cells (the paper gives both); ii: 3,511 spots; iii: 2,051 spots; iv: 17,214 nuclei, 22 clusters, 8 Undefined | cluster_only: the cluster→type map is in figure legends only. Dataset S1 has per-cluster DE. No per-cell labels and no processed object; raw FASTQ only. | medium |
| Huang2026 (cross-check only; group `tomato_seedling`) | Huang W et al. (2026) *Hortic Res* 13:uhag044, doi:10.1093/hr/uhag044 | DNBelab C4 snRNA, etiolated hook + hypocotyl | 117,929 nuclei | cluster tables only | see its README |
| Canto-Pastor2024 (cross-check only; `tomato_root`) | Canto-Pastor A et al. (2024) *Nat Plants*, doi:10.1038/s41477-023-01567-x | root scRNA | see its README | GEO | medium |
| Kajala2021 (cross-check only; `tomato_root`) | Kajala K et al. (2021) *Cell* 184:3333, doi:10.1016/j.cell.2021.04.024 | root TRAP-seq + reporters | – | – | – |

Other primary sources for gene IDs: Seo et al. 2024 (PMC11197305; SlCLV3 Solyc11g071380), Thomas et al. 2022 *Plant Physiol* (PMC8846177; SlWOX4 Solyc04g078650, PXY Solyc05g051640), Capua & Eshed 2017 *Development* (PMC5373412; LEAFLESS Solyc05g013540), Hendelman et al. 2013 (PMC3871814; GOBLET Solyc07g062840).

## Verdict matrix (Song 2023 labels vs the canonical names)

The Song 2023 label for each cell type is shown with the clusters it covers on each platform. A dash means no such label or cluster.

| Canonical type | Stereo-seq (i) | S1000 (ii) | Visium (iii) | snRNA (iv) | Verdict |
|---|---|---|---|---|---|
| Shoot_Meristem (progenitor) | "Shoot primordia" 5,6 (5 = surface band with PI-II; 6 has no meristem genes) | "Shoot primordia" 1; subtype 2 | 1 | 9 | **Revise**: core supported (STM in situ; STM/GOB/AIL6/KLUH DE on 3 platforms), but ~13% is too large and i:5/i:6 are doubtful |
| Lateral_Organ_Primordium | – | primordia subtype 3 | – | – | Revise (GO only) |
| Dividing_cells / S_Phase | – | primordia subtype 1 (G2/M GO) | – | **Undefined 18, 16 (G2/M), 20 (S)** | Revise: a state labelled as a type in ii; correctly left unassigned in iv (new here) |
| Epidermis | "Epidermis" 1 (air side) | 4 (air side) | 0,10 | 5 | **Adopt** for the air-side clusters (ATML1 in situ; ML1, PDF1-like) |
| Hypoxia_Stress (state) | – | "Epidermis" 6,7 | – | "Epidermis" 1, 11 | **Revise**: medium-contact hypoxia/wound state, not epidermis |
| Suberized_Surface | – | – | – | **Undefined 21** | New: full suberin program (ASFT, LACS4, GPAT5, MYB92, FAR3A, LTPG5; 0.5–0.9 vs ≤0.01) |
| Procambium | "Vascular" 4 (mixed) | "Vascular" 2 | 2,3,4 | 6 | **Adopt** iv:6 (WOX4, PXY, REV, PHB DE by ID); spatial clusters Revise (merged) |
| Xylem | – | "Vascular" 8 | 3 | 19 | **Adopt** iv:19 and ii:8 (3 SCW CESAs, VND6, VND2, XCP1/2) |
| Sieve_Element / Phloem | "Vascular" 4 (SEOa/b, PP2-A9) | 2 | 4 | 15 (SEO), 8 (APL, PP2, HMA, but also SKOR/PHO1) | **Revise**: iv:15 = SE lineage (good); iv:8 is phloem with xylem-parenchyma loading genes, unresolved |
| "Phloem-like" (Phloem_Parenchyma?) | – | – | – | 3, 14 | **Revise**: iv:3 has SWEETs, callose synthase, ABCG14 (Solyc08g005580) and STM; iv:14 is weak. WOL/HK4 (Solyc04g008110) is only 0.63 vs 0.38 |
| Callus_Parenchyma | "Inner callus" 0,3 | 0,3,5 | 5,6,8,9 | 4,10,12 | **Revise**: catch-all defined by exclusion |
| Mesophyll / Chlorenchyma | "Outgrowth shoot" 2 | 9 | 7,11 | 7 | **Revise**: organ-level bin called from photosynthesis genes; chlorenchyma is a module, not a cluster |
| Wound_Defense (state) | – | – | – | Undefined 13 (PR1, LTPs, peroxidases) | new, state |
| Unresolved | – | – | – | Undefined 0 (12 DE genes), 2, 17 (MYB48/MYB58, sulfate transporter: maybe xylem parenchyma) | – |

## Cross-study markers (same gene ID in independent tomato studies)

16 rows are supported by at least two independent studies. Confidence was raised where at least one study validated the gene (reporter, mutant, overexpression or cell-resolution Stereo-seq) or where the gene was cluster-specific in two studies.

| Gene | Symbol | Cell type | Studies | Effect |
|---|---|---|---|---|
| Solyc03g097500 | SlASFT | Suberized_Surface | Canto-Pastor (reporter + CRISPR) + Song iv:21 0.82/0.008 | function high |
| Solyc01g095750 | SlLACS4 | Suberized_Surface | Canto-Pastor (CRISPR) + Song iv:21 | medium → high |
| Solyc04g011600 | SlGPAT5 | Suberized_Surface | Canto-Pastor (CRISPR) + Song iv:21 | medium → high |
| Solyc05g051550 | SlMYB92 | Suberized_Surface | Canto-Pastor (CRISPR) + Song iv:21 | medium → high |
| Solyc06g074390 | SlFAR3A | Suberized_Surface | Canto-Pastor + Song iv:21 | low → medium |
| Solyc09g065420 | SlLTPG5 | Suberized_Surface | Canto-Pastor + Song iv:21 | expression, medium |
| Solyc09g083050 | SlKCS2a | Suberized_Surface | Canto-Pastor + Song + Huang | low → medium |
| Solyc01g094700 | SlGPAT4 | Suberized_Surface | Canto-Pastor + Song + Huang | not raised (also in cutin epidermis) |
| Solyc03g111810 | SlSEOa | Sieve_Element | Song (Stereo-seq i:4, snRNA iv:15) + Huang (0.66/0.03) | medium → high |
| Solyc05g013850 | SlSEOb | Sieve_Element | Song (all 4 platforms) + Huang (0.55/0.01) | medium → high |
| Solyc02g031740 | PP2-A9-like | Phloem | Song i:4, iv:8, iv:15 + Huang | low → medium |
| Solyc10g085910 | HMA protein | Phloem | Song iv:8 0.83/0.13 + Huang | expression, medium |
| Solyc06g034340 | SlVND6 | Xylem | Kajala (OE → ectopic SCW) + Song iv:19 | medium → high |
| Solyc03g096870 | CDC20.2 | Dividing_cells | Song iv:18 + Huang hook G2/M | function high |
| Solyc04g082430 | CycB2;4 | Dividing_cells | Song iv:18 + Huang | function high |
| Solyc01g099410 | H2A.1 | S_Phase | Song iv:20 + Huang | low → medium |

Studies that agree only on DE, or only on unvalidated dotplot claims, were noted in `basis` but did not raise confidence. These are ML1, PHB, CAD, APL, the CESAs, XCP2, VND2 and UXS6.

The suberin agreement spans organs: root exodermis in Canto-Pastor, and a callus cluster the authors left unassigned in Song. It supports a suberizing-cell identity, not exodermis.

## Gaps (expected types with no `function` marker in the draft)

Callus_Parenchyma, Callus_Middle_Layer (the pluripotent WOX5/PLT/SCR layer of Zhai & Xu 2021), Mesophyll, Chlorenchyma, Guard, Stomatal_lineage, Glandular_Trichome, Trichome, Xylem_Parenchyma, Phloem_Companion, Phloem_Parenchyma, Root_Primordium, S_Phase (it has a `characterized_enriched` row only), Hypoxia_Stress and Wound_Defense (both states).

Epidermis, Organizing_Center, SAM_Central_Zone, Organ_Boundary, Lateral_Organ_Primordium and Phloem each have only one `function` marker. For Guard, Stomatal_lineage, Phloem_Companion and Phloem_Parenchyma, use `arabidopsis_leaf.tsv` via homology.

## Recommended label reference

The only option is **Song 2023 snRNA (sample iv)**, at the cluster level, and only for the types adopted above:
- procambium iv:6
- xylem iv:19
- SE lineage iv:15
- air-side epidermis iv:5
- primordia core iv:9
- the reinterpreted Undefined clusters 16, 18, 20 and 21

No per-cell labels exist, so the labels must be re-derived from the CNGB raw reads and matched by markers. The Stereo-seq sample (i) is the only cell-resolution spatial reference: use it to check positions (vascular i:4, outgrowth shoot i:2), not as labels.

## Conflicts and corrections to the earlier review

- **The snRNA Undefined clusters can be resolved.** iv:18 is G2/M (CDC20 ×2, CycB2;4, MAD2), iv:16 is G2/M or mitotic (kinesins, TOP2, cyclin A1, POK1), iv:20 is S phase (histones only), iv:21 is suberizing cells, and iv:13 is a defense/wound state. Leaving them unassigned was good practice, but they are interpretable.
- **IDs the review lacked were found in primary tables.** SlWOL/HK4 is Solyc04g008110 (Song Dataset S3). SlWOX4 is Solyc04g078650 and PXY is Solyc05g051640 (Thomas 2022 tables). Both of the latter are DE in snRNA procambium iv:6, which confirms that call. SlCLV3 is Solyc11g071380 (Seo 2024). APL is Solyc12g017370 (Kajala/Canto-Pastor); it is DE in iv:8 (0.21/0.007), as the review stated from the figure.
- **SlABCG14a candidate.** Solyc05g056470 (the review's candidate) is DE only in primordia ii:1. Another ABCG14, Solyc08g005580 (ITAG "ABC transporter G family member 14"), is DE in the vascular clusters ii:2, iii:4, iv:3 and iv:8. It fits the vascular in situ better, but the paper gives no ID, so neither gene is in the table.
- **STM is also DE in "phloem-like" iv:3 (0.26/0.08).** STM is not specific to progenitors in this callus.
- **GOB vs "SlCUC1".** Song figures label Solyc07g062840 as SlCUC1, but Dataset S3, Hendelman 2013 and UniProt (NAM) all give GOBLET/CUC2.
- **Solyc05g051380 (AIL6/PLT3-like)** is a shoot-progenitor marker here and a root stem-cell-niche/root-cap marker in Canto-Pastor 2024. This is consistent with PLT expression in meristems: treat it as meristem-general.
- **SlGPAT4 and SlKCS2a** are DE in both the air-side epidermis (cutin) and iv:21 (suberin). Huang 2026 labelled the same signature "exodermis-like" in hypocotyl. These genes alone cannot separate cuticle epidermis from suberized cells; use ASFT, GPAT5 and MYB92 for the latter.
- **Duplicate ID in a source.** Thomas 2022 gives one ID (Solyc04g081235) for both MP and ATHB8, so neither was used.
- **Sample-i cell number.** Song reports both 28,036 and 6,759 cells (Results vs Methods). This is unresolved.

## Overlap with existing skill tables

The skill has no tomato (or other Solanaceae) table, so no rows overlap. The draft uses the same cell-type names as `arabidopsis_leaf.tsv`, `arabidopsis_root.tsv` and the `arabidopsis_shoot_apex` draft (Shoot_Meristem, SAM_Central_Zone, Organizing_Center, Organ_Boundary, Lateral_Organ_Primordium, Epidermis, Procambium, Xylem, Phloem, Sieve_Element, Dividing_cells, S_Phase).

Three names are new:
- `Suberized_Surface`
- `Chlorenchyma`
- `Hypoxia_Stress` (state)

Several Arabidopsis homologs of rows here are already in the skill tables (STM, WUS, CLV3, ATML1/PDF2, APL, WOX4, PXY, CDC20, CYCB). The Solyc IDs in this draft let tomato data use `--no-blast` instead of homology for those genes.

## Could not verify

- Gene IDs for the paper's in situ genes SlATML1, SlPI51, SlABCG14a/b and SlPDF1. The SlPI51 row uses an inferred ID (the top DE gene of i:5) and is graded `low`.
- Which secondary-wall CESA each of Solyc02g072240, Solyc09g072820 and Solyc07g005840 is (IRX1/IRX5 symbols come from Huang 2026 and were not verified). VND2/ANAC076 and PXY orthology was not verified either.
- SlSEOa (Solyc03g111810), SlVND2 (Solyc02g084350) and SlLACS4 (Solyc01g095750) have no UniProt entry; they were confirmed in ITAG4.0 descriptions only. All other draft IDs were confirmed in UniProt (taxon 4081) on 2026-10-20.
- The CNGB CNP0003986 file list and sizes, and the authors' server www.lilabpku-iaas.com. Neither was reachable during the earlier review, and I did not retry.
- Tomato in situ papers for WUS and CLV3 in the SAM. These rows rest on Arabidopsis function, the tomato IDs and Song's spatial maps, so they are graded `medium`.
- None of the marker calls were checked against expression data. All DE numbers are pct.1/pct.2 from Song Dataset S1 (`Song2023/supp/pnas.2310163120.sd01.xlsx`).

## Update 2026-10-20: gap-fill reviews

One new review was merged: **Song2026** (review in `Song2026/README.md`, unchanged). After the update, `markers_draft.tsv` has 53 rows (was 45), with the same 13 columns and ID convention (`ref_gene` = SL4.0/ITAG4 Solyc locus without version; `alt_id` = UniProt and Arabidopsis homolog). `expected_cell_types.tsv` function counts and notes were updated.

### New dataset

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Song2026 | Song X, Zhang S, ... Deng XW, Li B (2026) *Mol Plant* (cover date 6 July 2026), doi:10.1016/j.molp.2026.05.008, PMID 42141722 (confirmed in Europe PMC). Preprint bioRxiv 10.64898/2026.02.20.705279 v1. Same lab and callus system as Song2023 (Micro-Tom cotyledon on SIM), 0-16 DPE time course, plus *epfl8b*, *dcl2b/d* and *pin2* mutant sections. | Stereo-seq V1 and BMK S1000/S3000 (60 sections, segmented cells), 10x Xenium (41 sections, 50-gene panel), snRNA-seq (10x, BMK DG1000), ISSeq smFISH, bulk RNA-seq | 1.16 M in the paper; public integrated UMAP downsample 102,468 | large_object / partial: portal `umap/spatial_RNA-seq/clusters.json` (16 MB) has the 9 labels but sample names only, no cell IDs; per-section files have cell IDs with unnamed numeric clusters. No raw-data accession in the accessible text. | medium |

### Verdicts (Song2026 labels)

| Label | n (%) | Verdict | Canonical name here |
|---|---|---|---|
| UEC (upper epidermis) | 8,302 (8.1) | Adopt | Epidermis |
| UEC subtypes (WUS+, procuticle, young, late) | – | Revise | Epidermis states; WUS+ = transient pluripotency state |
| LEC (lower, medium-contact epidermis) | 7,515 (7.3) | Revise | Hypoxia_Stress (medium-contact state); 37% from mutant sections |
| SCN (stem-cell niche) | 27,169 (26.5) | Revise | Shoot_Meristem core plus proliferating callus; too large, label transfer, 56% from one batch of sections |
| SCN subtypes: WUS+ core / PLT3a+ inner / CUC2+ shell | – | Adopt (provisional) | Organizing_Center + SAM_Central_Zone (core), Shoot_Meristem (inner), Organ_Boundary (shell); de novo niche sublayers, not mature SAM zones |
| HNC (hypoxic niche cells) | 3,247 (3.2) | Revise | Hypoxia_Stress (state); 51% from mutant sections |
| HCC / LCC (higher / lower chlorenchyma) | 11,937 (11.7) / 16,722 (16.3) | Revise | Chlorenchyma (state); LCC is probably Callus_Parenchyma |
| CAC (cambium) | 19,109 (18.6) | Revise | Procambium plus vascular-derived callus |
| Vascular subtype: mitotically active | – | Revise | Dividing_cells (state) |
| Vascular subtype: procambium | – | Adopt (provisional) | Procambium (WOX4, CLE3) |
| PHC (phloem) incl. PIN1+ / LAX4+ | 8,407 (8.2) | Revise | Phloem (SE/CC/PP not resolved) |
| XYC (xylem) | 60 (0.06) | Revise | Xylem (type real, per-cell label unreliable) |

Every cell was assigned by Seurat label transfer (no unknown class), and mutant sections are mixed into the integrated atlas. Exclude mutants before using these labels as a WT reference.

### Markers raised

Song2026 is from the same lab and callus system as Song2023, but it is a new dataset (new sections, Xenium imaging at cell resolution), so it was counted as an independent study. The Xenium panel gives symbols only. The panel table with IDs (Supplemental Data 3) is behind a Cloudflare check, so every Song2026 symbol-to-ID link comes from Song 2023 Dataset S3 or a UniProt entry with an Ensembl Plants Solyc cross-reference (checked 2026-10-20). Rows were raised only when the tomato symbol is unambiguous (single gene).

| Gene | Symbol | Cell type | Change | Basis |
|---|---|---|---|---|
| Solyc02g083950 | SlWUS | Organizing_Center | medium → high | Xenium SCN core (Song2026) + Song2023 module/spatial maps; UniProt A0A3Q7F7V4 → Solyc02g083950 |
| Solyc11g071380 | SlCLV3 | SAM_Central_Zone | medium → high | Xenium SCN core marker (Song2026 Fig 2H); UniProt K4DAJ5 → Solyc11g071380; ID also from Seo 2024 |

Already high, with Song2026 support added to `basis`: STM (Solyc02g081120, inner compartment) and GOB/CUC2 (Solyc07g062840, shell; Song2026 calls it CUC2, which settles the 2023 figure label "SlCUC1").

Support noted but **not raised** because the paralog or ID link is unresolved: AIL6/PLT3-like Solyc05g051380 and Solyc11g010710 (panel has PLT3a and PLT3b), ML1 Solyc10g005330 (ATML1), PDF1-like Solyc07g055950, PXY Solyc05g051640 (panel PXYa), and WOX4 Solyc04g078650 (spatial DE only). ADH2 (Hypoxia_Stress) and LHCA2 (Chlorenchyma) got notes on the HNC and HCC/LCC labels.

### Markers added (8)

| Gene | Symbol | Cell type | evidence / confidence | Source |
|---|---|---|---|---|
| Solyc04g081590 | SlCLV1 (FAB) | Shoot_Meristem | function / medium | Song2026 Xenium inner compartment; UniProt A0A3Q7GAM8 (gene CLV1) → Solyc04g081590 |
| Solyc09g066270 | SBRL | Root_Primordium | function / high | Omary et al. 2022 Science (characterization survey) |
| Solyc01g105890 | TPS5/MTS1 | Glandular_Trichome | function / high | Spyropoulou 2014 (survey) |
| Solyc02g062400 | EOT1 | Glandular_Trichome | characterized_enriched / medium | Spyropoulou 2014 (survey) |
| Solyc08g005050 | SlMYC1 | Glandular_Trichome | function / medium | Xu 2018 Plant Cell (survey) |
| Solyc08g005680 | NDPS1/CPT1 | Glandular_Trichome | function / medium | Schilmiller 2009 PNAS (survey) |
| Solyc02g080260 | Wo | Trichome | function / medium | Yang 2011 PNAS (survey) |
| Solyc10g078970 | H | Trichome | function / medium | Chang 2018 Plant J (survey) |

The seven survey rows come from `survey/characterization/characterized_markers.tsv` (rows whose `gaps_filled` name `tomato_other:`). Their IDs and DOIs were checked by the survey agent. They were characterized in leaf, stem or hypocotyl, not in callus, so they apply to organs regenerated on callus. No survey row matched an existing draft ID, so none of them raised an existing row. The Arabidopsis survey rows for this group (SUC2, SWEET11/12, SKOR, NRT1.8, HKT1, SPCH, MUTE, FAMA, SLAC1, LBD16, WOX11) were not copied in; use them via homology.

Song2026 markers with no ID were not added: EPFL8b, ERb, ERL1 (SCN shell / plastic compartment), MP/ARF5, VND7b, CYCB1;2, MYB3R-4, E2Fa/E2Fb, CYCD3;1, WIND1, PI-2, CLE3, and the phloem transporters (PIN1, LAX4, AZG2, BOU, BAT1, AAP6, PROT1, SWEET1, SUT1). Add them once Supplemental Data 3 gives the IDs. ABCG14a was not added either: Song2026 puts it in the vasculature, but whether it is Solyc05g056470 or Solyc08g005580 is still open (see Conflicts above).

### Gaps

Closed (now have at least one `function` row): **Glandular_Trichome** (3), **Trichome** (2), **Root_Primordium** (1). These come from the characterization survey, not from Song2026.

Claimed by the Song2026 gap search but **not closed**:
- Chlorenchyma: HCC/LCC labels exist, but the only markers are photosynthesis genes, with no IDs.
- Hypoxia_Stress: an HNC state label exists, but no genes are named and the cells are mostly from mutants.
- The stomatal claim is wrong: EPFL8b/ER/ERL1 act in SCN organization here, not in the stomatal lineage.

Remaining gaps: Callus_Parenchyma (LCC is a label but has no marker), Callus_Middle_Layer (the SCN "plastic compartment" is not the Zhai & Xu middle layer), Mesophyll, Chlorenchyma, Guard, Stomatal_lineage, Xylem_Parenchyma, Phloem_Companion, Phloem_Parenchyma (for these five, use the Arabidopsis survey/core rows via homology), S_Phase, Hypoxia_Stress and Wound_Defense. Organizing_Center, SAM_Central_Zone, Organ_Boundary, Lateral_Organ_Primordium, Phloem and Root_Primordium still have only one `function` row each.

### Recommended label reference

Unchanged: **Song 2023 snRNA (sample iv)**, at the cluster level, for the adopted types. Song2026 does not replace it. Its per-cell labels were transferred to every cell, include mutants, and cannot be linked to cell IDs. Use Song2026 Xenium for one thing only: as the positional reference for SCN sublayers (CLV3/WUS core, STM/CLV1/PLT3a inner, CUC2/EPFL8b shell) and for the UEC vs LEC surface.

### Conflicts

- **SCN size.** The SCN bin (26.5%) holds far more than a niche. It likely includes proliferating callus (the paper reports proliferation-pathway enrichment) and is batch-skewed. Do not use SCN-wide DE genes as Shoot_Meristem markers.
- **WUS outside the core.** WUS+ cells also appear in the upper epidermis (as a transient state) and in early wound/vascular zones. The raised WUS row needs core context.
- **GOB name.** Song2026 calls Solyc07g062840 CUC2. That agrees with Song 2023 Dataset S3, Hendelman 2013 and UniProt, against the 2023 figure label SlCUC1.
- **Paralog suffixes.** PLT3a/b, PXYa/b, ABCG14a/b, ERb and VND7b cannot be mapped without the panel table.
- **LEC vs Epidermis.** As in Song 2023, the medium-contact surface is treated as Hypoxia_Stress, not Epidermis.

### Could not verify

- The final Mol Plant text beyond the first Results section, and Supplemental Data 1-8 (Xenium panel with IDs; vascular, UEC and SCN subtype DEGs). ScienceDirect and cell.com returned a Cloudflare check, which was not bypassed. The article is OA (CC BY-NC-ND), so the user can download the supplements in a browser. Most needed: Supplemental Data 3, 4, 6 and 7.
- A raw-data accession for Song2026.
- The identity of the ID behind each Song2026 symbol that has an a/b suffix.
