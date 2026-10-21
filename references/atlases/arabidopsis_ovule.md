<!-- Collated from the survey review of arabidopsis_ovule (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis ovule (primordia, stages 2-I to 2-III): marker resources

Group collation for the plant-celltype-annotation skill, written 2026-10-20. It is based on one dataset review (`Hou2021/README.md`). Nothing in the skill was edited.

Files in this folder:
- `expected_cell_types.tsv`: cell types expected from ovule-primordium anatomy plus the placenta and carpel tissue dissected with it. Built from anatomy, not from the published labels. `function_markers` counts this draft plus the `any`-tissue rows of the existing Arabidopsis tables.
- `markers_draft.tsv`: 27 rows in the skill schema plus `alt_id` (UniProt accession). There are 25 `type` rows (`tissue=ovule`) and 2 `state` rows (`tissue=any`).
- `Hou2021/`: the dataset review, with supplementary tables, an ID check and a README.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Hou2021 | Hou Z et al. 2021 *Commun Biol* 4:1149, doi:10.1038/s42003-021-02676-z (PMC8486858); ENA PRJEB47244 | Protoplast scRNA-seq, 10x 3' v2, Cell Ranger 2.1.0 + Loupe clustering; ovule primordia with placenta, pKNU:KNU-Venus (Ler); one library per stage (AC, MMC1, MMC2), no replicates | 16,872 (4,577 / 5,054 / 7,241) | Cluster-level only (Supp Data 3); no per-cell barcodes or processed object; reuse means re-processing fastq | Low overall. Good only for the MMC/meiocyte subcluster |

This is the only published single-cell dataset for this group in the survey, so there is no second dataset to agree or disagree with. Cross-study agreement below means agreement between Hou 2021 single-cell enrichment and an independent earlier reporter, in situ or immunolocalization study.

## Verdict matrix (published label to canonical type)

| Canonical type | Hou2021 |
|---|---|
| Megaspore_Mother_Cell | Adopt: AGGR.11-s2 (228), MMC1.10-s3 (62, caution), MMC2.6-s3 (168). Reject AC.1 / AC.1-s1 (no KNU/ASY1 enrichment; L1 + S-phase signature) |
| Nucellar_Epidermis | Revise: AGGR.11-s3, MMC1.10-s2 (weak; stress genes). Reject MMC1.10-s1 and MMC2.6-s1, which are G2/M states |
| Subepidermal_Nucellus | Revise or Reject: MMC2.6-s2 and MMC1.10-s4 have a cuticle/L1 signature; AC.1-s2 was called from WRKY28 alone |
| Nucellus (layer unresolved) | Revise: MMC2.6-s4 |
| Chalaza, Inner/Outer_Integument, Funiculus, Placenta, Transmitting_Tract, carpel tissues | Not labelled (83-95% of cells). Inferred from the DE tables only: AGGR C5 ovule L1/integument, C10 septum/TT, C7 ovary-wall epidermis, C12 procambium, C14 phloem-like |
| Dividing_cells | Present but mislabelled as nucellar epidermis (MMC1.10-s1, MMC2.6-s1, AGGR.11-s5, AC.1-s5) |

## Cross-study markers

Three markers have their confidence raised for agreement between independent studies:

| AGI | Symbol | Type | Independent validation | Hou 2021 single-cell |
|---|---|---|---|---|
| AT5G14010 | KNU | Megaspore_Mother_Cell | pKNU:KNU-Venus MMC reporter (Tucker et al. 2012 *Development*; Cao et al. 2018 *PLoS Genet*) | 18-24% of MMC subcluster cells vs <=3%; AGGR C11 log2FC 5.6 |
| AT1G67370 | ASY1 | Megaspore_Mother_Cell | Meiocyte immunolocalization (Armstrong et al. 2002 *J Cell Sci*) | 39-48% vs <=4%; log2FC 5.1-6.0 |
| AT3G22880 | DMC1 | Megaspore_Mother_Cell | Promoter-GUS in megaspore mother cells (Klimyuk and Jones 1997 *Plant J*) | log2FC 4.0-4.7 |

Not counted as independent:
- WRKY28 (Zhao et al. 2018 *PNAS*): same lab as Hou 2021, and the single-cell data do not support it.
- ERL1, ER, ERL2, PGDH1 and AT4G13710: their reporters come from Hou 2021 itself.

## Marker draft summary

| Type | function | characterized_enriched | Notes |
|---|---|---|---|
| Megaspore_Mother_Cell | 7 (ASY1, DMC1, SDS, SWI1, MND1, ASY3, PS1) | 4 (KNU, CALS5, CDM1, TPD1) | The meiotic genes mark meiotic prophase. In samples that include anthers they also mark male meiocytes |
| Nucellar_Epidermis | 1 (ERL1) | 4 (ER, ERL2, PGDH1, PIN1) | All five reporters are from single studies |
| Nucellus | 2 (SPL/NZZ, WUS) | 1 (AT4G13710) | Sparse in the scRNA data |
| Subepidermal_Nucellus | 1 (WRKY28) | 0 | Not supported in the data |
| Outer_Integument / Inner_Integument / Chalaza | 1 each (INO; ATS/KAN4; BEL1) | 0 | Literature only; the paper did not use them |
| Transmitting_Tract | 2 (NTT, HEC1) | 0 | Literature; carpel carryover |
| Dividing_cells (state) | 2 (KNOLLE, SCL28) | 0 | |

Not carried into the draft:
- **PAB7 (AT2G36660)**: a top MMC feature gene (log2FC 5.4-5.9), but supported by DE only. The skill's policy keeps DE-only picks out of the tables. It is a good candidate to check in data.
- **AGO9 (AT5G21150)**: mRNA is detected in 5-80% of all clusters. Protein localization conflicts between studies: Olmedo-Monfil et al. 2010 *Nature* placed it in somatic companion cells, while Hou 2021 Fig. 9h shows it in the MMC.
- **WIH1/WIH2 (AT5G67600/AT2G41420)**: detected in 20-97% of every subcluster.
- **STK (AT4G09960, UniProt Q38836)**: marks ovule identity across the whole ovule, so it is not specific to one cell type.

`requires`/`excludes` are empty in every row. The genes are conserved meiotic, ovule-patterning or cell-cycle genes, and none is restricted to a C3/C4 or grass/eudicot trait.

The `tissue` value `ovule` is new. The skill vocabulary currently has only `leaf`, `root` and `any`, so adopting this draft needs that value added, or the rows recoded as `any`.

## Gaps (no validated `function` marker, or only one weak one)

- Funiculus, Placenta and Replum have no marker. Mesophyll (valve) has no ovary-specific marker.
- Subepidermal_Nucellus has only WRKY28, which the scRNA data do not support.
- Nucellar_Epidermis has only ERL1. Chalaza has only BEL1, which is also expressed in integuments.
- Archesporial cell (stage 2-I): no marker separates it from the MMC or the L1. Treat it as Megaspore_Mother_Cell.
- Ovary-wall epidermis (Epidermis): only the leaf-tissue rows apply, and ovule L1 cells share PDF1/ATML1.

## Recommended label reference

Hou2021, for Megaspore_Mother_Cell only: AGGR.11-s2 together with MMC2.6-s3, whose meiotic program agrees across the per-stage and aggregated analyses. No public labels exist for any other ovule cell type. Label everything else de novo with the draft markers. Treat the Hou "nucellus" subclusters as candidates, and first check them for G2/M states (KNOLLE/SCL28) and an L1 cuticle signature.

## Conflicts and corrections to the review

- **AGO9:** the review recorded AGO9 protein "in MMC". The earlier immunolocalization (Olmedo-Monfil 2010) puts it in somatic companion cells, so the draft leaves AGO9 out.
- **PGDH1, AT4G13710:** both are feature genes of the germline subclusters, but their reporters are somatic (distal nucellar epidermis; central nucellus / integument epidermis). They are placed under Nucellar_Epidermis and Nucellus, with the conflict noted in `basis`.
- **WUS layer:** Hou 2021 uses it for the nucellar epidermis, but Gross-Hardt 2002 reports expression in the nucellus. The draft uses Nucellus.
- **TPD1:** enriched only in the AGGR.11-s2 subcluster (log2FC 4.5), not at cluster level (AGGR C11 0.8). Graded low.
- **AGGR C14 (163 cells; SUC2 log2FC 8.6):** also shows KNU 2.9 and CALS5 1.7. The extreme fold-changes may be an artifact, so check C14 before using KNU/CALS5 alone.
- **ERL1:** also active in the stomatal lineage, which matters if carpel-wall stomatal cells are captured.

Gene IDs were confirmed in the paper's tables (Supp Data 1/3/6) and in UniProt reviewed entries (`Hou2021/marker_id_check_uniprot.tsv`). UniProt was queried today for the three added genes: NTT = AT3G57670 = Q9SVY1 (WIP2), HEC1 = AT5G67060 = Q9FHA7, STK = AT4G09960 = Q38836. All literature DOIs were checked in Europe PMC, except the CDM1 primary paper, which is not cited with a DOI.

## Overlap with existing skill tables (Arabidopsis)

- **KNOLLE (AT1G08560), Dividing_cells:** the same row is in `arabidopsis_leaf.tsv` (`tissue=any`). It is repeated here so the draft stands alone; drop it when merging.
- **CYCB1;1, H3.1, PCNA1** (`arabidopsis_leaf.tsv`, any): apply to the proliferating ovule primordium. Hou AGGR C11 has PCNA1 4.2 and CYCB1;1 2.3.
- **SUC2** (leaf, Phloem_Companion) fits Hou AGGR C14. **ATHB8** (any, Procambium) and **PIN1** fit AGGR C12. **PDF1** (leaf, Epidermis) is high in ovule L1 clusters too, not only in the valve epidermis.
- None of the ovule-specific types (Megaspore_Mother_Cell, nucellus, integuments, chalaza, transmitting tract) exist in the current tables.

## Could not verify

- Cell-resolution localization papers for SDS, SWI1, MND1, ASY3 and PS1 in female meiocytes. These rows rest on meiotic function plus the Hou 2021 enrichment.
- Any ovule localization for CALS5, CDM1 and TPD1.
- The Hou Supplementary Information PDF (feature plots) was not reviewed figure by figure.
- No processed matrix or per-cell labels are public, so nothing was checked in the counts themselves.
- The scPlantDB and PlantscRNAdb portals were not searched interactively.
- No second ovule single-cell dataset was included in this group's survey. Later ovule or gynoecium atlases, if any, are not covered here.
