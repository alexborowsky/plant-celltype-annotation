# Part A: published annotations and expected cell types

This file covers Steps 1–3 in detail: finding the labels published with a
dataset, listing the cell types to expect, and judging which published
labels can be reused.

## Step 1: sourcing published annotations

### Where per-cell labels live, most likely first

1. **GEO supplementary files** for the series (`GSE...`). Look for files
   named `*metadata*`, `*annotation*`, `*celltype*`, `*.h5ad`, or `*.rds`.
   Read the GEO series page or use NCBI E-utilities. Don't download large
   objects to look for a label column; check the file list and sizes first.
2. **Repositories linked from the paper's data availability statement:**
   Zenodo, Figshare, Dryad, and GitHub (analysis code often includes a
   `metadata.csv`).
3. **Supplementary tables of the paper.** These usually have the cluster →
   cell type table and the marker list, and occasionally per-cell labels.
4. **Plant single-cell databases** (scPlantDB, PlantscRNAdb, the Plant Cell
   Atlas resources). These sometimes host the processed object with labels.
   Note that a database may have re-annotated the data, so record whose
   labels they are.
5. **The authors.** If nothing is public, tell the user which file is
   missing; they can ask the corresponding author.

### Formats

- **A Seurat `.rds`:** export the metadata in R
  (`write.csv(obj@meta.data, "published/labels.csv")`) in a job if the
  object is large. Use R from the `r_seurat` conda env or the R module.
- **A published `.h5ad`:** read only `obs`
  (`sc.read_h5ad(path, backed='r').obs`), and save it as a table.
- **Label tables:** save as `published/labels.tsv`, with the barcode in the
  first column. `--import-labels` reads `.h5ad`, `.csv`, `.tsv`, and
  `.txt`.

### Matching barcodes

- Published barcodes often differ from yours by a suffix (`-1`), a sample
  prefix or suffix (`S1_AAAC...`, `AAAC..._1`), or the integration's
  renaming (`AAAC...-1-0`). Compare a few barcodes from each side, and
  rewrite the label table's barcodes to match the h5ad.
- The same barcode can occur in several samples. After rewriting, check
  that the barcodes are unique before importing.
- Expect less than 100% matching. Authors filter cells differently. Report
  the match rate per sample. A sample with ~0% matched usually means a
  naming mismatch, not filtering.
- If the data were reprocessed from raw reads (a different aligner or
  genome), a match rate under ~70% makes the per-cell labels unreliable.
  Use the published markers and the cluster table instead.

### What to record in `published/README.md`

- **Label accessibility**, as one of:
  - a small barcode→label table (supplementary table, database CSV, web
    portal export);
  - only inside a large processed object (give its size);
  - cluster-level only (labels must be re-derived by re-clustering);
  - none.

  This decides how much Step 3b can reuse, as much as label quality does.
  Web portals sometimes embed per-cell labels in the page (for example, in
  a Plotly figure); extracting them is fine when the page is public.
- Citation, DOI, and accession.
- Each file's source URL, and the date it was downloaded.
- Platform (protoplast scRNA-seq or nuclei) and genome/annotation version.
- Barcode format, and any rewriting done to match the h5ad.
- The cell types annotated, with cell counts.
- How the paper says each type was called (markers, validation).

## Step 2: expected cell types

Build the list from the anatomy of the tissue at the sampled stage, not
from the published labels. Sources: plant anatomy texts and reviews, the
existing tables in `references/markers/`, and atlases of the same tissue in
related species (found in Step 4 if needed).

### Common starting lists (adapt to species and stage)

