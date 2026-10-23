---
name: plant-celltype-annotation
description: >-
  Annotate cell types in plant single-cell / single-nucleus RNA-seq data
  (Scanpy/AnnData) for any species and tissue. Use when the user wants to label
  Leiden clusters with cell types, find or pick marker genes for a non-model
  plant via Arabidopsis homology, build or revise a cluster→cell-type
  annotation table, subcluster an ambiguous cluster, apply annotations to an
  h5ad, reuse or audit the cell labels published with a dataset, or check
  whether an existing annotation is well supported. Covers the whole loop:
  published annotations → expected cell types → evaluate and reuse the
  published labels → literature search for species/tissue markers → ortholog
  mapping → multi-resolution cluster evidence → reasoning per cluster →
  annotation table → apply + validate. Ships curated marker tables for 55
  species x organ groups (Arabidopsis, maize, rice, wheat, soybean, tomato,
  legumes, trees, bryophytes...), reporter/in situ-characterized markers, and
  a catalog of ~390 reviewed published plant single-cell/spatial datasets.
---

# Plant cell-type annotation

This skill turns a clustered AnnData object into a defensible cell-type
annotation. It generalizes the workflow used to annotate an
*N. benthamiana* leaf atlas, and has been tested on leaf, root and
bryophyte data.

**Most of the value is in the reasoning and the curated references, not the
scripts.** The graded marker tables, characterized markers, atlas reviews and
pitfalls under `references/` hold knowledge that is not collected anywhere
else, so read them rather than relying on memory. The scripts produce
evidence. You read the evidence, propose labels with explicit
justification, and the user approves them. Do not treat any automated score
as a label.

## Operating rules

1. **Evidence before labels.** Every assigned cluster must cite at least one
   marker that is both *specific* (enriched relative to other clusters) and
   *biologically sensible* for the tissue. Presence alone is not evidence:
   photosynthesis genes are detected nearly everywhere in green tissue.
2. **`Unknown` is a valid answer, but only after a follow-up.** Leave
   clusters unlabeled rather than forcing a label. Before the report, though,
   form and test hypotheses for every unlabeled cluster (Step 8b).
   Low-quality, doublet-like, or treatment-only clusters should be called
   out as such, not assigned to a cell type.
3. **The user decides.** Present the proposed annotation table with an
   `Evidence` column and wait for approval before applying it to their main
   h5ad. Never overwrite the user's main h5ad unless they asked for that.
4. **Function beats statistics.** A characterized gene whose function
   defines the cell type (SUC2 loads sucrose in companion cells, SWEET11
   exports it from phloem parenchyma, CASPs build the Casparian strip) is
   stronger evidence than a gene picked by enrichment. Conserved function
   also makes the marker more likely to transfer across species. Marker
   tables record this in `evidence`: `function` > `characterized_enriched`
   > `expression`. Base a call on `function` markers whenever any exist for
   that cell type, and say so when a call rests only on expression-derived
   markers.
5. **Homology is a hypothesis.** A best BLAST hit is not an ortholog. For
   every marker you rely on, report the reference locus, hit rank, and %
   identity. Prefer reciprocal best hits (RBH). Check all paralogs, because
   polyploids have several copies.
6. **Separate states from types, and keep both.** Cell cycle, senescence,
   stress/defense, circadian, and treatment responses can form clusters.
   Record the state in the annotation table's `State` column and keep the
   underlying cell type in `CellType` (Step 7, item 9); use a state as the
   label only when the type truly cannot be resolved.
7. **Heavy work goes to the scheduler.** Never load an h5ad on a login node.
   Inside an interactive allocation (`$SLURM_JOB_ID` set), run the scripts
   directly if the object fits its memory and time; otherwise submit them with
   `sbatch` (see `scripts/run_step.sbatch`). Size memory at about 3–5× the
   h5ad size on disk (uncompressed).

## Inputs to collect (ask if missing)

| Input | Notes |
|---|---|
| Dataset provenance | Is this a published dataset (or a reanalysis of one)? Get the paper/DOI and accession (GEO/SRA/ENA). This decides whether Steps 1 and 3 apply. |
| Clustered h5ad | Needs log-normalized expression (`.raw` or a layer), an embedding (`X_umap`), and one or more cluster columns (`leiden_res0.5`, …). If it has no clustering yet, stop and cluster first. |
| Species, tissue, and developmental stage | Determines which marker tables apply (`references/markers/`), the `--target-traits` (e.g. `eudicot Solanaceae`, `grass C4`, `Sorghum`), and which caveats matter (C3 vs C4, monocot vs dicot, protoplast vs nuclei). |
| Species → reference homology | BLASTP/DIAMOND (outfmt 6) of the target's proteins against each reference hub that has tables for its lineage (`references/proteomes.tsv`; e.g. `arabidopsis` for Arabidopsis tables, `rice_msu7`/`maize_v5`/`sorghum_v5` for grass tables). Add the reverse search for RBH and paralog rescue. Build these in a job if absent; DIAMOND `--very-sensitive` takes minutes. |
| Any curated species markers | For example, a `CellTypeMarkers.txt` the user already trusts. These take priority over the mapped reference markers. |
| Metadata columns | Sample, replicate, and treatment, used for composition checks. |
| Transgenes and reporters | Promoter-reporters are strong validation. They are usually excluded from the embedding and may live in `obs` as `<gene>_expr`. |

## Workflow

The workflow has two parts:

- **Part A (Steps 1–3): find out what is already known.** Do this before
  annotating anything. It decides how much of Part B is needed.
- **Part B (Steps 4–10): annotate.** Run it only for the cell types that
  Part A did not settle.

Before submitting anything, plan all steps. Steps 6, 9, and 9b each load the
full h5ad, so for large objects they are the expensive jobs. The Step 3
in-data check runs inside the Step 6 job; don't run it as a separate one.

## Part A: what is already known

Details, search sources, and the evaluation rubric are in
`references/published_annotations.md`. **Read it before Step 1.**

### 1. Source the published annotations

Do this if the dataset, or the data it was reanalyzed from, has been
published. For the user's own new data, skip to Step 2. Atlases of the same
species and tissue are found in Step 4 instead.

**Check the survey first.** `references/atlas_catalog.tsv` lists about 390
published plant single-cell and spatial datasets (2026-10 survey), each with
its review status, quality, and label access. If the dataset is there and
was reviewed, start from its review: `references/atlases/<species>_<organ>.md`
summarizes the verdicts and the recommended label reference, and the full
review and downloaded supplements are in the Oak folder named in
`review_folder`.

Collect:

- **Per-cell labels** (barcode → cell type), with any cluster IDs. Look in
  the GEO supplementary files, Zenodo/Figshare/GitHub, and the paper's
  supplementary tables. Seurat `.rds` objects need their `meta.data`
  exported in R.
- **The cluster → cell type table and the marker list** used to call each
  type, with the gene-ID version.
- **The paper's validation**: in situ hybridization, reporter lines, and
  marker figures (dotplots, feature plots) for each type.
- **Methods that affect labels**: protoplast vs nuclei, filtering,
  integration, and clustering resolution.
- **How accessible the labels are**: a small barcode→label table, only
  inside a large object (give its size), cluster-level only, or none.

Save them in the project as `published/` (the labels table, the marker
table, and a short `published/README.md` with the citation, DOI, file
sources, and the barcode format). If the labels cannot be found, ask the
user. Some authors share them on request.

### 2. List the expected cell types for this species, tissue, and stage

