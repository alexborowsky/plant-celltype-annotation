# Marker tables

One table per reference species and tissue. `scripts/map_markers.py` maps
them onto a target species, either by homology or directly (`--no-blast`)
when the target is the reference species.

## Choosing markers: function over statistics

A good marker is a characterized gene whose **function defines the cell
type**. SUC2 loads sucrose into companion cells; SWEET11/12 export it from
phloem parenchyma; CASP1–4 build the Casparian strip. Functions like these
are conserved, understood, and often validated with reporters, so they also
transfer across species better than genes picked by enrichment. Every row
carries an `evidence` tier:

| evidence | Meaning | Default confidence |
|---|---|---|
| `function` | Characterized gene whose function is specific to (or defines) the cell type | high, or medium if restricted to a developmental stage |
| `characterized_enriched` | Characterized gene, but it marks the cell type by enrichment, not by a type-specific function | medium / low |
| `expression` | Selected from single-cell or bulk expression data only | low (medium for Guillotin genes specific to one lineage) |

Markers picked from a dataset's own DE genes do not belong in these tables.
That rule removed the Nb-derived picks (MPK20, MLP31, SAH7, FLA11, …) on
2026-10-01.

## Schema

`ref_species tissue cell_type ref_gene symbol kind evidence confidence requires excludes basis source [alt_id]`

- `alt_id` (optional): the same gene in a second ID system (rice RAP-DB IDs
  in `rice_root.tsv`). Select it with `map_markers.py --id-column alt_id`.

- `tissue`: `leaf`, `root`, or `any`.
- `kind`: `type` or `state` (cell cycle, senescence).
- `requires` / `excludes`: comma-separated trait tags. A row applies to a
  target only if the target has every `requires` tag and no `excludes` tag.
- `basis`: one line on why the gene marks the cell type. Rows starting
  `REVIEW:` need a basis or citation from the curator.

### Trait vocabulary

`eudicot monocot grass C3 C4 Brassicales Brassicaceae Solanaceae Sorghum Oryza Fabaceae Gossypium Rosaceae Apocynaceae Cucurbitaceae Capsicum gymnosperm conifer bryophyte moss liverwort hornwort lycophyte fern angiosperm tracheophyte magnoliid Triticeae Euphorbiaceae Phaseoleae`

Implications: `Sorghum` → `grass C4`; `Oryza` → `grass C3`; `Brassicaceae` → `Brassicales eudicot`; `grass` → `monocot`;
`Brassicaceae`/`Solanaceae` → `eudicot`; `liverwort`/`moss`/`hornwort` → `bryophyte`. Add new tags (a family or a
photosynthetic subtype) to `IMPLIES` in `map_markers.py` as needed.

Typical uses:
- `excludes=C4`: C3-specific photosynthetic compartment markers (Rubisco in
  mesophyll).
- `requires=C4`: C4 enzymes (PPDK, NADP-ME).
- `requires=grass`: grass-specific cell types (subsidiary, silica, ligule)
  and grass-specific gene clades (SUT1, SWEET13).
- `requires=eudicot`: position-dependent root epidermal patterning (GL2,
  TTG2) and trichome genes. Grass root epidermis is patterned by asymmetric
  division instead.
- Lineage exclusions written by `scripts/lineage_tags.py` (three ordered groups):
  - angiosperm-only (`excludes=bryophyte,lycophyte,fern,gymnosperm`): flowers,
    anther wall, fruit, endosperm, female gametophyte, seed coat, companion cells;
  - seed-plant (`excludes=bryophyte,lycophyte,fern`): SAM zones, meristem
    epidermis, axillary meristem, cambium/periderm, ovule, pollen, sperm, embryo, seed;
  - vascular-plant (`excludes=bryophyte`): vascular, root and stomatal types, shoot
    meristem, primordia, organ boundary, stem-cell niche, pavement, trichome, tapetum.
  Epidermis, protoderm and cell-cycle states are left untagged.
- `excludes=monocot,gymnosperm,bryophyte`: eudicot-only types from eudicot
  tables (palisade/spongy mesophyll, adaxial/abaxial epidermis, GL1/GL2/TTG
  trichome patterning).
- `requires=Brassicaceae`: Arabidopsis SULTR2;1 (xylem parenchyma) and
  SULTR2;2 (bundle sheath); see the SULTR2 pitfall.