| Tissue | Cell types |
|---|---|
| Eudicot leaf | Palisade and spongy mesophyll; bundle sheath; adaxial and abaxial pavement; guard cells; trichomes (and glandular trichomes in some lineages); hydathode; xylem (differentiating), xylem parenchyma; phloem parenchyma, companion cells, sieve elements; procambium; dividing cells in young leaves |
| Grass leaf | Mesophyll; bundle sheath (Kranz in C4); epidermis: pavement, guard, subsidiary, bulliform, silica, and cork cells, and hairs or prickles; xylem, phloem, companion cells; mestome sheath (C3, and some C4); ligule/auricle if sampled |
| Eudicot root | Root cap (columella, lateral root cap); quiescent center; atrichoblasts and trichoblasts; cortex; endodermis; pericycle; xylem (and xylem-pole pericycle); phloem, companion cells, phloem-pole pericycle; procambium; meristematic and elongating cells. Exodermis is present in some species (tomato) but not in Arabidopsis |
| Grass root | Root cap; epidermis and root hairs (not patterned by position as in Arabidopsis); exodermis/hypodermis; in rice, a lignified sclerenchyma layer under the exodermis; cortex (multilayered; aerenchyma in mature zones); endodermis; pericycle; metaxylem (central and peripheral) and protoxylem; phloem; meristematic cells. Worked example: `datasets/rice_root/expected_cell_types.tsv` in the resources folder |
| Leafy liverwort gametophyte (e.g. *Calypogeia*) | Leaf lamina cells; underleaves; stem epidermis and cortex; oil-body cells (idioblastic or in every cell, depending on the genus); rhizoids (on the stem or underleaf base); apical cell and dividing cells near the tip; gemmae if present. No vascular tissue, stomata or roots |
| Thalloid liverwort (*Marchantia*) | Dorsal epidermis with air pores; air-chamber assimilatory filaments; storage parenchyma; oil-body cells; ventral epidermis, scales and rhizoids (smooth and pegged); apical notch/meristem; gemma cups and gemmae; mucilage cells; sexual organs (antheridiophores, archegoniophores) if sampled |
| Moss gametophyte (*Physcomitrium*) | Protonema (chloronema, caulonema); leaf (phyllid) cells, midrib; stem epidermis, cortex, hydroids and leptoids; rhizoids; apical cells and buds |

### Lineage-specific types to check for

| Lineage | Types |
|---|---|
| C4 grasses (sorghum, maize) | Kranz bundle sheath vs mesophyll (marker roles invert relative to C3) |
| Grasses | Subsidiary, silica, cork, and bulliform cells; ligule |
| Solanaceae | Glandular trichomes (several types) |
| Brassicaceae | Myrosin idioblasts |
| Latex-producing plants (Euphorbia, Papaver, lettuce) | Laticifers |
| Legumes | Nodule cell types, if nodules are sampled |

### Capture bias

- **Nuclei (snRNA-seq):** mature sieve elements are enucleate and absent.
  Cell-type proportions follow nuclei, so large or multinucleate cells are
  not over-represented.
- **Protoplasts (scRNA-seq):** cells with thick or lignified walls (fibers,
  xylem, some epidermis) are under-recovered, as are cells larger than the
  droplet allows (big trichomes). Dissociation stress forms clusters.
- **Both:** mature xylem vessels and fibers are dead. Only differentiating
  cells appear.
- **Tissue sampling:** a "leaf" sample may or may not include the midrib,
  the petiole, or the margins. Ask the user if it matters.

## Step 3: evaluating the published annotation

### 3a. Paper review rubric

Score each published cell type on these questions. One serious problem is
enough to withhold `Adopt`.

| Question | Good sign | Bad sign |
|---|---|---|
| Is it on the expected list? | Yes, at a plausible granularity | A type the tissue doesn't have, or one lost in capture (sieve elements in nuclei data) |
| Is the proportion plausible? | Within the range for the tissue | A rare type at a large fraction (31% guard cells) |
| What was it called from? | `function` markers, reporter or in situ validation in this species | Cluster DE genes only, or one uncharacterized gene |
| Did the paper show the markers are specific? | Dotplot or feature plots with a clean diagonal | Markers shown only in the assigned cluster, or not shown |
| Is it a type or a state? | A cell identity | Stress, cell-cycle, or treatment cluster labeled as a type |
| Do the paper's markers make sense for this type? | Known function fits | Housekeeping or photosynthesis genes as markers in green tissue |
| Are the markers proliferation genes? | No | Histones, PCNA, MCMs (S phase) or cyclin B, CDKB, KNOLLE, CDC20 (G2/M) behind a "meristem", "initial", "stem cell niche", "QC" or even "root cap" label |
| Was every cell forced into a type? | Unassignable cells left as unknown | Every cell labeled by correlation or classifier; clusters labeled although their top marker score is ≤ 0; a large "mature cells" or "other" bin |
| Is it driven by one sample or batch? | Cells from all replicates | Cluster dominated by one replicate, chemistry (10x v2 vs v3), or condition |

