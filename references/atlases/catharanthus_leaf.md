<!-- Collated from the survey review of catharanthus_leaf (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Catharanthus roseus leaf: collated cell-type marker resources

Collated 2026-10-20. Inputs: the one dataset review for this group in
`../../survey/merged_reviews.json` (`group == "catharanthus_leaf"`, folder
`Li2023/`, which keeps its own review README). During collation I also
desk-checked the two other leaf atlases listed for this group in
`../../survey/all_datasets.tsv` (Sun 2023, Li 2025), because without a
second independent study no marker could get the cross-study tier. Their
files are in `Sun2023_supp/` and `Li2025_supp/`. These two are **not full
Part A reviews**: no per-type verdicts were scored against the rubric, and
nothing was re-analysed.

Files in this folder:

- `expected_cell_types.tsv`: cell types expected from the anatomy of a young
  to mature eudicot (Apocynaceae) leaf with bicollateral bundles (Step 2
  format). `function_markers` counts the `function` rows in
  `markers_draft.tsv`. Function rows that would come through homology from the
  skill's `arabidopsis_leaf.tsv` are named in `notes`; they are not counted.
- `markers_draft.tsv`: 39 rows, the skill schema plus `alt_id`. `ref_gene` is the
  *C. roseus* genome v3 locus (`CRO_01G006750`; Seurat writes `CRO-01G006750`),
  and `alt_id` is the v2 locus (`CRO_T133061`) where Li 2023 Table S6 gives one.
  Four rows (`EVM...`) use Sun 2023 IDs and start with `REVIEW:` (see below).
  Field counts were validated (13 fields on every line). The skill was not edited.
- `Sun2023_supp/`: Sun 2023 Supplementary Tables 1-19 (MOESM3), the
  Supplementary Information PDF (MOESM1), and Supplementary Data 2 (MOESM5,
  per-type pseudobulk expression, 11 MB). All are from the Springer ESM links,
  which are public although the article is paywalled.
- `Li2025_supp/`: the Europe PMC full text (PMC11617651), the GitHub README,
  `Multi_GEX_starsolo.Rmd` (cluster to type map) and `Integration.Rmd`.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| `Li2023/` (reviewed) | Li C et al. 2023 *Nat Chem Biol* 19:1031, 10.1038/s41589-023-01327-0; PRJNA847226; Dryad 10.5061/dryad.d2547d851 | Protoplast scRNA-seq, 10x 3' v3.1 (3 libraries) plus 1 Drop-seq replicate; young leaves, cv. Sunstorm Apricot; genome v3 | 15,437 (text) / 15,348 (Source Data) | Cluster-level only. Source Data Fig 4a has a cluster per cell but no barcodes, and the GitHub code gives 17 clusters, not the published 16 | medium |
| Sun 2023 (collation check only) | Sun S et al. 2023 *Nat Plants* 9:179, 10.1038/s41477-022-01291-y; PRJNA759937; genome PRJNA841429; figshare 10.6084/m9.figshare.20255094 | Protoplast scRNA-seq, 10x (3 leaf samples; 1.8-2.0 cm leaves used for RIH); own genome assembly, `EVM00xxxxx` gene IDs | 34,392 high-quality cells (Alevin) | Cluster-level only. Supplementary Data 1 (8.9 MB Plotly HTML) has cluster numbers per point but no barcodes. Quantification is in a 1.17 GB figshare tarball (`00_alignment_output.tar.gz`; not downloaded) | medium-high for the MIA types (new RIH for 4 markers plus TDC and G10H) |
| Li 2025 (collation check only) | Li C et al. 2025 *New Phytol* 245:347, 10.1111/nph.20208 (PMC11617651, open access); PRJNA1098712; figshare 10.6084/m9.figshare.25586979 | 10x snMultiome (RNA plus ATAC), mature leaves of 8-10-wk plants, 3 reps; genome v3 | 8,803 nuclei (RNA); 3,542 with both assays | Probably per-nucleus, inside `CRO_RNA.Rds` (283.9 MB) and `CRO_multiome.Rds` (445.3 MB) on figshare (not downloaded; the code writes `cell_type` into `meta.data`). STARsolo matrices are 34-39 MB per rep | not scored. Same lab, genome and marker list as Li 2023 |

Cell types per dataset, as published:

- **Li 2023:** Mesophyll 62.2%, Epidermis 14.6%, Unassigned 11.9%,
  Vasculature 4.9%, IPAP 3.8%, Idioblast 2.6%.
- **Sun 2023:** MC 75.9%, EC 8.2% (subclustered into EC1, EC2 and GC),
  VC 3.3%, IC 2.3% (Table S14), plus IPAP, PC (proliferating) and UN. Its
  anatomical estimate of epidermis is 30%, so protoplasting under-recovers
  epidermis.
- **Li 2025** (clusters at res 0.5, from `Multi_GEX_starsolo.Rmd`):
  Mesophyll 0,1,3,7 (54%); Epidermis 2,5 (18%); Guard cells 12;
  Vasculature 6,10,11,14,15; IPAP 13; Idioblast 8; Unassigned 4,9.

## Verdict matrix (by canonical cell type)

The Li 2023 column holds the review's verdicts. The Sun 2023 and Li 2025
columns are provisional desk assessments from the published tables and figure
legends, not rubric scores. "-" means the type is absent or not resolved.

| Cell type | Li 2023 | Sun 2023 | Li 2025 |
|---|---|---|---|
| IPAP | Adopt (10 MEP/iridoid genes with earlier in situ evidence; cluster 11) | Adopt-provisional (G10H RIH, SABP2 RIH; GES/G10H/SABP2 45-57x) | present (cluster 13; same marker list as Li 2023) |
| Idioblast | Adopt (D4H 96%, DAT 67%; may include laticifers) | Adopt-provisional (D4H 53x, DAT 146x) | present (cluster 8; source of IDM1) |
| Epidermis | Adopt (clusters 1, 14; sides not split) | Adopt-provisional (NLTP2 RIH, TDC RIH; EC1 = MIA/ATML1, EC2 = cuticle/AO) | present (clusters 2, 5) |
| Adaxial / Abaxial epidermis | - | - (EC1/EC2 not assigned to a side) | - |
| Guard | - (dropped after the preprint) | provisional (GC from EC subclusters; FAMA 26x) | present (cluster 12) |
| Mesophyll | Revise (lumped; subclusters driven by replicate) | Revise (lumped, 76%; CB21 RIH not specific in scRNA) | present (4 clusters) |
| Palisade / Spongy / Bundle_Sheath | - | - | - |
| Vasculature (xylem, phloem, CC, procambium) | Revise (one merged cluster 9; Arabidopsis-ortholog markers weak) | Revise (one VC cluster; PRS2 RIH; pseudotime marker panels for procambium, SE and CC, but no subclusters called) | present (5 clusters, not split) |
| Laticifer | - (possibly inside Idioblast) | - | - |
| Dividing_cells | - (none reported) | PC cluster (KNOLLE, CDKB2, KIN5C, histones): a state, not a type | - |
| Unassigned | Reject as a type (cluster 3 is batch-driven) | UN (not analysed) | Unassigned 4, 9 |

## Cross-study markers

Agreement was counted only when the same gene is in Li 2023 (v3 ID) and
Sun 2023 (EVM ID) with **the same *C. roseus* UniProt accession** in the two
papers' own tables (Li review `uniprot` column; Sun Table S5/S7 `Entry`),
and both place it in the same cell type. The EVM and v3 loci could not be
compared at the sequence level (see "Could not verify"), so this is
equivalence at the level of the characterized gene. Li 2025 is not counted
as independent, because it used the Li 2023 marker list.

12 genes agree at the accession level:

| Cell type | Gene (v3 ID; UniProt) | Li 2023 | Sun 2023 | Effect on confidence |
|---|---|---|---|---|
| IPAP | G8H/G10H (CRO_01G006750; Q8VWZ7) | 67% vs <=5% | 46x; RIH | already high |
| IPAP | GOR/8HGO (CRO_01G027010; W8JWV8) | 59% vs <=5% | 20x | already high |
| IPAP | IO/7DLS (CRO_03G004950; W8JIS5) | 77% vs <=13% | 36x | already high |
| IPAP | 7DLH (CRO_03G018360; U5NE19) | 38% vs <=8% | 5x | already high |
| IPAP | 7DLGT (CRO_05G028810; U5NH37 = U3U992) | enriched | 7x | kept medium (v3 locus split over 4 IDs) |
| IPAP | ISY (CRO_07G007680; K7WDL7) | 33% vs <=1% | 37x | low to **medium** |
| IPAP | DXR (CRO_04G024660; Q9M4W4) | 51% vs <=12% | 18x | medium to **high** |
| IPAP | MCS/MECS (CRO_07G005430; Q9M4W3) | 33% vs <=12% | 7x | medium to **high** |
| Epidermis | TDC (CRO_03G032340; P17770) | 33% vs <=7% | 4x; RIH | already high (in situ in two independent studies) |
| Epidermis | 16OMT (CRO_03G030620; B0EXJ8) | 17% vs <=7% | 20x | already high |
| Idioblast | D4H (CRO_06G013360; O04847) | 96% vs <=12% | 53x | already high |
| Idioblast | DAT (CRO_02G001090; Q9ZTK5) | 67% vs <=2% | 146x | already high |

Agreement on **non-specificity** lowered or held some genes: LAMT (broad
in both studies: medium), STR (in situ in epidermis, but not specific in
either scRNA dataset: low), NMT (idioblast plus epidermis in both: low).
GES, HDS, CS, APL, SUC2 and FAMA agree by gene name only (no accession on
one side), so they were not raised.

## Gaps

No validated marker (`function` tier, or in situ in *C. roseus*) for:
Mesophyll (photosynthesis genes only), Palisade_Mesophyll, Spongy_Mesophyll,
Bundle_Sheath, Adaxial/Abaxial epidermis, Guard (FAMA ortholog only,
`characterized_enriched`), Stomatal_lineage, Trichome, Laticifer (D4H/DAT
do not separate it from idioblasts), Colleter, Xylem, Xylem_Parenchyma,
Phloem / Phloem_Companion / Sieve_Element / Phloem_Parenchyma (Arabidopsis
orthologs at low confidence; PRS2 RIH is on an EVM ID), Procambium,
Dividing_cells and S_Phase (Sun's PC markers are on EVM IDs only). For the
non-MIA types, use `arabidopsis_leaf.tsv` through homology.

## Recommended label reference

- **For IPAP, idioblast and epidermis, use the markers rather than any
  label set.** Twelve genes agree across two independent atlases, and most
  also have earlier in situ evidence. No dataset gives barcoded labels in a
  small table.
- **Per-cell labels:** Li 2025 `CRO_RNA.Rds` (283.9 MB, figshare
  25586979) is the only source that probably has per-nucleus labels in v3
  IDs, and it is the only one with a guard-cell cluster on v3 IDs. Export
  `meta.data` in a job (`r_seurat` env) before relying on it, and give it a
  Part A review first (it has not had one).
- **Cluster-level reference:** Li 2023 (cluster map in `Li2023/cluster_to_celltype.tsv`)
  matches the v3 genome. Sun 2023 has the finer epidermal split (EC1, EC2,
  GC) and a dividing-cell cluster, but its EVM IDs need mapping to v3 first.

## Conflicts and corrections to the review

- **ID re-check:** all 33 v3 IDs in `Li2023/markers_li2023.tsv` were
  re-matched against Li 2023 Tables S6 and S8 and agree. The UniProt
  accessions in the review were confirmed (REST API, taxonomy 4058) as the
  named *C. roseus* enzymes. The v3 locus itself still could not be checked
  in an organism database (MPGR, `mpgr.uga.edu`, still does not respond).
- **GOR and ISY split loci:** the review says the v3 loci are split
  (CRO_01G027010/020; CRO_07G007680/690). That comes from Source Data Fig
  4b-2. Table S6 lists only CRO_01G027010 and CRO_07G007680. Use the first
  locus, and check the second in your data.
- **7DLGT accessions:** U5NH37 (Li review) and U3U992 (Sun Table S7) are
  two UniProt entries for the same gene (UGT709C2/UGT8). This is not a
  conflict.
- **GES accession:** Sun's GES entry J9PZR5 is auto-annotated in UniProt as
  "myrcene synthase (GS)". That is UniProt's label; the gene is the
  IPAP-specific GES in Sun's data.
- **STR:** the review graded it `function` (earlier in situ in epidermis).
  Neither scRNA dataset shows it as specific, so it was set to `low`, with
  the conflict noted in `basis`.
- **SWEET11:** Li 2023 Table S8 labels it "Ploem CC". In Arabidopsis,
  SWEET11 is a phloem-parenchyma marker, so it is filed as Phloem_Parenchyma.
- **CRO_03G000120:** Li 2023 Table S8 uses this locus as the root
  atrichoblast TTG2 ortholog. Li 2025 names the same locus IDW1 (Idioblast
  WRKY1), idioblast-specific in leaf. The organs differ, but don't carry the
  TTG2 label into leaf work.
- **Sun SLS and SGD paralogs:** Sun maps four SLS loci to one UniProt entry
  (Q05047), and SGD1/SGD2 to another (Q9M7N7). The Li-Sun locus match for
  SLS1 and SGD1 is therefore not resolved, and they were not counted as
  cross-study.
- **Canonical names:** `IPAP`, `Idioblast` (alkaloid idioblast, distinct
  from the skill's `Myrosin_Idioblast`), `Laticifer` and `Colleter` are new
  names. `Vasculature` is a lineage-level label (like `Stele` in the root
  tables), used only for Sun's PRS2.
- **New trait tag:** the MIA rows carry `requires=Apocynaceae`, so that
  homology mapping does not put them on other species, where GES/G8H
  homologs are not IPAP markers. This tag is not yet in the skill's
  vocabulary: add `Apocynaceae -> eudicot` to `IMPLIES` in `map_markers.py`
  before using the table.

## REVIEW rows (Sun 2023 EVM IDs)

`EVM0013196` SABP2 (IPAP), `EVM0026652` NLTP2 (Epidermis), `EVM0034564`
PRS2 (Vasculature) and `EVM0013845` CB21 (Mesophyll) were validated by RIH
in Sun 2023 (Ext Data Fig 4). They have no v3 ID. They will not match
v3-annotated data, and `map_markers.py` cannot BLAST them, until each EVM
protein is mapped to a v3 locus (BLAST of the Sun proteome, PRJNA841429,
against the v3 proteome, Dryad `cro_v3` files). Other useful Sun-only
markers waiting for the same mapping: GC (EVM0017755 FAMA, EPF2, MUTE), EC2
(EVM0009371 AO/CYP716AL1, CER3, CYP77A), Dividing_cells (EVM0031057 KNOLLE,
EVM0004978 CDKB2, KIN5C), VC panels (APL EVM0001919, SUC2 EVM0020471,
FTIP1, CEPR1, DOF5.6, PP2-A1, BRX).

## Overlap with existing skill tables

There is no *C. roseus* table in `references/markers/`. Through
`arabidopsis_leaf.tsv` (homology), five rows here are orthologs of genes in
that table: CA1 (AT3G01500), FAMA (AT3G24140), SUC2 (AT1G22710), APL
(AT1G79430) and SWEET11 (AT3G48740). For these, the skill table and this
draft should agree after mapping; check that `map_markers.py` hits the same
v3 loci that Li 2023 Table S8 lists. KCS6, TMO5, WOX4, ACL5, LHCB2 and CAB3
are not in the skill table. All MIA, IPAP and idioblast markers are new to
the skill.

## Could not verify

- **v3 locus IDs in an organism database:** MPGR (`mpgr.uga.edu`) timed out
  again (2026-10-20), and Dryad file downloads need a bearer token (the
  review did not get around this, and neither did I). UniProt has no v2/v3
  locus IDs. IDs rest on Li 2023's own tables, which agree with each other.
- **EVM to v3 mapping:** the Sun proteome and the v3 proteome were not
  available as small downloads, so no sequence-level match was made.
  Cross-study agreement is per UniProt accession instead.
- **Sun 2023 full text** is paywalled. I used only the public abstract,
  figure and Extended Data legends, and the ESM files, so its in-text
  validation details and per-type cell counts beyond Table S14 were not read.
- **Li 2025 Supporting Information** (Table S4 marker list on Wiley) was not
  fetched. The cluster map comes from the GitHub code, and the per-nucleus
  labels in the figshare Rds were not opened (too large for this session).
- **Prior in situ papers:** the attribution of individual genes to the papers
  behind Li 2023's in situ asterisks (refs 18-22: Burlat 2004, Miettinen 2014,
  Guirimand 2010, Guirimand 2011, Simkin 2013) and St-Pierre 1999 follows the
  paper titles and Li 2023's text. The original figures were not re-read.
