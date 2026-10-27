# Changelog

Versions follow [semantic versioning](https://semver.org/). While the version is 0.x, any release may change
script flags or table formats; breaking changes are listed under **Changed**.

## [0.9.0] - 2026-10-27

From a blinded leaf-atlas run on 0.8.0: a xylem-parenchyma program was left as `Vasculature`, a defense-state
population was typed by its parent cluster, and the adaxial/abaxial pavement split was dropped.

### Changed
- **`type_under_state.py` needs one candidate per lineage.** A two-candidate score cannot detect a third type: a leaf
  defense subset scored 0.85 toward bundle sheath against mesophyll alone, and 0.5 between bundle sheath and pavement
  once pavement was a candidate. The script warns with two candidates and prints a verdict: a type only when the
  query sits >= 0.7 (`--call-at`) toward it against every other candidate, otherwise "unresolved".
- **A state cluster is not typed by its parent cluster** (SKILL.md Step 7 item 10, pitfalls).
- **"Photosynthetic beyond ambient" is judged against the dataset's own non-photosynthetic types** (companion cells,
  phloem parenchyma, xylem, pavement), not in absolute terms; it no longer overrides a coherent program of another
  type.
- **Layer names are a last resort:** when the evidence favours one type, call it at low confidence and name the
  alternative.
- **Positional sub-identities** (adaxial/abaxial pavement, palisade/spongy, vein classes) are labelled when an
  existing resolution separates them with markers; this is not over-clustering.

## [0.8.0] - 2026-10-27

A blinded leaf-atlas run assembled types from many subclusters and fallback rows (52 rows, 6 subclusterings).

### Changed
- **Subclustering is for two cases only:** an expected type's function marker confined to a subset of one cluster,
  or a cluster that clearly mixes two types. Check existing resolutions first; a low-confidence label or `Unknown` is
  an acceptable answer; use low subcluster resolutions (0.1-0.3). Step 7 items 5 and 9 and the "expected type with no
  cluster" check no longer send the agent to subclustering by default.
- **The fold-back rule is generic:** a subcluster does not join a type defined by another, larger cluster (any type,
  not only the majority one). **Exception: cell-cycle clusters**, whose subclusters are expected to split among the
  types roughly as the dataset does.
- **Don't assemble a type from many pieces:** define each type by one cluster (or a few) at one resolution.

### Added
- `apply_annotations.py`: the fold-back warning compares a subcluster row with the type's cells from other cluster keys
  (not only base resolutions), skips cell-cycle rows and prints each cycling cluster's type split next to the dataset's
  shares; notes types assembled from three or more cluster keys (cell-cycle rows not counted) and more than four
  subclustering keys.

## [0.7.1] - 2026-10-26

### Fixed
- Examples taken from a test dataset are now generic: the `type_under_state.py` usage (cluster IDs, gene IDs,
  reporter and treatment names), the SKILL.md `type_under_state` and `--extra-genes` examples, the `Confidence` and
  `State` examples in `references/file_formats.md`, and the `apply_annotations.py` docstring.

## [0.7.0] - 2026-10-26

A cell type defined by clean subclusters was extended by a later coarse row with leftover cells from the edge of the
neighbouring (majority) cluster, and its report page plotted the coarse cluster instead of the subclusters.

### Added
- `apply_annotations.py` records the row that labelled each cell in `obs['cell_type_source']`, and warns when a row
  adds cells (>= 50, or >= 5% of the type) to a type that earlier rows already defined, naming the parent clusters
  those cells come from.
- Report cell-type pages list **cells by annotation row** with the top marker's detection in each row's cells.
- SKILL.md Step 9: add a coarse fallback row for a subcluster-defined type only when its leftover cells carry the
  markers.

### Changed
- The report's violins use the key of the rows that labelled most of the type's cells, not the key whose clusters
  overlap most of them (a coarse fallback row could win before).
- For h5ad files without the new columns, the report replays the table once for both source rows and confidence,
  and warns if the replay does not reproduce the labels.

## [0.6.0] - 2026-10-26

