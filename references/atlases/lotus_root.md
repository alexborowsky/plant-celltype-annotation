<!-- Collated from the survey review of lotus_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Lotus japonicus root: cell-type marker resources (group review)

Collated 2026-10-20 for the plant-celltype-annotation skill. Input: one dataset review, Frank et al. 2023, in
`Frank2023/`. Its README was left as is. I re-checked every gene ID used here against the paper's Source Data
and checked cross-study agreement against the Ye et al. 2024 nodule review (`../lotus_nodule/Ye2024/`).
Nothing in the skill was edited.

## Files

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Cell types expected from Lotus root anatomy (whole root at 10 dpi, root-hair zone without tips at 5 dpi), with `function` row counts from `markers_draft.tsv` |
| `markers_draft.tsv` | 45 rows (44 from `build_markers_draft.py` + LjFAR3.1 added by hand 2026-10-20) in the skill schema plus `alt_id`. `ref_gene` = Lotus Gifu v1.2 genome / v1.3 annotation (`LotjaGi…`). `alt_id` is empty because neither paper gives MG-20 v3 (`Lj…`) IDs |
| `build_markers_draft.py` | Writes `markers_draft.tsv`. The docstring lists the source sheets |
| `Frank2023/` | Dataset review, unchanged |
| `Sun2023/` | Dataset review (Sun et al. 2023), unchanged |
| `markers_Sun2023_Lj1gvBRI.tsv` | 16 Sun 2023 rows, same columns as `markers_draft.tsv`, but `ref_gene` = Lj1gvBRI (authors' private MG-20 assembly). Kept apart because they cannot match LotjaGi data |

## Datasets

| Dataset | Platform | Cells | Label access | Quality | Status |
|---|---|---|---|---|---|
| Frank et al. 2023 *Nat Commun* 14:7171, doi:10.1038/s41467-023-42911-1 (PMC10630511); ENA PRJEB57790; Figshare 10.6084/m9.figshare.23986200 | Protoplast scRNA-seq, 10x Chromium; Gifu roots, *M. loti* R7A vs mock | 10 dpi whole roots: 25,024 cells, 32 clusters (4 samples). 5 dpi susceptible zone, tips removed, WT and *cyclops-2*: 32,180 cells, 30 clusters (8 samples) | table: per-cell `Cell_type` and cluster in two small Figshare xlsx files (2.4 and 3.4 MB; `Frank2023/labels_*.tsv`). The infected, nodule and bacteroid cell selections are not in them. RDS files are 2.2 and 2.6 GB (not downloaded) | medium | reviewed |
| Ye et al. 2024 *Nat Commun* 15:6387, doi:10.1038/s41467-024-50737-8 | Stereo-seq bins (36-58 µm), nodules and the attached root | 19,238 bins | cluster_only | medium (zones) / low (cell types) | reviewed under `lotus_nodule`; used here only as a cross-study check for state markers |
| Sun et al. 2023 *J Integr Plant Biol* 65:1147, doi:10.1111/jipb.13435 (PMID 36537698) | Protoplast scRNA-seq, 10x 3' v3 (MGISEQ-2000); MG-20 root tips (5 mm), one library | 22,688 cells, 7 clusters | cluster_only | low | reviewed 2026-10-20 in `Sun2023/`; see "Update 2026-10-20" below. Gene IDs (Lj1gvBRI) cannot be mapped to LotjaGi |
| bioRxiv 10.64898/2026.04.10.717526, "Specialised root hair cells facilitate rhizobial infection" | ? | ? | ? | ? | not reviewed; found in Europe PMC, and the species was not checked |

Only one true single-cell root dataset was reviewed. There is no atlas-to-atlas agreement for any root **cell
type**. The only cross-study agreement is for **states** (dividing cells, rhizobial infection), shared
between Frank's clusters and Ye's spatial nodule clusters.

## Per-cell-type verdict matrix

Frank is the only root dataset. Ye has no resolved root cell types (its root clusters 1/2 were rejected and
cluster 0 is "vascular"), so it appears only where a state is shared.

| Canonical type | Frank 2023 label (10 dpi clusters; 5 dpi clusters) | Frank verdict | Ye 2024 | Best markers here |
|---|---|---|---|---|
| Trichoblast | Trichoblasts (2, 9; 18, 22) | Adopt | – | RHD6-like (reporter), EXPA7-like x2, RHS12/14-like |
| Atrichoblast | Atrichoblasts (4, 11, 23; 1, 21, 24) | Revise (tentative non-hair epidermis) | – | none |
| Epidermis / Lateral_Root_Cap | Root tip (0, 7, 13, 19; 2, 10) | Revise (zone label; cl0/13 → LRC hypothesis; cl7 stress) | – | SMB-like, BRN1/2-like, BFN1-like; PIN2 (low) |
| Columella, Quiescent_Center, Stem_Cell_Niche | – | Missing | – | none |
| Cortex | Cortex (1, 5, 8, 10, 12, 14, 15, 16, 18, 22, 31; 4, 6, 8, 12, 13, 16, 17, 26) | Revise (catch-all) | – | Ole e 1-like (low) |
| Endodermis | Endodermis (20, 24, 27; 20, 25, 28) | Adopt | – | CASP1/2/3-like, MYB36-like, SCR-like |
| Pericycle | Pericycle (6; 11) | Adopt (medium) | – | UMAMIT reporter, PHO1-like |
| Stele / Procambium | Stele (3, 17, 26; 0, 3, 5, 7, 9, 14, 15, 29) | Revise (merged; 34% at 5 dpi) | (cl0 "vascular", nodule) | LTP reporter, SHR-like |
| Xylem | Xylem (29; 23) | Adopt (differentiating) | – | XCP1-like reporter, CESA4/7/8-like, VND7-like |
| Phloem | Phloem (25, 30; 19, 27) | Adopt; **new: split** cl30/27 = sieve-element side (SEOR1-like x2, NAC020-like), cl25/19 = companion-cell side (PP2-A1-like) | – | SEOR1-like, PP2-A1-like |
| Dividing_cells (G2/M) | Quiescent center (28; 5 dpi in Cortex 16) | Reject as QC → state | Adopt as state (cl4 "Meristems") | CYCB2;3-like, CYCB1-like, UBC19-like (cross-study) |
| S_Phase | Meristem (21; 5 dpi in Cortex 13) | Revise → state | proliferative cl3/4/8 | histone H4, H3.1 |
| Rhizobia_responsive | Infected cells (paper selection, 96 cells; not in metadata) | Adopt as state | cl8/9 infection zone | NPL, SYMRKL1, NIN, NF-YA1 |
| Lateral_Root_Primordium | – (in 5 dpi Cortex 13/16) | Missing | – | none |
| Nodule cells | 98 bCA1+ / 21 LB+ cells | out of scope | see lotus_nodule | – |

Label counts were re-checked from `Frank2023/labels_*.tsv`: they match the review. Clusters where one sample
holds more than 50% of cells (10 dpi): cl31 100%, cl22 59%, cl30 57%, cl8 55%, cl4 54%, cl14 52%. No 5 dpi
cluster is over 50%, but Gifu_Control_2 alone has 4,210 of 11,041 'Stele' cells.

## Grading rules used

- `function`: the paper's Arabidopsis best hit has a cell-type-defining function (CASP, MYB36, SCR, SHR, VND7,
  SEOR1, SMB, BRN, RHD6, EXPA7, secondary-wall CESAs, G2/M cyclins, replication histones, nodulation genes).
  The confidence is `medium` when the support is single-cell enrichment only. It is `high` with a Lotus
  reporter (RHD6-like, XCP1-like), with a reporter and a mutant (NPL, SYMRKL1, NIN, NF-YA1), or with agreement
  across studies.