Build the list from the anatomy of the tissue, not from the data or the
published labels collected in Step 1. Otherwise the list can't be used to
check them. Write `expected_cell_types.tsv` (format in
`references/file_formats.md`), with one row per expected type:

- **Expected abundance**: common, moderate, or rare.
- **Capture bias** for this protocol:
  - Mature xylem vessels are dead, so only differentiating ones appear.
  - Mature sieve elements have no nucleus, so nuclei data misses them.
  - Protoplasting under-recovers cells with thick or lignified walls, and
    large cells.
- **Lineage-specific types** for the species: Kranz bundle sheath in C4
  grasses, glandular trichomes in Solanaceae, myrosin cells in
  Brassicaceae, and so on. Starting lists by tissue and lineage are in
  `references/published_annotations.md`.
- **Marker coverage**: does a table in `references/markers/` give this type
  at least one `function` marker after `--target-traits` filtering? Types
  without one are the targets of the Step 4 search.
- **Common states** that may form their own clusters (dividing cells,
  stress, senescence).
- **Bryophytes** (liverworts, mosses, hornworts): build the list from the
  body plan, not from angiosperm tissues. A leafy liverwort has leaf,
  underleaf, stem cortex/epidermis, rhizoids, oil-body cells and apical
  cells. A thalloid one adds air chambers, pores, assimilatory filaments,
  storage parenchyma, ventral scales and gemma cups. Mosses have hydroids
  and leptoids in some species. There is no xylem, phloem, stomata (in the
  gametophyte), roots or flowers. See `references/plant_pitfalls.md`.

Show the list to the user. They know the tissue and the sampling better
than any reference.

**If the tissue or stage is unknown** and the user can't be asked, infer it
from the data before writing the list, and state it as an assumption:
- the top expressed genes across all cells (photosynthesis genes for green
  tissue; root-hair, Casparian-strip, or root-cap genes for roots);
- whether dividing cells are present (young or meristematic tissue);
- C4 enzymes such as PEPC, PPDK and NADP-ME (C4 grass leaf).

### 3. Evaluate the published annotation, and reuse what holds

Judge each published cell type on its own. A paper can have well-supported
vascular labels and an implausible guard-cell cluster.

**3a. Review the paper.** Do this right away, from the paper alone:

- **Coverage:** compare the published types with the Step 2 list. Note any
  missing expected types, and any unexpected or implausible ones.
- **Proportions:** are they biologically plausible? One tomato reanalysis
  called 31% of cells guard cells.
- **Marker quality:** were types called from `function` markers, from
  reporter or in situ validation, or only from cluster DE genes? Did the
  paper show the markers to be specific to the type?
- **States vs types:** are stress, cell-cycle, or treatment clusters
  labeled as cell types? Check every "meristem", "initial", "stem cell
  niche", "QC", or "root cap" label for proliferation markers (histones,
  PCNA, cyclin B, CDKB, KNOLLE). In the rice root review, all five RNA
  datasets had at least one such label.
- **Forced assignment:** was every cell given a type, including clusters
  with no positive marker signal? Is there a large catch-all bin?

When several datasets cover the same species and tissue, review each one,
then compare their markers by gene ID (`published_annotations.md`,
"Agreement across datasets"). Markers that hold up across studies are the
best input to Step 4.

**3b. Check the labels in the data.** Import the published labels and add
them to the Step 6 evidence job, both as a cluster key and as a metadata
key:

```bash
--import-labels published/labels.tsv:<col>:published_celltype \
--cluster-keys published_celltype leiden_res0.5 leiden_res1.5 ... \
--meta-keys sample published_celltype
```

Then check:

- **The barcode match rate,** printed by the import. If it is low, fix the
  barcode format first (suffixes, sample prefixes).
- **Whether each label's own markers are enriched** in its cells, using
  `marker_scores_published_celltype.tsv` and the DE list in
  `cluster_evidence_published_celltype.md`.
- **Whether each label is a coherent group in the current clustering:**
  - `cluster_hierarchy.tsv` gives each label's main Leiden cluster at each
    resolution, and the share of the label's cells in it. A low share means
    the label is spread across clusters.
  - The composition section of each `cluster_evidence_leiden_*.md` shows
    how each Leiden cluster splits across published labels. A cluster split
    across unrelated labels is a warning sign.