### Added
- **Overall confidence per cell type in the report** (overview table column, a line on each cell-type page, and
  `<report>_confidence.tsv`). It is the lower of:
  - the annotation table's `Confidence` (cell-weighted median over the rows that labelled the cells);
  - the marker evidence found in the data: high for a function-tier marker plus another enriched gene; medium for a
    characterized marker, two enriched genes, or level only (the type's own markers clearly higher, though present in
    most cells everywhere); low for one expression-level gene or DE only.
  `_like` labels are capped at medium; `Unknown*` labels are "unresolved". Each page says which side set the level.
- **`Confidence` column in the annotation table** (high / medium / low), parsed by `apply_annotations.py` and written
  per cell to `obs['cell_type_confidence']`. Before, a Confidence column was read as part of the Evidence text.
  The report replays the table for h5ad files annotated before this version.

## [0.5.0] - 2026-10-23

In the blinded leaf-atlas re-run, a defense-state subset was left `Unknown` because its cell-type reporter had fallen
to background, although its other genes matched that type.

### Added
- `scripts/type_under_state.py`: places a state cluster between candidate types on each pair's own genes, at matched
  depth, leaving out the genes the state induces or represses. It also tabulates markers and reporters in the same
  depth band, and lists the state program it left out.
- SKILL.md Step 7 item 10: a state can hide its type's markers; run the script before calling a state cluster
  `Unknown`, and state the limits (circular candidates, shared regional programs).
- Pitfall: states suppress identity markers and reporters.
- Smoke test step 7e.

## [0.4.0] - 2026-10-23

States were listed only as a share on each cell-type page; the report did not show what set them or why.

### Added
- **State pages in `annotation_report.py`:**
  - A States page: a UMAP coloured by state, and a table of each state's cells, the cell types carrying it, the
    sample with the highest share, and the annotation rows that set it.
  - One page per state: the state on the UMAP; the Evidence of its rows; the cell types carrying it; its share of
    each sample/treatment/replicate; and gene panels against the same cell types without the state, with violins
    per type split into with (+) and without (-) the state.
  - Genes come from the gene IDs in the rows' Evidence, then `--state-genes STATE=GENE1,GENE2`, then the top genes
    of the contrast (labelled data-driven). Cited genes that are not enriched are listed.
  - New flags: `--state-key`, `--state-genes`, `--max-state-genes`, `--composition-keys`.
- SKILL.md Step 9b: state rows need evidence like type rows (genes with fractions vs the same types without the
  state, composition by sample and treatment).
- Smoke test step 7d: a state-only row is applied and gets its page.

## [0.3.1] - 2026-10-23

A re-run of the blinded leaf-atlas annotation on 0.3.0 still labelled a distinct cluster (a private program in most of its
cells, an arm off the mesophyll body on the UMAP) as `Mesophyll` with an "unexplained program" state.

### Changed
- **A private program you cannot explain is not a state.** The cluster is `Unknown_<program>`, not the majority type
  plus a state. Shared photosynthesis genes do not set the type of such a cluster.
- **UMAP shape is checked per cluster:** look at each cluster highlighted and note its shape (within body, island,
  arm/projection, bridge) in the Evidence column.

### Added
- `apply_annotations.py` warns when a State names no recognizable process, or when the Evidence calls it unexplained.

## [0.3.0] - 2026-10-23

Feedback from a blinded re-annotation of a 264k-cell leaf atlas.

### Added
- **Annotation table `State` column:** states (stress, treatment response, cell cycle, senescence) keep the cell type.
  - It writes `obs['cell_state']` and `obs['cell_type_with_state']`.
  - Rows with CellType `-` are state-only: they set the state and leave the type to other rows.
  - Report pages list each type's states.
- `apply_annotations.py`: a note when a tissue-layer name is used as a label, and a warning when a subcluster row
  assigns the broad type of other base clusters (fold-back).

### Changed (SKILL.md, pitfalls, file formats)
- **Name cell types, not layers:** Pavement, Guard, Trichome, Protodermal, species-specific epidermal types; vascular
  types. Layer names (Epidermis, Vasculature) are valid only when the identity within the layer is ambiguous.
