<!-- Collated from the survey review of sorghum_leaf (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# sorghum_leaf: collated cell-type marker resources

Created on 2026-10-20 from one dataset review (Swift et al. 2024, folder `Swift2024/`, which has its own README and the extracted supplementary tables). This is a new group. Nothing in the skill was edited.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Sorghum (C4, NADP-ME type) leaf/seedling-shoot cell types, built from anatomy. `function_markers` = the number of `function` rows in sorghum `Sobic.` IDs (this `markers_draft.tsv` plus the skill core `sorghum_leaf.tsv`, unique by gene ID). Homology sources (maize_leaf primary, arabidopsis_leaf) are listed in `notes` |
| `markers_draft.tsv` | 39 rows in the skill schema plus `alt_id` and `other_ids`. `ref_gene` = Sobic v3.1 IDs as published. `alt_id` = UniProt/Ensembl `SORBI_3` form. `other_ids` = UniProt accessions plus `v5.1_name_present`: the same locus name exists in the BTx623 v5.1 proteome (`SwiftMultiomeReanalysis/rna_reference_mapping/ortholog_map/v51_gene.faa`). This is a name check only; sequence identity between v3.1 and v5.1 was not checked |

## Datasets

| Dataset | Citation | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Swift2024 | Swift J, Luginbuehl LH, ... Ecker JR, Hibberd JM. Exaptation of ancestral cell-identity networks enables C4 photosynthesis. *Nature* 636:143-150 (2024). doi:10.1038/s41586-024-08204-3; PMC11618092; GEO GSE248919; code github.com/joey1463/C3-C4. Sorghum part only | Nuclei. (1) RNA atlas: 10x 3' snRNA + sci-RNA-seq3, 265,701 nuclei, 9 time points (0-48 h light after 5 d dark), median ~400-750 UMI. (2) 10x Multiome RNA+ATAC at 0 h and 12 h, 20,169 nuclei. BTx623 seedling shoots, not mature leaves | RNA atlas: 19 clusters, 7 unknown. Multiome: unknown 7,515 (37.3%), mesophyll 5,264 (26.1%), epidermis 2,309 (11.4%), bundle_sheath 1,704 (8.4%), guard 1,532 (7.6%), phloem 1,303 (6.5%), xylem 542 (2.7%); every label in all 11 samples | Sobic v3.1 | large object: RNA-atlas labels only via Script 26 map on the 2.5 GB RData; the group already has the Multiome per-cell labels (a maintainers' folder) | medium |

## Per-cell-type verdicts

| Published label (clusters) | Verdict | Canonical | Share | Reason (short) |
|---|---|---|---|---|
| mesophyll (0, 1) | Adopt | Mesophyll | 26.1% | C4 M enzymes partitioned in pseudobulk (PEPC 40 vs 7, beta-CA 48 vs 2.5, PPDK 53 vs 18; SuppT9). Cluster 1 = greening state. Per-gene enrichment weak (1.3-1.8x). No in situ |
| bundle_sheath (4, 15) | Adopt | Bundle_Sheath | 8.4% | NADP-ME (correct ID Sobic.003G036200), GLDP, GDC-H, GOX, DiT2-like. Cluster 15 = suberin genes (suberized Kranz sheath). No sorghum reporter |
| guard (14) | Adopt | Guard | 7.6% | FAMA-like (pct ratio 18), SLAC1, GORK, SAPK10, MYB60, HT1. Includes GMC/young GC; subsidiary cells possibly merged |
| epidermis (6, 8, 17) | Revise | Epidermis | 11.4% | Right lineage (HD-ZIP IV, PDF1, KCS, CER1-like) but pavement, bulliform, hair and silica/cork merged |
| phloem (9, 12, 13) | Revise | Phloem | 6.5% | Cluster 9 companion-cell-like (SUT1, FT-like, AAP3); 12 phloem/vascular parenchyma with lignin genes; 13 procambium/vascular parenchyma? No sieve elements (nuclei). Paper marker ABCG18 is in no DE list |
| xylem (10) | Adopt | Xylem | 2.7% | Secondary-wall and TE program (CESA4, CESA8, IRX3, XCP1/2, MC9, LAC17). Fibres may be included |
| unknown (2, 3, 5, 7, 11, 16, 18) | Reject (keep unassigned) | - | 37.3% | 7 = S phase, 11 = G2/M, 16 = proliferating, 3 = hypoxia/stress, 2 and 5 = protoderm/cuticle + CYP79 (epidermis or coleoptile?), 18 unclear. Proliferation correctly not labelled as a type |

## Draft marker table summary

