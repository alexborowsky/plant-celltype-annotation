<!-- Collated from the survey review of lotus_nodule (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Lotus japonicus nodule: collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill, from one dataset
review (Ye 2024). The skill was not edited. For cross-study checks I also used the
Lotus root review (Frank 2023, `../lotus_root/Frank2023/`), because that paper
includes nodule, infected and Lb+ cells from inoculated roots.

Files in this folder:
- `expected_cell_types.tsv`: written from determinate-nodule anatomy (with the parent root), not from published labels. Function-marker counts were made after the draft table was built.
- `markers_draft.tsv`: 24 rows, skill schema plus `alt_id`. `ref_species=lotus`, `tissue=nodule`, IDs are Gifu v1.2/1.3 (`LotjaGi...`), and `alt_id` holds the MG-20 v3 ID where UniProt gives one. Nodule types use `requires=Fabaceae`, the same tag as the soybean_nodule draft. That tag is not yet in the skill's trait vocabulary or in `IMPLIES`.
- `Ye2024/`: review folder with its own README, supplements and figures.

## Datasets

| Dataset | Platform | Units | Label access | Quality | Role here |
|---|---|---|---|---|---|
| Ye K et al. 2024 *Nat Commun* 15:6387, doi 10.1038/s41467-024-50737-8 (CNGB CNP0004336 / STOmicsDB STT0000041) | Stereo-seq spatial, 10 um cryosections, bin50 (~36 um) at 5/6 dpi and bin80 (~58 um) at 8/10 dpi; **not single-cell** | 19,238 bins, 72 sections, 24,929 genes, 14 clusters | cluster_only (no per-bin table in the supplements; STOmicsDB contents unknown) | medium (zones/stages); low as a cell-type reference | the only nodule dataset reviewed; source of cluster statistics |
| Frank M et al. 2023 *Nat Commun* 14:7171, doi 10.1038/s41467-023-42911-1 (lotus_root group) | protoplast scRNA-seq, 10x | 25,024 cells at 10 dpi; nodule-relevant subsets: 96 infected, 98 betaCA1+ nodule, 21 Lb+ cells | per-cell table (tissue level only; the nodule subsets are not in the metadata) | medium | independent cross-check (different lab, different platform, same Gifu IDs) |

## Verdict matrix (published label -> canonical name)

A = Adopt, R = Revise, X = Reject, – = not annotated. Frank 2023 has only the small nodule subsets.

| Canonical type | Ye 2024 (Stereo-seq bins) | Frank 2023 (nodule-related subsets) |
|---|---|---|
| Infected_Cell (N-fixing) | R: c5 "N-fixing zone" (~8%), the best-supported label. Uninfected cells are merged in. | A as a selection: 21 Lb+ "bacteroid-containing" cells (selected by Lb) |
| Infected_Cell (young/differentiating) | R: c9 "infected zone (differentiating)"; IZ-2..4 are stages | – |
| Uninfected_Cell | – (merged into c5/c9) | – |
| Infection_Thread_Cell (state) | R: c8 "pre-infection zone", which also contains dividing cells | A as a state: 96 infected cells (NPL-selected) |
| Nodule_Primordium | R: c4 "meristems" (a proliferation state; SCR1 GUS and NBCL1 support a primordium) | A as a selection: 98 betaCA1+ "nodule cells" (primordium/young nodule; selected by betaCA1) |
| Dividing_cells (state) | inside c4/c8 (cyclin B, UBC19) | cluster 28 "QC" (G2/M), "Meristem" (S); see lotus_root |
| Nodule_Parenchyma | R: c7 "peripheral tissues", merged with nodule vasculature | – |
| Nodule vasculature (Endodermis/Pericycle/Xylem/Phloem) | – (in c7) | – |
| Sclerenchyma (scleroid layer) | – (not separated from c6) | – |
| Cortex (nodule outer) | R: c6 "outer cortex", with Lb spillover | – |
| Cortex (root, responding) | R: c3 "early nodule cortex", a defense/flavonoid state | (root cortex; lotus_root) |
| Root stele | R: c0 "root vascular tissue", unresolved | (lotus_root) |
| Root epidermis/cortex/endodermis | X: c1, c2 "ground/dermal", a stage/bin-size split | (lotus_root) |
| Lenticel, Epidermis (nodule) | – | – |
| Boundary bins | X: c10-13 "mixture" (the authors left them unassigned) | – |

## Cross-study markers (same Gifu ID, independent enrichment in both papers)

Ye statistics are cluster log2FC (pct.1 vs pct.2) from Supp Data 1 `Figure_1c`. Frank statistics come from Source Data sheets `10_INF`, `10_NOD`, `10_BAC` and `10_CM`.

| Type | Gene (Gifu) | Symbol | Ye 2024 | Frank 2023 | Draft grade |
|---|---|---|---|---|---|
| Infected_Cell | LotjaGi2g1v0213700 | SST1 | c5 2.28 (0.56/0.12) | Lb+ 0.62/0.018 | function high |
| Infected_Cell | LotjaGi1g1v0613400 | FEN1 | c5 1.97 (0.58/0.12) | Lb+ 0.14/0 | function high |
| Infected_Cell | LotjaGi4g1v0031000 | SEN1 (added) | c9 1.24 (0.69/0.09); c5 1.23 | Lb+ 0.62/0 | function high |
| Infected_Cell | LotjaGi3g1v0005100 | EFD1 | c9 1.64 (0.49/0.10) | Lb+ 0.71/0.04 | char_enriched medium |
| Infected_Cell | LotjaGi4g1v0453800 | nsRING | c9 2.15 (0.74/0.06) | Lb+ 0.48/0.018 | char_enriched medium |
| Infected_Cell | LotjaGi3g1v0182500 | symLHW | c9 1.61 (0.77/0.13) | Lb+ 0.48/0.034 | char_enriched medium |
| Infection_Thread_Cell | LotjaGi2g1v0324000 | EPR3 | c8 0.95 (0.29/0.06) | infected 0.22/0.005 | function high |
| Infection_Thread_Cell | LotjaGi1g1v0643700 | ERN1 | c8 0.89 (0.28/0.06) | infected 0.79/0.17 | function high |
| Infection_Thread_Cell | LotjaGi5g1v0256800 | CERBERUS/LIN | c9 1.21 (0.53/0.05) | infected 0.18/0.05 | function high |
| Infection_Thread_Cell | LotjaGi5g1v0253300 | RPG | c9 1.86 (0.95/0.22) | infected 0.13/0.004; Lb+ 0.86/0.004 | function high |
| Infection_Thread_Cell | LotjaGi1g1v0001500 | NIN | c9 1.28 (0.79/0.17) | infected 0.25/0.005; Lb+ 0.52/0.006 | function high |
| Nodule_Primordium | LotjaGi5g1v0106700 | NF-YA1 | c8 1.48 (0.91/0.36), broad | nodule 0.19/0.015; infected 0.80/0.012 | function high |
| Nodule_Primordium | LotjaGi1g1v0664600 | NBCL1/NOOT | c4 0.83 (0.31/0.07) | nodule 0.28/0.007 | function high |
| Dividing_cells | LotjaGi1g1v0659100 | cyclin B | c4 1.18 (0.32/0.05) | cl28 0.70/0.006 | function high |
| Dividing_cells | LotjaGi2g1v0356100 | CYCB2;3-like | c4 0.94 (0.25/0.05) | cl28 0.73/0.002 | function high |
| Dividing_cells | LotjaGi3g1v0534800 | UBC19-like | c4 1.18 (0.38/0.08) | cl28 0.87/0.008 + GUS | char_enriched high |

Not counted as agreement:
- Lb1-3 (Frank selected its Lb+ cells with them), NPL (Frank selected its infected cells with it) and betaCA1 (Frank selected its nodule cells with it) are circular.
- symBIB is nodule-specific in both papers, but neither resolves the cell type.
- SCR1 is enriched in a different type in each paper (Frank: root endodermis; Ye: primordium).

## Gaps (expected types with no validated Lotus marker)

- **Uninfected_Cell**: no marker. Ye merges these cells into its central-tissue bins, and Frank has no UC selection. Use soybean uricase by homology (check that it is specific).
- **Nodule_Parenchyma**: only betaCA1 (stage-dependent, also reported in UC) and symBIB (low).
- **Sclerenchyma** (scleroid layer), **Lenticel**, nodule **Epidermis**, outer **Cortex**: no marker in any Lotus nodule data.
- **Nodule vascular** endodermis, pericycle, xylem and phloem: none from nodule data. Use arabidopsis_root by homology and the lotus_root (Frank) root markers, which are not validated in nodules.
- **Senescing**: not expected at 5-10 dpi.
- **Infected_Cell, young vs N-fixing**: these are states. Ye's IZ subclusters order them, but no reporter separates them.

## Recommended label reference

There is no cell-resolved Lotus nodule atlas. Use Ye 2024 as a **zone/stage reference** only. Its c5/c9/c8/c4/c7 labels are hypotheses for N-fixing central tissue, differentiating central tissue, the infection zone, the primordium and peripheral tissue. The defining markers are in the draft. Frank 2023 is the better source for **per-cell labels** in the parent root (lotus_root group). Its nodule subsets are marker-selected and small (21-98 cells), so they work as a marker cross-check but not as a label reference. For IC vs UC and for nodule parenchyma vs vasculature, label de novo from the draft markers. Medicago and soybean nodule atlases can help through homology.

## Conflicts and corrections to the review

- **Citations corrected** (checked in Europe PMC):
  - FEN1 is Hakoyama et al. 2009 *Nature* (10.1038/nature08594), not "2012 PNAS". The 2012 Hakoyama paper is SEN1 in *Plant Cell Physiol*.
  - CERBERUS is Yano et al. 2009 *Plant J* (10.1111/j.1365-313x.2009.03943.x), not PNAS.
  - Lotus ERN1 is Cerri et al. 2017 *New Phytol* (10.1111/nph.14547).
  - betaCA1 is Flemetakis et al. 2003 *Biochim Biophys Acta* (10.1016/s0167-4781(03)00142-8), not MPMI. Ye itself cites Wang et al. 2021 *IJMS*.
- **betaCA1 localization differs between studies.** Flemetakis found it in all cells of young nodules and only in the inner cortex of mature nodules. Wang 2021 found it in peripheral cortex plus uninfected cells. The draft therefore keeps it at medium for Nodule_Parenchyma.
- **NOOT name confirmed.** The review called LotjaGi1g1v0664600 "LjNBCL1 (inferred name)". Frank 2023's VAL sheet names the same ID NOOT, and Ye's annotation hit is UniProt G3LSH3 (Lj-NBCL). It is LjNBCL1 (Magne et al. 2018 *Plant J*).
- **NF-YA1 statistics corrected.** It is strongest in c8 (1.48, 0.91 vs 0.36), not ">0.5" as in the review. Its background is high (pct.2 0.36), so Ye shows little specificity for it.
- **RPG statistics corrected.** Ye c9 is 1.86 (0.95 vs 0.22), not ">=0.5".
- **SST1 has two names in Ye.** The same ID is called LjSST1 and LjSULTR2. The annotation hit is UniProt Q0P7I2 (Sst1), so the draft uses SST1.
- **Lb1/Lb2 MG-20 IDs.** UniProt lists Lj5g3v0035290 for both Lb1 and Lb2, so `alt_id` is empty for Lb2.
- **Lb grading.** The Lbs are graded function/medium, not high: they mark only the N-fixing stage and are ambient (76-91% of outer-cortex bins in Ye).
- **Dropped:** LjGS1 (LotjaGi6g1v0055300). Its enrichment is weak (pct.2 0.24), and the name appears only in a GO gene list, so the isoform is unverified.
- **Added:** SEN1 (from the Frank cross-check; also enriched in Ye c9/c5), CYCB2;3-like and UBC19-like (Frank G2/M genes that are also enriched in Ye c4).
- **Other ID inconsistencies inside Ye** (from the review, not used in the draft): LjPLT2 is given two IDs, and LotjaGi6g1v0076900 is called both CLC1 and CHC1.

## Overlap with the skill's marker tables

The skill (`references/markers/`) has no Lotus or legume table, so nothing overlaps for this species. Overlap is by homology only:
- arabidopsis_root function rows cover the root and nodule-vascular types (SCR, CASPs, MYB36, APL, IRX9, MYB46, SHR, GATA23).
- arabidopsis_leaf covers Dividing_cells.
- LjSCR1 is the Lotus counterpart of the arabidopsis_root SCR endodermis row, but in nodules it also marks primordia.

None of the symbiotic types (Infected_Cell, Infection_Thread_Cell, Nodule_Primordium, Nodule_Parenchyma) has an Arabidopsis counterpart. Related drafts outside the skill:
- `../soybean_nodule/markers_draft.tsv` uses the same type names and also has FEN1-like and RPG rows.
- `../medicago_root/` covers root types only, plus a Rhizobia_responsive state.

## Could not verify

- **Gifu gene IDs in a database.** UniProt carries the `LotjaGi` ID only for Lb1-3. Other IDs rest on agreement between two independent papers' own tables (Ye and Frank use the same ID for NIN, NPL, EPR3, ERN1, NF-YA1, CERBERUS, RPG, NBCL1/NOOT, betaCA1, SEN1 and Lb1-3) plus the UniProt accession of Ye's annotation hit (SST1 Q0P7I2, NPL H2DL22, nsRING A0ZT53, NBCL G3LSH3, cyclin B I3S1U1). Lotus Base gene pages redirect, and Ensembl has no Lotus Gifu.
- **Cell-level localization of the GUS reporters** (NLP3, SCR1, symLHW, symBIB). I could read the legends, but the images show the organ or region, not the cell.
- **The Frank nodule subsets** are 21-98 cells. Their statistics come from the paper's tables, not from re-analysis.
- **Contents of the STOmicsDB/CNSA processed objects.** These are JS portals; whether they carry per-bin labels is unknown.
- **No in-data check** (Step 3b) was run.