- **States never replace the cell type.** A state cluster that mixes types is resolved per cell.
- **Subclusters of trichome or vascular clusters never fold back into the majority type** (e.g. mesophyll). They keep
  the parent lineage name or Unknown.
- **A cluster with its own program** (private DE genes in ≥ 50% of its cells vs ≤ 5% elsewhere) is not given the
  majority label by exclusion. Sample enrichment is not batch when the cluster is present in all samples.
- **Senescence is tested with a gene panel;** a null result for a single unmeasurable marker counts as "untested".
- **UMAP shape is evidence:** arms and projections mark continuous programs to investigate.

## [0.2.1] - 2026-10-22

### Fixed
- **Xylem vs cell-death guidance:** the 0.2.0 text claimed that a rice panicle cell-death cluster was differentiating
  xylem. A re-run rejected that on evidence (no VND/XCP/CESA in it), and the xylem turned out to be a 182-cell subset of
  the procambium cluster (ACL5, XCP2, WAT1, VND-like, PXY), found by subclustering. SKILL.md, the pitfalls file and the
  rice inflorescence atlas note now say:
  - cell-death genes alone are neither senescence nor xylem; xylem needs identity genes and adjacency to procambium;
  - subcluster a cluster when an expected-but-missing type's marker is enriched only in a subset of it.
- `check_genes.py` resolves symbols through the aliases column of the Araport11 table (VND2, CESA7, CESA8, ATHB8...).

## [0.2.0] - 2026-10-22

Fixes from a 22-run test round (benchmarks, high- and low-quality published annotations, non-model species).

### Added
- **Reference proteome hubs:** `references/proteomes.tsv` (21 hubs: Arabidopsis, rice MSU7/RAP, maize v5, sorghum, wheat,
  barley, tomato, soybean, medicago, lotus, poplar, Brachypodium, Marchantia, Physcomitrium...). Each hub's gene IDs match
  the marker tables, with the measured match rate per table. `scripts/fetch_reference.sh` downloads a hub, keeps one isoform
  per gene, writes symbols and builds a DIAMOND database. SKILL.md Step 5 says which hubs to search for each target lineage
  (e.g. rice + maize + sorghum + Arabidopsis for grasses).
- `scripts/check_genes.py`: gene-level checks by symbol or ID, resolved through the gene maps (every copy), with per-cluster
  fraction, mean and z. Use it instead of typing gene IDs from memory.
- `scripts/score_gene_sets.py`: checks labels published only per cluster by scoring each published cluster's marker list
  in the current clusters (best match, margin, high-count warning).
- `references/markers/celltype_aliases.tsv` (synonymous cell-type names, used by the scripts);
  `references/annotation/araport11_genes.tsv.gz` (Arabidopsis symbols and descriptions);
  `references/annotation/rice_msu_rap.tsv.gz` (MSU7 ↔ RAP-DB).
- Markers: xylem cell-death genes (MC9, XCP1/2, BFN1, RNS3); moss and liverwort rhizoid genes (PpRSL1/2, MpLRL).
- `map_markers.py`:
  - `--match-unversioned`, `--id-rewrite`, `--query-rewrite`, `--h5ad`/`--target-genes` (ID match-rate check and warning);
  - symbols and a `relationship` column in `--orthology` mode;
  - close-species paralog rescue by identity (`--rescue-min-pident`);
  - a warning when one gene marks several cell types;
  - new traits: fern, angiosperm, tracheophyte, magnoliid, Triticeae, Euphorbiaceae, Phaseoleae.
- `cluster_evidence.py`: several `--gene-map` files; `--doublet-scores`; `--aliases`; QC compared with sibling clusters;
  markers detected / measurable / all-zero; `marker_score_details_<key>.tsv`; symbol columns in `de_<key>.csv`.
- `annotation_report.py`: `--gene-annotation`, several `--gene-map` files, `--extra-genes`, `--min-detect`.
- `subcluster.py --batch-key` (Harmony on the recomputed subset PCA).
- `tests/test_lineage_tags.py`; the smoke test now also runs the new helpers.

### Changed
- **Doublet flag** fires only for unrelated types. Pairs that share driving genes, a name, an alias or a lineage are skipped;
  each type needs ≥ 2 detected markers; per-cell doublet scores are used when available. On the test runs this cut flags
  from 348 to 31.
