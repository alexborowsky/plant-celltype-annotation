<!-- Collated from the survey review of tomato_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Tomato root: collated cell-type marker resources (Part A, Steps 1-4)

Date: 2026-10-20. Built from the two dataset reviews (2026-10-19) in `survey/merged_reviews.json` (group `tomato_root`), plus a re-check of primary tables and two papers the reviews cited but had not opened: Li et al. 2018 (Front Plant Sci) and Manzano et al. 2025 (Nat Plants). No single-cell data were re-analysed. The Kajala 2021 GEO count table (2 MB) was used for a CPM sanity check.

Files in this folder:

- `expected_cell_types.tsv`: written from tomato root anatomy (primary root tip, 0-3 cm). `function_markers` counts the `function` rows in `markers_draft.tsv`.
- `markers_draft.tsv`: 55 rows in the skill schema plus `alt_id` (73 after the 2026-10-20 update below). `ref_gene` is the unversioned Solyc ID. `alt_id` is the versioned ITAG4.1 gene ID as it appears in the Canto-Pastor 10x `features.tsv` (for example `Solyc03g097500.3`); it is empty for 1 row (SlbZIP11, which is not in ITAG4.1). Field counts are validated.
- `uniprot_id_check_group.tsv`: UniProt REST lookup (EnsemblPlants xref) for every `ref_gene`.
- `Kajala2021/`, `CantoPastor2024/`, `Yang2025/`: the per-dataset reviews (their README files are unchanged; `Yang2025/` was added in the update below).

## Datasets

| Dataset | Platform | Material | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Kajala et al. 2021 *Cell* 184:3333 (10.1016/j.cell.2021.04.024), GEO GSE149217 | **Not single-cell.** TRAP-seq of 10 promoter-defined populations + 2 constitutive lines; INTACT ATAC | M82, 1 cm primary root tips, 3-5 DAG; one transgenic line per construct | n/a (populations; 4-5 reps each) | ITAG3.2 | none (bulk). CTEG lists per population in Table S1 (`Cell2021_mmc1.xlsx`), core plate+field lists in Table S2 | high as a marker reference |
| Canto-Pastor et al. 2024 *Nat Plants* 10:118 (10.1038/s41477-023-01567-x), GEO GSE212403 | 10x 3' v3, protoplast scRNA-seq | M82, 7 d primary root, 0-3 cm, 2 reps | 22,207 after QC (22,734 GEO barcodes) | ITAG4.1 | cluster-level only, in figures (ED Fig. 4c, e). No per-cell table, cluster table or object; matrices 139 + 83 MB on GEO | medium |

Extra primary sources used to grade markers (not datasets): Li et al. 2018 *Front Plant Sci* 9:832 (PMC6024017; tomato promoter-GUS of SlMYB36a, SlPER64a, SlSGN3a/b, SlSHR), Manzano et al. 2025 *Nat Plants* (10.1038/s41477-024-01864-z, PMC11757151; SlCASP1/2/3 reporters, SlMYB36 and SlSGN3 mutants, SlEXO1, SlSCZ), Bucher et al. 1997 and 2002, Jones et al. 2008, Lauter et al. 1996, and Ron et al. 2014.

## Verdicts per expected cell type

A = Adopt, R = Revise, X = Reject/state, - = not resolved. Kajala "verdicts" apply to TRAP populations, not cells.

