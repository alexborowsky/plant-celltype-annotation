<!-- Collated from the survey review of cassava_leaf (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Cassava leaf: collated cell-type marker resources

Collated 2026-10-20 from the Part A review in `Zang2024/` (see `Zang2024/README.md`). This was a desk collation only: the data were not reanalysed.

Files in this folder:
- `expected_cell_types.tsv`: the cell types expected from eudicot leaf anatomy (Euphorbiaceae, young expanding leaf). `function_markers` counts the `function` rows in `markers_draft.tsv`.
- `markers_draft.tsv`: 49 rows in the skill marker schema. `ref_gene` uses the JGI v6.1 IDs (`Manes_XXGXXXXXX`), which are the IDs in the paper. `alt_id` holds the v8.1 IDs (`Manes.XXGXXXXXX.v8.1`), so for v8.1 data use `map_markers.py --id-column alt_id`. The Arabidopsis orthologs are given in `basis`.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Zang2024 | Zang Y ... Min Y. *Plant Physiol* 194:456-474 (2024). doi:10.1093/plphys/kiad500; PMC10756766. Data: NGDC GSA CRA012723 (raw reads only) | 10x 3' v2 on protoplasts; cv. SC8, the third leaf from the apex; 1 sample, no replicates | 11,177 cells, 15 Louvain clusters | Cluster level only. No barcode-to-label table, no processed object, no code | Low to medium. 4 clusters adopted (epidermis, companion cell, sieve element; dividing cells as states). About 21% of cells sit in stress, low-quality or unresolved clusters that carry type labels |

Other searches (2026-10-20): I found no other cassava leaf scRNA-seq or snRNA-seq dataset. The same group published a cassava tuberous root atlas (Song et al. 2023 *Front Plant Sci*, doi:10.3389/fpls.2022.1053669). That is a different organ, so I did not use it here. CassavaDB (Dai et al. 2025 *The Innovation*, doi:10.1016/j.xinn.2025.101092) has a single-cell UMAP viewer that probably re-hosts this dataset. I did not check whether it offers per-cell labels.

## Per-cell-type verdict matrix

There is only one dataset, so the matrix has one column. "Not reported" means the type is not annotated in that dataset.

| Expected type | Zang2024 |
|---|---|
| Epidermis | Adopt (c1) |
| Pavement (adaxial/abaxial) | Revise: subclusters 1-0..1-3; the polarity call from CHS/YAB5 is weak |
| Guard | Revise: subcluster 1-4, about 10-30 cells |
| Stomatal_lineage | Not labeled; EPF2/TMM signal is in c1 (EPF2 also in c3/c9) |
| Mesophyll | Revise: c0, c2, c4 merged |
| Palisade / Spongy mesophyll | Revise: the split is unsupported (RBR, ARP1, ABP19A) |
| Bundle_Sheath | Reject: c7 is a WRKY/defense state, and SCR is not enriched in it |
| Procambium / Xylem / Xylem_Parenchyma / Phloem_Parenchyma | Revise: all are merged in c5; the sub-labels have no published membership |
| Phloem_Companion | Adopt (c10) |
| Sieve_Element | Adopt (c12) |
| S_Phase | Revise to a state (c3) |
| Dividing_cells (G2/M) | Revise to a state (c8, c11) |
| Trichome, Hydathode, Laticifer | Not reported |
| Unresolved | c6 (growth/auxin state), c9 (plastid transcripts, low quality), c13 (stress), c14 (unknown): Reject |

## Cross-study markers

None. With a single dataset, no marker qualifies for the cross-study confidence increase. Every confidence value in `markers_draft.tsv` is based on Zang 2024 alone, plus the function of the Arabidopsis ortholog. No cassava reporter or mutant evidence exists for any row. The in situ data in the paper (Fig 1C, 5C) are low magnification and show no sense controls. They support only LHCB4.1 (mesophyll) and KCS1/ALDH3F1 (epidermal layer). The vascular probes (ACL5, the BURP gene "PGL3", Manes_04G116400) do not show cell-type specificity.

## Grading notes

- `function` means the Arabidopsis ortholog has a function that defines the cell type (orthology confirmed by Ensembl Plants v8.1, or flagged as unconfirmed in `basis`) and the gene peaks in the matching Zang cluster (Table S3/S10). The maximum confidence is `medium`, because nothing was validated in cassava. Where orthology is unconfirmed (TMM, SPCH, ATHB8, the second PXY, the third ACL5) or detection is very low (ALMT12, SPCH), confidence is `low`.
- Seven `expression` rows come from the paper's DE table S13 (ARP1, ABP19A, the BURP gene, Manes_04G116400, DJ1E, Manes_09G108300, ENODL). By the skill's rule they should not go into `references/markers/`. They are kept here only as a cassava-specific check list.
- Eight rows were added at collation from Table S3, because they are paralogs with the same symbol and the same cluster specificity: HDG2 Manes_13G071000, CER1 Manes_01G274900, KCS20 Manes_15G034900 and Manes_03G170600, MYB60 Manes_09G135700, ACL5 Manes_15G028000, PXY Manes_14G037000, DOF5.3 Manes_12G096300. I also added SPCH Manes_06G157200 and RBCS Manes_05G137400 and Manes_01G011500. All of them were checked in UniProt (MANES_...v8). The HDG2 and RBCS orthologs were also confirmed in Ensembl.
- `excludes=C4` is set on the photosynthesis genes, consistent with `arabidopsis_leaf.tsv`. SUC2 has `requires=eudicot`.

## Gaps (no validated `function` marker)

Mesophyll, Palisade_Mesophyll and Spongy_Mesophyll (only ambient photosynthesis genes); Bundle_Sheath (SCR only, and it conflicts with the data); Pavement; Xylem_Parenchyma; Phloem_Parenchyma (SWEET12 Manes_14G047600 is not detected, 0.01 in c5); generic Phloem (APL is not in the panel); Trichome; Hydathode; Laticifer (an Euphorbiaceae-specific type with no data); S_Phase (only characterized_enriched rows). Guard and Stomatal_lineage have function markers, but they are barely detected.

## Recommended label reference

Zang 2024 is the only reference. Use it at cluster level only, through marker transfer, because no per-cell labels exist. Adopt Epidermis (c1), Phloem_Companion (c10), Sieve_Element (c12) and the dividing states (c3 S phase, c8/c11 G2/M). Treat c0/c2/c4 as Mesophyll without a palisade/spongy split. Resolve c5 de novo into procambium, xylem and phloem using the Procambium/Xylem rows. Do not reuse the labels for bundle sheath (c7), the second and third epidermis clusters (c6, c9), or perivascular mesophyll (c13). For the missing types, use `arabidopsis_leaf.tsv` via homology.

## Conflicts and corrections to the review

- "FDH" Manes_16G087600 is a KCS family protein in UniProt. This is consistent: FDH is KCS10.
- "ACL5" names three loci. UniProt annotates all three as thermospermine synthase. Ensembl gives an AT5G19530 ortholog call for two of them but not for Manes_15G028000. The paralog used as the in situ probe is unknown.
- "PGL3" names two unrelated genes in the supplement: Manes_14G066900 (BURP domain, S13/S18) and Manes_01G038600 (6-phosphogluconolactonase, S16). The table uses the symbol "BURP" for the first.
- "VND7-like" Manes_02G191900 is labeled NAC030 in the paper. NAC030 is the Arabidopsis VND7 locus AT1G71930, so the symbol is VND7.
- EPF2 is listed as a guard-cell marker in the paper. Here it is placed under Stomatal_lineage, because EPF2 is expressed in meristemoids and GMCs.
- ARP1 and ABP19A, the paper's palisade and spongy markers, are placed under Mesophyll, because neither the paper's in situ nor Table S3 supports the split.
- DOF5.6/HCA2 and DOF5.3/TMO6, the paper's phloem markers, are placed under Procambium because they are restricted to the merged c5. They are graded low.
- SCR (bundle sheath) is kept, but the conflict is stated in `basis`: it is highest in dividing c11.
- Manes_09G108300 (companion cell) is missing from v8.1 in both Ensembl and UniProt, so `alt_id` is empty. Manes_18G018600 (HTR2, the S-phase H3.1 candidate in S13) is also missing from v8.1 and was left out.
- The review's verdicts stand. The single correction is that the review graded PDF1 as `function`. Here it is `characterized_enriched`, to match the skill's Arabidopsis table.

## Overlap with existing skill tables

There is no cassava table in `references/markers/`. By Arabidopsis ortholog, these rows correspond to genes already in `arabidopsis_leaf.tsv`: PDF1 (AT2G42840), FDH (AT2G26250), SUC2 (AT1G22710), SEOR1 (AT3G01680), XCP2 (AT1G20850), VND7 (AT1G71930), RBCS1A (AT1G67090, within the RBCS ortholog group) and CYCB1;1 (AT4G37490, within the CYCB1 ortholog group). ATHB8 (AT4G32880) is also in that table, but the cassava gene the paper calls ATHB-8 has no confirmed ortholog. SCR (AT3G54220) is in `arabidopsis_root.tsv`. The cassava-native rows add cassava paralogs that homology mapping may miss: HDG2 x2, ACL5 x3, MYB60 x2 and KCS20 x3.

## Could not verify

- I did not open the NGDC GSA CRA012723 / PRJCA019992 file lists, because they are behind a browser security check. I did not try to bypass it.
- The in situ probe paralogs (Table S18, 20-nt probes) were not BLASTed.
- I could not run a literature check on whether genes in the chr12 cluster that is DE in companion cells (UGT85K4 Manes_12G132300, UGT85K5 Manes_12G133000, CYP71E7 Manes_12G132900, CYP79D2 Manes_12G133500; Table S13) have published cell-level localization in cassava. These genes are not in the table. They are candidates for Phloem_Companion if a localization study confirms them.
- The orthology of TMM, SPCH, WOX4, ATHB8, KCS20, CER1 and DOF5.3 rests on the paper's symbols plus the UniProt family. Ensembl Plants v8.1 gives no 1:1 Arabidopsis ortholog for them.
- I did not check scPlantDB or the CassavaDB single-cell viewer for per-cell labels.