**Labels published only per cluster** (a cluster → type table and each
cluster's marker list, but no barcodes) can still be checked: write the
published clusters' marker genes as gene sets and score every current
cluster with `scripts/score_gene_sets.py` (best match per published label,
margin to the second best, high-count clusters flagged because they inflate
set scores). A published label is supported where its set wins clearly
*and* its known function markers agree; treat a narrow margin as unresolved.

If the paper's markers use the dataset's gene IDs, write them as a target
marker table (`published/markers.tsv`, format in
`references/file_formats.md`, graded as in
`references/literature_search.md`). Pass it to the same job's `--markers`,
so that they are scored alongside the reference markers.

**Verdict per cell type:**

| Verdict | When | What to do with it |
|---|---|---|
| `Adopt` | Plausible type and proportion, and its markers are enriched in the data | Use the published label as the call. Its validated markers join the marker tables. |
| `Revise` | Right lineage, but the boundaries or granularity are wrong (merged or split types, a state labeled as a type) | Use it as a starting hypothesis, and re-derive the call in Part B. |
| `Reject` | Its markers are not enriched, or the type is implausible for the tissue | Ignore the label, and re-derive the call in Part B. |

Present the verdicts to the user with the reasons, and wait for approval.
Record them in `published/evaluation.tsv`.

Adopted types are written as rows of the annotation table keyed on
`published_celltype` (see Step 9). Their `Evidence` text cites the paper,
its validation, and the markers you confirmed. Part B then covers the
cells and types that are left: revised and rejected types, missing expected
types, and cells that have no published label.

## Part B: annotate

### 4. Search the literature for markers (species + tissue)

Search only for the gaps: expected types (Step 2) that have no `function`
marker in `references/markers/` and were not adopted in Step 3. Check
`references/atlas_catalog.tsv` and `references/atlases/` before searching the
web: the atlas for this species and organ may already be reviewed, and each
atlas note lists its known gaps. If the atlas note and the marker tables
already give a `function` marker for every expected type, the web search
can be skipped; say so.

First decide whether `references/markers/` already covers **this species
(or a close relative) in this tissue**:

- **Close relative:** the same family for eudicots (Brassicaceae for
  Arabidopsis tables), or the same tribe for grasses (Andropogoneae, e.g.
  maize or sugarcane, for sorghum tables).
- **Tissue:** must match. A sorghum root table does not cover sorghum
  panicle, and an Arabidopsis leaf table does not cover tomato leaf.

If it is not covered, search the web before mapping anything. Do both
searches for the species *and* the tissue, then widen to the closest
relatives if nothing turns up:

1. **Existing single-cell data.** Find scRNA-seq/snRNA-seq atlases and
   collect the marker lists the authors used to annotate. These are in
   supplementary tables, GitHub, or Zenodo, and plant single-cell databases
   index them. Note any per-cell labels; they make a benchmark.
2. **Characterized markers and reporter lines.** Find genes shown by
   promoter-reporter, in situ hybridization, or mutant phenotype to be
   specific to a cell type in this species and tissue.

Grade everything you find with the existing evidence tiers. Reporter or in
situ validation of a gene with a cell-type function is `function`;
expression from an atlas is `expression`. Write the results as a new table
in `references/markers/`, with the DOI in `source` and a cited `basis`.
Report what you searched and found, and get the user's approval before
adding the table to the skill. An atlas's markers are only as good as its
annotation, so judge the atlas with the Step 3a review (coverage,
proportions, marker quality) before taking its marker list.

Search queries, sources, the grading rules, and access etiquette are in
`references/literature_search.md`. **Read it before searching.** If the
search tools are unavailable, say so, and continue with the existing tables
and the user's markers.

### 5. Map reference markers to the species (`scripts/map_markers.py`)

Pick marker tables from `references/markers/` (see its `README.md`) by
phylogenetic proximity and tissue, in this order:

1. **Primary atlas tables** (`primary/<species>_<organ>.tsv`) for the same
   species and organ, from the 2026-10 survey. Available for Arabidopsis
   (endosperm, fruit, inflorescence, leaf, root, seed, seedling, shoot apex,
   stem), Brassicaceae root, cotton ovule, Lotus root, maize (embryo,
   endosperm, inflorescence, leaf, root, seed, shoot apex), Medicago nodule,
   Populus stem, rice (inflorescence, seed), soybean (nodule, root, seed),
   tomato (root, other organs), and wheat (inflorescence, root). Read the
   matching `references/atlases/<group>.md` for caveats.
2. **Curated core tables** (below) for the lineage, for conserved functions,
   and the **characterized markers** (`characterized/<species>.tsv`):
   reporter-, in situ- and mutant-defined genes for cell types the atlases
   lack (root cap, QC, seed-coat layers, embryo sac, bundle sheath, sieve
   elements, endosperm domains, nodule zones). Map the Arabidopsis rows by
   homology like the core tables.
3. **Secondary atlas tables** (`secondary/`) only when nothing above covers
   the species and organ (barley, Brachypodium, cassava, Catharanthus,
   cucumber, Marchantia, Medicago root, peanut, pepper, Physcomitrium, pine,
   Selaginella, sorghum leaf and root, strawberry, rice leaf, and other organs
   of the species above). Treat calls that rest on them as hypotheses.

Each survey table uses one ID system per species (listed in the README);
switch with `--id-column alt_id`. Organ tables use tissue values such as
`seed` or `inflorescence`; filter with `--tissue <organ> --tissue any`.

Curated core tables:

| Target | Tables | Homology search against |
|---|---|---|
| Eudicot leaf | `arabidopsis_leaf.tsv` | `arabidopsis` hub (Araport11) |
| Eudicot root | `arabidopsis_root.tsv` (Shahan et al. 2022 curated + classic) | `arabidopsis` hub |
| Sorghum itself | `sorghum_leaf.tsv`, `sorghum_root_Guillotin2023.tsv` with `--no-blast` | none |
| Rice root | `rice_root.tsv` with `--no-blast` (MSU7 IDs; add `--id-column alt_id` for RAP-DB IDs), plus `arabidopsis_root.tsv` for conserved functions | Araport11 for the Arabidopsis table only |
| Other grasses | the sorghum tables (and `rice_root.tsv` for root), plus the Arabidopsis tables for conserved functions | `sorghum_v5` (or public `sorghum_v3`), `rice_msu7`, `maize_v5` and `arabidopsis` hubs (one run each) |

```bash
M=~/.claude/skills/plant-celltype-annotation/references/markers
python scripts/map_markers.py \
    --blast species_vs_Araport11.tsv [--blast-reverse Araport11_vs_species.tsv] \
    --query-strip-regex='-mRNA$' --ref-annotation araport11_annotation.tsv \
    --reference $M/arabidopsis_leaf.tsv --target-traits eudicot Solanaceae \
    --out-gene-map gene_map.tsv --out-markers markers_from_arabidopsis.tsv

# same species: reference IDs are already the data's IDs
python scripts/map_markers.py --no-blast --target-traits Sorghum \
    --reference $M/sorghum_leaf.tsv $M/sorghum_root_Guillotin2023.tsv --out-markers markers_sorghum.tsv
```

- **Always pass `--target-traits`.** Rows carry `requires`/`excludes` tags,
  and the script drops markers that don't apply to the target, listing each
  one with the reason. For example:
  - Rubisco as a mesophyll marker is excluded for C4.
  - Subsidiary, silica, and ligule markers require `grass`.
  - Arabidopsis root epidermal-patterning markers (GL2, TTG2) require
    `eudicot`.

  Vocabulary (full list and implications in `references/markers/README.md`):
  `eudicot monocot grass C3 C4 Brassicales Brassicaceae Solanaceae Capsicum
  Fabaceae Gossypium Rosaceae Apocynaceae Cucurbitaceae Sorghum Oryza
  gymnosperm conifer bryophyte moss liverwort hornwort lycophyte fern
  angiosperm tracheophyte magnoliid Triticeae Euphorbiaceae Phaseoleae`. Specific
  traits imply general ones (`Sorghum` implies `grass C4 monocot`; `Oryza`
  implies `grass C3 monocot`; `liverwort` implies `bryophyte`).
  - Vascular, root, stomatal, hydathode, periderm, axillary-meristem, flower
    and seed rows carry `excludes=bryophyte`.
  - Eudicot-only types (palisade/spongy mesophyll, adaxial/abaxial
    epidermis, GL2-type trichome patterning) carry
    `excludes=monocot,gymnosperm,bryophyte`.
  - The Arabidopsis SULTR2;1 (xylem parenchyma) and SULTR2;2 (bundle sheath)
    rows require `Brassicaceae`. The family marks vascular bundles everywhere,
    but the split between cell types is not conserved (see
    `references/plant_pitfalls.md`). `map_markers.py` warns when members of
    one gene family are listed for different cell types.
- **Non-angiosperm targets** (`liverwort`/`moss`/`hornwort` → bryophyte;
  `lycophyte`; `fern`; `gymnosperm`/`conifer`) drop the types they lack:
  bryophytes drop vascular, root, stomatal, SAM-zone, primordium, boundary,
  stem-cell-niche, pavement, trichome, flower, seed and endosperm types; ferns
  and lycophytes also drop SAM zonation, pollen/sperm, ovule, seed/embryo and
  secondary-growth types; gymnosperms drop flower, fruit, endosperm,
  seed-coat and companion-cell types. Epidermis, protoderm and cell-cycle
  states are kept. `scripts/lineage_tags.py` writes these tags; run it on
  *all* tables after adding rows (`tests/test_lineage_tags.py` checks).
- **Same-species tables (`--no-blast`): check that the IDs match.** Pass
  `--h5ad data.h5ad` (or `--target-genes var_names.txt`); the script reports
  how many table IDs are in the data and warns below 50%. Versioned
  var_names (tomato `Solyc..g......3`, `.1` suffixes): `--match-unversioned`.
  Other ID styles: `--id-rewrite 'FROM=>TO'` on the table side (e.g.
  `'Glyma\.=>GLYMA_'`) or `--query-rewrite` on the data side (e.g.
  `'_evm=>-evm'`). Rice RAP-DB data: `--id-column alt_id`, or convert with
  `references/annotation/rice_msu_rap.tsv.gz`.
- **Read the "gene marks several cell types" warning.** Pairs marked `*` are
  subtypes or fragmented names; merge true synonyms through
  `references/markers/celltype_aliases.tsv`, or don't use those genes to
  separate the two types.
- **Tissue filter.** `--tissue leaf --tissue any` keeps rows whose tissue
  value contains `leaf` as a token (`leaf_stem_phloem` counts). Cell types that
  are shared across organs (phloem, xylem, procambium, guard, dividing
  cells) can be taken from another organ's table when the target organ's
  table lacks them: add that organ to `--tissue`, and say so in the Evidence
  column.
- **Reference proteomes (hubs).** `references/proteomes.tsv` lists, per
  reference species, a public proteome whose gene IDs match the marker
  tables, with the measured match per table. `bash
  scripts/fetch_reference.sh <key> <outdir>` downloads it, keeps one isoform
  per gene, renames headers to the table gene ID, and writes
  `<key>.pep.fa`, `<key>_annotation.tsv` (symbols, descriptions) and
  `<key>.dmnd`; `list` shows the keys. Build each hub once and reuse it.
  Search each hub that has tables for your lineage:

  | Target lineage | Hubs (keys) | Tables to map, and ID column |
  |---|---|---|
  | Grasses (maize, sorghum, millets, sugarcane, rice relatives) | `rice_msu7`, `maize_v5`, `sorghum_v5` (Phytozome login; public: `sorghum_v3`), `arabidopsis` | rice tables with `rice_msu7` (ref_gene) or `rice_rap` (`--id-column alt_id`); maize primary tables; sorghum core tables; Arabidopsis tables for conserved functions |
  | Triticeae and other Pooideae (wheat, barley, rye, oat, Brachypodium) | `wheat`, `barley`, `rice_msu7`, `arabidopsis` (+ `brachypodium` with `--id-column alt_id`) | wheat_*, barley_* (ref_gene); rice tables; Arabidopsis tables |
  | Other monocots | `rice_msu7`, `arabidopsis` | |
  | Solanaceae (tomato, potato, pepper, Nicotiana) | `tomato`, `arabidopsis` | tomato_*, characterized/tomato; Arabidopsis tables |
  | Fabaceae | `soybean` (Wm82.a4; `soybean_a2` for soybean_nodule), `medicago` (MtrunA17; `medicago_mt4` with `--id-column alt_id` for Mt4.0 Medtr IDs), `arabidopsis` | soybean_*, medicago_*, characterized/{soybean,medicago}; Lotus tables cannot be mapped from public files (Gifu `LotjaGi` IDs; only lotus_nodule alt_id via `lotus_mg20`) |
  | Brassicaceae | `arabidopsis` | Arabidopsis tables (`--no-blast` for Arabidopsis itself) |
  | Salicaceae / trees | `poplar`, `arabidopsis` | populus_stem (ref_gene), populus_root (`--id-column alt_id`) |
  | Bryophytes | `marchantia` (liverworts), `physcomitrium` (mosses), `arabidopsis` | marchantia_other, characterized/marchantia, physcomitrium_other; pass `--target-traits bryophyte liverwort` or `moss` |
  | Other eudicots | `arabidopsis` + the nearest hub (`tomato` for asterids; `poplar`, `soybean` or `medicago` for rosids) | |

  Run DIAMOND in the allocation, forward and reverse, once per hub
  (minutes per hub).
  Reduce your species' proteome to one isoform per gene first.
  ```bash
  H=/path/to/hubs  # the fetch_reference.sh outdir
  hub=arabidopsis
  diamond makedb --in species.pep.fa -d species
  diamond blastp --very-sensitive -k 10 -e 1e-5 -q species.pep.fa -d $H/$hub \
      -o species_vs_$hub.tsv --outfmt 6 -p $SLURM_CPUS_PER_TASK
  diamond blastp --very-sensitive -k 10 -e 1e-5 -q $H/$hub.pep.fa -d species \
      -o ${hub}_vs_species.tsv --outfmt 6 -p $SLURM_CPUS_PER_TASK
  python scripts/map_markers.py \
      --blast species_vs_$hub.tsv --blast-reverse ${hub}_vs_species.tsv \
      --query-strip-regex='-mRNA$' --ref-annotation $H/${hub}_annotation.tsv \
      --reference $M/arabidopsis_leaf.tsv $M/primary/arabidopsis_leaf.tsv \
      --target-traits eudicot Solanaceae \
      --out-gene-map gene_map_$hub.tsv --out-markers markers_$hub.tsv
  ```
  - Hub FASTA headers are already the tables' gene IDs, so the default
    `--ref-strip-regex` works for every hub (it only removes `.<digits>`,
    which no hub gene ID ends with). `--query-strip-regex` must turn your
    species' protein IDs into `adata.var_names`.
  - When the hub's ID system is the table's `alt_id` (rice_rap, wheat_v2,
    medicago_mt4, brachypodium, lotus_mg20, poplar for populus_root), add
    `--id-column alt_id`.
  - Use the Arabidopsis gene map for DE annotation (best symbols). Other hubs
    carry few symbols; the marker table's `symbol` column names the marker.
  - Login-only resources (Phytozome sorghum v5.1, Lotus Gifu, cotton ZJU) are
    listed with `access` notes; build them from your own download with
    `LOCAL_SRC=/path/to/proteins.fa.gz bash scripts/fetch_reference.sh <key> <outdir>`.
  - Without DIAMOND, `blastp -max_target_seqs 10 -outfmt 6` works on the same
    FASTA but is slower.
- **Close species** (maize ↔ sorghum, rice ↔ other grasses): the
  reverse-best paralog rescue also accepts pairs with ≥ 90% identity over
  aligned residues (`--rescue-min-pident`); the log says which rule rescued.
- **Orthology tables instead of BLAST.** When the dataset comes with an
  OrthoFinder-style table (one row per species gene, with its Arabidopsis
  orthologues and the relationship), pass `--orthology table.tsv` instead of
  `--blast` (columns set by `--orth-query-col`, `--orth-ref-col`,
  `--orth-rel-col`; defaults `gene_id`, `At_orthologues`, `At_relationship`).
  Symbols and descriptions come from the table's `<prefix>_symbols` /
  `<prefix>_descriptions` columns automatically, and the outputs carry a
  `relationship` column (1:1, many:1, …) instead of % identity.
  Every listed orthologue counts as rank 1. One-to-one pairs are marked
  `rbh=yes`. There is no identity or bitscore, so the copy cap falls back to
  file order.
- **BLAST depth.** Run BLASTP with `-max_target_seqs 5` or more and add the
  reverse search (`--blast-reverse`). With one hit per gene, markers whose
  target gene best-hits a paralog are lost silently; histones, PCNA, cyclins
  and CDKs are typical, which empties the cell-cycle marker sets.
  `map_markers.py` warns when the file looks like one hit per gene, and
  lists unmapped markers and cell types left with none.
- With several reference species, run once per reference and pass all
  outputs to the next steps (`--markers a.tsv b.tsv`). Use the
  Arabidopsis-based gene map for DE annotation; it has the best functional
  annotation.
- Look at the query IDs in the BLAST file and in `adata.var_names` first.
  Then set `--query-strip-regex` so that they match. The evidence script
  reports the match rate, and anything under ~50% means the IDs don't line up.
- Pass regexes with `=` (`--query-strip-regex='-mRNA$'`). Otherwise
  argparse reads a leading `-` as a new flag.
- By default only species genes whose **best** hit is the marker locus are
  kept (`--max-marker-rank 1`).
  - With `--blast-reverse`, the script also rescues the species gene that is
    the marker's own best hit, even if that gene best-hits a paralog. This
    recovers PCNA1, CYCB1;1, and XCP2 in tomato. Rescued rows are marked
    `via=reverse_best`.
  - A rescue needs a bitscore ratio of at least `--rescue-min-ratio`
    (default 0.85): bitscore(gene, marker) ÷ bitscore(gene, its own best
    hit).
    - Same-function duplicates score 0.89–1.00.
    - When the target has no true ortholog, the "rescue" grabs a different
      subfamily. In sorghum, Arabidopsis SUC2 landed on a SUT4-type
      vacuolar transporter at 0.78. Blocked rescues are logged; review them
      for markers you care about.
- `--max-copies 5` caps the species genes per marker (RBH first, then
  bitscore). Without the cap, family markers (LTP, chitinase, BAHD) map to
  dozens of genes and dilute the scores.
- Lineage-specific cell types (for example, Solanaceae glandular trichomes)
  do not transfer through Arabidopsis. Supply markers curated in a relative
  from the same family as an extra marker table, or leave these types
  unlabeled.
- **Solanaceae (Nicotiana, tomato, pepper, potato).** Use the Arabidopsis
  core and `characterized/arabidopsis.tsv` tables via Araport11, plus the
  tomato tables via a search against the `tomato` hub (SGN ITAG4.1; a second
  `map_markers.py` run): `primary/tomato_root.tsv`, `primary/tomato_other.tsv`
  (glandular trichome: TPS5, SlMYC1, NDPS1; trichome: Wo, H) and
  `characterized/tomato.tsv`. Pass `--target-traits eudicot Solanaceae`.
- Merge in the user's curated markers (same columns: `gene_id`, `symbol`,
  `cell_type`). Curated markers win.