- `characterized_enriched`: a characterized gene without a type-defining function. The confidence is
  `medium` with a Lotus reporter, or with pct.2 ≤ 0.02 at both time points. Otherwise it is `low`.
- **10 dpi and 5 dpi are the same lab, the same protocol and the same Gifu background.** Agreement between
  them is replication, not an independent study, so it never raised confidence.
- Nodulation rows have `requires=Fabaceae`. This is a new trait tag. It would need
  `Fabaceae → eudicot` in `IMPLIES` in `map_markers.py` before the table goes into the skill.

## Cross-study markers (same gene ID in Frank 2023 and Ye 2024)

| Gene | Symbol | State | Frank 2023 | Ye 2024 (Supp Data 1 Figure_1c/1d) | Effect |
|---|---|---|---|---|---|
| LotjaGi3g1v0534800 | UBC19-like | Dividing_cells | cl28 0.88 vs 0.03; promoter:GUS; 5 dpi cl16 | cl4 0.38 vs 0.08 | characterized_enriched medium → **high** |
| LotjaGi2g1v0356100 | CYCB2;3-like | Dividing_cells | cl28 0.82 vs 0.008 | cl4 0.25 vs 0.05; PT-1 | function medium → **high** |
| LotjaGi1g1v0659100 | CYCB1-like | Dividing_cells | cl28 0.65 vs 0.014 | curated cl4 marker, 0.32 vs 0.05 | function medium → **high** |
| LotjaGi6g1v0096900 | NPL | Rhizobia_responsive | infected cells 0.73 vs 0.002 | cl8 0.49 vs 0.08; curated, UniProt H2DL22 | already high |
| LotjaGi1g1v0001500 | NIN | Rhizobia_responsive | infected 0.25 vs 0.005 | cl9 0.79 vs 0.17 | already high |
| LotjaGi5g1v0106700 | NF-YA1 | Rhizobia_responsive | infected 0.80 vs 0.012 | cl8 0.91 vs 0.36 | already high |
| LotjaGi3g1v0277900 / 0290800 | histone H4 / H3.1 | S_Phase | cl21 0.97 vs 0.08 / 0.12 | cl3, cl4, cl8 (all proliferative; not specific) | not raised |
| LotjaGi1g1v0461700 | SCR-like | Endodermis (Frank) vs nodule primordium (Ye) | cl24 0.26 vs 0.04 | cl4 0.31 vs 0.02 | different cell types; not raised |