### Recurring problems (rice root review, 2026-10)

These came up in most of the six rice root datasets reviewed. Look for them
first:

- **Proliferation states labeled as types.** Every RNA dataset had at least
  one: four "meristem" clusters, an "endodermis-cortical initial" driven by
  G2/M genes, a "stem cell niche" that was every meristem-zone cell, and a
  "root cap" whose in situ markers were KNOLLE, CDC20, and cyclin B. Check
  each label's markers against cell-cycle genes before anything else.
- **Rare tip types missing or invented.** QC and root cap were absent or
  doubtful in all the protoplast and nuclei RNA datasets. A published label
  for a rare type needs a marker with a known function in it (QHB/WOX5 for
  QC, root-cap/columella genes for cap).
- **Merged layers.** Tissue-level labels such as
  `epidermis_exodermis_sclerenchyma` or one "stele" or "vascular" class.
  These are `Revise`: right lineage, split in Part B.
- **Forced assignment and catch-all bins.** Labels transferred by
  correlation or a classifier to every cell, including cells the authors
  could not annotate. Proportions that swing between conditions for the
  same samples are a sign of this, or of capture loss.
- **Gene-ID errors in secondary sources.** Agent and web summaries gave
  the wrong locus for QHB, and the same symbol (XCP2) named different genes
  in different papers, while one gene had two names (OsHyPRP06 and
  OsLTPL120). Check every ID against the paper's own table and a gene
  database (see `literature_search.md`, Gene IDs).

### 3b. In-data check

Run with the Step 6 evidence job (see SKILL.md for the flags), then for
each published type:

- **Marker enrichment:** its markers (the paper's, and the skill's tables
  for the same type) have z ≳ 1 in its cells, with fraction expressing
  ≳ 0.2, and the top DE homologs agree.
- **Coherence:** in `cluster_hierarchy.tsv`, most of its cells fall in one
  Leiden cluster at some resolution (≳ 70% is good; under ~40% is a
  warning). In the composition sections of the Leiden evidence files, the
  clusters that hold it are not split across unrelated published types.
- **Replicates:** the type is present in every replicate where it should
  be.

### Verdict table: `published/evaluation.tsv`

```
published_label	n_cells	match_rate	verdict	canonical_name	reason
Guard cell	1520	0.97	Adopt	Guard	FAMA reporter in paper; KAT1/FAMA z>2 here; 1.4% of cells
Mesophyll 3	8200	0.97	Revise	Mesophyll	defense state (PR1/PR5 DE); merge with Mesophyll
Stele	4100	0.97	Revise	-	contains xylem and phloem; resolve in Part B
Cluster 14	600	0.97	Reject	-	no marker enrichment; low counts
```

- `canonical_name` is the name the skill's annotation will use. Use the
  marker tables' cell-type names, so markers are matched in the report.
- Show this table to the user, and get their approval before Part B.

### Reusing what holds

- **Labels:** adopted types become rows of the annotation table keyed on
  `published_celltype` (see SKILL.md, Step 9), placed before the de novo
  rows.
- **Markers:** the paper's markers for adopted types go into a marker
  table, graded with the tiers in `references/literature_search.md`. Most
  are `expression` unless the paper validated them. Keep the table in the
  project, and offer to add `function` and `characterized_enriched` markers
  to `references/markers/`.
- **Agreement across datasets:** when several published datasets exist
  for the species and tissue, compare their markers per cell type. A
  marker validated (in situ, reporter, or spatial) in two independent
  studies, or validated in one and specific in another, is the strongest
  evidence available for a non-model species; raise its `confidence` one
  level (see `literature_search.md`, Grading). Agreement is per gene ID,
  not per symbol.
- **Evidence:** cite the paper's validation (reporters, in situ) in each
  adopted row's `Evidence` text, together with what you confirmed in the
  data.
- **Revised types:** carry the published label into Step 7 as a hypothesis,
  and say in the `Evidence` column where the new call departs from it.