### 6. Build per-cluster evidence (`scripts/cluster_evidence.py`)

```bash
python scripts/cluster_evidence.py --h5ad data.h5ad --output evidence/ \
    --gene-map gene_map.tsv --markers markers_from_arabidopsis.tsv [markers_sorghum.tsv] \
    --stress-genes ~/.claude/skills/plant-celltype-annotation/references/stress/protoplasting_induced_Shahan2022.txt \
    --meta-keys sample Treatment [--cluster-keys leiden_res0.3 leiden_res0.5 ...]
```

- `--stress-genes` flags clusters whose top DE genes are mostly
  dissociation-induced. The list is the protoplasting response in
  Arabidopsis root (Shahan et al. 2022), matched through each gene's rank-1
  Arabidopsis homolog. Treat a flag as "probably a stress state", not proof.
  It is less informative for nuclei (snRNA-seq) data.
- In marker scores, `*` marks function-evidence markers.

For every cluster key it writes:
- `cluster_evidence_<key>.md`, the file you read. Each cluster gets its
  size, sample/treatment composition (with enrichment flags), QC relative to
  the dataset, parent clusters at coarser resolutions, top marker-set scores,
  and top DE genes with Arabidopsis homolog symbol/description.
- `marker_scores_<key>.tsv`: cluster × cell-type score (mean z-scored marker
  expression across clusters) plus the fraction of cells expressing.
