# File formats

All tables are tab-separated with a header row.

## Annotation table (`CellTypeAnnotations*.txt`)

```
Resolution	Cluster	CellType	Evidence
1.5	23	Xylem	XCP1/IRX3 z>2; top DE CESA4/7
0.5	9	Phloem_Parenchyma	SWEET11/12 specific
cl6_sub0.3	1	Phloem_Parenchyma	subcluster of res0.3 cl6
0.5	0	Mesophyll	RBCS/PSBQ high, no other type signal
```

Optional `State` column (detected by its header) so that states keep the cell
type:

```
Resolution	Cluster	CellType	State	Evidence
sub_cl24	0	Mesophyll	Sulfur_Starvation	SULTR1;1/APR up; mesophyll program
sub_cl24	1	Bundle_Sheath	Sulfur_Starvation	same state in BS-marker cells
1.5	24	-	Sulfur_Starvation	state-only row: sets the state, type comes from rows above/below
1.5	0	Mesophyll		no state
```

- `State` sets `obs['cell_state']` (`none` where unset) and
  `obs['cell_type_with_state']` (`Mesophyll (Sulfur_Starvation)`).
- A row with CellType `-` and a State is **state-only**: it records the state
  but does not claim the cells' type, which other rows assign.
- States: stress/treatment responses, cell cycle (`S_Phase`, `G2M`),
  senescence, circadian. Types: everything else. Never put a state in
  `CellType` when the cells' type can be resolved.
- A state names a tested process. A private program you cannot explain is
  not a state: write `Unknown_<program>` in `CellType` instead
  (`apply_annotations.py` warns about state names that describe no process).


- `Resolution` is either a number (read as `leiden_res<number>`) or any
  `adata.obs` column name, including labels imported with `--import-labels`.
- `Cluster` is compared as a string against that column. A comma list
  (`0,1,12`) matches any of the listed clusters.
- A numeric `Resolution` also resolves Seurat-style columns
  (`snn_res0.5`, `SCT_snn_res.0.5`, `RNA_snn_res.0.5`, `integrated_snn_res.0.5`, `louvain_res0.5`).
- `CellType` should use `Title_Case_With_Underscores`. Names are matched
  case-insensitively to the color file and replaced with the canonical
  spelling.
- `Evidence` is optional free text that the script ignores. Always fill it
  in: it is the audit trail.
- **Semantics:** rows are applied top to bottom, and each row labels only
  cells that are still `Unknown`. Put the most specific rows (high
  resolution, subclusters) first and the broad catch-all rows last.
- Legacy files without tabs (whitespace-separated) are still parsed. There,
  every token after the second is joined with `_` to form the cell type.

## Expected cell types (`expected_cell_types.tsv`, Step 2)

```
cell_type	abundance	capture	lineage	function_markers	notes
Mesophyll	common	ok	-	3	C4: RBCS is a bundle-sheath marker
Phloem_Companion	rare	ok	-	1	SUC2
Sieve_Element	rare	absent (nuclei)	-	0	enucleate at maturity
Glandular_Trichome	rare	under-recovered	Solanaceae	0	Step 4 search target
```

- `abundance`: `common`, `moderate`, or `rare`.
- `capture`: `ok`, `under-recovered`, or `absent`, with the reason.
- `function_markers`: the number of `function` markers for the type in
  `references/markers/` after `--target-traits` filtering. Zero means the
  type is a Step 4 search target.
- Use the marker tables' cell-type names, so that later steps match.

## Published-label evaluation (`published/evaluation.tsv`, Step 3)

The format and verdicts are in `references/published_annotations.md`.

## Reference marker tables (`references/markers/*.tsv`)

These are the inputs to `map_markers.py`, keyed by reference-species IDs.
The schema, evidence tiers, and trait tags are in
`references/markers/README.md`.

## Target marker table (output of `map_markers.py`, or curated)

Required columns: `gene_id`, `cell_type`. Optional columns: `symbol`,
`evidence`, `confidence`, `ref_species`, `ref_gene`, `hit_rank`, `pident`,
`rbh`, `via` (`forward`, `reverse_best`, or `same_species`), `basis`,
`source`. Several tables can be passed at once (`--markers a.tsv b.tsv`).
The first table wins for a repeated (gene, cell type) pair.

The legacy column names `NbID`/`Gene`/`CellType` are accepted as aliases.
`gene_id` must match `adata.var_names`. If a gene is absent from `var_names`
but `adata.obs['<gene_id>_expr']` exists (for example, transgenes kept out
of the matrix), that column is used instead.

## Color table (`CellTypeColors.txt`)

```
CellType	Color
Mesophyll	#0A5E40
```

Cell types with no color get an automatic palette color, and `Unknown` is
always `#C8C8C8`.

## Gene map (`gene_map.tsv`, from `map_markers.py`)

`query_gene, hit_rank, ref_gene, ref_symbol, ref_description, pident, evalue, bitscore, rbh`

Each query gene has one row per distinct reference locus (isoforms are
collapsed), ranked by bitscore. `rbh` is filled only when `--blast-reverse`
was given.

## BLAST input

Standard `-outfmt 6` (12 columns). If there are extra columns in the
Araport11-annotated layout (col 15 `Symbols:...`, col 16 full name), symbols
and descriptions are read from them. Otherwise, provide
`--ref-annotation locus<TAB>symbol<TAB>description`.
