# Changelog

Versions follow [semantic versioning](https://semver.org/). While the version is 0.x, any release may change
script flags or table formats; breaking changes are listed under **Changed**.

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
