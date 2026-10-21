<!-- Collated from the survey review of arabidopsis_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis root single-cell datasets: group summary (Part A, Steps 1-3a)

Date: 2026-10-20. This is a paper-only review (Step 3a). No in-data check (Step 3b) has been run yet.
It merges four per-dataset reviews (`survey/merged_reviews.json`, group `arabidopsis_root`). Each dataset folder has its own README, supplements and label extracts.

Files in this folder:
- `expected_cell_types.tsv`: expected cell types, written from root anatomy (primary root tip plus the secondary-growth zone) before the published labels were read. `function_markers` counts the unique `function` genes per type across `markers_draft.tsv` and the skill's `arabidopsis_root.tsv` combined.
- `markers_draft.tsv`: 113 rows at first build, one per gene (167 rows after the 2026-10-20 update; see the end of this file). Columns are the skill schema plus `alt_id` (the UniProt accession).
- `group_build/`: `rows.py` (row definitions), `build_markers.py`, `uniprot_check.py` and `uniprot_check.tsv`. The check found all 113 AGI IDs in UniProt, taxon 3702.

## Datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Shahan et al. 2022 *Dev Cell* ([10.1016/j.devcel.2022.01.008](https://doi.org/10.1016/j.devcel.2022.01.008)); GEO GSE152766 | Col-0 primary root tip (distal 0.5 cm), 5-7 d; 16 WT samples (includes Denyer 2019 and Ryu 2019) | Protoplast scRNA-seq, 10x v2/v3 | 110,427 | TAIR10 | Small table: Data S3 (mmc3.zip, 65 MB) has per-cell `celltype.anno` for every cell. Exported as `Shahan2022/Shahan2022_labels.tsv`. Barcode format `<16-mer>_<sample n>` | High. Four labelling methods and literature markers with loci. Weakness: forced final assignment (37% of cells not in the consensus) |
| Lee et al. 2025 *Nat Plants* ([10.1038/s41477-025-02072-z](https://doi.org/10.1038/s41477-025-02072-z)); GEO GSE226097 | Whole seedlings, 3/6/12 d. No separate root sample | snRNA-seq, 10x 3', plus MERFISH (shoot/hypocotyl only) | 6 d 41,314; 12 d 115,967 (whole seedling) | TAIR10/Araport11 (strip R suffixes such as `AT1G556701`) | Small table: per-cell labels for 6 d, 12 d and merged, exported from the cellxgene portal (`Lee2025/seedling_*_labels_from_portal.tsv`). 3 d labels only in a 1.3 GB rds | Medium overall, low for root. Only Trichoblast and 6 d Endodermis are named root types. 55% of 12 d nuclei are Unknown |
| Lyu et al. 2025 *Nat Plants* ([10.1038/s41477-025-01938-6](https://doi.org/10.1038/s41477-025-01938-6)); GEO GSE270140; figshare 10.6084/m9.figshare.27569697 | Col-0 30 d root, top 2 cm (secondary growth) | Protoplast scRNA-seq, 10x v3, one library | 11,760 | TAIR10 | Large object only: 2.33 GB Seurat rds plus the figshare cluster map script. The 534 MB figshare CSV header lists labels without barcodes | High for reporters (93 lines with T1 counts). One library and no replicates |
| Nobori et al. 2023 *Nat Plants* ([10.1038/s41477-023-01439-4](https://doi.org/10.1038/s41477-023-01439-4)) PHYTOMap | Col-0 5 d root tips (5 roots) | Whole-mount multiplexed FISH, 28-gene panel | 3,608 segmented cells | TAIR10 | None. Cluster names are in a figure legend for one root only. No matrix | Medium. Useful as spatial validation of 28 Shahan markers, not as a label source |

## Per-cell-type verdicts

A = Adopt, R = Revise, X = Reject/relabel, – = absent or not annotated. Verdicts are on the paper only (Step 3a).

| Expected type | Shahan 2022 | Lee 2025 (seedling nuclei) | Lyu 2025 (secondary root) | Nobori 2023 (spatial) |
|---|---|---|---|---|
| Quiescent_Center | R (158 cells, threshold-selected; includes columella stem cells; no WOX5) | – | – | R (merged "Columella/QC") |
| Stem_Cell_Niche | – (in QC/meristem) | – | – | – |
| Columella | R (7.7%, inflated; 91% outside consensus) | – | – | R (cl 19, tiny) |
| Lateral_Root_Cap | R (16.7%, inflated; LRC/columella border unstable) | – | – | – (absent) |
| Atrichoblast | A | – (GL2 only in shoot clusters; root non-hair cells probably in 6 d c2 "abaxial epidermis") | – | R (merged in "Epidermis") |
| Trichoblast | A | A (12 d c3; merged c5/c6/c14); R for 6 d "Trichome/trichoblast" | – | R (merged in "Epidermis"; LRL3-high cl 10 mislabelled Endodermis) |
| Cortex | A | – (probably 6 d c2 / Unknown clusters) | – (lost in secondary growth) | R (cl 5/6 fit; cl 2 is LRC/epidermis) |
| Endodermis | A | A (6 d c17); R (3 d c14 labelled Unknown) | – | R (cl 9/11 fit; cl 10 is trichoblast) |
| Pericycle | R (XPP 11.1% and PPP 4.2%; about half from the forced step) | R (6 d c7 / 3 d c9 "phloem parenchyma" look like pericycle/xylem loading, inferred) | – | R (cl 16 fits; cl 13 has a cortex gene) |
| Procambium | R (no bulk reference) | – | – | – (in "Stele") |
| Xylem | A (protoxylem); R (metaxylem: weak markers) | R (root and shoot merged) | A (vessel identity/expanding; late vessel) | R (in "Stele") |
| Phloem / Sieve_Element / Phloem_Companion | R (protophloem kept; "Metaphloem & CC" merged) | R (root and shoot merged) | A (SE 104 cells; CC 127 cells) | R (in "Stele") |
| Vascular_Cambium | – | – | R (S and G2/M clusters and formative phloem cells mixed in) | – |
| Xylem_Parenchyma | – | – | A (young, maturing and mature states) | – |
| Xylem_Fiber | – | – | R (CLE46 reporter in only 10/23 roots) | – |
| Phloem_Parenchyma | – | – | A (mature PP, merge stress subclusters; CPP) | – |
| Periderm | – | – | R (layers not separated) | – |
| Myrosin_Idioblast | – | – | A (TGG2 26/26, FAMA, Coomassie) | – |
| Lateral_Root_Primordium | – | – | R (39 cells, label only in the script) | – |
| Dividing_cells (state) | not labelled as a type (correct) | R (honest state label; pools root and shoot) | R (hidden inside "Vascular cambium") | – |
| Stress / catch-all | R (22% stressed_branch across types) | X (iron-deficiency and heat-shock clusters; 55% Unknown) | X ("Mixed identity" 7.9%) | – |

## Cross-study markers

Agreement is by AGI ID. It counts when a gene was validated (reporter, in situ or spatial) in one study and validated or cluster-specific in another independent study. Nobori 2023 took its panel from the Shahan atlas, but its in situ data are new, so it counts. Denyer 2019 and Ryu 2019 cells are part of the Shahan atlas, so they do not count as independent of Shahan. Lee 2025 built its curated list mostly from Shahan, so only Lee's own DE and MERFISH results are counted.

33 rows have genuine agreement between studies:

| Type | Genes (studies) |
|---|---|
| Trichoblast | LRL3 AT5G58010 (Shahan, Lee, Nobori); RSL1 AT5G37800 (Shahan, Nobori); RHD6 AT1G66470, RSL2 AT4G33880, COBL9 AT5G49270, EXPA7 AT1G12560, LRX1 AT1G12040, EXT12 AT4G13390 (Shahan, Lee) |
| Atrichoblast | GL2 AT1G79840 (Shahan DE; Nobori weak) |
| Endodermis | MYB36 AT5G57620 (Shahan reporter, Nobori in situ, Lee MERFISH); SCR AT3G54220 (Shahan, Nobori); CASP2 AT3G11550, CASP3 AT2G27370, CASP5 AT5G15290, UCC1 AT2G32300 (Shahan, Lee) |
| Cortex | C/VIF2 AT5G64620 (Shahan DE, Nobori in situ) |
| Pericycle | BHLH68 AT4G29100 (Shahan PPP DE, Nobori in situ) |
| QC / niche | PLT1 AT3G20840, LECRK-S.4 AT3G55550 (Shahan DE, Nobori in situ; both QC + columella) |
| Phloem | APL AT1G79430, DOF5.6/HCA2 AT5G62940, PEAR1 AT2G37590 (Shahan DE, Lyu reporter/cluster); OBP2 AT1G07640 (Lee DE, Lyu reporter); CYSTM12 AT5G04080 (Shahan, Lee) |
| Phloem_Companion | SUC2 AT1G22710 (Lee MERFISH, Lyu CC cluster); AHA3 AT5G57350 (Shahan DE, Lee stem MERFISH) |
| Xylem | ACL5 AT5G19530 (Shahan, Lyu reporter 14/14, Lee stem); AT3G10080 (Shahan metaxylem DE, Lyu reporter 14/14, Nobori panel); LAC6 AT2G46570 (Shahan list, Nobori, Lyu reporter 12/12); MYB46 AT5G12870 (Shahan, Lyu); CESA8 AT4G18780, CESA4 AT5G44030, CESA7 AT5G17420 (Shahan, Lee) |

Eight more rows cite two studies that conflict or only weakly agree, so their confidence was not raised: CO2, AT2G40260, AGL12, LBD14, NHL26, VND7 (not specific in Nobori), CDF4 and OCT3. They are listed under Conflicts.

## Gaps

These expected types have no `function` marker in the draft or in the skill table:
- **Cortex.** The only markers are reporter-enriched genes (C/VIF2, CORTEX/AED3, CO2) and AT1G62510.
- **Xylem_Parenchyma** and **Periderm.** These have Lyu 2025 reporter genes only. Several periderm genes are JA/wound-inducible.
- **Lateral_Root_Primordium.** Not curated. LBD16/LBD29/PUCHI are candidates; GATA23 is filed under Pericycle.

These types have only one function marker:
- **Quiescent_Center:** WOX5, which none of the four datasets used.
- **Lateral_Root_Cap:** SMB.
- **Phloem_Companion:** SUC2.
- **Stele:** SHR.
- **Vascular_Cambium:** ANT, which is weakly detected.
- **Phloem_Parenchyma:** CDF4.
- **Xylem_Fiber:** NST1, which is weak in the data.

Protophloem and metaphloem are not split, and protoxylem and metaxylem share the `Xylem` name (VND7 marks protoxylem; ACL5 and VND6 mark metaxylem). S-phase markers for Arabidopsis are not in the tables.

## Recommended label reference

**Shahan 2022** is the best label reference for the primary root tip. It has small per-cell tables, four labelling methods and literature markers with loci.
- Adopt its Atrichoblast, Trichoblast, Cortex, Endodermis and Protoxylem labels.
- Treat Columella, LRC, QC, Pericycle, Procambium, Metaxylem and the phloem labels as hypotheses. Keep only cells in its consensus (`cb.anno`) that have marker support.

**Lyu 2025** is the reference for secondary-growth roots: cambium, periderm, xylem and phloem parenchyma, myrosin idioblasts and SE/CC. Its labels must be rebuilt from the 2.3 GB rds with the figshare cluster map. Its reporter genes are its most reusable product.

**Lee 2025** is useful only for trichoblast and 6 d endodermis nuclei. **Nobori 2023** is a spatial validation source, not a label source.

## Conflicts and corrections

- **AT5G62940 is DOF5.6/HCA2 (PEAR2).** Shahan Data S2F labels it PEAR1/DOF2.4; PEAR1 is AT2G37590 (UniProt O80928). Both are in the draft under Phloem.
- **AT1G62500 (CO2; UniProt: putative proline-rich cell-wall protein DEG27).** It is a cortex reporter in the primary root (Heidstra 2004; Shahan list), but its reporter marks mature phloem parenchyma in secondary-growth roots (Lyu 2025, 15/15). The draft keeps it as Cortex with this caveat.
- **AT3G60650 is RGF10/CLELn** (UniProt F4JBX1), not an uncharacterized gene. Shahan DE puts it in QC (pct 0.76) much more than in columella (0.18). The skill table files it as an uncharacterized Columella gene; the draft moves it to Quiescent_Center.
- **DRO3/LZY2 AT1G17400.** Shahan used it as a columella marker, but its DE is higher in the QC label (0.66 vs 0.16), so that QC label probably holds columella stem cells. It is a gravitropism function gene, so the draft grades it `function`/medium. The skill table has `expression`/low.
- **GATA23 AT5G26930** is stage-restricted (lateral-root founder cells), so the draft has medium. The skill table has high.
- **OPS AT3G09070.** The skill table files it under Procambium; the review and the draft use Phloem (protophloem differentiation). **AGO10** is `function` in the skill table and `characterized_enriched` in the draft, because it marks provasculature by expression, not by a type-defining function.
- **Lyu 2025 Supp Table 4 ID errors.**
  - The pDIR1 construct is listed as AT5G42510 (a dirigent protein), while the dataset gene called DIR1 is AT5G48485 (the SAR lipid-transfer protein). It is unresolved which promoter was cloned, so DIR1 was **left out** of the draft.
  - The pAT4G27435 reporter row carries AT5G18240, and its pattern is CC plus late vessel, so it was **left out**.
  - RPS8A is listed as the plastid ATCG00770.
- **Nobori 2023 cluster names contradict its own panel table.**
  - Cl 10 is LRL3-high (trichoblast) but labelled Endodermis.
  - Cl 13's top gene AT2G40260 is a cortex gene in its table, but the cluster is labelled Pericycle.
  - Cl 0 is driven by OCT3, LAC6 and VND7 but labelled Epidermis.
  - AGL12 is "Elongating-Phloem" in the panel but phloem-pole pericycle in Shahan DE.
  - NHL26 is "Xylem" in the panel but a companion-cell gene in leaves.
- **ABCG29 AT3G16340.** Lee 2025 calls it endodermis (DE and spatial), but Lee's own curated list puts it in maturing phloem-pole pericycle. It is in the draft as Endodermis, low.
- **CASP1, SUC2, WOX5 and AGL42** are named in Shahan 2022 without loci. CASP1 (AT2G36100) and SUC2 (AT1G22710) IDs come from Lee 2025 tables and UniProt. WOX5 (AT3G11260) comes from UniProt Q8H1D2.
- **Lee 2025 suberin cluster** (12 d c13; CYP86A1, GPAT5, ASFT). The suberized-endodermis identity is inferred. Only CYP86A1 was added (Endodermis, medium, with a periderm caveat).

## Overlap with the skill's `arabidopsis_root.tsv` (51 rows)

- **23 genes are in both tables.** For 21 of them the cell type is the same; the 2 that differ are OPS and AT3G60650 (see above). Grades differ for 7 genes: AT3G60650, PLT1 (medium to high), DRO3, AT1G62510 (low to medium), GATA23, AGO10 and DOF5.6 (medium to high).
- **28 skill-table rows are not in the draft.**
  - Function rows: CASP4, PER64, WRKY44, IRX9.
  - Shahan/Ryu enrichment rows: BAM2, GH9B6, CYP75B1, IAMT1, GH9C1, MES15, WEL2, XTH17, PME32, CDF6, RDA2, AT1G55200 and other `expression` rows.
  - The draft does not replace them. A merge should keep the four function rows.
- **90 draft rows are new** to the skill. Most are the Lyu 2025 secondary-growth types, the cross-study trichoblast/endodermis/xylem genes, and two Dividing_cells state rows.
- **New cell-type names** (none are in the existing tables): Vascular_Cambium, Xylem_Parenchyma, Xylem_Fiber, Periderm, Myrosin_Idioblast (requires `Brassicaceae`). Phloem_Parenchyma, Phloem_Companion and Sieve_Element follow the names in the leaf and sorghum tables.

## What I could not verify

- No in-data check (Step 3b) has been run, so enrichment in a target dataset is untested for every row.
- I did not open the literature citations in `basis` (author/year/journal), apart from what the dataset reviews recorded. DOIs are given only for the four datasets.
- Lyu 2025 per-cell labels need the 2.33 GB GEO rds. Shahan's 45 GB rds, Lee's rds objects and Nobori's image tarballs were not downloaded.
- Lee 2025 3 d labels: the cellxgene instance returned HTTP 500.
- The reviews read Nobori cluster-to-gene links by eye from the Fig. 2e heatmap.
- The Shahan per-dataset reviewer could not get the Europe PMC `/bin/` supplements because of a Cloudflare bot check; the files came from the Cell Press CDN instead.
- The DIR1 and AT4G27435 reporter identities in Lyu 2025 remain unresolved; checking them would need the primer sequences matched against TAIR10.

## Update 2026-10-20: gap-fill reviews

Three reviews were merged: Li 2016 and Otero 2022 (this run) and Roszak 2021 (an earlier run, `survey/run5_done_reviews.json`). The script is `group_build/update_20261020.py`. Pre-update copies are `group_build/markers_draft_pre_20261020.tsv`, `group_build/expected_cell_types_pre_20261020.tsv` and `group_build/README_pre_20261020.md`.

- `markers_draft.tsv` now has **167 rows** (113 before): 54 rows added and 37 existing rows edited. No existing row was removed. The column set is unchanged (13 columns; `alt_id` = UniProt).
- A gene can now have more than one row (SKOR, AT1G48750, CDF4/PAPL2), one per cell type.
- Li 2016 values are gene-level FPKM: TAIR10 isoforms from Table S5 (mmc6), summed by the reviewer (`Li2016/Li2016_geneFPKM_sum_of_isoforms_from_TableS5_mmc6.tsv.gz`). Ratios are derived from those values; the paper publishes no enriched-gene tables.
- **Independence rule used for raises.** Otero 2022 and Roszak 2021 come from the same lab and share reporter lines, so together they count as **one** source. Li 2016 (Benfey lab, sorted bulk RNA-seq) is independent of Shahan 2022 (Benfey/Ohler, scRNA-seq), because the data and method differ. This judgement call is open to challenge.

### New datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Li et al. 2016 *Dev Cell* ([10.1016/j.devcel.2016.10.012](https://doi.org/10.1016/j.devcel.2016.10.012)); companion microarray Brady 2007 *Science*, GEO GSE8934 | Col-0 5-6 d roots: 15 GFP-reporter sorted populations, sorted and unsorted whole root, 3 dissected zones, CHX/mock | FACS + Illumina RNA-seq, 3 reps (57 libraries) | Bulk populations | TAIR10 | Population level only. No SRA accession found | High. Bulk marker and agreement source, not a label source |
| Otero et al. 2022 *Nat Plants* ([10.1038/s41477-022-01178-y](https://doi.org/10.1038/s41477-022-01178-y)); GEO GSE181999 | Col-0 root phloem pole: 6 reporter sorts (MAKR5 tip and whole root, S17, sAPL, APL, PEAR1-del) | FACS + 10x scRNA-seq | 10,204 | TAIR10 | Small table: per-cell labels in `Otero2022/cell_metadata.csv` (1.1 MB, GitHub release v2022.09.04). The 522.6 MB SCE rds was not downloaded | High. No replicate sorts; proportions reflect the sorting |
| Roszak et al. 2021 *Science* ([10.1126/science.aba5531](https://doi.org/10.1126/science.aba5531)); GEO GSE140778, GSE142259 | Col-0 5 d root tip: 7 phloem reporter sorts | FACS + Smart-seq2 (plates), plus bulk sorted PSE | 1,242 pass QC (758 PSE) | TAIR10 | Population level: GEO gate labels only; the per-cell calls (Table S17) are inaccessible | High, but phloem lineage only. All supplements blocked |

DOIs were confirmed in Europe PMC (PMIDs 27840108, 35927456, 34941412).

### Verdicts

**Li 2016**
- Adopt: WOX5 (QC/niche), E30 (mature endodermis), CO2 (meristematic cortex), COR (mature cortex), COBL9 (trichoblast), GL2 (atrichoblast), PET111 (columella).
- Adopt as a control, not a type: sorted whole root (SCOL/ACOL). This is the protoplasting/sorting signature.
- Revise, because these populations are merged: SCR (endodermis + QC), WER (LRC + non-hair), S32 (proto- + metaphloem SE), APL (SE + CC, CC-rich), WOL (stele).
- Revise, because the labels do not match the data:
  - S17 is labelled phloem-pole pericycle but is XPP-rich. Use it as pericycle with the pole unresolved.
  - S18 is vessel-dominated. Use it as maturing xylem.
  - S4 is mixed xylem precursors plus pericycle.
- Reject: the dissected zones and the CHX/mock samples.
- Two gap-search claims were wrong: Li 2016 has no LRC-only population and no protophloem vs metaphloem split.

**Otero 2022**
- Adopt: PSE (Sieve_Element), CC (Phloem_Companion), PPP (Pericycle, phloem-pole subtype), dividing (Dividing_cells, a state).
- Revise:
  - early PSE: mixed with cell-cycle identity, per the authors' own code.
  - MSE: the evidence is in the paywalled main Fig. 2, and doublets or meristem contamination are possible.
  - intermediate CC/PPP: a PSE-adjacent ring state, not a type.
  - Pericycle cluster 11: generic or non-phloem-pole pericycle.
  - outer layers: epidermis and LRC contaminants.
- Reject: early/undetermined. The authors left these cells unassigned on purpose.

**Roszak 2021**
- Adopt: the PSE pseudotime domains and phases I-VII, as Sieve_Element maturation **states**. Phases I-II are proliferating, so do not label them as a type or call them from cell-cycle genes.
- Adopt: the bulk-sorted PSE populations (GSE142259).
- Revise:
  - The PSE-gated sorts: the GEO gate is not the final call.
  - The pPEAR1-del sort: merged PSE, MSE, procambium and columella cells.
  - The MSE and procambium trajectories: small and inferred.
- Reject: the empty wells.

### Markers added (54)

- **Protoplasting_stress (new, 10 state rows, medium):** BCB, TAT3, DREB2A, ERF109, ERF13, HSP17.4A, WRKY40, CML38, HSP17.7, TCH4/XTH22. Each has log2FC 5.4-7.5 between the Li 2016 sorted and unsorted whole root, and each is in the Shahan 2022 protoplasting list.
- **Cortex:**
  - IAMT1 (medium): also a Ryu 2019 cortex marker in the scKB list.
  - GA3OX1, NPF6.4/NRT1.3, CYP71B34 (low; Li 2016 bulk only).
- **Pericycle:**
  - SKOR (function, medium).
  - LBD17 (low).
  - AT1G48750 (expression, low).
  - Phloem-pole subtype from Otero: S17/BZIP6 (medium), MES7 (high), CALS8 (medium).
- **Xylem_Parenchyma:** SKOR (function, medium). This comes from `survey/characterization/characterized_markers.tsv` (Gaymard 1998), matched by ID to the Li 2016 S17 signal.
- **Xylem:** XCP1, LAC4/IRX12 (function, medium; Li 2016 S18).
- **Phloem_Companion:**
  - NAKR1 (function, high).
  - LOR8/AT2G38640 and SAPL (high).
  - PLC5, MC3 (medium).
  - CYSTM6 (low).
- **Sieve_Element:**
  - NAC045, NEN4 (function, high).
  - CVP2 (high).
  - ROP9, NAC020, NAC057 (medium).
  - NAC073, NAC010, ZAT14, ZAT14L (low; late PSE, but shared with xylem in Li 2016 S18).
- **Phloem:**
  - PEAR2/DOF5.1 (function, high).
  - DOF6 (high).
  - ROPGEF5, PAPL1, CDF4/PAPL2 (function, medium). The CDF4/PAPL2 row is the primary-root PSE-adjacent ring; the existing Phloem_Parenchyma row stays for secondary growth.
  - MAKR5, AT3G16330 (medium).
  - ROPGEF3, ROPGEF2, PP2-B1, PER30, CDF2 (low).
- **Dividing_cells:** KNOLLE, CYCB1;1, AUR1 (function, high).

### Existing rows raised one level (and why)

- **WIP4** (QC): Li 2016 WOX5 sort.
- **CORTEX/AED3** and **AT1G62510** (Cortex): Li 2016 COR sort.
- **XPP, PHO1, NPF7.3, FRD3** (Pericycle): Li 2016 S17 sort.
- **VND6** and **XCP2** (Xylem): Li 2016 S18 sort.
- **GATA20, SYTD, MCTP2** (Sieve_Element): Li 2016 S32 sort.
- **AHA3** (Phloem_Companion): Otero CC DE plus the Li APL sort.
- **SBT4.12** (Phloem_Companion): Otero reporter, independent of Lyu.
- **AT2G48090** and **IPT3** (Phloem_Companion): Li APL sort.

All raises are medium to high. Rows that already had high confidence (WOX5, CASP1, APL, PEAR1, CALS7, NAC086, SUC2, MYB46, CESA4/7, VND7, C/VIF2) got the new support added to `basis` and `source`.

### Existing rows changed or caveated by the new evidence

- **PER15 AT2G18150 (Periderm): lowered medium to low.** In 5-6 d roots, which have no periderm, it is mature-endodermis-specific (Li 2016: E30 160 FPKM, others <=21).
- **PER49 AT4G36430 (Periderm, already low)** is also mature-endodermis-specific (E30 143). **PBP1** is broad in young roots (epidermis and columella, hundreds to more than 1,000 FPKM).
- None of the periderm rows has a stage tag, because the trait vocabulary has none. **Use them only on secondary-growth roots.** In primary-root data, PER15 and PER49 mark mature endodermis.
- **AT1G48750 (Xylem_Parenchyma, medium, kept).** In 5-6 d roots it is in the S17 pericycle sort (305 FPKM) and not in S18 (6). It is kept for secondary-growth roots; a Pericycle row (low) was added for primary roots.
- **ERF14 AT1G04370 (Phloem_Companion).** Li 2016 does not support it in young roots: APL sort 4 FPKM, against 101 after CHX treatment. It is stress or CHX-inducible. Kept medium for secondary-growth roots, with a caveat.
- **SBT4.12.** Li 2016 S17 (pericycle) is nearly as high as APL (1157 vs 1326 FPKM). It was still raised, on the two independent CC reporters, with the caveat in `basis`.
- **CO2 AT1G62500 (Cortex).** It is as high in the Li 2016 WOX5 sort as in the CO2 sort (25 vs 23), so it marks ground-tissue initials and meristematic cortex. It stays medium because of the Lyu 2025 phloem-parenchyma conflict.
- **Correction to the Conflicts section above.** AT5G62940 is DOF5.6/HCA2 ("PHLOEM EARLY DOF HCA2", UniProt Q9FM03). It is one of the six PEAR DOFs, but it is **not PEAR2**. PEAR2 is DOF5.1, AT5G02460 (UniProt Q9LZ56), and is now its own Phloem row.
- **Protoplasting-list caveat.** These new rows are also in the Shahan 2022 protoplasting-induced list, which is flagged in each `basis`: SKOR, LBD17, S17/BZIP6, CYSTM6, AT3G16330, PP2-B1, NAC073, ROPGEF3. Check them against the Protoplasting_stress score before relying on them.

### Gaps closed

- **Protoplasting_stress:** 10 independent-study state rows. Before this update the group only had the Shahan list reference.
- **Cortex:** 9 rows, and two are now high. There is still no gene whose function defines cortex, so this gap is closed for markers but not for `function` evidence.
- **Xylem_Parenchyma:** partly closed. It has its first `function` row (SKOR, medium), but no study separates xylem parenchyma from pericycle.
- **Phloem, Sieve_Element, Phloem_Companion and phloem-pole pericycle** are much stronger now, with PSE stage markers and more CC reporters. These were not listed as gaps.

### Gaps remaining

- **Lateral_Root_Primordium:** still no rows. `survey/characterization/characterized_markers.tsv` has function rows ready to merge (LBD16, PUCHI, ACR4, PLT3, PLT7, and GATA23 for founder cells). The Brady 2007 RM1000 LRP sort list sits in the Science SOM, which was not accessed.
- **Periderm:** no `function` row here. characterized_markers.tsv has MYB67, MYB68, WOX4 (shared with cambium) and GPAT5 (shared with suberized endodermis); they were not merged in this update.
- **Xylem_Parenchyma:** characterized_markers.tsv also has NRT1.8/NPF7.2 and HKT1. HKT1 is S17-enriched in Li 2016 (43 FPKM), which again shows that XP and pericycle are not separated.
- **Protophloem vs metaphloem SE:** no verified MSE-specific marker. Otero's MSE evidence is paywalled, and Roszak's MSE trajectory has no accessible gene list.
- **Lateral_Root_Cap vs columella:** no LRC-only population in the new data.
- **Procambium:** Otero has no procambium label, and Roszak's procambium trajectory is small and inferred.
- **Cortex:** no `function` marker.

### Recommended label reference (revised)

- **Shahan 2022** stays the label reference for the whole primary root tip.
- **Otero 2022** is now the label reference for the **phloem pole**: PSE, CC, PPP and the PSE-adjacent ring. It has small per-cell labels and reporter-backed CC, PPP and PSE calls. It is better than Shahan's phloem labels, which Shahan itself treats as hypotheses.
- **Li 2016** is the bulk reference: use it to check whether a marker is specific to a sorted population, and as the source of the protoplasting signature.
- **Roszak 2021** is the reference for PSE maturation **states**, not types.
- **Lyu 2025** stays the reference for secondary growth.

### Conflicts

- **S17 reporter pole identity.** Otero 2022 images pS17 in the phloem-pole pericycle, but the Li 2016 S17 bulk is XPP-rich (XPP 613, PHO1 245, NRT1.5 84 FPKM). Otero's S17-derived cells also include a generic or mature pericycle cluster (11). Conclusion: S17 sorts capture more than the phloem-pole pericycle. Phloem-pole subtype calls rest on MES7, CALS8 and S17/BZIP6 rather than on the sort label.
- **CDF4/PAPL2.** It marks the PSE-adjacent ring, columella and epidermis in the primary root (Otero 2022), but conductive phloem parenchyma in secondary growth (Lyu 2025). Both rows are kept, each with its stage noted.
- **PEAR1.** Otero calls it an early-SE marker, while Roszak and the draft use it for the phloem pole (PSE + MSE). It stays under Phloem.
- **ROPGEF3.** It is phloem-pole and PEAR-dependent in Roszak 2021, but the Li 2016 COBL9 hair-cell sort is higher (67 vs 8 FPKM in S32). Graded low.
- **NAC073, NAC010 and ZAT14.** Roszak calls them late-PSE genes, but in Li 2016 they are higher in S18 xylem. Graded low and marked as shared with xylem.

### Could not verify (this update)

- Otero 2022 main figures, including the MSE evidence and the MC3, CYSTM6 and PP2-B1 reporter images, are paywalled.
- All Roszak 2021 supplements were blocked by reCAPTCHA or Cloudflare checks, and Europe PMC lists the article as not open access. Roszak gene IDs therefore come from UniProt by symbol; ZAT14 and ZAT14L are the exception, with IDs given in the paper text.
- Brady 2007 Science SOM enriched lists (RM1000 LRP, J0121 XPP) were not accessed. No Li 2016 SRA accession was found.
- Function claims marked "from literature" (Avci 2008, Furuta 2014, Tian 2010, Miyashima 2019, Gaymard 1998 and others) were not re-read in this run.
- No in-data check (Step 3b) has been run for any new row.
- Large objects were not downloaded: the Otero SCE rds (522.6 MB, GitHub release v2022.09.04) and GSE181999_RAW.tar (909 MB).