Ye's data are spatial bins, not cells. Its clusters are nodule zones, so agreement only counts for states
that do not depend on the tissue.

## Gaps (no validated Lotus marker)

Columella; Quiescent_Center; Stem_Cell_Niche; Atrichoblast; Cortex (Ole e 1-like reporter is cortex plus
epidermis, and peaks in the photosynthetic cl14); Pericycle `function` marker; Procambium;
Lateral_Root_Primordium; proto- vs metaxylem. No root cell type has a marker validated in two independent
studies. Cell types with no `function` row: Columella, QC, Stem_Cell_Niche, Epidermis, Atrichoblast, Cortex,
Pericycle, Procambium, Lateral_Root_Primordium.

## Recommended label reference

Use **Frank 2023** (the only reviewed root atlas). Its per-cell labels are public and small. Adopt
Endodermis, Xylem, Trichoblasts, Phloem and Pericycle at both time points. Relabel 10 dpi cl28 as
Dividing_cells and cl21 as S_Phase. Carry 'Root tip' cl0/13 (10 dpi) and cl2/10 (5 dpi) as a Lateral_Root_Cap
hypothesis to test with SMB-like and BRN1/2-like. Do not reuse 'Cortex', 'Stele', 'Atrichoblasts' or
cl7/cl19 as types. Exclude cl8 (ribosomal) and cl31 (one sample). The 10 dpi whole-root set is the better
benchmark, because the 5 dpi set has no tip and its 'Stele' is replicate-skewed. Barcodes look like
`AAACCCAAGGGCAGTT-1_1`, where the `_n` suffix is the sample index.

## Conflicts and corrections to the dataset review

- **PIN2 (LotjaGi4g1v0307500) is flagged `protoplast-induced`** in Frank's own 10_CM table. The review did
  not say so. Its specificity is moderate (pct.2 0.18-0.23), so the row is `low`, and it is filed as
  Epidermis rather than root cap.
- **The Ole e 1 reporter gene's top cluster is cl14** (the photosynthetic/nodule cluster, 0.50 vs 0.10).
  Cortex cl1 comes second. So it is not a clean cortex marker, and the row is `low`.
- **IPN2 is not phloem-specific in planta.** Frank's VAL sheet lists Lotus IPN2 expression in "infected
  cells, nodule cells, epidermis, cortex, vasculature". It is phloem-restricted only in the scRNA clusters.
  The row is `low`, with the conflict in `basis`.
- **The phloem clusters can be split.** cl30 (10 dpi) and cl27 (5 dpi) carry SEOR1-like x2 and NAC020-like
  (sieve-element side). cl25 and cl19 carry PP2-A1-like (companion-cell side). The review said SE and CC were
  not resolved. This split is new and rests on Arabidopsis best hits only. cl30 is 57% one replicate.
- **The 'Root tip' clusters carry a root-cap NAC trio** (SMB-like, BRN1/2-like, BFN1-like) at both time
  points, even though the 5 dpi roots had their tips removed. Possible explanations are lateral-root caps,
  incomplete tip removal, or a non-cap outer layer expressing these genes. This is unresolved.
