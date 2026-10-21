<!-- Collated from the survey review of maize_inflorescence (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Maize inflorescence (developing ear): collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill. This is a desk collation of published tables. No data were re-analysed. The skill itself was not edited.

## Files

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Expected cell types of a 5-10 mm B73 ear, listed from anatomy. `function_markers` counts the `function` rows in `markers_draft.tsv` |
| `markers_draft.tsv` | 73 rows (56 from Xu 2021/2025 + 17 from the 2026-10-20 Wang 2024 update) in the skill marker schema plus `alt_id`. `ref_gene` = B73 v5 (`Zm00001eb`), `alt_id` = v4 (`Zm00001d`), and the v3 ID is at the end of each `basis`. The ZmCLE7 row is the exception (see Conflicts) |
| `id_check_v3_v4_v5_uniprot.tsv` | For every gene considered: v3 ID, MaizeGDB v3→v4/v5 crosswalk, the v5 ID given in the Xu 2025 table, and the UniProt hit for each v5 ID (queried 2026-10-20) |
| `Xu2021/` | Earlier review of Xu et al. 2021 (README, supplements, crosswalks, `markers_Xu2021.tsv`). Added here: `TableS1_sheet4_metacluster_DE_binary.tsv` (sheet 4 exported) |
| `Xu2025_maize/` | Maize part of Xu et al. 2025, extracted from Table S1 (`mmc2.xlsx`, kept in `../arabidopsis_shoot_apex/Xu2025/`): `maize_eartip_cluster_markers_TableS1.tsv` (3,738 Seurat DE rows, v3 + v5 IDs), `maize_eartip_labels.tsv` (11,554 barcodes → cluster number + the Fig 1B name), `library_info_TableS1.tsv` |
| `build/make_markers.py`, `build/update_wang2024.py`, `build/make_expected.py` | Scripts that write the two TSVs (run in this order). Every `Zm00001eb`/`Zm00001d` ID is asserted to be in the MaizeGDB crosswalk for its v3 ID |

## Datasets

| Dataset | Platform | Cells | Label access | Gene IDs | Quality |
|---|---|---|---|---|---|
| **Xu X, Crow M, ... Gillis J, Jackson D (2021)** *Dev Cell* 56:557. doi:10.1016/j.devcel.2020.12.015. SRA PRJNA646989/646996/647001 | Protoplasts, FACS-cleaned, 10x Chromium (chemistry not stated); B73 ears 5-10 mm; 3 replicates | 12,525; 12 MetaNeighbor meta-clusters | Cluster-level only. No barcode table, GEO series or processed object | B73 v3 | Medium. About 20 new in situs, a YAB14 reporter with FACS RNA-seq/ATAC, and an HDZIV6-YFP reporter. Cortex, pith and "bundle sheath" are unvalidated, lateral organs are lumped together, and there is no stem-cell cluster |
| **Xu X, Passalacqua M, ... Gillis J, Jackson D (2025)** *Dev Cell*. doi:10.1016/j.devcel.2025.07.024. Maize B73 ear tip: SRA PRJNA1039503/1039507/1036155/1036156 | Optimized protoplasting (OptiPrep gradient), 10x Genomics (chemistry for maize not checked); finely dissected B73 ear tips (IM + early SPMs); 4 replicates. Molecular Cartography (Resolve) spatial on developing ears | 11,554; 14 Seurat clusters | **Per-cell table**: Table S1 sheet "Maize_B73_cell barcode" (cluster number per barcode). Cluster names only in Fig 1B, so they were transcribed into `Xu2025_maize/maize_eartip_labels.tsv` | v3 (plus v5 in the marker table) | Medium. It recovers stem cells (1,208 ZmCLE7+, 112 ZmWUS1+), and spatial data confirm 6 domains. 30% of cells are cell-cycle clusters, there is no boundary cluster, and xylem, phloem and sheath are one "Vasculature" cluster |

Xu 2025 was reviewed earlier under `arabidopsis_shoot_apex/Xu2025` for its Arabidopsis half only. Its maize half belongs to this group, so it is added here as the second dataset. **Both studies are from the Jackson/Gillis labs.** Xu 2025 used new B73 samples, a different protocol and its own clustering, and it compared its markers to Xu 2021 (Table S1 "vs Xu et al 2021" sheets, chi-squared overlap p < 0.001). The two count as independent data but not as independent labs. Cross-study agreement below is per gene ID (v3), and it raised `confidence` one level.

Other maize single-cell data were not in this group's reviews (maize leaf, root and embryo are separate groups). The Satterlee et al. 2020 vegetative shoot apex study was not reviewed.

## Verdict matrix (per expected cell type)

Xu 2021 verdicts are from `Xu2021/README.md`. Xu 2025 verdicts are from this collation (desk review of Fig 1B-D and the DE table; no in-data check).

| Cell type | Xu 2021 (meta-cluster, %) | Xu 2025 maize (cluster, n) | Best markers (confidence) |
|---|---|---|---|
| Central_Zone | absent | Adopt: c3 IM CZ (933), c5 SPM CZ (845); ZmCLE7 Molecular Cartography | ZmCLE7 (medium; ID unresolved), ZmLOG7, FEA4 (low) |
| Organizing_Center | absent | inside c3/c5 (WUS1+ 112 cells), not a cluster | ZmWUS1 (medium) |
| Meristem (inner, KN1+) | spread over MC1,4,5,8-12 | spread over c1,c3,c4,c5 | KN1 (high, broad) |
| Meristem_Epidermis | Adopt: MC6 (5%) | Adopt: c2 (1,175) | ZmPROPEP1 (high) + pan-epidermal genes |
| Epidermis (lateral organ) | inside MC3 (subcluster) | Adopt: c10 (482) | HDZIV8, HDZIV6, MFS18, PLTP3 (high) |
| Meristem_Boundary | Adopt (domain): MC9 (9%) | no cluster; BD1 in spatial data | BD1 (high); MIPS2 (medium); GST41 (low) |
| Adaxial_Meristem_Periphery | Adopt (domain): MC11 (7%) | Adopt: c12 (388); ZmACO2 spatial | BA1, PAO1 (high) |
| Meristem_Base | Revise: MC10 (2%) | Adopt: c6 (453); RA3 spatial | RA3 (high); RA1, RA2 (medium) |
| Lateral_Organ | Revise: MC3 (19%, merged) | Adopt: c9 non-epidermal (824), c10 epidermal (482); YAB14 spatial | YAB14 (high); YAB8, TSH1, FPF1, BOP2, DRL2 (medium) |
| Floral_Organ_Primordia | not separate | not separate | none |
| Cortex | Revise: MC1 (10%) | Revise: c1 (1,555); its top DE gene is RNRL1 (ribonucleotide reductase), and the MC1 top markers are not DE | AT1G62510-like (low) |
| Pith | Revise: MC8 (11%) | Revise: c4 (914); weak, high-background DE | 3 expression rows (low) |
| Procambium | not separate | not separate | none |
| Xylem | Adopt: MC4 (5%) | inside c13 Vasculature (291) | TMO5-LIKE3, WAT1 (high) |
| Phloem / Phloem_Companion / Sieve_Element | Adopt: MC5 (10%) with PEAR and PP2-A1 subclusters | inside c13 | ZNF30 (high); APL (medium); PEAR, PP2-A1 (low) |
| Vascular_Sheath | Revise: MC12 "bundle sheath" (5%) | inside c13; SHR1 spatial "bundle sheath" strands | SHR1, SHR1-like1 (medium) |
| Dividing_cells (state) | Reject as type: MC2 (14%) | Reject as type: c7 + c11 (1,228) | CYCB2-4 (high) |
| S_Phase (state) | Reject as type: MC7 (3%) | Reject as type: c0 + c8 (2,238) | HIS2A (high) |
| Guard, Trichome | absent (stage) | absent (stage) | not needed |

## Cross-study markers (28 rows raised by agreement)

A gene counts when it was validated (in situ, reporter or Molecular Cartography) in one study and is cluster-specific or spatially confirmed in the matching domain of the other, or when it is DE only in the matching cluster in both.

- **Validated in both** (in situ/reporter + Molecular Cartography): BD1 (boundary), RA3 (meristem base), ZmYAB14 (lateral organ), ZmSHR1 (vascular sheath).
- **Validated in one, cluster-specific in the other:** BA1, ZmPAO1 (adaxial periphery); ZmPROPEP1 (meristem epidermis); ZmHDZIV8, ZmHDZIV6, MFS18, ZmPLTP3 (epidermis); ZmTMO5-LIKE3, ZmWAT1 (xylem); ZmZNF30 (phloem, but at vasculature level in Xu 2025); ZmCYCB2-4 (G2/M); ZmHIS2A (S); KN1 (inner meristem, broad).
- **DE in the matching cluster in both (expression or characterized, now medium):** ZmOCL4, ZmHDZIV10 and two KCS genes (epidermis); ZmYAB8 and TSH1 (lateral organ); WAT1-related Zm00001eb039040 (xylem); ZmSHR1-like1, Cel21 and Zm00001eb252230 (vascular sheath); Zm00001eb266820 (adaxial periphery).

## Gaps

- **No validated marker:** Floral_Organ_Primordia, Procambium, Cortex and Pith. Cortex/pith markers are `expression`/low, and both studies' calls rest on homologs. Phloem_Companion and Sieve_Element have only low-confidence subcluster genes. Meristem_Epidermis has one specific gene; the rest are pan-epidermal.
- **Central_Zone:** the key marker ZmCLE7 has no v4/v5 ID (see below). ZmWUS1 is too low to cluster on.
- **No function-grade marker:** Meristem_Epidermis, Epidermis (HD-ZIV genes are `characterized_enriched`), Phloem_Companion, Sieve_Element and Vascular_Sheath. The grass phloem `function` rows in the skill (sorghum SUT1, SWEET13) are leaf transport genes and may be off in a sink ear.
- **Both datasets** are B73 ears from one lab at a similar stage. No tassel, no nuclei data, and no other genotype.

## Recommended label reference

**Xu 2025 maize ear tip** is the only dataset with per-cell labels (`Xu2025_maize/maize_eartip_labels.tsv`, cluster numbers from the publisher's Table S1 and names from Fig 1B). Adopt c2, c3, c5, c6, c10 and c12. Treat c9 as lateral organ (non-epidermal). Treat c13 as one vasculature class and split it with the xylem, phloem and sheath rows. Re-derive c1 and c4 (ground tissue), and re-assign identity in c0, c7, c8 and c11 (cell cycle, 30% of cells). Barcodes have a `-1_<rep>` suffix (`AAAC...-1_1` = rep1). Expect to rewrite them, and a match rate below 70% if you re-align with another genome version. Use **Xu 2021** for its validated domain markers (boundary MC9, which Xu 2025 lacks) and as a cluster-level cross-check. Its labels cannot be reused without re-clustering the SRA reads.

## Conflicts and corrections

- **ZmCLE7 ID unresolved.** Its v3 ID GRMZM2G372364 was added to AGPv3.31 by Xu 2021 (Table S4, chr4:7,570,071-7,571,261, minus strand). It is absent from the MaizeGDB v3→v4/v5 crosswalk, and Xu 2025 Table S2 also leaves its v4/v5 blank. UniProt, Ensembl name search and NCBI Gene found nothing. The row keeps the v3 ID with `basis` starting `REVIEW:`. Map it by hand (BLAST the v3 model against v5) before use.
- **Boundary and adaxial-periphery markers disagree between datasets.** In Xu 2025: ZmMIPS2 is weakly DE in cortex/pith; ZmGST41 and ZmCUC3-LIKE are DE in lateral-organ epidermis and meristem base, not c12; ZmDI19-like is broad. MIPS2 keeps `medium` because the in situ is strong. GST41 and CUC3-LIKE were lowered to `low`.
- **ZmCER1 and ZmPN** were called lateral organ in Xu 2021, but in Xu 2025 they are DE in epidermal clusters. CER1 is a wax gene, so both stay `Lateral_Organ` at `low`, with the conflict noted.
- **"Bundle sheath" → `Vascular_Sheath`.** Both papers use "bundle sheath" (Xu 2021 MC12; Xu 2025 Fig 1D legend for SHR1). In the 5-10 mm ear there is no Kranz anatomy, and the Xu 2025 spatial SHR1 signal runs along the vascular strands. The rows are named `Vascular_Sheath` so they are not matched to C4 leaf bundle-sheath markers (sorghum NADP-ME).
- **Symbol clashes:** UniProt names Zm00001eb149490 "LTP3", while Xu 2021 Table S1 uses ltp3 for GRMZM5G898755. UniProt names ZmYAB8 "Yabby15", ZmYAB14 "YABBY 5" and ZmACO2 "ACO1". UniProt names BD1's v5 model EREB151 (AP2/ERF). Compare by ID.
- **Multi-mapping v3 IDs:** TMO5-LIKE3 maps to Zm00001eb099400 (the Xu 2025 table; UniProt "uncharacterized") and Zm00001eb099390 (UniProt bHLH). Both rows were kept. For the others, the ID chosen is in `basis`: BA1 v4 042989/042988; BOP2 v5 093200 (UniProt NPR5) rather than 196460; SHR1 v5 020850 rather than 020840 (per Xu 2025); MYB46 v4 023932/023931; GRMZM2G151807 v5 129770/129760.
- **KN1 v5** is `0` in the Xu 2025 table (unmapped there). The crosswalk gives Zm00001eb055920, and UniProt P24345 (KN-1) and Ensembl (display name KN-1) confirm it.
- **Figure-legend errors in Xu 2021** (from the earlier review, unchanged): the Fig S2A "LTP1" ID GRMZM2G126646 is HDZIV13, and the Fig S2B XCP2 ID is malformed. XCP2 is not in the table.
- **Correction to the earlier Xu 2021 review:** it listed ZmDI19-like and ZmTMAAT as `expression`. Here they are `characterized_enriched`, because in situ specificity counts as that tier under the skill's grading (as in `rice_root.tsv`). Its statement that Xu 2021 has "no central-zone/stem-cell cluster" stands, and Xu 2025 fills that gap.

## Overlap with existing skill tables

There is no maize table in `references/markers/`. Same-family tables: `sorghum_leaf.tsv` (17 rows, leaf) and `sorghum_root_Guillotin2023.tsv` (maize v5 genes projected to sorghum; root). By v5 ID, 5 draft genes are in the Guillotin source list, all as root `expression` markers: TMO5-LIKE3 (Zm00001eb099400; Xylem there too), ZmPP2-A1 (Phloem), ZmGST41 (Epidermis_2), ZmDI19-like (Cortex_3) and one pith gene (Cortex_3). Only TMO5-LIKE3 and PP2-A1 agree on lineage. `sorghum_leaf.tsv` shares no gene directly. Its PEAR2, XCP1/IRX1/CESA7 and SUT1 rows reach maize only by homology, and only the xylem genes are expected to transfer to a young ear. Arabidopsis/rice tables give `function` markers for Xylem, Phloem, Epidermis and Dividing_cells by homology, but none for the inflorescence meristem domains.

Suggestion, not done: if this becomes `references/markers/maize_inflorescence.tsv`, consider a trait tag `Andropogoneae` (implies `grass C4`) for RA1. RA1 currently uses `requires=grass`.

## Could not verify / not accessed

- The ZmCLE7 v4/v5 ID (above). Ensembl's AGPv3→v5 coordinate mapping endpoint refused the AGPv3 slice. The MaizeGDB gene page gave no parsable content.
- The literature in situs cited through Xu 2021 (Jackson 1994, Chuck 2002, Gallavotti 2004, Vollbrecht 2005, Bortiri 2006, Satoh-Nagasawa 2006, Javelle 2011, Strable 2017) were not re-read. They are cited as reported by Xu 2021.
- The Xu 2025 ShinyCell portal (sc-jackson.maizegdb.org) returned 403 in the earlier review and was not used. The Xu 2025 Table S3 (maize mutants) and Table S4 (138 MB, GWAS) were not downloaded. The Molecular Cartography images were read from the Fig 1D thumbnail only.
- UniProt no longer indexes v4 IDs (free-text v4 queries return nothing). v4 IDs come from the MaizeGDB crosswalk, and the gene-name checks used v5.
- No in-data check: proportions and DE come from the papers' tables. Barcode matching and marker z-scores still need to be run on real data (Step 3b).
- PlantscRNAdb's third-party Xu 2021 zip was not found (earlier review). scPlantDB was not checked.

## Update 2026-10-20: gap-fill reviews

One new dataset was reviewed (folder `Wang2024/`, review in `Wang2024/README.md`). It was merged into `markers_draft.tsv` by v5 gene ID with `build/update_wang2024.py`. That script runs after `make_markers.py` (which rebuilds the Xu-only base table), and `make_expected.py` runs last. Every new v5/v4 pair was checked against the MaizeGDB v3 crosswalks, and every old row was kept. The table now has **73 rows** (56 + 17 new). Each changed row ends with a basis note starting `Update 2026-10-20 (Wang 2024):`.

### New dataset

| Dataset | Platform | Units | Label access | Gene IDs | Quality |
|---|---|---|---|---|---|
| **Wang Y, Luo Y, Guo X, ... Jackson D, Zhang Z, Xu X, Yan J, Liu H, Liu L, Yang N (2024)** *Nat Plants* 10:815-827. doi:10.1038/s41477-024-01683-2 (Europe PMC confirmed). CNGBdb CNP0004249; processed data in STOmicsDB MDESTA (not listed or downloaded) | Stereo-seq analysed at **bin50 (25 µm, several cells per bin)**, clustered on imputed expression; 4 sections of a 6 mm B73 ear. Also protoplast 10x scRNA-seq (2 replicates), projected onto the sections with STRIDE | 33,994 bins (S1S2 17,900; S3 7,126; S4 8,984); 19,583 scRNA cells | Per-bin spatial-domain table (`Wang2024/labels_spatial_bin50_TableS8-10.tsv`). scRNA: cluster numbers only, no names | B73 v5 | Medium. About 19 informative in situs (the authors themselves marked 9 of 28 probes as inconsistent) plus 24 literature genes compared with the Stereo-seq maps, and CRISPR function for MADS8/14. The labels are spatial domains, not cell types, and they differ between sections. Main text paywalled; supplements public |

**Independence:** the Wang study comes from a different lead lab (Yang/Liu, Huazhong) and has its own samples and platform. D. Jackson (the senior author of Xu 2021/2025) is a co-author, so the studies are independent data but not fully independent labs. Raises below count it as an independent study.

### Verdicts (Wang 2024 spatial domains → canonical types)

| Wang label | Verdict | Canonical |
|---|---|---|
| IMT (IM tip) | Revise | Central_Zone + apical L1 (WUS1/FEA4/LOG7 DE in 3 sections; proliferation confound; S3 IMT carries vascular genes) |
| IM | Revise | Meristem (inner IM / rib zone) |
| IMP | Revise | Meristem periphery / L1 flank (no specific gene) |
| ME (meristem epidermis) | Revise (merged) | Meristem_Epidermis + Spikelet_Meristem + Lateral_Organ + Meristem_Boundary |
| MI | Revise | Meristem (inner SPM/SM) |
| MB (meristem base) | Reject | RA1-3 not DE here |
| AMP | Reject | BA1 not DE here; positional only |
| DLO ("determinate lateral organs") | Revise (mislabeled) | Meristem_Base / Adaxial_Meristem_Periphery (top DE: RA1, RA2, RA3, BA1, 266820) |
| Vas | Revise (merged) | Vascular (lineage level); split with the Xylem/Phloem/Vascular_Sheath rows |
| Cortex, Pith-1, Pith-2 | Revise | Cortex, Pith (positional hypotheses only) |
| DMT/DMP sub-clusters (Fig 2) | Revise | Spikelet_Meristem (SM/FM; tip/periphery split not supported) |
| S3/S4 Cluster4/9/10/11 | Reject | unnamed |
| scRNA Sc-clusters 0-12 | Reject as labels | numbers only |

### Markers added (17)

- **Spikelet_Meristem** (new expected type, SM + FM): **ZmMADS8 Zm00001eb400120** and **ZmMADS14 Zm00001eb008690**, both `function`/high (in situ of the whole SM/FM dome, absent from the IM tip; the CR-mads8/14 double mutant turns florets into branches).
- **Meristem_Epidermis:** WOX3A/NS1 092480 and ASN synthetase 013430 (in situ, medium); Ser/Thr kinase 330590 and AP2/ERF 015020 (in situ, but their DE points elsewhere, so low); **OCL1 Zm00001eb126140** (medium). OCL1 is not a Wang review marker. It came from the survey's characterized table (Ingram 2000 L1 in situ), and its top Wang DE domain is ME in all 3 sections, which independently supports it.
- **Central_Zone:** ZmPIP2-5 077130 and NAC 264380 (apex in situ, low).
- **Meristem:** 165580 (in situ in the central core under the IM, medium).
- **Floral_Organ_Primordia:** **ZAG1 Zm00001eb284010** (low; see Conflicts).
- **Vascular** (new lineage-level type): HD-ZIP II 074830 and CASP-like 410980 (expression, low).
- **Pith:** MYB 067190 and 4CL 308860 (expression, low). **Cortex:** 189430 and GMD 377770 (expression, low).

### Existing markers raised by independent validation in Wang 2024 (9)

| Gene | Cell type | Change | Wang evidence |
|---|---|---|---|
| KCS Zm00001eb047970 | Epidermis | expression/medium → characterized_enriched/high | in situ in SPM/SM L1 (Fig 1e) |
| ZmLOG7 160700 | Central_Zone | low → medium | IMT DE in all 3 sections |
| FEA4 280500 | Central_Zone | low → medium | IMT DE in 3 sections; Stereo-seq matches the published in situ |
| 266820 | Adaxial_Meristem_Periphery | expression/medium → characterized_enriched/high | in situ on the IM periphery; top DE in DLO (= RA/BA1 domain) |
| RA1 312340, RA2 123060 | Meristem_Base | medium → high | Stereo-seq matches the literature in situs; DE in DLO |
| ZmYAB8/YAB15 248640 | Lateral_Organ | medium → high | Stereo-seq matches the Chen 2021 in situ |
| ZmTMO5-LIKE3 099390 | Xylem | medium → high | in situ in vascular strands (Wang probes this v5 model) |
| ZmTMO5 398190 | Xylem | low → medium | Vas DE in all 3 sections (vasculature-level agreement, as with ZNF30 and Xu 2025 c13) |

Support was noted in `basis` without a change for BA1, RA3, BD1, ZNF30, TMO5-LIKE3 099400 and PROPEP1 (all already high), and for WUS1, APL, MYB46 and SHR1. These four stay medium because 25 µm bins cannot resolve OC from CZ or the vascular sub-types. ZmYAB8's symbol is now `ZmYAB8/ZmYAB15`.

### Gaps closed

- **Meristem_Epidermis** (partly): it now has 6 specific rows (2 medium in situ, OCL1 medium, 2 low, plus PROPEP1 high), and KCS 047970 has an L1 in situ. There is still no `function`-grade L1-specific marker.
- **Determinate meristem:** the first `function`/high markers (MADS8/14) for spikelet and floral meristems, a domain the Xu datasets did not separate.
- **Central_Zone / Meristem_Base:** strengthened (LOG7 and FEA4 are now medium; RA1 and RA2 are now high).

### Gaps remaining

- **Floral_Organ_Primordia:** only ZAG1 (low). The survey characterized table has SI1/ZmMADS16 (`function`/high, Ambrose 2000, v4 Zm00001d036425). It was not added because it is not a Wang marker and its v5 ID was not checked. Add it after a v5 check.
- **Procambium:** no marker. Wang's Vas-specific HD-ZIP is class II, not III. Rice Oshox1 (characterized table) could serve by homology only.
- **Cortex, Pith:** expression-tier, low, positional in all three studies.
- **Phloem_Companion, Sieve_Element, Vascular_Sheath:** not resolved by Wang. ZmSUT1 (characterized table, Zm00001eb005460) is DE in Vas only in S4 and in Cortex in S1S2, so it was not added.
- **Epidermis of lateral organs, Guard, Trichome, S_Phase:** nothing new.
- **ZmCLE7:** still no v4/v5 ID. Wang does not report it.

### Recommended label reference

Unchanged: **Xu 2025 maize ear tip** remains the label reference. Wang 2024 labels are 25 µm spatial domains on imputed data. Several are merged or mislabeled (DLO, MB, AMP), and the domain sets differ between sections, so they are not cell-type ground truth. Use Wang 2024 for marker validation (in situs, plus spatial placement of RA/BA1, apex and vascular genes). If you use its bin labels, map them as in the verdict table above.

### Conflicts

- **Zm00001eb284010 is ZAG1** (NCBI Gene 542244 = LOC542244, aliases ZAG1/MADS37; the survey characterized table pairs it with v4 Zm00001d037737). The Wang review graded it as a Meristem_Epidermis marker from an unnamed in situ (outer layer of the IM apex and SMs, Supp Data 1 p6; at 70 dpi the signal looks broad over the IM tip and SMs). That does not match the published ZAG1 pattern (stamen/carpel primordia and inner FM, Schmidt 1993). The row was placed in Floral_Organ_Primordia at low and is **not** used as an L1 marker. Check it in data.
- **Wang figure ID errors:** WUS1 is labelled Zm00001eb067340 (UniProt: C3H1 zinc finger; the correct ID is 067310), and IDS1 and STS1 share one ID (062460, an AP2/ERF). Neither was used.
- **MADS8/MADS14 symbols:** Entrez 541985 calls Zm00001eb400120 "MADS14". The IDs follow Wang's probe table (S7) and Ensembl display names, so compare by ID.
- **Cortex gene 071050** (Xu 2021) is not cortex-DE in Wang (highest in AMP and the S4 Vas/IMT domains). It stays low, with the conflict noted.
- **Domain names:** Wang's "DLO" holds the RA/BA1 genes, and its "ME" holds the lateral-organ YABBYs, BD1 and MADS8/14. Map by marker content, not by label name.
- **FEA4** keeps its Xu 2021 conflict (enriched in MC3/4/8), although Wang supports the apex.

### Could not verify

- Wang main text and Methods (paywalled; not bypassed). The STOmicsDB MDESTA file list and sizes (JavaScript portal) could not be listed, and no h5ad or matrices were downloaded.
- Names of the Wang scRNA clusters (none exist in the tables).
- The kcs15 = Zm00001eb047970 link, inferred from matching images. The ZAG1 in situ was viewed only at 70 dpi.
- The literature in situs that Wang compared (Vollbrecht 2005, Bortiri 2006, Chuck 2002, Chen 2021, Pautler 2015) and Ingram 2000 (OCL1) were not re-read.
