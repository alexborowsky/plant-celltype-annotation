<!-- Collated from the survey review of wheat_inflorescence (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Wheat inflorescence (spike): collated cell-type resources

Collated 2026-10-20 for the plant-celltype-annotation skill. The skill was not edited.

Inputs: the three reviews for this group in `survey/merged_reviews.json` (Xu 2025, Long 2026, Zhang 2026; each review's README is in its folder). The `Liu2025/` folder holds downloaded tables but has no review entry or README, so I did a light check of it here (main-text annotation section, Tables S1, S3, S5). Liu 2025 is the only dataset with a small per-cell table for nuclei.

Files here:
- `expected_cell_types.tsv`: cell types expected at W2.5–W5 (double ridge to carpel primordium), written from spike anatomy. `function_markers` counts the `function` genes (not homoeolog rows) for each type in `markers_draft.tsv`.
- `markers_draft.tsv`: 80 marker genes in 223 rows. Schema: the skill's marker-table columns plus `alt_id`. Field counts were checked with awk.
  - `ref_gene` is the IWGSC RefSeq **v1.1** ID (`TraesCS..02G......`), with one row per homoeolog. `alt_id` is the RefSeq **v2.1** ID (`TraesCS..03G.......`), taken from the IWGSC correspondence table (`iwgsc_refseq_all_correspondances.csv`, URGI). All 223 IDs map.
  - Homoeologs come from the papers' tables: Long Table S1 lists `homoeolog_gene_ids`, and Xu Table S1 gives the A and B copies. Where neither paper names the third copy, I took the Ensembl Plants `homoeolog_one2one` call. The `basis` field says when an ID came from Ensembl.
  - Kronos (tetraploid) IDs are not stored. They are in `Xu2025/tables/Table_S1.tsv`.
  - Use `map_markers.py --no-blast` for RefSeq v1.1 data, or `--id-column alt_id` for v2.1 data.
- `Xu2025/`, `Long2026/`, `Zhang2026/`: the dataset reviews and their downloads (not modified). `Liu2025/`: downloads only.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Xu2025 | Xu X ... Dubcovsky J. *Genome Biol* 2025. doi:10.1186/s13059-025-03811-3 | Tetraploid Kronos spikes at W2.5 and W3.5. Protoplast scRNA-seq (10x v3.1) plus Resolve smFISH (99 genes, cell-segmented, W1.5–W3.5) | scRNA: 26,009 cells; 8,726 cell-cycle cells removed, leaving 17,283 in 23 clusters. smFISH: 48,225 cells in 21 clusters | scRNA: `large_object` (1.16 GB Seurat .rds in a 2.9 GB Zenodo zip). smFISH: small per-cell table (`Xu2025/smFISH_cell_labels.tsv`) | medium for labels; high as a spatial reference |
| Long2026 | Long KA ... Uauy C. *Plant Cell* 38:koaf282 (2026). doi:10.1093/plcell/koaf282 | Hexaploid Paragon NILs (VRT-A2a and VRT-A2b), W2.5–W5. MERFISH, 200-gene panel; probes do not separate homoeologs | 50,731 cells in 18 expression domains (ED0–ED17) | `table` inside a 137.8 MB Zenodo tar (not downloaded). Labels belong to MERFISH cells and cannot be transferred to sc/snRNA barcodes | medium (organ-level domains, one section per stage and genotype) |
| Zhang2026 | Zhang X ... Su YH. *Mol Plant* 19:402–424 (2026). doi:10.1016/j.molp.2025.12.020 | BMKMANU S1000/S3000 cell-segmented spatial (W2.0–W3.5) plus 10x snRNA-seq at W3.5 | 53,167 spatial cells (median 724 genes); 16,353 nuclei | `none`: data unreleased (PRJCA032338), portal down. Cluster tables only | low for labels; medium for its in situ markers |
| Liu2025 | Liu X ... Uauy C, Xiao J. bioRxiv 2025, doi:10.1101/2025.01.18.633750 (also Research Square rs-6080581). Preprint, **not formally reviewed** | Hexaploid snRNA-seq (DNBelab C4, 12 libraries, W2.5–W5) plus snATAC, scStereo-seq (W3.25, W4) and Long's MERFISH | 73,729 nuclei in 20 clusters (R0–R19); 20,183 scStereo cells | `table`: per-nucleus labels in Table S1 (4.9 MB; `Liu2025/TableS1_snRNA_cell_metadata.tsv`). Cluster names are in `Liu2025/cluster_to_celltype.tsv` | low–medium (labels are stage-confounded; see below) |

The datasets are not all independent. Liu 2025 shares authors (Uauy, Long, Lister) with Long 2026 and used Long's MERFISH data to annotate its clusters. So a gene that Long 2026 validates spatially is not confirmed again by being specific in a Liu cluster. I counted Liu as independent only when it agreed with Xu or Zhang. Xu, Long and Zhang come from three separate groups.

Not collated: Qu et al. 2026 *Sci Adv* (Stereo-seq bin domains, listed in `survey/all_datasets.tsv`) has no review.

## Per-cell-type verdicts across datasets

Abbreviations: sc = Xu scRNA cluster; c = Xu smFISH cluster; ED = Long MERFISH domain; R = Liu snRNA cluster. Zhang's labels are its own spatial cluster names.

| Expected type | Xu2025 | Long2026 | Zhang2026 | Liu2025 |
|---|---|---|---|---|
| Epidermis | sc7, sc13, sc15: **Adopt**. sc5: Revise (weak). sc16: Revise (cycling) | ED4 L1 & epidermis: **Adopt**. ED1: Revise (glume, lemma and leaf epidermis merged). ED14 stamen epidermis: **Adopt** | LOP-1 (nsLTP in 99% of cells): Revise, probably protoderm | R3: **Adopt** (FDH, DCR, ROC7, SCR) |
| Shoot_Meristem / Spikelet_Meristem | sc20: **Adopt** (IM/SM and FM mixed). c8 early SM and IM: **Adopt** (spatial) | ED0: Revise (meristem plus base; IM, SM and FM not separated) | SP-1/SP-2: Revise. These are S-phase and G2/M states (~40% of cells) | R15 "spikelet primordium": Revise (PIN1, TFL1, SHR; partly provascular) |
| Floret_Meristem | c18: **Adopt** (spatial). c17 LFY band: Adopt (positional). sc14: Revise (stress-correlated) | ED7 floral organ primordium base: Revise | LOP-2: Revise (weak detection; plausibly floret primordium) | R14 "floret": **Adopt** as a merged floret class (AGL6, SEP3, B- and C-class) |
| Organ_Boundary | sc9 adaxial boundary, sc11 glume axilla: **Adopt**. c14 and c16: Adopt (spatial) | ED11: Revise (top gene CycD3) | SPB: Revise (positional) | R0/R1/R5/R9 "spikelet base" (33% of nuclei): Revise. These are stage-split (R1 is 90% W2.5, R5 95% W3) KNOX-high cells, not a boundary type |
| Suppressed_Bract | sc1: Revise (mixed with ground tissue). sc15: Adopt as epidermis. c6 and c19: Adopt (spatial). sc8: Revise (positional) | ED12 leaf ridge: **Adopt** | LBP: Revise (leaf primordia merged in) | – |
| Axillary_Meristem | – | ED9: Revise (merged with leaf); MND1 marks the AMs | – | – |
| Lateral_Organ_Primordium / Glume / Lemma | c7 glume and lemma: Adopt (spatial). No scRNA cluster | ED2 (glume, lemma and leaf): Revise. ED8 midrib: Revise | LOP-1: Revise | R10 "glume/lemma" (98% W5; high RBCS): Revise |
| Palea, Lodicule | – | ED15 palea: **Adopt**. ED17 lodicules: **Adopt** | – | inside R14 |
| Stamen_Primordium | inside sc20 and c18 | ED10 stamen: **Adopt** (labelled "16" in the Zenodo xlsx) | – | inside R14. **R19 "ovary": Revise → anther (Stamen_Primordium)**; see Corrections |
| Carpel_Primordium | inside c18 | ED16 carpel: **Adopt** | – | – (R19 is not carpel) |
| Rachilla | – | ED5: Revise (weak label) | – | – |
| Ground_Tissue / Chlorenchyma | sc6, sc10, sc12: Revise (merge; photosynthesis-defined). sc2, sc4: Revise. sc17: Reject | ED3 developing rachis: **Adopt** | LR/UR: Revise (positional rachis) | R8 pith, R6/R13 cortex: Revise (photosynthesis-defined; R13 is 97% W3) |
| Intercalary_Meristem | c10: Adopt (spatial) | – | – | – |
| Procambium / Phloem / Xylem | sc18: Revise; split into sc18_1 phloem and sc18_2 xylem. sc19: Revise (cycling). c4/c13: **Adopt** (provascular) | ED6, ED13: Revise (vascular types merged) | not resolved | R12 → Phloem-leaning (CALS7, JUL1, DOF), R17 → Xylem-leaning (VND, XCP, TMO5L1): both Revise from "vasculature" |
| S_Phase / Dividing_cells | 9 removed clusters plus sc0, sc16, sc19, sc21: state | panel has almost no cell-cycle genes | SP-1 (S), SP-2 (G2/M): state | R2 (G2/M), R4/R7/R11 (G1/S): state |
| Wound_response | sc3, sc22 (protoplasting): **Reject** | – | BZ basal zone: Revise (cut end, JA/wound genes) | R18 (W2.5 only; hypoxia/glycolysis and WRKY genes): **Reject**. R16 unnamed, epidermis-like: Reject (unknown) |
| Phloem_Companion, Sieve_Element, Meristem_Central_Zone, Organizing_Center, Ovule, Stomatal_lineage | not resolved | not resolved | not resolved | not resolved |

## Cross-study markers (confidence raised one level)

These 29 genes have the same RefSeq v1.1 triad validated in one study (smFISH, MERFISH or in situ) and validated or cluster-specific for the same type in another independent study. For Xu's epidermal and vascular genes, Xu's support is scRNA cluster DE; its smFISH "imputation" does not count as validation.

| Cell type | Gene (v1.1, one homoeolog shown) | Symbol | Studies |
|---|---|---|---|
| Epidermis | 7A02G308400 | ROC7 | Long ED1/4 MERFISH; Xu sc7/13/15 (also Liu R3) |
| Epidermis | 1D02G197300 | ROC3/OCL4-like | Long MERFISH (matches ZmOCL4 in situ); Xu epidermal clusters |
| Epidermis | 4D02G296400 | FDH/ONI1 | Long MERFISH; Xu epidermal clusters; Liu R3 |
| Epidermis | 1D02G343400 | PEL3/DCR | Long ED4-unique; Xu epidermal clusters; Liu R3 |
| Epidermis | 4A02G191300 | SCR2 | Long ED1-unique; Xu epidermal clusters; Liu R3 |
| Shoot_Meristem | 4A02G256700 | KNOX5/KN1 | Long ED0 (matches ZmKN1 in situ); Xu smFISH; Zhang UR |
| Organ_Boundary | 7D02G246100 | CUC3 | Long ED11 MERFISH; Xu sc13 |
| Organ_Boundary | 5A02G207300 | TCP24 | Xu smFISH c16; Zhang SPB |
| Suppressed_Bract | 1A02G418200 | TSH1/TRD1/NL1 | Long ED12-unique; Xu sc8; Zhang LBP |
| Suppressed_Bract | 5A02G265900 | SPL17 | Long ED12-unique; Xu smFISH c19; Zhang LBP |
| Suppressed_Bract | 6A02G287300 | LEC1 | Long ED12-unique; Zhang LBP |
| Lateral_Organ_Primordium | 1D02G162600 | YABBY1 (OsYABBY3) | Long ED2/12/13; Zhang LOP-1 |
| Lateral_Organ_Primordium | 2A02G386200 | TOB1 (OsYABBY5) | Zhang in situ; Long ED2/8 |
| Lateral_Organ_Primordium | 1A02G052000 | WOX3/LSY1 | Zhang in situ (1B copy); Long ED17 (1A copy) |
| Glume | 7D02G120500 | SEP1-4 (OsMADS5) | Xu smFISH c7; Long ED2; Zhang in situ |
| Lemma | 4A02G058900 | SEP1-2 (LHS1) | Xu smFISH c7; Zhang LOP-2; Liu R10 |
| Floret_Meristem | 6A02G259000 | AGL6 | Xu smFISH c17/c18; Zhang in situ |
| Floret_Meristem | 7D02G261600 | SEP3-1 | Xu smFISH c18; Long ED10/14/16/17 |
| Floret_Meristem | 5A02G286800 | SEP3-2 | Xu smFISH c18; Long |
| Stamen_Primordium | 7A02G383800 | AP3 | Long ED10/14/17; Xu c18 |
| Stamen_Primordium | 1A02G264300 | PI1 | Long (matches TaPI1 in situ); Xu c18 |
| Stamen_Primordium | 3A02G406500 | PI2 | Long; Xu c18 |
| Stamen_Primordium | 1D02G127700 | AG1 | Long ED10/14/16; Xu c18 |
| Ground_Tissue | 1B02G042200 | MT2 (1B only) | Long ED3-unique; Zhang LR |
| Procambium | 7A02G190600 | PIN1a | Xu smFISH c4/c13; Long ED6/13 |
| Procambium | 1A02G077800 | LAX4 | Xu smFISH c4; Long ED6/13 |
| Procambium | 2A02G192600 | SHR1 | Long ED6/13; Xu sc18 |
| S_Phase | 3D02G075900 | H2B.1 | Zhang in situ; Liu R7/R4 |
| Xylem | 5A02G138700 | XCP1 | Xu sc18_2 and Liu R17. Both are cluster-level, so this was raised only from low to medium |

Raised from function evidence alone, not from cross-study agreement: FZP is `high` because of smFISH plus the CRISPR phenotype in one study (Xu 2025).

## Gaps (expected types with no validated marker)

- **Inflorescence_Meristem**: no IM-specific gene in any dataset. Call it by tip position.
- **Meristem_Central_Zone, Organizing_Center**: no CLV3/FON2-like or WUS signal with an ID anywhere.
- **Lodicule**: only the B-class-plus-AGL6-without-AG code, and PLT8-like (`expression`, low; conflicting with Liu).
- **Rachilla**: only KNOX3 (`expression`, low; Long ED5 is a weak label).
- **Glume**: SEP1-4 is high but `characterized_enriched` and also in lemma. There is no glume-identity `function` gene.
- **Phloem_Companion, Sieve_Element**: none. Use rice/sorghum SUT1 and Arabidopsis SEOR1 via homology.
- **Ovule, Stomatal_lineage**: not expected before W5.
- **Ground_Tissue, Chlorenchyma, Procambium, Axillary_Meristem**: covered only by `characterized_enriched` rows (no `function` gene).
- **Xylem/Phloem split**: only Xu sc18 subclusters and Liu R12/R17 separate them. No wheat in situ, apart from APL smFISH, which has low detection.

## Recommended label reference

- **For a protoplast or nuclei sc/snRNA query:**
  - **Xu 2025** is the best-annotated scRNA reference. Its annotation is evidence-integrated and unknowns are left unforced.
  - Exporting Xu's per-cell labels needs the 1.16 GB .rds (an R job), and the cell-cycle cells were removed before final clustering.
  - Use its Adopt labels: Epidermis (sc7/13/15), Organ_Boundary (sc9, sc11), meristem sc20. Use the sc18 split for vasculature.
- **For nuclei, or when a small table is needed:** Liu 2025 Table S1 (73,729 nuclei, W2.5–W5, RefSeq v1.1) is the only small per-cell table. Before reuse:
  - relabel R19 as anther (Stamen_Primordium);
  - treat R2, R4, R7 and R11 as states;
  - merge R0/R1/R5/R9 and R6/R8/R13 as stage-split ground and meristem-base cells;
  - split vasculature into R12 (phloem-leaning) and R17 (xylem-leaning);
  - drop R16 and R18.
- **For marker validation and positions:** use Long 2026 MERFISH and Xu 2025 smFISH. These spatial labels cannot be transferred to droplet barcodes.
- **Zhang 2026:** use only its in situ markers.

## Conflicts and corrections

1. **Zhang 2026 "TaLHS1" (Table S3) / "TaAGL6" (Table S4) = TraesCS7D02G120500 is SEP1-4, the OsMADS5 ortholog, not LHS1.**
   - Ensembl Plants calls its rice ortholog Os06g0162800 (UniProt Q0DEB8, OsMADS5), and Long Table S1 agrees.
   - Zhang's own table pairs it with rice Os03g0215400 (OsMADS1/LHS1). That pairing is wrong.
   - The true LHS1 ortholog is SEP1-2 (TraesCS4A02G058900 / 4B02G245700, "WLHS1-A").
   - The Zhang2026 review README says to "use the LHS1 assignment". That advice is corrected here: the gene is in the table as Glume SEP1-4.
2. **Liu 2025 R19 "ovary" is most likely developing anther.**
   - Its "TaBHLH10" marker (TraesCS7A02G117100/7B02G014500/7D02G113100) is the ortholog of rice TIP2/OsbHLH142 (UniProt Q5JNS0), a tapetum and anther-wall regulator.
   - R19 also expresses AP3 (0.61 vs 0.04), SEP3 and MSP1/EMS1 (UniProt Q8RZV7).
   - The marker is listed under Stamen_Primordium.
3. **Zhang 2026 Table S4 mislabels SPL14.** It calls TraesCS7A02G246500 "TaSPL17", but Xu and Long both call it SPL14 (rice ortholog Os08g0509600 = OsSPL14). It also calls the 7D copy "TaSPL15". The real SPL17 is TraesCS5A02G265900.
4. **Zhang 2026 "TaGASA"** (TraesCS2A02G041400) is an FAAH-like amidase, as the Zhang review noted. It is not used here.
5. **SPL14 location disagrees between studies.** Xu: suppressed bract (smFISH c6, plus the mutant). Long: rachis ED3 and ED12. The SPL14 row stays at medium confidence.
6. **CEN5/TFL1 (TraesCS5A02G128600 triad) location disagrees.** Xu: vasculature c13 (0.75 vs 0.04, smFISH). Liu: spikelet primordium R15. Listed under Procambium, medium.
7. **TMO5L1 (TraesCS5A02G230500) location disagrees.** Xu sc18_2 and Liu R17: xylem. Long: unique to stamen ED10. The two papers' tables also give different rice orthologs (Xu Os08g0432800; Long Os09g0410700). Listed under Xylem, low.
8. **AG2 is not carpel-specific in Xu's smFISH.** It is in c18 floral meristem, and as strongly in c12 "leaf abaxial" (0.79 vs 0.08). Long finds it unique to carpel ED16. Listed under Carpel_Primordium, medium.
9. **MND1 cell type disagrees.** Long: suppressed axillary meristems (ED9). Barley draft (`datasets/barley_inflorescence/`): Ground_Tissue. Kept as Axillary_Meristem.
10. **PLT8-like (TraesCS2D02G256600) disagrees.** Long: lodicule-unique. Liu: vasculature R12 and spikelet base R5. Listed under Lodicule, `expression`, low.
11. **Homoeolog-specific behaviour.**
    - MT2: the 1D homoeolog (TraesCS1D02G034800) is in every nucleus and was excluded.
    - ULT1: only the A copy marks meristems; Xu says the B copy is in ground tissue.
    - VRT2-B is "divergent" in Zhang S4 but was kept.
    - The SEP1-4 homoeologs in Xu Table S1 (7A02G122000, 7B02G020800) differ from Ensembl's calls (7A02G122100, 7B02G0209/210/211). Xu's IDs were kept.
12. **Long ED10 is labelled "16" in the Zenodo xlsx** (noted in the Long review).
13. **Survey entry correction (from the Zhang review):** the Zhang spatial platform is BMKMANU, not Stereo-seq.

## Overlap with existing skill tables

There is no wheat table in `references/markers/`. The closest tables are `rice_root.tsv` and `sorghum_leaf.tsv` (same family, different organ) and the Arabidopsis tables. Shared genes, by orthology:
- **APL:** the wheat rice ortholog Os06g0664800 is the rice_root Phloem MYB (LOC_Os06g45410). Arabidopsis APL is in the Arabidopsis leaf and root tables.
- **SHR1:** ortholog of rice OsSHR1 (Os07g0586900; rice_root Stele) and Arabidopsis SHR.
- **SCR2:** its rice orthologs include OsSCR1 (Os11g0124300), which is a rice_root Endodermis marker. In the wheat spike SCR2 marks epidermis, so use it per organ.
- **XCP1:** ortholog of rice Os05g0108600, the Zhang 2021 rice-root "XCP2". That is not the rice_root.tsv XCP2-like row (LOC_Os01g73980). Sorghum and Arabidopsis XCP1 are Xylem markers.
- **FDH:** Arabidopsis FDH is in arabidopsis_leaf Epidermis (function, high).
- **Cell-cycle genes:** CDKB2-1 is the ortholog of rice CDKB2;1 (Os08g0512600 = LOC_Os08g40170, rice_root Dividing_cells). CYCB1 and the histones overlap with the rice and Arabidopsis S_Phase and Dividing_cells rows.

The cell-type names follow the barley inflorescence draft (`datasets/barley_inflorescence/`), so the two grass-spike tables can be merged. Three names are new: `Axillary_Meristem`, `Intercalary_Meristem` and `Wound_response` (a state). None of them appears in an existing skill table.

## What I could not verify

- **Large files and web viewers (not downloaded or scraped):**
  - Xu 2025's per-cell scRNA labels (1.16 GB .rds) and its 77.6 MB Additional file 1 (dotplots). Xu's scRNA specificity was taken from Tables S9, S16 and S18 and the review.
  - Long 2026's per-cell domain table (137.8 MB tar) and the WebAtlas.
  - Zhang 2026's main-article figures (64 MB PDF). Zhang's raw data are unreleased, and the WSSED portal does not resolve.
- **Liu 2025:**
  - Only the Research Square PDF text and Tables S1, S3, S5 and S8 were read. The Extended Data figures (marker dotplots, MERFISH panels) and the GitHub code were not checked.
  - Liu's claim that TaBHLH10 is ovary-specific in MERFISH could not be checked against Long's per-cell data.
  - No full dataset review exists for Liu 2025.
- **ID checks:**
  - Kronos IDs cannot be checked in a public database.
  - Wheat genes are poorly named in UniProt, so IDs were checked against the papers' own tables (Xu S1, Long S1/S2, Zhang S3/S4, Liu S3), the IWGSC v1.1→v2.1 correspondence, and Ensembl Plants Compara (homoeologs and rice orthologs).
  - Rice ortholog identities that decide a call were confirmed in UniProt: OsMADS5, OsMADS1, TIP2/bHLH142, MSP1, OsYABBY3/4/5, OsMADS3/13/58, OsPLT8.
- **STK1 ID:** inferred (the Long Table S1 row whose ortholog is OsMADS13). The paper gives no ID.
- **Homoeologs added from Ensembl** (named in each row's `basis`) were not tested in any study. Probes in Long 2026 do not separate homoeologs.
- **Zhang 2026 cluster proportions** were read by eye from a bar chart in the review.