- `marker_expression_<key>.tsv`: long table of per-marker mean, fraction,
  and z for each cluster.
- `de_<key>.csv`: top Wilcoxon genes, annotated with homologs.
- `cluster_hierarchy.tsv`: how clusters nest across resolutions.
- `evidence_plots.pdf`: UMAPs per key, and marker dotplots per key.

DE is subsampled per cluster (`--max-cells-per-cluster`, default 2000) to
keep large datasets tractable.

- **Same-species runs (`--no-blast`) have no gene map,** so DE genes would be
  bare IDs. Pass `--gene-annotation` with a `gene_id, symbol, description`
  table for the species (for example the Phytozome `annotation_info` file:
  locus, best Arabidopsis hit name, defline), or run a BLAST against
  Araport11 anyway and pass its `--gene-map`.
- **The stress check needs Arabidopsis IDs.** Without a gene map it matches
  nothing, and the script says so; don't read its 0% as "no stress".
- **Scores are relative and capped.** The largest possible marker score with
  n clusters is about sqrt(n−1), so compare scores within one cluster key,
  not across resolutions or subclusterings. A marker adds to a cluster's
  score only if at least `--min-frac` (default 2%) of its cells express it.
  The low floor keeps sparse transcription-factor markers (SCR/SCL23 in
  nuclei) in play. Each driving marker is shown as `z (frac in vs mean frac
  in other clusters)`.
- **Gene names.** When several marker tables give one gene different names,
  the species' own name (same-species or user-curated table) is shown, and
  the reference-homolog name is kept in `ref_symbol`.
- **Markers found vs measurable.** The log prints `N/M in var_names, K/M
  found (detected in ≥ 1 cell)`. Markers with zero counts everywhere are
  listed as *not measurable here* and left out of the scores; when ≥ 20% of
  markers are missing or all-zero (or the gene list looks filtered:
  HVGs only, < ~12,000 genes) the script warns. A type whose markers are
  not measurable cannot be called absent.
- **Marker-score line:** `det a/b` = markers detected out of those measured,
  `best` = the highest in-cluster fraction of any marker, `[1 gene]` = the
  score rests on one gene (weak). Per-type details are in
  `marker_score_details_<key>.tsv`.
- **QC vs siblings:** QC entries read `x<dataset ratio>; sib x<ratio to
  sibling clusters>` (same parent at the next coarser resolution). The
  `low-QC candidate` flag needs counts and genes < 0.6× both medians.
- **Doublet flag:** fires only for two *unrelated* types, each with ≥ 2
  detected and ≥ 2 driving markers that are not all expression-tier; pairs
  sharing a driving gene, a name token, an alias or a lineage group are
  skipped, and counts must be ≥ 1.3× the median. Pass per-cell scores with
  `--doublet-scores scrublet.tsv` (barcode + `doublet_score`; or keep them in
  `obs`); the cluster median must then be ≥ 1.5× the dataset median. It is a
  prompt to check, not a call.
- **Several gene maps:** `--gene-map primary.tsv second.tsv …`; the first
  names DE genes, the others are appended (`[Mp: SYMBOL (ID)]`).
  `de_<key>.csv` carries `ref_symbol`, `ref_description`, `symbol` and
  `other_homologs`. For Arabidopsis symbols without a BLAST file, pass
  `--gene-annotation references/annotation/araport11_genes.tsv.gz`.
- The script warns about markers missing from the data, grouped by cell
  type, and about cell types with no marker present at all. Calling such a
  type "absent" is not supported by the markers.

With published labels (Step 3b), add `--import-labels`, the published key
in `--cluster-keys`, and the published key in `--meta-keys`. Cells with no
published label appear as `nan`.

### 7. Reason about each cluster

Read the evidence markdown, starting with the coarsest resolution. Skip
clusters that are already covered by adopted published types (Step 3), but
do check that they agree with the published labels. For each remaining
cluster:

1. **Quality first.** Is it low in counts or genes, high in organellar
   fraction, or driven by one sample? Compare it with its **sibling
   clusters** (same parent at the coarser resolution; the evidence file gives
   both ratios), not only with the dataset median: nuclei of some types
   (vacuolated parenchyma, epidermis) are small everywhere. Call
   `Low_Quality` only when it is low against siblings too and has no
   biological program; a low-RNA cluster that still carries a program is
   `Unknown_<hint>` (e.g. `Unknown_low_RNA_cortex_like`). A cluster driven
   by one library or stage is a batch question first: check whether the
   same program appears, weaker, in the other libraries' cells of the
   neighbouring type, and whether it is anatomically plausible (a stem
   region, a developmental stage) before calling it technical.
   **Doublets:** a cluster with high counts (≳1.3× the median) that
   co-expresses two unrelated lineage programs is likely doublets. The
   evidence markdown flags "possible doublets" only for unrelated types
   (pairs that share driving genes, a name, an alias or a lineage are
   skipped, and each type needs ≥ 2 detected markers); still confirm two
   independent programs gene by gene.
   Check at a finer resolution. Doublet scores (scrublet) help, but their
   automatic threshold often misses plant nuclei doublets; compare the
   cluster's median score with the others. Label such clusters
   `Doublet_like` or exclude them (Step 9).
