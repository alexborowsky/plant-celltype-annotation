<!-- Collated from the survey review of medicago_nodule (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Medicago truncatula nodule: group summary of cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill, from two dataset reviews (`Ye2022/`, `Jhu2026/`)
and the characterized-marker survey (`survey/characterization/characterized_markers.tsv`). This is a new group.
No row in that survey has a `medicago_nodule:` entry in `gaps_filled`, but 7 Medicago nodule rows there match
IDs used here (ENOD2, ENOD11, ENOD12, PLT3, PLT4/BBM) or fill meristem gaps (PLT1, NOOT1, NOOT2). They are
used as independent support or added as rows, and their `basis` says so. The skill was not edited.

Files written here:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Expected types for an indeterminate (14-49 dpi) Medicago nodule, from anatomy (zones I-IV plus peripheral tissues). `function_markers` is counted from `markers_draft.tsv` |
| `markers_draft.tsv` | 60 rows (59 genes). Skill schema + `alt_id` + `other_ids`. `ref_gene` = MtrunA17r5.0 (`MtrunA17Chr#g#######`), the same convention as `medicago_root`. `alt_id` = Mt4.0 `Medtr` (blastp, checked against UniProt MTR_ names). `other_ids` = UniProt accession |

## Datasets

| Dataset | Platform | Cells | Label access | Quality | Role here |
|---|---|---|---|---|---|
| **Ye et al. 2022** *Mol Plant* 15:1852-1867, doi 10.1016/j.molp.2022.10.019 (confirmed via Crossref and the article PDF; Europe PMC and PubMed have no record, rechecked 2026-10-20); CNCB PRJCA012129 / CRA008337 | Protoplast scRNA-seq, 10x 3'; infected and uninfected protoplasts purified separately then pooled; A17 x Sm1021, 14 dpi | 9,756 cells, 2 replicates, 13 clusters | cluster only (web viewer unreachable) | medium | Source of 12 promoter-GUS and 2 GFP-fusion validated cluster markers; the only reporter-validated nodule scRNA atlas |
| **Jhu et al. 2026** bioRxiv, doi 10.64898/2026.06.23.733685 (preprint, CC-BY) | 10x Xenium in situ, FFPE; 50-gene pilot + 405-gene Medicago panel + 50-gene *S. meliloti* panel; A17, R108, 5 mutants; 14 and 49 DPI, 4D series | >136,000 cells; 4D WT atlas 90,389 cells in 21 clusters | cluster only (GEO controlled access until publication; Table S3 blocked by Cloudflare 1015) | high | Cell-resolution spatial validation of Ye markers; anatomical names; recasts Ye clusters |

## Per-cell-type verdict matrix

| Expected type | Ye 2022 (scRNA, 14 dpi) | Jhu 2026 (Xenium) |
|---|---|---|
| Nodule_Meristem | NA2 (365, 3.7%) **Revise**: partly a G2/M state (CDK2, CDKB2;2); NAC969-GUS in a few meristem cells | NAC_CM **Revise** (apex cortex + central meristem; no cell-cycle genes in top-3); NRMerPr (4D shared meristem/primordium) Revise, state |
| Nodule_Apex | NA1 (460, 4.7%) **Revise**: flavonoid-rich distal apex, meristem vs outer tissue unresolved | (inside NAC_CM / NOC_RC) |
| Infection_Zone | PI (495, 5.1%) **Adopt** (distal state); IF (235, 2.4%) **Adopt** (proximal state) | IF_R108 **Adopt**; IF_IZ_A17 **Revise** (IZ merged); 49 DPI InIFZ/PreIFZ **Adopt** |
| Interzone_Infected | NF1 (611, 6.3%) **Adopt** | IZ_R108 **Adopt**; 49 DPI InIZ **Adopt** |
| Infected_Cell | NF2 (255, 2.6%) **Adopt**, strongly under-recovered | InNF **Adopt** |
| Uninfected_Cell | UiC2 (882, 9.0%) **Adopt**; UiC1 (351) **Revise** (no own marker; merge or resolve) | UninNF **Adopt**; UninIFZ **Adopt**; 49 DPI UninNF/UninNF_L **Revise** (one type, two states) |
| Nodule_Parenchyma | NP (1,220, 12.5%) **Adopt** (check doublets: highest UMI) | NPC_RIC **Revise** (merged with root inner cortex); NEP **Revise** (with epidermis) |
| Nodule_Vascular_Endodermis | UN1 (420, 4.3%) **Revise**: unresolved peripheral layer -> vascular endodermis per Jhu in situ | NV_Endo **Adopt**; RNV_Endo **Revise** (root + nodule) |
| Nodule_Vasculature | VA (189, 1.9%) **Revise** (merged) | (RNV_Peri is a proliferation state; RPeri is root) |
| Nodule_Cortex | - | NOC_RC **Revise** (with root cortex) |
| Nodule_Epidermis | - | NEP **Revise** (with parenchyma) |
| Dividing_cells (state) | inside NA2 | 14-DPI "RNV_Peri" **Revise** -> Dividing_cells |
| Senescing (state) | - | SenZ (dual-species) **Revise**: bacteroid transcripts, no host marker |
| not a type | MIX (4,005, 41.1%) **Reject** (low-UMI ambient/mito bin); UN2 (268) **Reject** (HSP70 stress state) | InIZ_NF Revise (bacteroid state); root-only clusters REndo_RIC, RC, RPeri (outside nodule scope) |

## Recommended label reference

**Jhu 2026** for compartment identity: it is cell-resolution in situ, its names follow anatomy, and it leaves
mixed cells unforced. Its labels cannot be transferred per cell (cluster only, controlled access, targeted
405-gene panel). **Ye 2022** remains the practical scRNA reference for protoplast data (same chemistry as most
users), using the Jhu recasting: UN1 -> Nodule_Vascular_Endodermis, NA2 -> Nodule_Meristem + Dividing_cells,
NA1 -> Nodule_Apex, UiC1 unresolved, MIX and UN2 rejected. Expect infected cells to be under-recovered in
protoplast data.

## Markers (`markers_draft.tsv`)

60 rows, 59 genes (APY-9 has deliberate rows in Infection_Zone and Nodule_Vascular_Endodermis, because the
two studies conflict). Evidence: 18 `function`, 31 `characterized_enriched`, 11 `expression`.
Confidence: 12 high, 34 medium, 14 low. By type: Infection_Zone 11, Infected_Cell 9, Uninfected_Cell 8,
Nodule_Meristem 7, Nodule_Vascular_Endodermis 7, Interzone_Infected 5, Nodule_Vasculature 4, Dividing_cells 3
(kind=state), Nodule_Cortex 2, Nodule_Parenchyma 2, Nodule_Apex 1, Nodule_Vascular_Meristem 1.

Grading choices:
- Xenium is cell-resolution spatial, so it counts as in situ. Jhu top-3 genes without a characterized function
  are `expression` but `medium`; genes from merged root+nodule clusters are `low`.
- Ye promoter-GUS is zone-level, not cell-level: `characterized_enriched` medium unless the cluster
  specificity is weak (then low).
- All nodule rows carry `requires=Fabaceae`; the Dividing_cells rows carry no tag. `tissue=nodule`.
- Ye cell-type names were harmonized: Infection_Zone_Distal (PI) and Infection_Zone_Proximal (IF) ->
  `Infection_Zone` (distal/proximal kept in `basis`); Fixation_Zone_Infected -> `Infected_Cell` (tagged
  `[Fixation_Zone_Infected]` in basis); Nodule_Peripheral_UN1 -> `Nodule_Vascular_Endodermis`;
  Nodule_Meristem_Distal -> `Nodule_Apex` (CHS4) or `Nodule_Cortex` (N13). Jhu's Interzone ->
  `Interzone_Infected`, and its Vascular_Endodermis (root+nodule) -> `Nodule_Vascular_Endodermis`.

### Cross-study confidence raises (same gene ID, independent studies)

| Gene | Type | Studies | Change |
|---|---|---|---|
| MtLb1 Chr5g0435611 | Infected_Cell | Ye GUS + Jhu Xenium | medium -> high |
| MtNodGRP1B Chr5g0438361 | Interzone_Infected | Ye GUS + Jhu Xenium | medium -> high |
| MtN19 Chr2g0292611 | Infection_Zone | Ye GUS + Jhu Xenium | medium -> high |
| MtENOD12 Chr3g0082981 | Infection_Zone | Ye IF enrichment + Jhu Xenium + Pichon 1992 in situ | medium -> high |
| MtENOD11 Chr3g0082991 | Infection_Zone | Journet 2001 reporter + Ye PI enrichment | medium -> high |
| MtN6 Chr1g0180241 | Infection_Zone | Ye PI (weak) + Jhu Xenium | low -> medium |
| MtAS1 Chr5g0430381 | Uninfected_Cell | Ye GFP fusion + Jhu Xenium | medium -> high |
| MtAS2 Chr3g0105311 | Uninfected_Cell | Ye GFP fusion + Jhu Xenium | medium -> high |
| MtLEC4 Chr1g0197771 | Uninfected_Cell | Ye enrichment (GUS broad) + Jhu Xenium | low -> medium (not high: Ye reporter is broad) |
| MtENOD2 Chr1g0186761 | Nodule_Parenchyma | van de Wiel 1990 in situ + Ye NP + Jhu Xenium | -> high |
| MtUMAMIT14 Chr1g0160171 | Nodule_Vascular_Endodermis | Ye GUS + Jhu Xenium | medium -> high |
| MtPLT4/BBM Chr7g0249621 | Nodule_Meristem | Franssen 2015 + Jhu NAC_CM top-3 | medium -> high |

Not raised: MtPLT3 (Franssen 2015 + Ye NA2 only weakly enriched, 0.86 vs 0.53); MtN13 (Ye NA1 vs Jhu NOC_RC are
not the same compartment).

Lowered: MtMMPL1 medium -> low (its r1.7 ID is absent from LIS ann1_6 and UniProt; no Mt4.0 alt_id).
MtAPY-9 Infection_Zone medium -> low (conflicts with Jhu, see below).

## Gaps (expected types without a validated marker)

- **Nodule_Endodermis**, **Nodule_Epidermis**: no marker; not resolved in either atlas.
- **Nodule_Vasculature** sub-types (xylem, phloem, pericycle): only merged-VA markers, none `function`.
- **Nodule_Vascular_Meristem**: only NOOT1 from the characterized survey; no atlas cluster.
- **Senescing** (zone IV): no host marker (Jhu SenZ is bacteroid-driven; Ye at 14 dpi has none).
- **Nodule_Cortex** and **Nodule_Apex**: no `function` marker; Jhu cortex clusters merge root cortex.
- **Uninfected_Cell**: Ye UiC1 has no specific marker.
- Function markers with unconfirmed IDs: ERN1 (alt_id by symbol only), MMPL1.

## Conflicts

- **MtAPY-9** (Chr7g0252881): Ye promoter-GUS at the distal infection zone (PI) vs Jhu Xenium top-3 of
  RNV_Endo (root + nodule vascular endodermis). Two rows, both low.
- **NRAMP1**: Ye puts it in NF1 (interzone infected); Jhu's top marker of RC (root cortex). Not in the table.
- **Symbol clashes (match by ID):** paper "MtLb1" Chr5g0435611 = UniProt G7KGS8 "Lb120-1"; UniProt P27992
  "Lb1/Lb2/Lb6" = Chr5g0427351 = paper "MtLb2". Paper "MtNodGRP1B" Chr5g0438361 is "NodGRP1C" in UniProt
  G7KH53 and the GFF (the paper's NodGRP1C is Chr5g0438231). Jhu "MtN8|MtLP14" = ENOD2.
- **UN1 identity**: Ye left it unknown; Jhu UMAMIT14 in situ places it in the vascular endodermis.
- **LEC4**: Jhu in situ uninfected-specific vs Ye GUS broad (meristem periphery, ZII, IZ).
- **AS2** is also Jhu's NEP top marker, so it is not exclusive to uninfected cells.

## Could not verify / access

- Jhu 2026: Table S3 (cluster sizes, DE), supplementary figures and the panel table (bioRxiv Cloudflare 1015;
  NCBI deposit controlled access). Cluster cell counts are unknown.
- Ye 2022: the web viewer (http://1.15.171.133:3889) was unreachable during the review; GSA run sizes not retrieved.
  No per-cell labels. DOI has no Europe PMC record (confirmed via Crossref only).
- MtERN1 and MtMMPL1 r1.7 IDs could not be matched to LIS ann1_6 or UniProt by ID.
- Jhu 2026 `alt_id`s for NCR685 (94%) and GIF2 (93%) are partial blastp hits.