| Expected type | Kajala 2021 (TRAP population) | Canto-Pastor 2024 (scRNA label) | Best tomato markers |
|---|---|---|---|
| Trichoblast | - (inside EP) | A (Dif10/Dif54/EXT1) | SlEXT1, SlDif54, SlDif10 |
| Atrichoblast | - (inside EP) | R (transporters also in hair cells) | none reliable |
| Epidermis + LRC | R (EP = AtWER: epidermis + LRC) | - | - |
| Exodermis | A (EXO; reporters MYB41, WRKY71) | A, mature suberizing tip only | SlASFT, SlMYB41, SlGPAT4 (+GPAT5, MYB92, LACS4) |
| Cortex | A (iCOR); R (gCOR = cortex + exodermis) | A (layers not split) | SlGRAS18, SlCORTEX4, SlREO, SlPEP |
| Endodermis | A (EN; SCR; includes a QC tier) | A (CASPs, MYB36-b) | SlSCR, SlCASP1, SlCASP2, SlPER64a, SlMYB36-b |
| Pericycle | - (inside V) | A, medium (no tomato-validated marker) | SlPFA1 (expression) |
| Xylem | R (XY = AtS18 also marks epidermis) | A (one island; proto/meta not split) | SlIRX1, SlIRX5, SlXCP2, SlVND6 |
| Phloem | A at lineage level (PH; SE/CC not split) | R (merged with procambium) | SlAPL, SlCVP2, SlPL1 |
| Procambium | - (inside V) | R (merged with phloem) | none reliable |
| Stele (whole) | R (V = SlSHR domain) | - | SlSHR (weak) |
| QC | R (QC line = QC + all vascular initials) | R (merged; WOX5 not detected) | SlWOX5 |
| Columella / root cap | R (MiCO = meristematic cortex + columella) | R (RC & Col & QC merged) | none reliable |
| Meristem / dividing | X (MZ is a zone) | X ("Meristematic zone" = cyclins) | SlCycB1;1, SlCycA1;1 (state) |

## Recommended label reference

Neither dataset gives per-cell labels. **Use Canto-Pastor 2024 as the label reference for tomato root scRNA/snRNA** (same tissue, ITAG4.1, 10x). To use it, re-cluster the GEO matrices and re-derive its 10 coarse labels from the ED Fig. 4e panel. Then split RC/Col/QC and Phloem/Procambium, and treat "Meristematic zone" as the Dividing_cells state. **Use Kajala 2021 as the marker and validation reference:** the EXO, EN, iCOR and PH CTEG lists plus the SCR, WOX5 and APL anchors are the best tomato evidence for those types. Treat the EP, XY, V, MiCO and QC lists only as lineage hints. The two studies are not fully independent: Canto-Pastor called its clusters by overlap with the Kajala gene sets (same lab). Agreement between them therefore raised confidence by at most one level, and only for the same cell type (see below).

## Markers supported across studies

Confidence was raised one level for these 12 rows, because two independent sources agree on the same gene ID and the same cell type:

| Gene | Symbol | Cell type | Sources that agree |
|---|---|---|---|
| Solyc12g049070 | SlEXT1 | Trichoblast | Bucher 2002 promoter-GUS (trichoblast, not atrichoblast); CP scRNA; Kajala EP CTEG |
| Solyc03g082790 | SlDif54 | Trichoblast | Bucher 1997 (organ-level); CP scRNA |
| Solyc01g005880 | SlDif10 | Trichoblast | Bucher 1997; CP scRNA |
| Solyc02g079280 | SlMYB41 | Exodermis | Kajala promoter:nlsGFP + EXO CTEG; CP hairy-root mutant suberin phenotype |
| Solyc01g094700 | SlGPAT4 | Exodermis | CP mutant + scRNA; Kajala EXO CTEG |
| Solyc01g008910 | SlGRAS18 | Cortex | CP scRNA; Kajala gCOR+iCOR CTEG (AtPEP > SlPEP) |
| Solyc04g077260 | SlMYB36-b | Endodermis | Li 2018 promoter-GUS; CP scRNA |
| Solyc12g089360 | SlPER64a | Endodermis | Li 2018 promoter-GUS; Kajala EN CTEG |
| Solyc12g017370 | SlAPL | Phloem | Kajala PH (79 vs <=4 TPM); CP phloem/procambium |
| Solyc09g082370 | SlCVP2 | Phloem | Kajala PH CTEG; CP phloem/procambium |
| Solyc02g031740 | SlPL1 | Phloem | Kajala PH CTEG; CP phloem/procambium |
| Solyc10g078330 | SlCycB1;1 | Dividing_cells | CP meristem cluster; Kajala MZ line highest |