- **Lineage tags** rewritten as three explicit groups (angiosperm-only, seed-plant, vascular-plant). Moss and liverwort
  targets no longer score shoot-apex zones, primordia, pavement, trichome or sperm-cell rows; ferns, lycophytes and
  gymnosperms drop the types they lack.
- **Report** marker choice ranks by specificity, with a 10% detection floor. Labels no longer overlap, `Xylem` markers no
  longer count for `Xylem_Parenchyma`, and orthology mode shows relationships instead of "nan%".
- **SKILL.md:**
  - developmental cell death (xylem, tapetum, root cap) is separated from senescence;
  - Step 8b also covers state-labelled and low-confidence clusters while an expected type is missing;
  - confidence is capped when the best marker is detected in < 15% of cells;
  - QC is compared with sibling clusters;
  - label conventions (`<Type>_like`, transitions, developmental states, `Unknown_<hint>`);
  - per-cluster published labels; ID-matching guidance.
- Marker data: Catharanthus FAMA row corrected (it pointed to MUTE); atlas notes corrected (tomato root, rice
  inflorescence, soybean root), with label-source recipes and a new `atlases/rice_root.md`.

## [0.1.1] - 2026-10-21

### Added
- Evidence report: **cluster pages** after the overview. For each cluster key used by the annotation rows
  (and so by the violin plots), a UMAP with cluster IDs printed on it and a table of each cluster's size and
  assigned cell type. Subclusterings are drawn over the full UMAP, with the cells they cover stated. The
  report now stands alone: cluster IDs on the cell-type pages can be looked up without the h5ad.

## [0.1.0] - 2026-10-21

First public pre-release, for testing. Feedback welcome as issues.

### Workflow (`SKILL.md`)
- Part A: find the labels published with a dataset, list the expected cell types, and judge each published
  type with a review rubric (Adopt / Revise / Reject).
- Part B, the annotation loop:
  - literature search for marker gaps;
  - homology mapping;
  - multi-resolution cluster evidence;
  - per-cluster reasoning;
  - subclustering;
  - applying the table;
  - an evidence report.
- Step 8b: before the report, form and test hypotheses for clusters left `Unknown` (pathway genes from
  UniProt, DIAMOND to the target, judged by expression level).
- Guidance for nuclei vs protoplasts, doublets, C4 grasses, bryophytes, sparse transcription-factor
  markers, and paralog families split across cell types (e.g. SULTR2).

### Scripts
- `map_markers.py`: maps marker tables to a target species from BLAST/DIAMOND (forward and reverse, with
  paralog rescue) or from OrthoFinder-style tables. Filters rows by lineage traits and tissue.
- `cluster_evidence.py`: per-cluster evidence for each resolution:
  - marker scores, with the fraction in vs out for each driving marker;
  - DE genes annotated with Arabidopsis homologs;
  - QC, composition and doublet flags;
  - the protoplasting-stress check.
- `subcluster.py` (optional fresh PCA), `apply_annotations.py` (comma cluster lists, Seurat cluster
  columns, imported labels).
- `annotation_report.py`: a PDF with one page per cell type, ordered by cell count. Each page shows the
  marker evidence and homology, and the report stamps the skill version.
- `lineage_tags.py`: adds lineage tags to marker tables.
- `tests/smoke_test.sh`: the whole chain on synthetic data.

### Curated data
- Survey of 394 published plant single-cell, spatial and sorted-population datasets (69 species), 116
  reviewed in depth (`references/atlas_catalog.tsv`, `references/atlases/`).
- Marker tables:
  - 30 primary and 25 secondary survey tables;
  - 290 characterized (reporter, in situ, mutant) markers;
  - curated core tables for Arabidopsis leaf and root, rice root, and sorghum leaf and root.
- About 650 cited DOIs.

### Known limitations
- Some `basis` texts are marked as pending review.
- Tested on Arabidopsis-mapped eudicot leaf and root, sorghum leaf, and a leafy liverwort. Other lineages
  have had less testing.
- Doublet scores (scrublet) are read per cluster; there is no automatic doublet removal.
