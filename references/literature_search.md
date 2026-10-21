# Step 4: literature search for markers

Goal: before relying on markers transferred from a distant reference, find
what is already known for the **target species and tissue**. Published
single-cell marker lists and, above all, reporter-validated
cell-type-specific genes beat anything transferred through Arabidopsis.

## When to search

Check `references/markers/README.md` for existing tables. For each
(species, tissue) pair in the dataset:

| Situation | Action |
|---|---|
| A table exists for this species and tissue | Skip the search, unless the user asks or the table is thin (fewer than ~3 `function` markers per expected cell type). |
| A table exists for a close relative and the same tissue | Use it via homology. Do a quick search for species-specific reporter lines only. |
| A table exists only for a different tissue | Search. Tissues have different cell types (root cortex vs leaf mesophyll), so markers rarely carry over. |
| No table within the family/tribe | Do the full search (both parts below). |

"Close relative" means the same family for eudicots and the same tribe for
grasses. For lineage-specific cell types (glandular trichomes, silica
cells, Kranz bundle sheath, laticifers, nodule cells), only the same genus
or family counts.

## Part 1: existing single-cell data

Search for atlases of the species and tissue, then its closest relatives.

Example queries:
- `"<species>" single-cell RNA-seq <tissue>` / `single-nucleus`
- `"<species>" <tissue> cell atlas`
- `"<common name>" scRNA-seq <tissue> cell types`

Sources, in order:
1. **Papers.** Look for the marker table used to annotate. It's usually a
   supplementary table, or a figure listing "known markers". Distinguish:
   - curated markers used for annotation: the most useful
   - full cluster DE tables: `expression` tier, use sparingly
2. **Code and data repositories** linked from the paper: GitHub, Zenodo,
   Figshare. These often hold the curated marker CSV and per-cell labels.
   For Shahan et al. 2022, the curated list was in ohlerlab/scKB
   `supp_data/`.
3. **Plant single-cell databases** that aggregate markers and atlases:
   scPlantDB, PlantscRNAdb, PCMDB, and the Plant Cell Atlas resources. Treat
   their marker lists as `expression` unless the entry cites validation.
4. **GEO/SRA** (NCBI E-utilities) for datasets without papers. Check the
   supplementary files for annotation or metadata tables with labels.

For each atlas, record:
- citation and DOI
- platform (protoplast scRNA vs nuclei)
- genome/annotation version of the gene IDs
- the cell types annotated
- where the marker list lives
- whether per-cell labels exist (a potential benchmark)

## Part 2: characterized markers and reporter lines

Search for genes with direct, cell-resolution evidence in this species and
tissue (or the genus).

Example queries:
- `"<species>" <cell type> promoter GUS` / `GFP reporter` / `in situ hybridization`
- `"<species>" <gene family> expressed specifically in <cell type>`
- `<cell type> specific promoter <species or family>`
- the orthologs of the strong Arabidopsis markers (SUC2, SWEET11/12,
  CASPs, KAT1, FAMA, SMB, ...) plus the species name, to see whether a
  study already validated the species gene

Good evidence, strongest first:
1. Promoter-reporter or protein fusion localized to one cell type, plus a
   cell-type function (mutant phenotype, transport activity). Example: maize
   CST1, a subsidiary-cell SWEET (Wang et al. 2019 *Plant Cell*).
2. Reporter or in situ localization alone.
3. Single-cell enrichment backed by a biochemical rationale. Example:
   sorghum CYP79A1 for dhurrin synthesis in the trichome cluster (Adaramodu
   et al. 2026 bioRxiv).

## Grading into the table schema

| Evidence found | `evidence` | `confidence` |
|---|---|---|
| Reporter or in situ specificity + cell-type function | `function` | high |
| Characterized cell-type function, but stage-restricted or validated only in a close relative's ortholog | `function` | medium–high |
| Reporter or in situ specificity, function unrelated to the cell type | `characterized_enriched` | medium |
| Characterized gene, enrichment shown only by single-cell or bulk data | `characterized_enriched` | low |
| Atlas marker list or DE, uncharacterized gene | `expression` | low (medium if specific to one lineage) |

Spatial transcriptomics with cell resolution (Molecular Cartography,
MERFISH, single-cell Stereo-seq) counts as in situ evidence.

**Agreement across studies raises confidence one level** (low → medium,
medium → high). It counts when the same gene ID is validated in two
independent studies, or validated in one and cluster-specific in another
for the same cell type. A study that only re-uses another's marker list
is not independent. Name the studies in `basis`.

Write `basis` as one line stating the function and the evidence, with the
first author, year, and journal (`... (Wang et al. 2019 Plant Cell)`). Put
the DOI or URL in `source`. Set `requires`/`excludes` from the biology (see
`references/markers/README.md`).

## Gene IDs

- Map published IDs to the dataset's genome version before use. Old
  annotations (e.g. Sorghum v3 vs v5.1, maize B73 v4 vs v5, tomato ITAG2 vs
  ITAG4) rename or merge genes.
- Use the organism database's ID conversion tables, or BLAST the published
  protein against the current proteome.
- Never infer an ID from a gene name in the text; take IDs from the paper's
  tables.
- **Same symbol, different gene, and the reverse.** Papers name genes by
  homology, so "XCP2" can be two different rice loci, and one locus can
  carry two names (OsHyPRP06 = OsLTPL120). Compare studies by ID.
- **Confirm each ID in a database.** UniProt's REST API returns a gene's
  ordered-locus names, which often include both ID systems:
  `https://rest.uniprot.org/uniprotkb/search?query=gene:<ID>+AND+taxonomy_id:<taxid>&fields=accession,gene_names,protein_name&format=tsv`.
  Uncharacterized genes are often missing there; use the paper's own
  table that lists both IDs, or the organism database.
- **Rice has two ID systems.** RAP-DB (`Os01g0100100`, IRGSP-1.0) and MSU7
  (`LOC_Os01g01010`). Datasets use either one. RAP-DB's download server
  refuses scripted access, so don't try to get around it. Use these
  instead:
  - Oryzabase's gene list (named genes, with both IDs), kept in the
    resources folder (see SKILL.md, Environment notes);
  - UniProt;
  - tables that list both IDs (Zhu et al. 2025, Supplementary Table 3).

  `rice_root.tsv` keeps MSU7 IDs in `ref_gene` and RAP IDs in `alt_id`.
  Use `map_markers.py --id-column alt_id` for RAP-ID data.

## Verification and access

- **Get marker tables from the raw files.** Download the supplementary
  file or repository CSV and read it. Do not trust gene IDs paraphrased by a
  web-page summarizer; they can be wrong.
- Use APIs and repositories that allow scripted access: NCBI E-utilities,
  the Europe PMC REST API, GitHub, Zenodo, journal supplementary links.
- Do not try to get around captchas, logins, or paywalls. If a needed
  supplement is inaccessible, tell the user which file you need and ask
  them to download it.
- Published annotations can be wrong. Compare an atlas's cell-type
  proportions with the biology before adopting its labels as ground truth.

## Reporting to the user

Before writing a new table into the skill, show:
1. **The queries run**, and the atlases and papers found, each with a
   one-line assessment.
2. **The proposed rows** (gene, cell type, evidence, basis), grouped by
   cell type, with gaps called out: cell types that have no `function`
   marker.
3. **Where the table will be saved:**
   `references/markers/<species>_<tissue>[_<firstauthor><year>].tsv`.

Then use the new table in Step 5, with `--no-blast` if it is in the
target's own IDs, or via homology if it comes from a relative.