In addition, SlCASP1 (Solyc06g074230) and SlCASP2 (Solyc10g083250) are endodermis by reporter and CS localization (Manzano 2025) and specific in CP. They are graded `function`/high on that basis and are counted as cross-study (14 in total). Agreement that was only at stele level (Kajala V vs CP Xylem or Procambium) was not counted: SlIRX1, SlIRX5, SlXCP2, SlHCA2.

## Gaps (expected types without a validated tomato marker)

- **Columella, Lateral_Root_Cap, Root cap:** no tomato marker with reporter evidence. SlSGR9 conflicts between the studies, and SlFEZ and SlARF10A are low. Use Arabidopsis SMB/BAM2 via homology and check in the data.
- **Quiescent_Center / Stem_Cell_Niche:** only SlWOX5, whose tomato domain includes the vascular initials and which is barely detected in protoplast scRNA. SlPLT3 is uncertain (ID conflict).
- **Atrichoblast:** no specific marker. The transporters are epidermis-wide. Try GL2/WRKY44 orthologs.
- **Pericycle:** no tomato-validated marker, and XPP/PPP are not split.
- **Procambium, Phloem_Companion vs Phloem_Sieve_Element:** unresolved in both datasets.
- **Protoxylem vs Metaxylem:** pan-xylem markers only.
- **Cortex:** no `function` marker (four reasonable `characterized_enriched`/`expression` markers).
- **Lateral_Root_Primordium:** not addressed.

## Conflicts and corrections

