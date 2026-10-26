# plant-celltype-annotation

> **In development (v0.6.0, pre-release).** This skill is being tested and changes often. Feedback is
> very welcome: please open an issue with what you ran (species, tissue, cells
> or nuclei), what worked, and where the annotation or the instructions went
> wrong.

A [Claude Code](https://claude.com/claude-code) skill for annotating cell types in
plant single-cell and single-nucleus RNA-seq data (Scanpy/AnnData), for any
species and tissue.

It guides the agent through the whole loop:

1. Find the labels published with the dataset, list the cell types expected
   for the tissue, and evaluate the published labels.
2. Search the literature for species and tissue markers.
3. Map reference markers to the species by homology (BLAST/DIAMOND or an
   OrthoFinder table).
4. Build per-cluster evidence across resolutions (marker scores, DE genes, QC,
   doublet and stress flags).
5. Reason about each cluster, write an annotation table, apply it, and build
   an evidence report that shows why each label holds.

Most of the value is in two places: the reasoning steps in `SKILL.md`, and the
curated reference data. The scripts gather evidence; they don't decide.

The curated data isn't available in one place elsewhere:
- marker tables graded by evidence (function, reporter/in situ, expression),
  each row with its basis and source, and tagged by lineage so that markers
  only apply where the cell type exists;
- reporter- and mutant-characterized markers for cell types that atlases
  miss;
- reviews of ~390 published plant single-cell and spatial datasets, with
  label access, quality, and the problems found in each annotation;
- plant-specific pitfalls learned from testing on real data.

## What's included

- `SKILL.md`: the workflow and the rules the agent follows.
- `scripts/`: Python scripts:
  - `map_markers.py`: map markers by homology;
  - `cluster_evidence.py`: per-cluster evidence;
  - `subcluster.py`;
  - `apply_annotations.py`;
  - `annotation_report.py`;
  - `check_genes.py`: gene-level checks by symbol or ID through the gene maps;
  - `score_gene_sets.py`: scores labels published only per cluster;
  - `type_under_state.py`: the cell type of a state cluster, judged on genes the state does not change;
  - `fetch_reference.sh`: downloads and builds a reference proteome hub;
  - `lineage_tags.py`.
- `references/markers/`: marker tables with evidence tiers (`function`,
  `characterized_enriched`, `expression`) and lineage tags (C3/C4, grass,
  eudicot, bryophyte...):
  - curated core tables for Arabidopsis leaf and root, rice root, and sorghum;
  - survey tables for 55 species × organ groups;
  - reporter-, in situ- and mutant-characterized markers.
- `references/atlas_catalog.tsv` and `references/atlases/`: a catalog of ~390
  published plant single-cell and spatial datasets, with reviews of the main
  atlases.
- `references/proteomes.tsv`: reference proteome hubs (Arabidopsis, rice,
  maize, sorghum, wheat, barley, tomato, soybean, medicago, bryophytes…)
  whose gene IDs match the marker tables, with measured match rates.
- `references/annotation/`: Arabidopsis gene symbols and a rice MSU7 ↔ RAP-DB
  map; `references/markers/celltype_aliases.tsv`: synonymous cell-type names.
- `references/plant_pitfalls.md`: homology traps, ambient RNA, doublets,
  states vs types, and lineage-specific anatomy.
- `tests/`: a synthetic smoke test of the whole script chain.

## Install

Clone a release into your Claude Code skills folder (see
[Releases](https://github.com/alexborowsky/plant-celltype-annotation/releases) and `CHANGELOG.md`):

```bash
git clone --branch v0.6.0 https://github.com/alexborowsky/plant-celltype-annotation ~/.claude/skills/plant-celltype-annotation
```

Omit `--branch` to follow the latest development version on `main`. On claude.ai, upload the
`plant-celltype-annotation-<version>.zip` attached to each release as a skill. When you report a problem,
include the version (it is printed in the report header and stored in `VERSION`).

Then ask Claude Code to annotate a clustered `.h5ad`. The skill loads when the
request matches its description, or you can name it.

Requirements: Python with scanpy ≥ 1.8, anndata, pandas, numpy, scipy,
matplotlib and leidenalg. You also need BLAST+ or DIAMOND to map markers to a
non-model species. Run heavy steps on a compute node; the skill assumes an
HPC setting with Slurm, but the scripts run anywhere.

Check the install:

```bash
CONDA_SH=~/miniconda3/etc/profile.d/conda.sh CONDA_ENV=scanpy bash ~/.claude/skills/plant-celltype-annotation/tests/smoke_test.sh
```

## Sources

Every marker row cites its evidence in the `basis` and `source` columns:
about 650 distinct DOIs in total. Check the original paper before relying on
a marker.

- **Literature survey (2026-10).** 394 published plant single-cell, single-
  nucleus, spatial and sorted-population datasets across 69 species
  (`references/atlas_catalog.tsv`). 116 of them were reviewed in depth: label
  access, marker quality, validation, and problems such as states labeled as
  types. The reviews are summarized per species × organ in
  `references/atlases/`, and their markers make up the survey tables:
  - `primary/`: 30 tables (2,402 rows) for well-supported species × organ
    groups;
  - `secondary/`: 25 tables (885 rows) for thinner groups.
- **Characterized markers** (`characterized/`). 300 rows from reporter, in
  situ and mutant studies, mostly outside single-cell data. They cover cell
  types the atlases miss: root cap, QC, seed-coat layers, embryo sac,
  sieve elements, nodule zones and laticifers.
- **Curated core tables:**
  - Arabidopsis leaf: function-based literature curation.
  - Arabidopsis root: Shahan et al. 2022 *Dev Cell* curated markers
    (ohlerlab/scKB, MIT), plus classic functional markers.
  - Rice root: six single-cell datasets cross-checked against each other and
    against the characterized genes they cite.
  - Sorghum leaf: lab curation, cited row by row.
  - Sorghum root: the conserved grass root markers from Guillotin et al.
    2023 *Nature*.
- **Protoplasting stress list:** Shahan et al. 2022 *Dev Cell*.

The survey, reviews and table curation were done with Claude (Anthropic)
and are being checked by hand. Some `basis` texts are still marked as
pending review. Corrections are welcome as issues.