2. **Marker-set score.** Is there a clear top cell type (score ≳ 1, well
   above the runner-up)? Which individual markers drive the score? One
   strong marker plus a coherent DE list beats several weak ones.
   - **Cap confidence by detection.** If the best marker for a call is
     detected in fewer than ~15% of the cluster's cells, the call is `low`
     at most, whatever the score; a score driven by one gene (`[1 gene]` in
     the evidence file) is a lead, not a call.
   - **Rows from the wrong organ or lineage can win** (a periderm row in a
     root tip, an embryo-sac row in a panicle). Check that the top type
     exists in this tissue (`expected_cell_types.tsv`) before reading the
     score.
   - **Judge each marker by its fraction in vs out, not by an absolute
     fraction.** Transcription factors and channels are sparse in nuclei.
     SCL23 in 6% of a cluster vs 0.5% elsewhere is real enrichment; a
     transporter in 90% vs 60% is not specific.
   - **Weigh a marker by its family.** When the driver is one member of a
     family split across neighbouring types (SULTR2, SWEET, AAP, NPF), and
     especially when it was matched by best hit rather than RBH, it tells
     you the compartment (vascular bundle), not the type.
3. **Unbiased DE.** Do the top DE homologs tell the same story? Look for
   known functions: cuticle/wax → epidermis; SWEETs → phloem parenchyma;
   SUC2 → companion cell; XCP/IRX/cellulose synthases → xylem; histones →
   S phase; cyclin B / KNOLLE → G2/M; PR proteins → defense state. If DE
   contradicts the score, trust DE and investigate.
   - **Cell-death programs are not automatically senescence, and not
     automatically xylem.** Papain-like cysteine proteases (RD21, CEP1),
     MC9-type metacaspases and nucleases (BFN1) mark *developmental* PCD,
     which happens in differentiating xylem, tapetum, root cap, nucellus and
     degenerating organs. Call **senescence** only with senescence evidence
     (SAG12, chlorophyll breakdown *and* declining photosynthesis/ribosome
     programs, in an old organ). Test senescence with a **panel**, never
     one gene: SAG12, SAG13, SAG20/21, SAG101, ORE1/NAC092, WRKY53, NYE1/SGR,
     NYC1, PAO, autophagy (ATG8), aspartic/cysteine proteases (APA1, RD21),
     glyoxalases and protease inhibitors, plus falling photosynthesis.
     When the canonical marker is not measurable (absent or all-zero), the
     result is "untested", not "not found". Call **xylem** only with xylem identity
     genes (VND/NAC, XCP1/2, ACL5, WAT1, secondary-wall CESA4/7/8, IRX)
     enriched in the cells, plus adjacency to procambium; PCD genes alone
     are not enough. In a rice panicle test the xylem was a 182-cell subset
     *inside the procambium cluster* (ACL5 35% vs 5%, XCP2 RBH 15% vs ≤2%,
     WAT1, VND-like 26%, PXY), found only by subclustering it; a separate
     PCD cluster (MC9 homolog 51%) had no xylem identity genes and was not
     xylem.
4. **Resolution.** When a function marker of an expected-but-missing type
   is enriched only "in a subset" of a cluster (the evidence shows it at
   10–20% of the cluster and ~0% elsewhere), subcluster that cluster
   (Step 8, `--recompute-pca --batch-key sample`) and check the type's
   markers per subcluster before labelling the whole cluster. Rare types
   (guard, xylem, companion cells, trichomes)
   often separate only at high resolution. Common types (mesophyll) are
   often split into state sub-clusters at high resolution, so label them at
   low resolution. Use `cluster_hierarchy.tsv` to choose the level.
5. **Ambiguous or mixed.** If markers of two types are both present, or DE
   is uninformative, subcluster it (Step 8) or leave it `Unknown`.
6. **Abundance and program.** Compare the cluster's share of cells with the
   type's expected abundance (`expected_cell_types.tsv`, or the published
   atlas for the organ). For example, where bundle sheath is expected to be
   several-fold more abundant than xylem parenchyma, a cluster holding 10% of
   the cells is unlikely to be xylem parenchyma. Also use the cluster's broad program.
   In a C3 leaf, a vascular-associated cluster that also carries a
   photosynthetic program (RBCS, LHCB, CA at mesophyll-like levels, beyond
   ambient) points to bundle sheath; xylem and phloem parenchyma are not
   photosynthetic. In C4 grasses, the bundle sheath carries the Kranz
   program instead (see the pitfalls).
7. **A cluster with its own program is not the majority type.** If a
   cluster has private DE genes (in ≥ 50% of its cells vs ≤ 5% elsewhere),
   do not give it the majority label "by level and exclusion" (Mesophyll in
   leaves). Label it `<Type>_like` or `Unknown_<program>` and test
   hypotheses (Step 8b: senescence, development, a minor type, a treatment
   or stress state). **Sample enrichment is not batch** unless the cluster
   is absent (or nearly so) from other samples of the same condition; a
   cluster present in every sample but enriched in one is biology until
   shown otherwise.
8. **Read the UMAP shape.** A long arm or projection leaving the main body
   of a type, a thin bridge between types, or a gradient along one axis
   usually means a continuous program (development, ageing/senescence,
   stress, a transition), not noise. Name it, test the genes that change
   along it, and don't absorb it into the neighbouring type.
9. **States never replace the cell type.** A stress, treatment, cell-cycle
   or senescence state can span several types (sulfur starvation in both
   mesophyll and bundle-sheath cells). Keep the type and record the state
   in the annotation table's `State` column (`references/file_formats.md`).
   When a state cluster mixes types, resolve the type per cell: subcluster
   it (`--recompute-pca`), score type markers within it, or follow its
   cells' parent clusters at a coarser resolution. Then write type rows for
   the parts plus a state-only row for the whole cluster.

Consult `references/plant_pitfalls.md` for the relevant tissue and lineage
(C4 grasses invert the mesophyll/bundle-sheath markers, for example).

Then compare the calls with `expected_cell_types.tsv`:

- **An expected type with no cluster** may be rare, lost in capture, or
  merged into a neighbor. Look for it at a higher resolution, or by
  subclustering, before calling it absent.
- **A call that isn't on the list** needs stronger evidence, or a reason
  why the list missed it.

**Name cell types, not tissue layers.** "Epidermis", "Vasculature",
"Vascular", "Stele" and "Ground tissue" are layers or tissue systems made of
several cell types. Label the types: **Pavement** (the bulk of non-guard,
non-trichome epidermal cells), **Guard**, **Trichome** / **Glandular_Trichome**,
**Protodermal** (undifferentiated, young epidermal cells), and
species-specific types (Bulliform, Subsidiary, Silica, Cork, Long/Short cells
in grasses); in the vasculature Xylem, Xylem_Parenchyma, Phloem_Companion,
Sieve_Element, Phloem_Parenchyma, Procambium, Bundle_Sheath. Layer names
(`Epidermis`, `Vasculature`) are valid **only when the identity within the
layer is ambiguous**: say why in the Evidence column (which types were tested
and why none fits). `apply_annotations.py` prints a reminder when a layer
name is used.