`scripts/lineage_tags.py` only adds tags, never tags a species against its own
lineage, and must be run on **all** tables after rows are added
(`tests/test_lineage_tags.py` checks; `survey/sync_to_skill.py` runs it).

## Tables

| File | Rows | Source | Notes |
|---|---|---|---|
| `arabidopsis_leaf.tsv` | 33 | Curated by function from the literature (`classic`) | Tier C (data-picked) rows removed. `basis` lines drafted by Claude and pending review. |
| `arabidopsis_root.tsv` | 51 | Shahan et al. 2022 *Dev Cell* curated markers (43; via ohlerlab/scKB `supp_data/Curated_Markers.csv`, MIT), plus 7 classic functional markers (SCR, CASP1, SHR, WOX5, PLT1, SMB, EXPA7) | Each Shahan row keeps its original source (Ryu 2019, Denyer 2019, Clark 2019, Nagawa 2006, Beekman 2014, or the paper's own enrichment scoring, "escoring"). |
| `sorghum_leaf.tsv` | 17 | Brophy lab sorghum curation (`source/CellTypeMarkersSorghumLeaf.txt`) | IDs are BTx623 v5.1 `Sobic.` loci. The CCR1 row was split into Bundle_Sheath and Sclerenchyma. CST1 basis: Wang et al. 2019 *Plant Cell* (maize subsidiary-cell reporters). CYP79A1 basis: Adaramodu et al. 2026 bioRxiv (snRNA-seq trichome cluster only, so `low`). |
| `rice_root.tsv` | 46 | Six rice root single-cell datasets reviewed 2026-10 (Zhang 2021, Liu 2021, Wang 2021, Zhu 2025, Wang 2025, Yan 2025) plus the characterized genes they cite | `ref_gene` = MSU7 `LOC_Os` IDs; `alt_id` = RAP-DB IDs (empty for 4 rows). Each ID was checked against the paper's own table, plus UniProt or Oryzabase for named genes. Most rows are in situ or spatially validated (`characterized_enriched`), and cross-study agreement raised `confidence`. No row is `expression`-only. Conflicts are noted in `basis` (FRDL1 pericycle vs root cap; OsHyPRP06 = OsLTPL120; LOC_Os01g73980 is not Zhang's "XCP2"). The review is in the resources folder (`datasets/rice_root/`). |
| `sorghum_root_Guillotin2023.tsv` | 1187 | Guillotin et al. 2023 conserved grass root markers, maize genes projected to sorghum (`source/CommonMarkersGrasses_Guillotin2023.tsv`) | All `expression`. 292 of 733 genes mark more than one lineage and are `low`. Renamed `LRC`→`Lateral_Root_Cap` and `G2_M`→`Dividing_cells`; numbered substates (Cortex_1…4) kept. |

`source/` holds the original files exactly as received or downloaded.

## Characterized markers (`characterized/`)

300 markers from characterization studies, not single-cell atlases:
promoter-reporter, translational fusion, in situ, mutant phenotype, and
sorted-cell or microdissection profiling. They were collected (2026-10) to
fill cell types that had no `function` marker in the atlas tables, such as
root cap, QC, seed-coat layers, embryo-sac cells, bundle sheath, hydathode,
sieve elements and companion cells, endosperm domains, and nodule zones.

- One table per species with at least 5 rows (`arabidopsis` 157, `rice` 34,
  `maize` 31, `marchantia` 15, `medicago` 11, `soybean` 10, `tomato` 9,
  `barley` 6, `brachypodium` 6), plus `other_species.tsv` (21 rows: Lotus,
  Phaseolus, Catharanthus, Hevea, pea, Populus, sorghum, wheat, Physcomitrium).
- Added 2026-10-22 (IDs checked in Araport11/MarpolBase/Ensembl Plants, DOIs in
  Europe PMC): xylem cell-death markers XCP1, XCP2, MC9 (`function`), BFN1
  and RNS3 (`characterized_enriched`, low) as `Xylem`; MpLRL (`Rhizoid`, low);
  PpRSL1/PpRSL2 (`Rhizoid` and `Caulonema`, `requires=moss`). The PCD genes
  are shared with tapetum, root cap, senescence (BFN1) and other
  developmental cell death, so they mark xylem only next to vascular markers
  (VND6/7, CESA4/7/8); a PCD programme near vascular clusters points to
  differentiating tracheary elements, not senescence.
