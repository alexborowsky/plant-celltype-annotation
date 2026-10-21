<!-- Collated from the survey review of rice_seed (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Rice seed (caryopsis) single-cell datasets: collated review

Date: 2026-10-20. Built from the three dataset reviews in this folder (`Jing2026/`, `Liu2026/`, `Wang2025/`, each with its own README) and `survey/merged_reviews.json`. This is a paper-only review: no in-data check (Step 3b) was run.

Files:
- `expected_cell_types.tsv`: expected types, written from caryopsis anatomy (0 HAP to ~21 DAP plus germination), not from the published labels. `function_markers` counts the existing skill tables (`references/markers/`, rice-applicable rows). `notes` gives the count in the draft below.
- `markers_draft.tsv`: 64 rows in the skill's marker schema plus `alt_id`. `ref_gene` holds MSU7 `LOC_Os` IDs and `alt_id` holds RAP-DB IDs, as in `rice_root.tsv`. `tissue = seed`, a new value: the skill README currently lists only leaf/root/any. AL1 has no MSU7 ID (`ref_gene = -`), so use `--id-column alt_id` for it. No row needs `requires`/`excludes`; the types are shared by grasses, and the table is rice-only for now.

## Datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Jing et al. 2026 *Cell* 10.1016/j.cell.2026.09.023 (ZH11) | whole grain 0 HAP-21 DAP + germination 2-48 HAI | Stereo-seq (square bins, not cells) + snRNA-seq (DNBelab C4) | atlas: 851,725 nuclei + 347,640 bins; 96 seed labels; per-type counts unknown | ZH11 T2T (`ZH01G...`); no RAP/MSU crosswalk | large objects only (per-sample h5ad 0.1-4.1 GB on CNGB FTP; labels in obs unverified); portal marker export (492 seed rows) | medium |
| Liu et al. 2026 *JIPB* 10.1111/jipb.70373 (Songjing 2) | whole caryopsis 3/5/7 DAP | snRNA-seq (10x-style) | 67,922 nuclei, 22 clusters | RAP-DB (OMIX features.tsv) | cluster-level only (figure legend); matrices on NGDC OMIX010779/OMIX010934 | medium (best validated: 8 in situ, 5 GUS) |
| Wang et al. 2025 *Nature* 10.1038/s41586-025-09251-0 (Nipponbare) | grain ~2 weeks after fertilization (GEO: "Spikelet") | 10x Multiome (snRNA + snATAC) | 6,276 nuclei, 5 labels | MSU7 | per-cell table from portal (`Wang2025/seed_portal_labels.tsv`) | low (labels); useful DE |

Liu 2026's 7 DAP matrices (OMIX010934) are shared with Wang et al. 2025 *Nat Commun*, which this group did not review. Its in situ results (GE, SWEET14) are cited second-hand only.

## Verdicts by expected cell type

A = Adopt, R = Revise, X = Reject, - = not annotated.

| Expected type | Jing 2026 | Liu 2026 | Wang 2025 |
|---|---|---|---|
| Stigma_Style_Remnant | A (0-12 HAP) | - | - |
| Pericarp (incl. cross cells) | R (merged Pericarp-Testa layers; photosynthesis markers) | A (C2, layers merged) | R ("Epidermis" = outer maternal layer, undefined) |
| Seed_Coat | R (merged into Pericarp-Testa, Integument) | R (C10 published as "ventral aleurone"; cuticle genes) | - |
| Nucellus / nucellar epidermis / projection | A (Nucellus 0-3 DAP) | A (C17, C18) | R ("Vascular" = maternal sucrose-unloading tissue) |
| Ovular_Vascular_Trace | R (Vascular_cell_I-V; xylem/phloem unsplit) | - (GIF1, SWEET11b, CCR14 sit in the C7 "embryonic axis" panel) | R ("Vascular") |
| Coenocytic_Endosperm | A (stage) | - | - |
| Starchy_Endosperm | R (oversplit 1-6, dorsal/ventral/peripheral states) | A (6 clusters) | X: published "Scutellum" (40%) and "Plumule" (22%) are endosperm by DE |
| Aleurone | A (dorsal/lateral not split) | A (C6, SUT1 in situ) | - (possibly inside "unknown") |
| Embryo_Endosperm_Interface | A (Endosperm_adjacent_to_scutellum, GSTF12 in situ) | R (C19 EEI mixes both sides) | - |
| Proembryo / Embryo | A (Proembryo); X (Embryo_unknown_1-7) | R (Em-1 C15, Em-2 C5) | R ("unknown" = embryo/aleurone maturation) |
| Protoderm | - | R (Em-2 C9, BDG in situ + GUS) | - |
| Scutellum | R (Scutellum_1-8 oversplit) | A (C1, 3, 12, 20) | X (label is endosperm) |
| Scutellar_Epithelium | A (Scutellum_epidermis; RAmy); X (germination Scutellum_epidermis_2 = endosperm contamination) | - (inside C19?) | - |
| Embryonic_Axis (plumule, radicle, provasculature) | R (merged organ-pair bins) | A region-level (C7, FIB in situ) | X ("Plumule" is endosperm) |
| Coleoptile | R (LAZY1 DE) | - | - |
| Coleorhiza / Epiblast | R (merged bins) | - | - |
| Root_Cap | R (no root-cap function marker) | - | - |
| Dividing_cells | R (G2/M state labelled "Cellularized_endosperm") | A (C11, labelled as a state) | - |

## Markers supported by more than one dataset (by gene ID)

| Type | Gene (MSU7 / RAP) | Support | Draft confidence |
|---|---|---|---|
| Starchy_Endosperm | Wx LOC_Os06g04200 / Os06g0133000 | Liu panel; Wang DE (relabelled cluster) | function, high |
| Starchy_Endosperm | SSIIIa/FLO5 LOC_Os08g09230 / Os08g0191433 | Liu; Wang | function, high |
| Starchy_Endosperm | bZIP58/RISBZ1 LOC_Os07g08420 / Os07g0182000 | Liu; Wang | function, high |
| Starchy_Endosperm | RPBF LOC_Os02g15350 / Os02g0252400 | Liu; Wang | function, high |
| Starchy_Endosperm | ONAC023 LOC_Os02g12310 / Os02g0214500 | Liu; Wang | characterized_enriched, medium |
| Starchy_Endosperm | OsRFPHC-11 LOC_Os05g01230 / Os05g0102600 | Jing spatial; Wang DE | expression, medium |
| Aleurone | AL1 Os01g0382200 (= ZH01G18610) | Kuwano 2011 GUS (dorsal aleurone); Liu panel; Jing (cites Kuwano) | characterized_enriched, high |
| Embryo_Endosperm_Interface | OsSWEET14 LOC_Os11g31190 / Os11g0508600 | Jing spatial ESR; Liu C19 (+ in situ in Wang 2025 Nat Commun, unread) | characterized_enriched, medium |
| Nucellus (maternal unloading) | OsSWEET11 LOC_Os08g42350 / Os08g0535200 | Ma 2017 and Yang 2018 reporters; Liu nucellus; Jing Inner_Pericarp-Testa_2; Wang "Vascular" | function, high |
| Ovular_Vascular_Trace | OsGA2OX3 LOC_Os01g55240 / Os01g0757200 | Jing Vascular_cell_I; Wang "Vascular" | characterized_enriched, medium |
| Ovular_Vascular_Trace | OsMADS21 LOC_Os01g66290 / Os01g0886200 | Jing Vascular_cell_2; Wang "Vascular" | characterized_enriched, medium |
| Pericarp | OsGER3/GLP8-2 LOC_Os08g08960 / Os08g0189100 | Jing Outer_Pericarp-Testa_3; Wang "Epidermis" | characterized_enriched, medium |
| Pericarp (green layer) | DYE1/Lhca4 LOC_Os08g33820 / Os08g0435900 | Jing Pericarp-Testa (1-3 DAP); Liu pericarp | characterized_enriched, medium |
| Embryonic_Axis | FIB/OsTAR2 LOC_Os01g07500 / Os01g0169800 | Liu in situ + GUS + mutant; Jing Vascular_cell_V | function, medium (not raised; see conflicts) |
| Embryo | OsEnS-115 LOC_Os08g03410 / Os08g0127900 | Liu in situ C15; Wang "unknown" DE | characterized_enriched, medium (not raised; Wang cluster identity unresolved) |

Agreement that rests on a Wang 2025 cluster uses this review's relabelling: the published "Plumule"/"Scutellum" clusters are read as endosperm. That relabelling is supported by many endosperm function genes, but it is a hypothesis until the in-data check.

## Gaps (no validated marker in any dataset)

- Coenocytic_Endosperm, Coleorhiza, Epiblast, Root_Cap of the radicle, embryonic SAM/leaf primordia, and Procambium: no seed `function` marker. For the radicle use `rice_root.tsv`, and for the plumule shoot-apex markers in Part B.
- Cross_Cells and tube cells: only photosynthesis genes (filed under Pericarp).
- Nucellar projection vs nucellar epidermis vs ovular vascular trace: the markers (SWEET11/15, GIF1, MADS21) span all three, and no dataset split them.
- Dorsal vs lateral aleurone: AL1 only.
- Seed_Coat: only Liu's C10 cuticle genes, under a reinterpreted label.
- Integument: the Wang "Vascular" DE has OsMADS13 (LOC_Os12g10540, ovule identity), but its tissue is unclear, so it was left out.

## Recommended label reference

**Liu 2026** for cell identities: it has the most in situ and GUS validation, keeps a separate cycling cluster and an unknown cluster, and its matrices with RAP IDs are public. Its labels are cluster-level only, so re-derive them by clustering the OMIX matrices and scoring with `markers_draft.tsv`. Revise C10 (seed coat?), C19 (mixed interface) and C7 (may hold maternal vascular-trace cells).
**Jing 2026** for spatial position and time course (0 HAP to germination), and as the only source for early nucellus, ESR (GSTF12 in situ), pericarp layers and germination scutellar epithelium. Its per-cell labels exist only in large h5ad files and are bin-based, so do not use them as single-cell ground truth.
**Wang 2025** only for its DE tables. Do not reuse its seed labels: two of its five labels are endosperm under embryo names.

## Conflicts and corrections

- **Wang 2025 "Scutellum" and "Plumule"** (61% of nuclei) are endosperm by DE. The reviewer's call is accepted here and used for cross-study agreement.
- **Liu 2026 C7 "embryonic axis"**: three of its five panel genes (OsCIN2/GIF1, SWEET11b, OsCCR14) are ovular vascular-trace genes in Jing (GIF1) or DE in Wang's maternal "Vascular" cluster (SWEET11b, CCR14). C7 may include maternal vascular cells, or the panel may be mixed. FIB/TAR2 confidence was therefore not raised.
- **Liu 2026 C10 "ventral aleurone"**: all its markers are cuticle/wax genes. It is filed here as Seed_Coat (hypothesis).
- **OsGZF1**: in situ "surrounding the scutellum" (Chen 2014, abstract checked); Liu lists it as an aleurone marker; Wang used it for "Scutellum" although it is not DE there. Filed as Embryo_Endosperm_Interface, low.
- **OSTF1** (Os01g0788800, HD-ZIP IV TF1): the literature in situ is protoderm (Yang 2002, abstract checked), but Jing filed it under Aleurone. Filed as Protoderm, low.
- **OsMFT1**: in situ at the interface (Liu), but DE in Wang's endosperm-like cluster, so its expression may be broader.
- **OsVPE4**: Liu nucellus vs Jing "Blank" bins.
- **Symbol traps**: Jing's portal symbols: "OsARF1" (chr1) is ARF16 (Os01g0236300); "OsPIN1a" (chr6) is PIN1c; "OsBBM4" is on the wrong chromosome; RAmy1A is assigned to two ZH loci (ZH02G37350/37370). Liu's in situ probe "glutelin" Os08g0127900 is OsEnS-115, not a glutelin. OsNF-YB1 (Os02g0725900) and OsLEC1/NF-YB7 (Os02g0725700) are adjacent loci.
- **Correction to the Wang 2025 review**: LOC_Os07g44060 is not unmappable. `rice_root.tsv` pairs it with Os07g0634400 (HAD-like hydrolase; UniProt Q8LHP3, no MSU name in UniProt), where it is a root Pericycle marker. Its seed in situ near the dorsal vascular bundle is consistent with a vascular-associated gene.
- **ID pairings checked for this draft**: UniProt REST for 24 RAP IDs, plus the Oryzabase gene list. ZH11-to-RAP pairs for AL1, GSTF12, SWEET14, CycB1;1, KNOLLE and CDC20.1 were checked by gene length and position offset against Ensembl Plants coordinates; MADS21 and DYE1 by portal symbol (DYE1 also by position).

## Overlap with existing skill tables (same species)

`rice_root.tsv` shares four loci: OsSUT1 LOC_Os03g07480 (root Phloem there; Aleurone here), LOC_Os07g44060 (root Pericycle there; seed Ovular_Vascular_Trace here), and CycB1;1 LOC_Os01g59120 (Dividing_cells in both). KNOLLE and CDC20.1 are new Dividing_cells rows. They are not in `rice_root.tsv`, though its README mentions KNOLLE. No other rice table exists. The seed cell types (endosperm, aleurone, nucellus, scutellum, ...) have no rows in any skill table.

## Could not verify

- Full texts and supplements of Jing 2026 (Cell) and Liu 2026 (JIPB) are paywalled and were not accessed. Liu marker IDs come from a press-release figure image, then UniProt/Oryzabase. Jing marker IDs come from the portal export.
- Jing per-cell labels (h5ad 0.1-4.1 GB, `https://ftp.cngb.org/pub/SciRAID/stomics/STDS0000421/`) and the Wang `GSE232863_scRNA_omics.Rds` (5.1 GB) were not downloaded.
- Literature functions not re-read here: Wx, SSIIIa, bZIP58, RPBF, FLO2, FLO4, BT1-1, NAC20/26, RAmy1A/3E, OsLEC1, GE (Nagasawa 2013), OsMADS29 (original Yin and Xue 2012; only a later summary was checked), and the Qu and Takaiwa 2004 GUS patterns (cited by the Wang review). Abstracts checked: Kuwano 2011 (AL1), Xu 2016 (NF-YB1), Ma 2017 (SWEET11), Yang 2018 (SWEET11/15), Yang 2002 (OSTF1), Wang 2008 (GIF1), Chen 2014 (GZF1), Khurana 2022 (MADS29).
- The localization of GIF1 in the ovular vascular trace comes from Jing's citation; the Wang 2008 abstract does not state it.
- AL1 MSU7 ID: not found in Oryzabase, UniProt or Ensembl cross-references.
- The Wang et al. 2025 *Nat Commun* in situ data (GE, SWEET14) were not read.
