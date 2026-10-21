# plant-celltype-annotation

> **In development.** This skill is being tested and changes often. Feedback is
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
- `references/plant_pitfalls.md`: homology traps, ambient RNA, doublets,
  states vs types, and lineage-specific anatomy.
- `tests/`: a synthetic smoke test of the whole script chain.

## Install

Clone into your Claude Code skills folder:

```bash
git clone https://github.com/alexborowsky/plant-celltype-annotation ~/.claude/skills/plant-celltype-annotation
```

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

The marker tables are built from published studies and cite them row by row
(`basis` and `source` columns). The protoplasting stress list and the
Arabidopsis root markers come from Shahan et al. 2022 (*Dev Cell*). The
sorghum root markers come from Guillotin et al. 2023 (*Nature*).
Check the original papers before relying on a marker.