- Every row had its gene ID and DOI checked by the search agent (gene ID in
  UniProt or the organism database; DOI in Europe PMC). The 13 rows that
  failed either check were left out; they are in the Oak survey folder.
- Extra columns: `validation` (method and figure) and `gaps_filled`
  (`group:cell_type` gaps the marker addresses, directly or by homology).
- **Use them alongside the atlas tables, as a cross-species source of
  `function` markers.** Most rows are Arabidopsis genes, so for other species
  they map by homology like the core Arabidopsis tables.
- ID conventions: rice uses MSU7 in `ref_gene` (RAP-DB in `alt_id`); maize
  uses v5. Rows keyed by a UniProt accession (10; barley, Catharanthus, Hevea,
  pea, one Lotus) are reference-only and marked in `basis`; they will not
  match gene IDs in a dataset.
- Cell-type names were normalized to Title_Case_With_Underscores. The
  original wording is kept in `basis` in square brackets.

## Atlas tables from the 2026-10 survey (`primary/`, `secondary/`)

One table per species x organ group, collated from reviews of published
single-cell, spatial, sorted-cell and microdissection datasets (110 reviews,
55 groups; the last 31 were gap-filling reviews of 2026-10-20). Per-group notes are
in `../atlases/<group>.md` (datasets, verdicts, recommended label reference,
gaps, conflicts); the full dataset list is `../atlas_catalog.tsv`.

**Order of use:** for a target species and organ, use the `primary/` table if
one exists, together with the curated core tables above for that lineage.
Use a `secondary/` table only when no primary or core table covers the
species and organ. Secondary tables come from a single dataset or from
datasets with little validation, so treat their calls as hypotheses.

- **Tier rule:** `primary` = at least 15 high-confidence markers, or at least
  2 reviewed datasets and at least 9 high-confidence markers. Tiers are
  recomputed by `survey/sync_to_skill.py` (Oak) whenever drafts change.
- **Status: drafts.** The collation agents checked IDs against the papers'
  tables and UniProt or organism databases, but rows were not independently
  re-verified. Some agents added literature genes beyond the reviews.
  `n_cross_study` and cross-study confidence raises were defined per agent.
- **Cell-type names** are not harmonized across groups (222 names, some
  synonymous, e.g. Vascular / Vasculature / Vascular_Bundle). True synonyms
  are merged by `celltype_aliases.tsv` (below); the evidence report matches
  other related names by tokens; use `--alias` otherwise.
- **Extra columns:** `alt_id` = the same gene in a second ID system (use
  `--id-column alt_id`); `other_ids` = multi-species or non-gene IDs (UniProt,
  orthologs in relatives), for reference only.
- **Tissue values** go beyond leaf/root/any: seed, inflorescence, flower,
  ovule, pistil, anther, embryo, endosperm, fruit, stem, shoot_apex,
  seedling, nodule, thallus. Filter with `--tissue <value> --tissue any`.