- **The GL2 best hit (LotjaGi3g1v0018300) is enriched in pericycle cl6**, not in epidermis. The same thing
  happened in Medicago, where it was in cortex. The `requires=eudicot` GL2/WRKY44 atrichoblast rows in
  `arabidopsis_root.tsv` should not be used for legumes.
- **Panel letters.** The review gives RHD6 = Suppl. Fig 1c and UBC19 ('QC') = 1b. The main text calls the
  'quiescence center marker' Supplementary Fig. 1c. I could not read the supplementary PDF (no PDF text tool
  is available), so `basis` cites only "Suppl. Fig 1/2/3" without panel letters.
- **The review put Arabidopsis IDs in `alt_id`.** That column is reserved for a second ID system of the
  same species (`map_markers.py --id-column alt_id`), so the AT best hits moved into `basis` and `alt_id`
  stays empty.
- **Names.** The review used "Infection-thread cells". This table uses `Rhizobia_responsive` (kind=state),
  to match `medicago_root/expected_cell_types.tsv`.

## ID checks

- All 44 IDs are present in Frank's Source Data (10_CM, 5_CM, 10_INF, VAL, or 'promoter sequences'), and all
  cluster statistics in `basis` were read from those sheets. All 26 review markers are kept, and 18 genes
  were added beyond the review: CASP2-like, CASP3-like, SCR-like, SHR-like, IRX9-like, VND7-like,
  SEOR1-like x2, NAC020-like, BRN1/2-like, BFN1-like, PHO1-like, EXPA7-like (2), CYCB1-like, CDC20-like,
  histones H4 and H3.1, and PCNA-like. I found them by searching the paper's `Arabidopsis_ID` column for
  best hits of known markers. They are not the paper's own picks.
- **No database confirmation was possible.** `LotjaGi` IDs are not indexed in UniProt, NCBI Gene or Protein,
  or Ensembl Plants. Lotus Base (lotus.au.dk) redirects to projects.au.dk/lotus, and LIS hosts only MG-20 v3
  annotations. The only independent ID link is NPL: Ye 2024's annotation column maps LotjaGi6g1v0096900 to
  UniProt H2DL22 (LjNPL). The NIN, NF-YA1 and SYMRKL1 IDs were also checked against the 10_INF and VAL sheets,
  and NIN/NF-YA1 against Ye's tables, where they are the same IDs.
- "Ortholog" here always means the paper's best Arabidopsis hit. It was not checked by reciprocal BLAST,
  because no Gifu proteome was downloadable by script.

## Overlap with existing skill tables

There is no Lotus or other legume table in `references/markers/`. Through Arabidopsis homology, the
`arabidopsis_root.tsv` rows that map onto these Lotus genes, going by the paper's best-hit column, are:
CASP1 → LotjaGi5g1v0099800/0100000; CASP2 → LotjaGi5g1v0102500; CASP3 → LotjaGi3g1v0178400 (and
1g1v0619100); MYB36 → LotjaGi4g1v0298100; SCR → LotjaGi1g1v0461700 (and 5g1v0156700, in cortex cl15);
EXPA7 → LotjaGi4g1v0217400/2g1v0429600; SMB → LotjaGi3g1v0129900; APL → LotjaGi3g1v0132600 (IPN2). They
behave as expected in Frank, except GL2, which falls in pericycle. WOX5, PLT1, COBL9 and GATA23 hits are not
cluster markers in Frank. The Medicago group draft (`../medicago_root/markers_draft.tsv`, CP 2022 nuclei)
has the same lineage pattern: CASP-like/MYB36-like in endodermis, PHO1 in pericycle, EXP7 in root hairs, and
GL2 off-target. Those are different species' IDs, so this is supportive, not cross-study agreement. If this
table goes into the skill, the file would be `references/markers/lotus_root.tsv` (`ref_gene` = Gifu v1.3),
with `Fabaceae` added to the trait vocabulary.

## Could not access or verify

- The images and legends of the reporter figures (Suppl. Figs 1-3, 11). No PDF text extraction tool was
  available, so reporter claims rest on the dataset review and the main text.
- Sun et al. 2023 JIPB: main text paywalled; supplements reviewed 2026-10-20 (see the update section below).
- Database confirmation of Gifu IDs (see ID checks). There are no MG-20 v3 cross-references.
- RDS objects (2.2 and 2.6 GB, Figshare), not downloaded by design. All specificity values are the paper's
  FindConservedMarkers pct.1/pct.2 (Control columns), not my own per-cell statistics.
