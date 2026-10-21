<!-- Collated from the survey review of brassicaceae_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Brassicaceae root: collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill. This folder has one reviewed dataset so far, Wang et al. 2026. Its full review is in `Wang2026/README.md`. The skill itself was not edited.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Expected cell types of a Brassicaceae primary root tip (4-6 d), built from anatomy. `function_markers` counts distinct `function` genes in the skill's `arabidopsis_root.tsv` plus `markers_draft.tsv`, root rows only |
| `markers_draft.tsv` | 35 rows (34 genes), skill marker schema plus `alt_id`. `ref_gene` is the TAIR10 AGI. `alt_id` holds the 1-to-1 orthologs as `Esa:<id>;Sir:<id>;Spa:<id>` |
| `Wang2026/` | Review folder: supplements, figures, code excerpts, `markers_selected.tsv` (per-species ID columns and OG IDs) |

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Wang2026 | Wang G, Ryu KH, Dinneny A, et al. (2026) Evolutionary diversity of cell-type-specific expression and stress response in Brassicaceae roots. *Nat Commun*. doi:10.1038/s41467-026-73270-2 (PMC13381801); GEO GSE268881 | Protoplast scRNA-seq, 10x 3' v3.1, root tips of A. thaliana, S. irio, S. parvula, E. salsugineum, C. sativa; control, ABA, NaCl; 2 reps | 174,820 (4 diploids) + 27,442 (C. sativa); per-type counts not published | large_object: per-cell labels only in Seurat RDS on GEO (7.8-45 GB each) | High for inner layers and vasculature; medium for root cap and epidermis |

Gene IDs in Wang2026:
- Ath: TAIR10 AGI.
- Esa: Phytozome 12 v1.0 (`Thhalv...m.g`).
- Spa: Phytozome 12 v2.2 (`SpNgNNNNN`).
- Sir: BRAD v1.0 plus CoGe 57216 gene models (`Si-s...`).
- Csa: BRAD v2 (`Csa...`).

## Verdict matrix (cell type x dataset)

Only one dataset, so the matrix has one column. Canonical names follow the skill tables.

| Canonical cell type | Wang2026 label | Wang2026 verdict | Note |
|---|---|---|---|
| Lateral_Root_Cap | LRC | Revise | DDPS5 HCR in 4 spp; LRC/columella boundary soft |
| Columella | Columella | Revise | No HCR; only PPDK conserved in 4 spp |
| Quiescent_Center | - | not annotated | Authors report no QC cluster |
| Trichoblast | Trichoblast | Adopt | MOP10/PRPL1 HCR in 4 spp |
| Atrichoblast | Atrichoblast | Revise | No HCR; GL2 not detected; may include young epidermis |
| Cortex | Cortex | Adopt | ELP HCR in 4 spp |
| Inner_Cortex | Cortex "middle" subpopulation (Sir, Spa) | Adopt (species-specific) | AED3-ortholog HCR in S. irio |
| Endodermis | Endodermis | Adopt | UCC1 HCR; CASPs, MYB36, PER64 conserved |
| Pericycle | Pericycle | Adopt (caveat) | SIAR1 HCR; no pole split; shares genes with procambium |
| Procambium | Procambium | Revise | LAX3 HCR is stele-wide; likely undifferentiated-stele catch-all |
| Phloem / Sieve_Element / Phloem_Companion | Phloem | Revise | SAPL HCR; SE and CC merged |
| Xylem | Xylem | Adopt | FLA11 HCR; proto/meta not split |
| all types, C. sativa | (transferred) | Revise | Label transfer only, no in situ |

Global flags for Wang2026:
- Forced assignment (consensus vote and classifier transfer, no unknown class).
- Treatment cells were labelled by transfer from the Arabidopsis control reference.
- Developmental zones are a separate field, so proliferation is not encoded as a type.

## Marker table (`markers_draft.tsv`)

Summary:
- 35 rows: 18 `function`, 14 `characterized_enriched`, 3 `expression`.
- The 27 genes from the review were merged by AGI.
- 8 rows were added at collation from Wang SD2: known markers that are specific in 3-4 species and have a cell-type function. They are CASP2, ASFT, AHA3, IRX9, IRX15, IRX8 and GUX1. The eighth is AED3, which was split into a Cortex row and an Inner_Cortex row.
- Every AGI and its Esa/Sir/Spa orthologs were re-checked against the primary tables (SD2 TableS2, SD3 TableS3.1, SD5 for Si-s1384-01650). All matched.
- Every AGI was checked in UniProt (2026-10-20).