| Tier | Group | ref_species | `ref_gene` example | `alt_id` example |
|---|---|---|---|---|
| primary | arabidopsis_endosperm | arabidopsis | `AT5G60440` | — |
| primary | arabidopsis_fruit | arabidopsis | `AT3G24140` | `Q56YJ8` |
| primary | arabidopsis_inflorescence | arabidopsis | `AT2G16910` | `Q9ZVX2` |
| primary | arabidopsis_leaf | arabidopsis | `AT3G01500` | `P27140` |
| primary | arabidopsis_root | arabidopsis | `AT3G11260` | `Q8H1D2` |
| primary | arabidopsis_seed | arabidopsis | `AT1G61720` | `Q9SEV0` |
| primary | arabidopsis_seedling | arabidopsis | `AT3G01500` | `P27140` |
| primary | arabidopsis_shoot_apex | arabidopsis | `AT2G27250` | `Q9XF04` |
| primary | arabidopsis_stem | arabidopsis | `AT1G22710` | `Q39231` |
| primary | brassicaceae_root | arabidopsis | `AT5G58784` | — |
| primary | cotton_ovule | cotton | `Ghir_D04G020730` | `GH_D04G2108` |
| primary | lotus_root | lotus | `LotjaGi6g1v0059900` | — |
| primary | maize_embryo | maize | `Zm00001eb055920` | `GRMZM2G017087` |
| primary | maize_endosperm | maize | `Zm00001eb354390` | `Zm00001d010889` |
| primary | maize_inflorescence | maize | `Zm00001eb055920` | `Zm00001d033859` |
| primary | maize_leaf | maize | `Zm00001eb383680` | `Zm00001d046170` |
| primary | maize_root | maize | `Zm00001eb086310` | `Zm00001d004089` |
| primary | maize_seed | maize | `Zm00001eb083790` | `Zm00001d003776` |
| primary | maize_shoot_apex | maize | `Zm00001eb011320` | `Zm00001d028495` |
| primary | medicago_nodule | medicago | `MtrunA17Chr5g0435611` | `Medtr5g080400` |
| primary | populus_stem | poplar | `Potri.014G025300` | `pou24718` |
| primary | rice_inflorescence | rice | `LOC_Os01g40630` | `Os01g0588900` |
| primary | rice_seed | rice | `LOC_Os02g49410` | `Os02g0725900` |
| primary | soybean_nodule | soybean | `Glyma.17G195900` | `GLYMA_17G195900` |
| primary | soybean_root | soybean | `Glyma.17G133100` | `Glyma17g14230` |
| primary | soybean_seed | soybean | `Glyma.09G092700` | — |
| primary | tomato_other | tomato | `Solyc02g081120` | — |
| primary | tomato_root | tomato | `Solyc12g049070` | `Solyc12g049070.1` |
| primary | wheat_inflorescence | wheat | `TraesCS7A02G308400` | `TraesCS7A03G0760400` |
| primary | wheat_root | wheat | `TraesCS7D02G019600` | `TraesCS7D03G0043000` |
| secondary | arabidopsis_ovule | arabidopsis | `AT5G14010` | `Q9FFX4` |
| secondary | barley_inflorescence | barley | `HORVU.MOREX.r3.2HG0198150` | `HORVU2Hr1G106970` |
| secondary | barley_root | barley | `HORVU.MOREX.r3.3HG0301330` | `HORVU3Hr1G085050` |
| secondary | barley_shoot_apex | barley | `HORVU.MOREX.r3.2HG0198150` | `HORVU2Hr1G106970` |
| secondary | brachypodium_leaf | brachypodium | `BdiBd21-3.1G0240400` | `Bradi1g18400` |
| secondary | cassava_leaf | cassava | `Manes_01G128300` | `Manes.01G128300.v8.1` |
| secondary | catharanthus_leaf | catharanthus | `CRO_01G006750` | `CRO_T133061` |
| secondary | cotton_anther | cotton | `Ghir_A13G009770` | — |
| secondary | cucumber_inflorescence | cucumber | `CsaV3_2G007120` | `Csa2G034560` |
| secondary | lotus_nodule | lotus | `LotjaGi5g1v0024700` | `Lj5g3v0035290` |
| secondary | marchantia_other | marchantia | `Mp3g07510` | `MARPO_0006s0226` |
| secondary | medicago_root | medicago | `MtrunA17Chr7g0238371` | `Medtr7g060540` |
| secondary | peanut_fruit | peanut | `arahy.Tifrunner.gnm2.ann1.V28JVI` | `LOC112699822` |
| secondary | pepper_fruit | pepper | `LOC107859694` | `T459_09470` |
| secondary | physcomitrium_other | physcomitrium | `Pp3c2_7150` | `Pp1s59_223V6` |
| secondary | pine_shoot_apex | pine | `Pt6G36960` | — |
| secondary | populus_root | populus_84K,populus_simonii | `Psi03G016300` | `Potri.016G084400` |
| secondary | rice_embryo | rice | `LOC_Os02g52710` | `Os02g0765600` |
| secondary | rice_leaf | rice | `LOC_Os03g57220` | `Os03g0786100` |
| secondary | rice_ovule | rice | `LOC_Os10g33250` | `Os10g0471100` |
| secondary | selaginella_root | selaginella | `LOC9660776` | `SMO361G0372` |
| secondary | sorghum_leaf | sorghum | `Sobic.010G160700` | `SORBI_3010G160700` |
| secondary | sorghum_root | sorghum | `Sobic.002G066400` | `SORBI_3002G066400` |
| secondary | strawberry_fruit | strawberry | `FvH4_3g24570` | `gene06886` |
| secondary | tomato_seedling | tomato | `Solyc10g005330` | `LOC101256132` |