**Label conventions** for calls that are not a clean type:
- `<Type>_like` with `low` confidence: lineage-consistent but no specific
  marker (e.g. `Cortex_like` called by exclusion). Say "by exclusion".
- Transitional states: `<TypeA>_to_<TypeB>` (e.g. `Procambium_to_Xylem`)
  when a cluster carries both programs at intermediate levels along a
  trajectory, not two unrelated programs (that is a doublet).
- Developmental-state blocks when no organ marker separates them:
  `Young_<lineage>`, `Expanding_<lineage>`, `Mature_<lineage>`; state the
  organ-identity alternative in the Evidence column.
- `Unknown_<hint>` for clusters with a program but no identity.
- A layer or lineage name (`Epidermis`, `Vasculature`, `Trichome`) for
  cells that a parent clustering separated as that lineage but whose exact
  type is ambiguous.

Then draft the annotation table (format in `references/file_formats.md`),
including an `Evidence` column, and present it to the user as a compact
table. Say which rows were adopted from the publication and which were
derived here.

### 8. Subcluster ambiguous clusters (`scripts/subcluster.py`), if needed

**Subclusters never fold back into the majority type.** The parent
clustering separated these cells (a trichome or vascular cluster) from the
majority (mesophyll). A subcluster that only looks like mesophyll (ambient
photosynthesis RNA, no private program) keeps the parent's layer or lineage
name (e.g. `Vasculature`, `Trichome`) or `Unknown`, not Mesophyll, unless its
own markers clearly say so;
`apply_annotations.py` warns when a subcluster row reuses a broad base label.

```bash
python scripts/subcluster.py --h5ad data.h5ad --cluster-key leiden_res0.3 \
    --clusters 6 --output-h5ad sub_cl6.h5ad --resolutions 0.1 0.3 0.5
```

Then run `cluster_evidence.py` on `sub_cl6.h5ad` with
`--cluster-keys leiden_sub_0.3`, and reason about the result the same way.

By default the subclusters reuse the global (integrated) PCA. Its axes
separate the major types and may not capture variation within one cluster.
When looking for a rare type inside a cluster, add `--recompute-pca`
(subset HVGs + PCA). Add `--batch-key sample` (or the library column) so
the subset PCA is Harmony-corrected; without it, subclusters often split by
library. Still check the subclusters against sample.

### 8b. Follow up on unlabeled clusters (required before Step 9b)

Do this without being asked, for every cluster still `Unknown` after
Steps 7–8, and always when Unknown holds more than ~10% of cells. Also do it
for clusters labelled only as a **state** (senescing, stress, wound,
defense) or at **low** confidence **whenever an expected type has no cluster
yet**: the missing type is often hiding under a state label. And test every
expected-but-missing type explicitly, not only the hypotheses the DE
suggests. Reference
marker tables are built from model species and miss lineage- and
organ-specific programs, so a large Unknown block usually means a known type
with no marker in the tables, not a new type.

1. **Write one or more hypotheses per cluster.** Draw them from:
   - expected types (`expected_cell_types.tsv`) that have no cluster yet;
   - the organ's function in this species: storage (inulin, starch, oil,
     protein), specialized metabolism (latex, resins, alkaloids, glucosinolates),
     symbiosis, or defense;
   - the cluster's own top DE homologs, read as a program (transporters,
     biosynthetic enzymes, cell-wall genes);
   - where the cluster sits in `cluster_hierarchy.tsv` and on the UMAP
     (which labeled neighbours it splits from);
   - small distinct programs inside a majority type (a few hundred cells
     with private DE genes inside "Mesophyll") are hypotheses too.
2. **Find marker genes for each hypothesis.** Prefer the pathway's
   characterized enzymes or transporters from the same genus or family. Their
   sequences are in UniProt, which the REST API serves without a key (check
   that the node has network access):
   ```bash
   curl -s "https://rest.uniprot.org/uniprotkb/search?query=(taxonomy_id:<genus taxid>)+AND+(<enzyme name>)&fields=accession,protein_name,organism_name,length&format=tsv"
   curl -s "https://rest.uniprot.org/uniprotkb/<ACC>.fasta" >> hypothesis_refs.fa
   ```
   Search them against the target proteome with DIAMOND (`--very-sensitive
   -k 25`). Assign each target gene to the reference it matches best, so that
   paralogs from the same family (invertase vs fructosyltransferase vs
   exohydrolase) are separated. Write the genes as a small marker table with
   `basis` and `source`.
3. **Test the hypothesis in the data.** Score the genes per cluster with
   `scripts/check_genes.py` (symbols or IDs in; resolves every copy through
   the gene map; per-cluster fraction, mean and z out) or
   `cluster_evidence.py`. **Never type gene IDs from memory**: resolve them
   through the mapped marker table or the gene map (a test rejected a
   validated type after checking a mistyped AGI). Test the genes the
   competing explanation rests on too, and cite counter-evidence.
   Pathway enzymes of abundant products are often detected in most nuclei
   everywhere, so judge them by **level**: a cluster with clearly higher mean
   expression and no competing identity supports the hypothesis. The report
   counts a marker as enriched when its mean is ≥ 1 log unit higher and at
   least half the cells express it.
4. **Label or keep `Unknown`.** Label the cluster when the evidence holds, at
   lower confidence if it rests on level only. Otherwise keep `Unknown`, and
   write the hypotheses you tested, and why they failed, in the Evidence
   column.
5. **Report what you did.** List the hypotheses, the genes and their
   identity to the reference, and the result. Present this with the
   annotation table.

Example: in an Asteraceae storage root, a third of the nuclei were Unknown
after the Arabidopsis root tables. The hypothesis was inulin storage
parenchyma. 1-SST and 1-FFT from a congener were >95% identical to single
target genes. Those genes were detected in most nuclei everywhere, but were
highest in three Unknown clusters, which were then labeled storage
parenchyma at medium-low confidence.

### 9. Apply and validate (`scripts/apply_annotations.py`)

```bash
python scripts/apply_annotations.py --h5ad data.h5ad --annotations CellTypeAnnotations.txt \
    --colors CellTypeColors.txt --markers species_markers.tsv \
    [--import-labels sub_cl6.h5ad:leiden_sub_0.3:cl6_sub0.3] \
    [--import-labels published/labels.tsv:<col>:published_celltype] \
    --plots-dir annotation_qc/ --meta-keys sample Treatment \
    --out-h5ad annotated.h5ad            # or --inplace, if the user asks
```

- Rows are applied **in file order**, and the first matching row wins. Put
  fine-resolution and subcluster rows *before* coarse rows. Cells that match
  no row stay `Unknown`.
- **Excluding clusters:** a row whose CellType is `Unknown` claims its cells,
  so later, broader rows can't relabel them. Use it, or a QC label such as
  `Low_Quality`, `Doublet_like` or `Unresolved_Mixed`, for clusters that are
  not a cell type. The report lists QC labels (`--qc-labels` regex) on the
  overview page without a cell-type page.
- Adopted published types are rows keyed on the imported column. The
  `Cluster` value is the published label, spelled exactly as in the file:
  ```
  published_celltype	Guard cell	Guard	Adopted (<Author Year>; FAMA reporter); KAT1 z=2.1 here
  ```
  Put them *before* the de novo rows. Cells with no published label fall
  through to the cluster rows below.