1. **CASP naming differs by paper.** The same IDs are Solyc06g074230 = SlCASP1 (CP, Manzano) = SlCASP1b (Li 2018); Solyc10g083250 = SlCASP2 = SlCASP1a; Solyc09g010200 = SlCASP3 = SlCASP1c. Compare by ID.
2. **CASPs are not EN CTEGs in Kajala 2021.** All three are in the **MZ** list, and their TRAP CPM is highest in the SlRPL11C (MZ) line, not the SlSCR line. CP scRNA and the Manzano reporters both say endodermis, so the table follows them and records the conflict.
3. **The review's SlCASP "validation" overstated Li 2018.** Li 2018 did not make tomato CASP reporters; it listed the homologs and tested the *Arabidopsis* CASP1 promoter in tomato. The tomato CASP reporters are in Manzano 2025, where SlCASP3's reporter is also in cortex and exodermis (so SlCASP3 was downgraded to characterized_enriched/medium).
4. **There are two MYB36 genes.** Solyc04g077260 is "SlMYB36a" in Li 2018 (GUS in endodermis) and "SlMYB36-like" in CP, but Manzano 2025 shows its mutant keeps the CS (SlMYB36-b). The functional ortholog is **Solyc07g006750** (mutant lacks CS). Both are in the table: the first as an expression marker, the second as `function`/medium. Its endodermal TRAP enrichment (Manzano ED Fig. 3i) did not reproduce in median CPM from the GEO counts.
5. **SlMYB41 (Solyc02g079280):** the Kajala review sourced the mutant evidence from Jo 2025. It is in CP itself: hairy-root slmyb41 mutants have exodermal suberin phenotypes (ED Fig. 6). The same ID is slmyb107a (Manzano 2025) and MYB102 (UniProt).
6. **SlASFT** is listed as a **QC** CTEG in Kajala Table S1. CP's reporter is exodermis-specific; TRAP CPM is highest in SlPEP among the cell-type lines.
7. **SlREO** is a cortex promoter (Jones 2008) and cortex in CP, but an **EXO** CTEG in Kajala (SlPEP 434 vs AtPEP 214 CPM). It was not raised.
8. **SlSGN3 (Solyc05g007230):** the GUS reporter is endodermis-specific in Li 2018, but the GFP reporter covers endodermis, inner cortex and exodermis in Manzano 2025, and it is an EXO+gCOR CTEG in Kajala. It is kept as a low-confidence endodermis marker. SlSGN3b (Solyc03g112680) is not in ITAG4.1 and is in the Kajala cortex lists, so it was not carried.
9. **PLT3 is two different genes:** CP's SlPLT3 is Solyc05g051380, while Kajala Table S1's "PLT3" is Solyc11g010710. Both are AP2/ERF in UniProt, and neither name was checked by phylogeny.
10. **SlSGR9 (Solyc09g007060):** CP puts it in RC/Col/QC; Kajala has it in the cortex lists (at very low level).
11. **SlLTPG5:** a CP exodermis top gene, but an EP CTEG in Kajala.
12. **IDs:** SlFAR3B is Solyc11g067180 (the CP text's Solyc11g067190 does not exist in ITAG4.1). SlbZIP11 (Solyc03g033730, ITAG3.2) is not in the ITAG4.1 features, and neither is SlSGN3b. These are in ITAG4.1 but not UniProt: Solyc01g095750 (LACS4), Solyc11g067180, Solyc08g078900 (CORTEX4), Solyc01g150101 (PFA1), Solyc09g007060 (SGR9), Solyc10g078330 (CycB1;1). The Kajala preprint's VND7 is VND6 in the Cell tables (Solyc06g034340). UniProt names Solyc04g077210 KN1 (Kajala: SlKNAT1).
13. **LeAMT1;1 (Solyc09g090730)** is an "atrichoblast" marker in CP, but Lauter 1996 reports it as root-hair-preferential. It is kept as low, epidermis-level.
14. **Grading changes from the reviews:** SlbZIP11 and SlKNAT1 were moved from `function` to `characterized_enriched`, because overexpression phenotypes show capacity, not cell-type identity. SlEXO1 is low as an exodermis marker: it is equal in the cortex and exodermis TRAP lines, and its mutant phenotype is in the inner cortex.

## Overlap with existing skill tables

The skill has no tomato table. The tomato rows overlap by orthology with `arabidopsis_root.tsv` for SCR, CASP1-3, MYB36, PER64, SHR, WOX5, APL, DOF5.6/HCA2 (Phloem in the Arabidopsis table; Procambium here) and PLT. There are no Exodermis rows anywhere except `rice_root.tsv`, whose exodermis biology differs (rice forms a Casparian band; tomato forms a polar lignin cap and suberin). Tomato exodermis rows carry `requires=Solanaceae`. `arabidopsis_leaf.tsv` mentions tomato only to say that GL1 has no tomato ortholog. For tomato data, the Arabidopsis root table via homology adds function markers mainly for LRC (SMB), Atrichoblast (GL2, WRKY44), Procambium (OPS, AGO10) and Pericycle (GATA23), which are the gaps here.

## What could not be verified

- The Cell full text of Kajala 2021 is paywalled; the review used the bioRxiv preprint and the open Cell supplements.
- AtS32 (PH) and AtS18 (XY) libraries could not be matched to columns of the GEO count table, so the PH/XY numbers come from Table S1 only (APL 79 TPM), not from a CPM re-check.
- The "validated in S. lycopersicum" references for SlGRAS18, SlPT1, SlST1, SlHAK5 and SlARF10A (Bouzroud 2018) in CP ED Fig. 4e were not opened.
- Bucher 1997 (Dif10/Dif54) was read as an abstract only: organ-level mRNA, no cell-resolution data.
- Whether scPlantDB or another portal hosts re-annotated per-cell labels for GSE212403 was not checked.
- Other tomato root single-cell datasets were not searched for in this collation, because it was limited to the two reviewed datasets.
- No in-data check (Step 3b) has been run; every confidence level is desk-based.

## Update 2026-10-20: gap-fill reviews

One new dataset was reviewed (`Yang2025/README.md`) and merged into `markers_draft.tsv` by gene ID. The 55 original rows were all kept: 4 were edited (1 raise, 3 basis/source additions) and 18 rows were added (73 in total). Field counts were validated (13 columns on every line). `alt_id` follows the existing convention (ITAG4.1 versions from the Canto-Pastor `features.tsv`). Yang uses ITAG4.0, and the version differs for 3 genes: CHUP1 (.3 in Yang, .4 here), HSFA2-like (.4 / .5) and Histone H3 (.4 / .5). IDs were checked against UniProt (EnsemblPlants xref). Solyc05g006850 has no UniProt entry but is in the ITAG4.1 features. No `characterized_markers.tsv` row (survey/characterization) for `tomato_root` matches a new gene ID. The tomato SBRL, SlEXO1 and SlSCZ rows there cover Lateral_Root_Primordium and ground tissue, which Yang 2025 does not address.

### New dataset

| Dataset | Platform | Material | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Yang et al. 2025 *bioRxiv* 2025.12.27.696651 (10.64898/2025.12.27.696651; Europe PMC PPR1229888), SRA PRJNA1218210, Figshare project 236603 | 10x Chromium protoplast scRNA-seq; apparently one library | Heinz 1706 **adventitious roots** (0.1-1 cm) from excised stems, 55 h | 7,920 cells, 12 clusters (2 left Unknown, 18%) | ITAG4.0 (versioned) | `table`: per-barcode labels (`Slar_published_cell_annotations.csv`) plus a per-cluster pseudobulk table | low as a label reference; medium as a marker source for phloem and stele |

### Verdicts (Yang 2025)

| Published label | n (%) | Verdict | Maps to |
|---|---|---|---|
| Phloem | 180 (2.3) | Adopt | Phloem (SE and CC not split) |
| Root stele | 1144 (14.4) | Revise | Stele (contains xylem, pericycle and procambium) |
| Root cortex | 778 (9.8) | Revise | Cortex (layers merged; no exodermis or endodermis markers in any cluster) |
| Root epidermis | 401 (5.1) | Revise | unresolved (defence-gene profile; SlPLT3, SlFEZ, SlARF10A and SlPT1 peak here) |
| Root cap | 899 (11.4) | Revise (hypothesis) | Root_Cap? (authors call it putative) |
| Protoxylem | 881 (11.1) | Reject | unresolved (no xylem markers) |
| Root hair | 797 (10.1) | Reject | - (SlEXT1/Dif54/Dif10 ~0 everywhere) |
| Non-hair | 624 (7.9) | Reject | - |
| Lateral root cap | 591 (7.5) | Reject (state) | Protoplasting_stress (heat-shock) |
| QC | 210 (2.7) | Reject (state) | Dividing_cells |
| Unknown_1, Unknown_8 | 926 + 489 | Reject (unassigned) | - (left unlabelled by the authors, correctly) |

### Markers raised or updated

- **SlPL1 (Solyc02g031740), Phloem: medium -> high.** This is the third study to agree, and the first from a different lab (Kajala PH CTEG, Canto-Pastor phloem/procambium, Yang phloem 0.68 vs <=0.06).
- **SlAPL (Solyc12g017370), Phloem:** already high. Yang was added to `basis` and `source` (0.30 vs <=0.01).
- **SlCORTEX4 (Solyc08g078900), Cortex:** Yang was added (0.42 vs <=0.13). It was not raised: the gene is uncharacterized (`expression` tier, capped at medium), and the Yang cortex label is merged.
- **SlCycA3;1 (Solyc12g088530), Dividing_cells:** it is also specific to the Yang "QC" proliferation cluster (0.13 vs <=0.01). This was noted, not raised: there are two cluster calls and no validation.

### Markers added (18)

- **Phloem (4):**
  - CHUP1 (Solyc09g008660; characterized_enriched/medium; in situ in the peripheral stele, figure not viewed)
  - DUF7866 (Solyc09g005200; expression/medium)
  - unnamed Solyc05g006850 (expression/medium)
  - LeMT(A) (Solyc04g058150; expression/low)
- **Stele (2):** DOF11 (Solyc03g082840; expression/medium), XSP10 (Solyc03g079880; characterized_enriched/low).
- **Cortex (1):** Organ-specific protein S2 (Solyc10g009150; expression/low).
- **Root_Cap (1):** UP1261-X1 (Solyc03g083010; expression/low). It has in situ signal at the AR tip but is only weakly enriched in the data, so treat it as a hypothesis.
- **Protoplasting_stress (7, kind=state):**
  - ERF109/ERF-D4 (Solyc10g050970), **medium**. It is in both Canto-Pastor 2024 Table S2 (logFC 9.8) and the Yang stress clusters, which are independent.
  - HSFA2-like (Solyc08g062960), CLPB1 (Solyc03g115230), HSP90-1 (Solyc03g007890), HSP90/HSP83A (Solyc06g036290), HSP17.4B (Solyc03g123540) and HSP70-5-like (Solyc03g117630), all low.
- **Dividing_cells (3, kind=state):** Histone H4 (Solyc04g011390), H3 (Solyc01g086820) and H2A.1 (Solyc01g099410), all expression/low. H3 and H4 are multicopy families.

Not carried: **LEA3 (Solyc09g075210)**. The authors' in situ shows a stele gradient, but the gene is detected in 57-96% of cells in every cluster, so it is not a usable marker.

### Gaps

- **Closed (partly):** Protoplasting_stress now has tomato state rows (it had none). Phloem is strengthened (SlPL1 high, plus CHUP1).
- **Still open:** Columella, Lateral_Root_Cap, Root_Cap (UP1261-X1 is a low hypothesis only), Quiescent_Center, Stem_Cell_Niche, Atrichoblast, Pericycle, Procambium, Phloem_Companion vs Phloem_Sieve_Element, Protoxylem vs Metaxylem, Cortex `function` marker, and Lateral_Root_Primordium. The study was recommended for root cap, LRC and QC, but it fills none of them.

### Conflicts and caveats (new)

1. **Heat-shock genes vs Canto-Pastor's protoplasting list.** Of the 7 stress genes, only ERF109 is in Canto-Pastor 2024 Table S2 (821 genes, tomato root, logFC > 2). The HSP/HSF genes come from Arabidopsis (Denyer 2019) orthologs. The heat-shock state may therefore be specific to the Yang protocol (or to 55 h excised stems) rather than general to tomato protoplasting. In other tomato data, check for it before using the HSP rows.
2. **Tip regulators peak in Yang's "Root epidermis" cluster.** SlPLT3, SlFEZ, SlARF10A and SlPT1 are all highest in C9. This is consistent with distal-tip or cap-lineage cells, or with an epidermis that has regulators in it. The cluster's identity is unresolved, so the existing rows were not changed.
3. **Endodermis and exodermis markers are near zero in Yang.** SlCASP1-3 and SlPER64a have weak maxima (<=0.09) in the "Protoxylem" cluster, and SlASFT, SlGPAT4/5, SlSCR and SlMYB36 are ~0 everywhere. Either these layers were not captured in the young adventitious roots, or they are merged into other clusters. This is not counted against the existing rows.
4. **SlCycB1;1 (Solyc10g078330) is ~0 in Yang** (max 0.01), even in the proliferation cluster. SlUXS6 and SlKNAT1 (Xylem rows) peak in Yang's cortex rather than its stele (0.23-0.29, weak). These were noted, not acted on: it is a single library from a different organ.
5. **Documentation problems in Yang 2025.** The clustering parameters differ between the Methods and the Figshare README. The composition percentages in the Results are wrong (the authors have corrected them). Do not use the older `slar_final.rds` / `slar_labeled.rds` objects (a different 21-cluster annotation).

### Recommended label reference (unchanged)

**Canto-Pastor 2024 remains the label reference** for tomato primary root tips. Yang 2025 is the only tomato root dataset with public per-cell labels, but most of its labels are rejected or revised, and it comes from adventitious roots in a single library. Use its labels only for **Phloem** (Adopt) and coarse **Stele**. Map its "QC" to Dividing_cells and its "Lateral root cap" to Protoplasting_stress. Its pseudobulk table is a useful third check for phloem and stele markers.

### Could not verify (Yang 2025)

- bioRxiv blocked scripted access (Cloudflare 1015 / HTTP 429). Fig 1e (the marker dotplot), Figs S1-S2 and the in situ images (Fig 1g-j) were not seen.
- Table S4 (cluster markers) and the originally posted supplementary tables are not on bioRxiv or Figshare. Marker IDs come from the authors' pseudobulk table and the figure legends.
- The single-library design is inferred: the label table has no sample column.
- The large objects (`.rds`, 1.5-2 GB each; 10x matrix 368 MB) were not downloaded. Their URLs are in `Yang2025/README.md`.