ID notes: each species uses one `ref_gene` convention where a second system
exists (maize v5 `Zm00001eb`, rice MSU7 `LOC_Os`, wheat IWGSC v1.1 `..02G`).
`survey/sync_to_skill.py` on Oak enforces this by swapping `ref_gene` and
`alt_id`; rows with no second ID keep their original system (a few maize_root
and rice_embryo rows). Tables are regenerated by that script; edit the Oak
drafts, not these copies. `arabidopsis_root` here is the
survey table (Shahan 2022, Lyu 2025, PHYTOMap, Lee 2025, Brassicaceae root);
the curated core `arabidopsis_root.tsv` above stays the first choice for
classic root markers.

Trait tags added for these tables (in `map_markers.py` IMPLIES): `Fabaceae`,
`Gossypium`, `Rosaceae`, `Apocynaceae`, `Cucurbitaceae` (all imply `eudicot`),
`Capsicum` (implies `Solanaceae`), `conifer` (implies `gymnosperm`). Rows tagged
`moss`, `gymnosperm`, `liverwort` or `lycophyte` apply only when passed in
`--target-traits`. `Brassicales` (implies `eudicot`; implied by
`Brassicaceae`) covers glucosinolate/myrosinase rows such as TGG1.

## Cell-type aliases (`celltype_aliases.tsv`)

`alias  canonical  note`, one row per synonym (37 rows). Names with the same
canonical name count as one cell type: `annotation_report.py` treats alias
markers as markers of the type itself, and `map_markers.py` does not warn
when one gene is listed under two names that are aliases. Matching is
case-insensitive and one level deep (an alias maps straight to its
canonical name).

- Only true synonyms: spelling and case variants (Stomatal_Lineage,
  Protodermal), abbreviations (LRC, QC, SAM, G2_M), published-label spellings
  (Root_Hair/Non_Hair, Companion_Cell, Guard_Cell), and names for the same
  cell population in different tables (Seed_Coat_Endothelium = Endothelium,
  Phloem_Idioblast = Myrosin_Idioblast, Outer_Integument_2 =
  Seed_Coat_Outer_Epidermis, Arabidopsis border-like cells = Border_Cell).
- Parent/child pairs are **not** aliases (Columella vs Root_Cap, Xylem vs
  Xylem_Parenchyma, Protophloem_Sieve_Element vs Sieve_Element, numbered
  substates such as Cortex_1). Use `--alias` for a one-off grouping.
- Canonical names are the most common spelling in the tables. When a new
  table introduces a synonym, add a row here instead of renaming the table.

## Gene annotation tables (`../annotation/`)

Lookup tables for symbols and ID conversion (not marker tables). Use them to
show symbols in reports and DE tables and to convert rice IDs.

| File | Rows | Columns | Source |
|---|---|---|---|
| `araport11_genes.tsv.gz` | 27,653 loci (protein-coding, incl. 208 ATCG/ATMG) | `gene_id symbol description aliases` | Araport11 protein BLAST db headers (all symbols, full names) + Ensembl Plants release 63 TAIR10 pep `gene_symbol` (one primary symbol per locus) |
| `rice_msu_rap.tsv.gz` | 56,939 pairs (55,801 MSU, 33,580 RAP loci) | `msu_id rap_id` | RAP-DB `RAP-MSU_2026-02-05.txt.gz` (https://rapdb.dna.naro.go.jp/download/archive/) |

- `symbol` is TAIR's primary symbol, so some differ from common usage (FAMA
  is `FMA`, with FAMA in `description`); `aliases` lists every Araport11
  symbol. "No symbol available" placeholders are empty.
- Rice: one row per MSU-RAP pair; transcript suffixes removed, comma lists
  split, loci without a counterpart dropped. The mapping is many-to-many, so
  do not assume 1:1. All 313 `ref_gene`/`alt_id` pairs in the rice marker
  tables agree with it.
- To refresh: dump the headers with `blastdbcmd -db <Araport11_db> -entry all`
  (or use the TAIR/Ensembl pep FASTA) and take the newest
  `RAP-MSU_<date>.txt.gz` (release dates are on RAP-DB `news.html`; the old
  `rapdb.dna.affrc.go.jp` host returns 403). The build script is in the Oak
  resources folder (`annotation_tables/build_annot.py`).

## Adding a table

1. Use the schema above. Give every row an `evidence` tier and a `basis`.
2. Set `requires`/`excludes` from the biology, not from convenience.
3. Record provenance in `source` and add a row to the table above.
4. Validate the field counts:
   `awk -F'\t' 'NR==1{n=NF} NF!=n{print FILENAME": line "NR}' new.tsv`