- Lotus root anatomy details (number of cortex layers, diarch vs triarch stele, whether hair cells are
  position-patterned) were not checked against a primary anatomy source.

## Update 2026-10-20: gap-fill reviews

One new review: **Sun et al. 2023** *J Integr Plant Biol* 65(5):1147-1152, doi:10.1111/jipb.13435 (DOI and
PMID 36537698 confirmed in Europe PMC; not open access). Folder: `Sun2023/`. Protoplast 10x 3' v3 scRNA-seq of
22,688 cells from 500 MG-20 root tips (5 mm). One library, Seurat res 0.3, 7 clusters, 7 ISH probes, and a bulk
protoplast-vs-intact-root comparison. Main text and Fig 1 (antisense ISH images) were blocked by Wiley (403)
and were not circumvented. The supplements (Tables S1-S25, SI PDF, Figs S1-S6) were read.

### Verdicts

| Published label | n (%) | Verdict | Canonical | Why |
|---|---|---|---|---|
| Root cap | 6,760 (29.8) | Reject | – | catch-all: top genes pct.2 0.87-0.98; its ISH probe Lj1gvBRI21766 is shared with Root hair (0.92 vs 0.75); no columella/LRC/QC split |
| Root hair | 2,115 (9.3) | Revise | Trichoblast | ortholog-conserved with Arabidopsis root hair (Fig S6A), two-branch pseudotime; markers only moderately specific (pct.2 0.35-0.5) |
| Cortex | 4,639 (20.4) | Revise | Cortex (+ proliferation) | ISH-backed; middle vs 1st+4th layer split (Fig S5A); ~78% S+G2/M |
| Epidermis | 3,279 (14.5) | Revise | Epidermis (weak) | 78 genes, near-ubiquitous; ISH gene is a 14-3-3 (0.83 vs 0.47) |
| Exodermis | 2,624 (11.6) | Revise | Cortex (outer ground tissue) | differentiated exodermis not established for Lotus; ~80% S+G2/M. Note: **0** of its 381 enriched genes are protoplast-induced, so it is a real tissue cluster, not stress |
| Endodermis | 2,139 (9.4) | Reject | Protoplasting_stress (state) | 219 of 540 enriched genes are protoplast-induced in the authors' Table S21 (19 of the top 30 by lfc in my count; the review said 20, the difference is the ranking used); G1-dominant; no ISH probe enriched |
| Stele / "Metaxylem" (Table S20) | 1,126 (5.0) | Revise | Stele | best-supported cluster: ISH Lj1gvBRI17778 0.80 vs 0.08; orthologs conserved with Arabidopsis stele (Fig S6B); whole stele, not metaxylem |

I re-counted the protoplast overlap for all clusters from `Sun2023/Table_S21_protoplast_DEGs.tsv` and
`Table_S22_cluster_enriched_genes.tsv` (induced / enriched): Endodermis 219/540, Stele 89/314, Root_hair 38/211,
Cortex 23/137, Root_cap 19/102, Epidermis 11/78, Exodermis 0/381.

### Markers added or raised