- The `Cluster` field may list several clusters (`0,1,12`).
- The script warns about cluster IDs that don't exist (fix these) and about
  rows that label zero new cells because earlier rows claimed all their
  cells. A shadowed row is harmless when it is a deliberate coarse fallback
  whose cells were all labelled at finer resolution. Otherwise it signals a
  wrong row order or a wrong cluster ID.
- Review `annotation_qc/` with the user:
  - Marker dotplot by cell type: is the diagonal clean?
  - Cell-type × cluster crosstab.
  - Per-sample counts: is every type present in every replicate?

### 9b. Build the evidence report (`scripts/annotation_report.py`)

Always produce this after applying, and only after Step 8b. It is the
deliverable that shows *why* each label holds. Look at it: render pages with
`pdftoppm -png -r 60 report.pdf page` (poppler) and read the PNGs.

```bash
python scripts/annotation_report.py --h5ad annotated.h5ad --annotations CellTypeAnnotations.txt \
    --markers markers_from_arabidopsis.tsv [markers_sorghum.tsv] --gene-map gene_map.tsv [gene_map_maize.tsv] \
    [--gene-annotation target_genes.tsv] [--colors CellTypeColors.txt] \
    [--extra-genes Bundle_Sheath=Nb05g00210,ACA1,NPF6.2] [--alias Procambium_Dividing=Procambium,Dividing_cells] \
    --output annotation_qc/annotation_report.pdf
```

The PDF contains:
- **An overview page:** UMAP labeled by cell type, plus a summary table
  with the strongest marker for each type, ordered by cell count.
- **Cluster pages:** a UMAP of each cluster key used by the annotation rows
  (and so by the violin plots), with cluster IDs printed on it and a table
  of each cluster's size and assigned cell type. The report can be read
  without the h5ad.
- **One page per cell type**, which shows:
  - a UMAP highlighting the type, and the annotation rows with their
    Evidence text
  - for each marker: a viridis expression UMAP, violins across the
    clusters of the defining key (the annotated clusters highlighted), and
    a text panel with the marker's evidence tier, homology (locus, rank,
    % identity, RBH, rescue), basis, source, and in-data enrichment
- **A dotplot** of every marker shown, by cell type.

Markers per page:
- Markers must be enriched in the cell type and detected in at least
  `--min-detect` (default 10%) of its cells. Up to `--max-markers` (default
  3) are shown, ranked by specificity (how much more often and more strongly
  the type expresses the gene than all other cells); evidence tier and
  confidence only break near-ties. At least one function-tier marker is
  shown when one passes the floor. Enriched markers below the floor (sparse
  regulators such as GL2 or FAMA) are listed in the text panel and plotted
  only when nothing reaches the floor. Other gene copies of a shown marker
  are listed with their detection.
- **A call that rests on genes outside the marker tables** (DE genes, Step 8b
  hypothesis genes) must show them: `--extra-genes CellType=GENE1,GENE2`
  (repeatable; IDs or symbols resolved through the gene maps and
  annotations, never typed from memory), labelled "extra (not in marker
  tables)".
- A marker counts as enriched by a clear mean gap with a detection ratio
  ≥ 1.5, by a detection ratio ≥ 3 for sparse markers, or by a mean gap
  ≥ 1 log unit in at least half the cells for abundant genes detected
  everywhere.
- Markers from the tables that are *not* enriched are listed, because
  contradicting evidence must stay visible.
- With no enriched marker, the page falls back to top DE genes, labeled as
  data-driven only. Treat such cell types as weakly supported.
- Use `--alias` when an annotation name differs from the marker tables'
  cell-type names. True synonyms in `references/markers/celltype_aliases.tsv`
  are matched automatically; otherwise related names are matched by name
  tokens (`Phloem` markers count for `Phloem_Companion`, but base-type
  markers never count for `<X>_Parenchyma` or `Phloem_Pole_Pericycle`).

### 10. Iterate and record

Record the decisions (which published labels were adopted, revised, or
rejected; which markers were dropped and why; which clusters were left
`Unknown`) in the annotation file's `Evidence` column or a README
next to it. Offer to add species-validated markers to the matching table in
`references/markers/`. Give each one an `evidence` tier, a one-line `basis`,
trait tags, and a source, so that the skill improves across species. Only
add `function` or `characterized_enriched` markers by hand. Expression-only
markers belong in published atlas tables, labeled as such.

## Environment notes

- The scripts need scanpy ≥ 1.8, anndata, pandas, numpy, scipy, and
  matplotlib. They are written to work with scanpy 1.8.2 / pandas 1.5.
- Use a large-memory node for h5ad objects over ~40 GB.
- The per-dataset reviews behind `references/atlases/` and
  `references/atlas_catalog.tsv` (supplements, label extracts, ID tables) are
  kept in the maintainers' resources folder, not in this repository.
- `tests/smoke_test.sh` runs the whole script chain on a synthetic dataset in
  about a minute (on a compute node). Run it after changing any script.
  `tests/README.md` describes the test protocol.
- `scripts/run_step.sbatch` is a generic wrapper:
  `sbatch --mem=256G -p bigmem scripts/run_step.sbatch python .../cluster_evidence.py ...`

## Reference files

| File | Open when |
|---|---|
| `references/published_annotations.md` | Steps 1–3. Covers where published labels live, barcode matching, starting lists of expected cell types and capture biases, and the evaluation rubric and verdict table. |
| `references/literature_search.md` | Step 4, when the species or tissue is not covered. Covers search queries, sources, evidence grading, gene-ID versions, and access etiquette. |
| `references/markers/README.md` | Picking marker tables. Covers the table schema, evidence tiers, trait tags, the provenance of each table, the primary/secondary survey tiers, and each table's ID system. |
| `references/atlas_catalog.tsv` | Step 1 and Step 4: is this dataset (or an atlas of this species and organ) already found or reviewed? 389 datasets with review status, quality, label access, and Oak review folder. |
| `references/atlases/README.md`, `references/atlases/<group>.md` | Before using a survey table, or when choosing a label reference: per species x organ datasets, verdicts, recommended reference, gaps, conflicts. |
| `references/markers/*.tsv`, `primary/*.tsv`, `secondary/*.tsv`, `characterized/*.tsv` | Checking why a gene is a marker. Read its `basis` and `evidence`. |
| `references/proteomes.tsv`, `scripts/fetch_reference.sh` | Step 5: which reference hub (proteome with IDs matching the marker tables) to search for the target lineage; download and build it. |
| `references/markers/celltype_aliases.tsv` | Merging synonymous cell-type names across tables (used by the scripts automatically). |
| `references/annotation/araport11_genes.tsv.gz`, `rice_msu_rap.tsv.gz` | Arabidopsis gene symbols/descriptions (`--gene-annotation`, `--ref-annotation`); rice MSU7 ↔ RAP-DB ID conversion. |
| `scripts/check_genes.py` | Any gene-level check (Steps 3, 7, 8b): symbols/IDs → every gene copy → per-cluster fraction, mean, z. Use it instead of typing IDs. |
| `scripts/score_gene_sets.py` | Step 3 for labels published only per cluster: score the published clusters' marker lists in the current clusters. |
| `references/stress/protoplasting_induced_Shahan2022.txt` | Judging whether a cluster is dissociation stress. |
| `references/plant_pitfalls.md` | Reasoning about clusters: states vs types, ambient RNA, lineage-specific cell types, homology traps. |
| `references/file_formats.md` | Writing annotation, expected-cell-type, marker, color, or gene-map tables. |