Trait tags:
- `Inner_Cortex` (AED3) `requires=Brassicaceae`. Only species with two cortex layers have it, and it is shown only in this family.
- SUC2 `requires=eudicot`, the same as `arabidopsis_leaf.tsv`.

Other markers in the table:
- The 3 `expression` rows (PER69, PER27, BHLH68) are conserved DE genes with no validation. They are kept only because Atrichoblast and Pericycle have little else.
- Wang's "tau >= 0.89" specificity cut-off is the paper's own; it is not re-derived here.

### Cross-study markers

Within this group there is no second dataset, so no within-group agreement exists. Under the skill's rule (validated in one study, cluster-specific in an independent one), 5 genes were raised one confidence level. The other study is the prior Arabidopsis single-cell atlas that Wang SD2 cites as the marker's source:

| AGI | Symbol | Cell type | Wang 2026 validation | Independent cluster marker (per Wang SD2 `Reference`) | Confidence |
|---|---|---|---|---|---|
| AT5G58784 | DDPS5 | Lateral_Root_Cap | HCR 4 spp | Coate et al. 2020 Front Genet | medium -> high |
| AT2G32300 | UCC1 | Endodermis | HCR 4 spp | Wendrich et al. 2020 Science | medium -> high |
| AT1G44800 | SIAR1 | Pericycle | HCR 4 spp | Shahan et al. 2022 Dev Cell | medium -> high |
| AT3G12730 | SAPL (PHL12) | Phloem | HCR 4 spp | Coate et al. 2020 Front Genet | medium -> high |
| AT5G03170 | FLA11 | Xylem | HCR 4 spp | Denyer et al. 2019 Dev Cell | medium -> high |

Caveats:
- The original marker lists of Coate, Wendrich, Shahan and Denyer were not re-opened. The attribution comes from Wang SD2.
- Wang used Shahan 2022 as its label-transfer reference. Wang's own cluster specificity is therefore not counted as independent support for literature markers that had no new validation (for example PPDK, ACO4, BHLH30, SKS15). Those rows were not raised.

Classic function markers (CASP1/2/3/5, MYB36, PER64, SCR, APL, SUC2, IRX genes, RSL4, COBL9) were already `high` from function. Wang shows they stay specific in other Brassicaceae, except as noted in `basis`: RSL4, COBL9 and LRL3 are not specific in Esa, SCR is not specific in Sir or Spa, and CASP2 is not called in Spa.

## Overlap with existing skill tables

Comparison with `references/markers/arabidopsis_root.tsv` (same species and tissue):

- **Shared AGIs (10):** SCR, CASP1, CASP2, CASP3, MYB36, PER64 (Endodermis), COBL9 (Trichoblast), SKS15 (Lateral_Root_Cap), APL (Phloem), IRX9 (Xylem). Cell type and evidence agree for all 10.
- **New for the skill (24 genes):**
  - All 6 HCR-validated genes: DDPS5, MOP10, ELP, UCC1, SIAR1, SAPL. FLA11 and LAX3 are also HCR-validated.
  - The Inner_Cortex type.
  - CASP5, ASFT, AHA3, IRX15, IRX8, GUX1, RSL4, LRL3, PPDK, ACO4, BHLH30, BHLH68, PER69, PER27.
- **Elsewhere in the skill:** SUC2 is already in `arabidopsis_leaf.tsv` as Phloem_Companion (leaf).
- **FLA11:** The skill README says Nb-derived DE picks including FLA11 were removed on 2026-10-01. The FLA11 row here has independent support (HCR in 4 Brassicaceae plus a Denyer 2019 cluster marker), so it does not conflict with that removal. Re-adding it is a curator decision.
- **Possible uses:** extend `arabidopsis_root.tsv`, or add a `brassicaceae_root_Wang2026.tsv`. For Esa/Sir/Spa data, split `alt_id` into per-species columns first. `map_markers.py --id-column` expects one ID per cell. The per-species columns are already in `Wang2026/markers_selected.tsv`.

## Gaps (expected types with no validated, specific marker)