| Cell type | Rows | function | characterized_enriched | expression | high | Best markers |
|---|---|---|---|---|---|---|
| Mesophyll | 6 | 3 | 2 | 1 | 2 | PEPC Sobic.010G160700, beta-CA Sobic.003G234200 (high); PPDK Sobic.009G132900 |
| Bundle_Sheath | 13 | 4 | 7 | 2 | 2 | NADP-ME Sobic.003G036200, GLDP Sobic.008G039900 (high) |
| Guard | 6 | 5 | 1 | 0 | 0 | FAMA-like Sobic.009G250000, SLAC1 Sobic.006G186500, MYB60 Sobic.005G155900 |
| Epidermis | 5 | 0 | 5 | 0 | 0 | HDG2/HDG11-like HD-ZIP IV, PDF1 (all low) |
| Xylem | 4 | 2 | 2 | 0 | 1 | CESA8/IRX1 Sobic.003G296400 (high, see raise), CESA4 Sobic.001G224300 |
| Phloem | 4 | 1 | 3 | 0 | 0 | SUT1 Sobic.001G488700 (requires grass) |
| Silica | 1 | 1 | 0 | 0 | 1 | SLP1 Sobic.001G265900 (Kumar et al. 2020 J Exp Bot; from the survey characterized_markers.tsv) |

Changes from `Swift2024/markers_carry_forward.tsv` (38 rows):
- **Raised:** CESA8/IRX1 Sobic.003G296400 Xylem medium -> high. The same ID was validated by HCR in sorghum root xylem (Guillotin et al. 2023 Nature, ED Fig 8c; `../sorghum_root/`), and it is xylem-cluster-specific in Swift 2024. These are independent studies (different tissue, same cell type).
- **Not raised:** CESA4 Sobic.001G224300 (Guillotin root enrichment is scRNA only); SUT1 Sobic.001G488700 (weak and unvalidated in Guillotin root).
- **Tags:** SUT1 now `requires=grass` (grass SUT1 clade; matches the core table).
- **Added:** SLP1 (Silica). Its ID matches `survey/characterization/characterized_markers.tsv` (sorghum row, gaps brachypodium_leaf/maize_leaf:Silica). No row in that file names `sorghum_leaf:` in `gaps_filled`, so this was the only ID match.
- **Cleaned:** the "MEP" symbol and basis quoting for Sobic.003G431900.
- **Agreement with the skill core `sorghum_leaf.tsv`** (Brophy lab curation, v5.1 IDs, not an independent study, so no raise): PPDK, NADP-ME, IRX1, SUT1 and FTL12 (Swift "FT-like PEBP" Sobic.010G164200) have the same IDs. Core rows not in Swift's data or this draft: XCP1, CESA7, WBC11, CHX20, CST1, SWEET13, PEAR2, CCR1, LG1, CYP79A1.

## Gaps

Closed (new group, first coverage): Mesophyll, Bundle_Sheath, Guard, Xylem (function markers); Phloem (partial: lineage-level, companion-cell-like cluster only); Epidermis (generic lineage only, no function marker from Swift); sorghum ortholog anchors for the maize_leaf BS/M split (PEPC, CA, PPDK vs NADP-ME, GLDP); Silica (SLP1, from the characterized table, not single-cell).

Remaining: Subsidiary (core CST1 only, never resolved in sorghum single-cell data), Bulliform, Cork, Trichome/prickle (only CYP79A1, low), Stomatal_lineage, Sclerenchyma, Phloem_Sieve_Element (absent from nuclei), Phloem_Companion vs Phloem_Parenchyma split in data, Procambium, Ligule, Coleoptile, and mature-leaf (non-seedling) states. Mestome_Sheath is not expected (single Kranz sheath). No marker for any sorghum leaf type has reporter, in situ or spatial validation in sorghum.

## Recommended label reference

Swift et al. 2024 Multiome labels (already exported in `SwiftMultiomeReanalysis/SwiftCellTypes.tsv`): adopt Mesophyll, Bundle_Sheath, Guard and Xylem; keep Epidermis and Phloem as lineage-level labels to split in Part B; keep `unknown` unassigned. Caveat: seedling shoots under de-etiolation, so states may differ from mature leaves. Check the v3.1 -> v5.1 ID mapping before using markers on v5.1 data (all 39 names exist in v5.1).

## Conflicts

- **Gene-ID error in the paper:** Supp Table 1 and the Script 26 dotplot use Sobic.003G002600 as "NADPME", but UniProt A0A1W0VV80 lists it as a MYB-domain protein. The C4 NADP-ME is Sobic.003G036200 (UniProt C5XM00), which the paper itself uses in Supp Table 9 and Script 31. The draft uses Sobic.003G036200; Sobic.003G002600 is not included.
- **ABCG18** (paper phloem marker Sobic.007G054500) is in no DE list; not carried forward.
- **SUT1 placement:** Swift's phloem label merges types, so the draft has SUT1 as `Phloem`; the core table has it as `Phloem_Companion`. Same ID, consistent biology.
- **SWEET:** Swift Sobic.004G136600 (phloem, also BS cluster 4) is not core SWEET13 Sobic.008G094400. Compare by ID, not by symbol.

## Could not verify

- RNA-atlas per-cell labels and counts: only in the 2.5 GB GEO RData (not downloaded); the labelled object from Script 26 was not deposited.
- ED Fig 2h/4 images were not inspected; the review used the text, legends and supplementary tables.
- v3.1 -> v5.1 mapping: name presence only (the Phytozome synonym table needs a login).
- Functional names for six genes that are uncharacterized in UniProt (DiT2-like, MYB36-like, HDG11-like, HDG2-like, SUT1, FT-like) come from the paper's best-hit annotation only.