- **`markers_draft.tsv`: no Sun rows added, none raised, none changed.** One row was added from the
  characterized-markers survey (see below), so the table now has 45 rows. Sun's gene IDs
  (`Lj1gvBRI#####`, the authors' own MG-20 assembly, 38,675 genes) are not in UniProt, NCBI or Lotus Base, and
  no conversion to Gifu `LotjaGi` or MG-20 v3 `Lj` IDs is public. Merging by gene ID is impossible, so no Frank
  marker can count as validated by an independent study. Merging by Arabidopsis best hit would be homology,
  not the same gene, so I did not do it.
- **New sidecar table `markers_Sun2023_Lj1gvBRI.tsv`** (16 rows, same 13 columns as `markers_draft.tsv`).
  Stats for every row were re-read from Table S22 and match the review. Rows: Stele 7 (ISH Lj1gvBRI17778
  `characterized_enriched` medium; 12470, 35751, 07157, 07940, 20215 WAT1-like `expression` low), Cortex 3
  (ISH 10561, 21026, 36354, `characterized_enriched` low; 36354 is from the published 'Exodermis'), Epidermis 1
  (08110 14-3-3, `expression` low), Trichoblast 6 (11214 GH9C1-like `characterized_enriched` low; 21367, 24979,
  33897, 25553, 13435 `expression` low). The probe-to-type assignment is inferred from Table S22 because the ISH
  images were not seen. Use these rows only on data aligned to Sun's assembly, or after an ID conversion.
- Not used: Lj1gvBRI21766 (Root cap / Root hair probe, not specific); Lj1gvBRI11791 (Cortex probe, also Stele,
  0.96 vs 0.67).
- **Characterized-markers survey** (`survey/characterization/characterized_markers.tsv`). Its `lotus_root:` gap
  rows (Columella 9, Stem_Cell_Niche 8, QC 6, LRP 5, Procambium 4, Nodule_cells 4, Atrichoblast, Cortex,
  Epidermis, Pericycle 1 each) are Arabidopsis or Medicago genes, plus LjRHL1, which is keyed by UniProt
  D0PX88. None matches a LotjaGi ID in this table, so none raises a row. They stay usable by homology from
  the survey table. One Lotus row in the survey does carry a LotjaGi ID: **LjFAR3.1 (LotjaGi3g1v0175200)**.
  It has a promoter:YFP reporter in root vascular endodermis (Venado et al. 2022 PNAS,
  doi:10.1073/pnas.2206291119, DOI confirmed in Europe PMC). It was **added as Endodermis,
  `characterized_enriched`, `low`**. It is low because Frank's endodermis clusters do not list it: it appears
  only in the 5 dpi NF-YA1 subsets (0.09 vs 0.001), and Frank's bulk comparison shows protoplasting represses
  it (logFC -4.29). This row was appended by hand. `build_markers_draft.py` does not write it, so add it there
  before regenerating the table.

### Gaps closed

None in `markers_draft.tsv`. Partial, in Lj1gvBRI IDs only:
- **Cortex**: 3 ISH-backed genes (function unknown) and a middle vs outer/inner cortex split.
- **Protoplasting_stress**: a bulk protoplast-vs-root gene list (Table S21: 4,069 DE genes, 1,756 induced). Sun's
  'Endodermis' cluster is the single-cell form of this state. Frank's own list (655 genes, LotjaGi IDs) is still
  the one to use for Gifu data.

### Gaps remaining

Columella, Quiescent_Center, Stem_Cell_Niche, Atrichoblast, Cortex `function` marker, Pericycle `function`
marker, Procambium, Lateral_Root_Primordium, proto- vs metaxylem. No root cell type has a marker validated in
two independent studies by the same gene ID. `function` counts in `expected_cell_types.tsv` are unchanged. Its
notes now carry the Sun evidence.

### Conflicts

- **Endodermis.** Frank's endodermis (CASP/MYB36/SCR-like) is solid. Sun's 'Endodermis' is a protoplasting
  artifact. Do not import Sun's label or its markers as endodermis.
- **Exodermis.** Sun calls a cluster Exodermis and also places '1st layer cortex' inside Cortex (Fig S5A).
  Frank has no exodermis. Treat it as outer cortex. Exodermis is not added to `expected_cell_types.tsv`.
- **Root cap.** Frank's 'Root tip' cl0/13 carries SMB/BRN-like. Sun's 30% 'Root cap' has no specific cap genes.
  Sun gives no support to the LRC hypothesis.
- **Stele naming.** Sun's Table S20 calls the stele cluster "Metaxylem" and Table S22 calls it "Stele". It is the
  whole stele.
- **Proliferation.** Sun's Cortex and Exodermis are ~80% S+G2/M. A 5 mm tip is dominated by meristem. Frank
  separates proliferation into states (Dividing_cells, S_Phase), which is the better model.

### Recommended label reference

Unchanged: **Frank 2023**. Sun 2023 is lower quality (one library, 7 coarse clusters, 2 of 7 labels rejected, no
per-cell labels, private gene IDs). It should not be used as a label reference.

### Could not access or verify (Sun 2023)

- The main text and Fig 1 (Wiley 403): antisense ISH images, probe-to-type mapping, data-availability statement.
  No GEO or other accession was found.
- The Lj1gvBRI genome, annotation or proteome. None is public as far as the review found, so no ID conversion is
  possible. The realistic route is a conversion table or proteome from the authors (the user's call).
- The review's NCBI BLAST of the ISH primers (RID DG99JM7X016) was not retrieved. It would give MG-20 RefSeq
  hits, not LotjaGi IDs, in any case.