- **Columella:** no `function` marker and no in situ in Brassicaceae data. PPDK and ACO4 are low.
- **Quiescent_Center, Stem_Cell_Niche:** only WOX5 and PLT1 from the skill table. No Brassicaceae-relative validation, and no QC cluster in Wang.
- **Atrichoblast:** GL2 and WRKY44 come only from the Arabidopsis table. In other Brassicaceae, only unvalidated peroxidases are conserved.
- **Cortex, Inner_Cortex:** HCR-validated but `characterized_enriched`. There is no cortex function marker.
- **Sieve_Element:** no root SE marker. APL and SAPL are pan-phloem.
- **Pericycle subtypes:** no xylem-pole or phloem-pole marker. GATA23 marks founder cells only.
- **Procambium:** LAX3 is stele-wide. OPS and AGO10 come only from the Arabidopsis table.
- **Protoxylem vs Metaxylem:** no split.
- **Lateral_Root_Primordium, Dividing_cells:** no root rows. Use cell-cycle genes from `rice_root.tsv` or `arabidopsis_leaf.tsv`, mapped by homology.

## Recommended label reference

Use **Wang2026, A. thaliana control, for these types: Trichoblast, Cortex, Endodermis, Pericycle, Xylem.** The same holds for the diploid relatives, with Inner_Cortex added for S. irio and S. parvula. It is the only multi-species Brassicaceae root atlas, it has HCR validation in 4 species, and it keeps zones separate from types.

For Lateral_Root_Cap/Columella, Atrichoblast, Procambium and Phloem, treat its labels as hypotheses and resolve them with markers. For Arabidopsis alone, Shahan et al. 2022 (the reference that Wang's Arabidopsis labels were partly transferred from) remains the primary label source.

Per-cell labels need a compute job that exports `meta.data` from the GEO RDS objects. They are not on a login node.

## Conflicts and corrections to the review

1. **PRPL1 symbol (correction).** The review says the paper's name "PRPL1" for AT5G05500 conflicts with UniProt, and that PRPL1 is AT4G38770. That is wrong. UniProt Q9FFG5 (AT5G05500) lists `MOP10`, `AtPRPL1` and "proline-rich protein-like 1" as gene names, and AT4G38770 is PRP4 (Q9T0I5). The paper's name is consistent with UniProt. The table uses `MOP10/PRPL1`.
2. **MOP10 source is a rice paper.** In Wang SD2, AT5G05500's known-marker source is "Liu et al (2020) Mol Plant 14:1-11". The only matching reference in the paper is Liu Q et al. 2021 Mol Plant 14:384, *Transcriptional landscape of rice roots*. So this Arabidopsis "known marker" probably comes from a rice ortholog. It was not counted as independent Arabidopsis evidence, and its confidence stays `medium`.
3. **SIAR1 symbol.** UniProt has no symbol for AT1G44800 ("WAT1-related protein At1g44800"). SIAR1 (Siliques Are Red 1, an UMAMIT amino acid exporter) is the paper's name, and it matches the literature naming of this locus as recalled. The ID was taken from SD2/SD3, not from the name.
4. **SKS15 grade.** The review graded SKS15 as `expression`. It is `characterized_enriched low` here, to match the same row in `arabidopsis_root.tsv`.
5. **AED3 rows.** The review listed AED3 only under "Inner cortex". In SD3 it is a conserved Cortex gene in all 4 species, and HCR marks the whole cortex in Ath/Esa. It therefore has two rows: Cortex (no tag) and Inner_Cortex (`requires=Brassicaceae`).
6. **LAX3 grade.** Kept as Procambium but set to `low`, because the HCR is stele-wide.

## Not verified / not accessed

- Per-cell labels and per-type counts: RDS objects of 7.8-45 GB, not downloaded.
- Esa, Sir and Spa IDs: checked only against the paper's own tables, not against Phytozome, BRAD or CoGe.
- C. sativa marker IDs (SD3.3) were not used.
- The original marker lists of Coate 2020, Denyer 2019, Wendrich 2020 and Shahan 2022 were not re-opened. The cross-study attributions rely on Wang SD2's `Reference` column.
- AHA3, ASFT, IRX15, IRX8 and GUX1 functions are from UniProt names and standard literature knowledge. No primary reporter papers were re-read for root companion-cell, endodermis or xylem localization. AHA3 is `medium` for that reason.
- Supp. Data 8 (58 MB) and the Shiny browser were not explored (see `Wang2026/README.md`).
