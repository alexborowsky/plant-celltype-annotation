<!-- Collated from the survey review of arabidopsis_seedling (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis seedling: collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill from the one dataset review in this group (`Lee2025/`, whose own README is left as it was). This is a draft. The skill itself was not edited.

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 29 expected types/states, written from the anatomy of a whole light-grown Col-0 seedling at 3-12 d: cotyledons, first true leaves (12 d), SAM, hypocotyl, primary and lateral roots, and the etiolated apical hook. `function_markers` = the union of `function` rows for that name in `markers_draft.tsv`, `arabidopsis_leaf.tsv` and `arabidopsis_root.tsv`, after filtering for the Arabidopsis traits (eudicot, Brassicaceae, C3). The split by table is in `notes`. |
| `markers_draft.tsv` | 58 rows, 57 genes (GL2 appears twice: Trichome and Atrichoblast), 15 cell types/states. Skill schema plus `alt_id`, which holds the UniProt accession (as in the shoot-apex draft). `tissue` = `seedling` (`any` for the cell-cycle states). The skill README lists only `leaf`/`root`/`any`; the organ is given in `basis`. Every row has 13 fields (checked with awk). |
| `Lee2025/` | Dataset review, supplementary tables, per-cell portal labels, UniProt ID checks |

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Lee2025 (seedling part) | Lee TA, Illouz-Eliaz N, Nobori T, Xu J, Jow B, Nery JR, Ecker JR. A single-cell, spatial transcriptomic atlas of the Arabidopsis life cycle. *Nat Plants* 11:1960-1975 (2025), doi:10.1038/s41477-025-02072-z. GEO GSE226097; PMC12416547 | snRNA-seq, 10x Chromium X 3', Cell Ranger 7 with introns, TAIR10/Araport11 AGI IDs. MERFISH (1,000 genes) on **etiolated** 3-d seedlings and hook only | 3 d about 13,382; 6 d 41,314; 12 d 115,967; merged 167,430 nuclei | `table`: per-cell labels for 6 d, 12 d and merged from the public CELLxGENE portal (`Lee2025/seedling_*_labels_from_portal.tsv`); cluster→type table in Supp Table 2. 3 d labels only in a 1.3 GB rds / 560 MB h5ad; hook only in a 707 MB rds | medium. Large and well replicated, no batch-driven clusters, unknowns left unlabeled, curated literature marker list (S1), MERFISH for mesophyll, epidermis, vasculature, dividing and hook-cortex markers. Weaknesses: coarse labels, several wrong (see the matrix), most root and ground tissues unlabeled, 12 d is 55% Unknown, spatial data from etiolated seedlings while the snRNA samples were light-grown |

Only one seedling dataset was reviewed for this group. Cross-study agreement therefore comes from the independent Arabidopsis studies reviewed in the sibling groups (`arabidopsis_root`: Shahan 2022, Nobori 2023 PHYTOMap, Lyu 2025; `arabidopsis_leaf`: Kim 2021, Tenorio Berrio 2025, Nobori 2025; `arabidopsis_shoot_apex`: Zhang 2021, Xu 2025). The `Lee2025` entries in the root, leaf, stem and seed groups are the same atlas and were **not** counted as independent.

## Verdict matrix (canonical type × Lee 2025 time point)

Verdicts are from the `Lee2025/` review, plus my own reading of the Supp Table 2 DE sheets (marked "collation"). `-` = no such cluster.

| Canonical type | 3 d | 6 d | 12 d | merged |
|---|---|---|---|---|
| Mesophyll | c0, c3: Adopt | c3: Adopt; c1: Revise (weak, low-complexity); c12: Revise (S-phase state) | c1, c7: Adopt | c4: Adopt; c3: Revise |
| Epidermis (shoot) | c8 hypocotyl: Adopt; c6: Revise (organ unclear) | c0: Adopt | - | c1: Adopt |
| "Abaxial epidermal" | - | c2: **Reject** (root epidermis: thalianol cluster, NIP5;1) | c2: **Reject** (no specific markers) | - |
| Trichome | c15 (text only): **Reject** (cotyledons lack trichomes at 3 d; elongating ground tissue) | c16 "Epidermal": Revise → Trichome (+ epidermis) | c12: Revise → Trichome; c18: Revise (root/hypocotyl elongating tissue) | c9: Revise → Trichome |
| Trichoblast | c17: Adopt; c5 (Unknown) also trichoblast | c10, c15 "Trichome/trichoblast": Revise → Trichoblast | c3: Adopt; c15 "Xylem": **Reject** → Trichoblast (root hair) | c5, c6, c14: Adopt |
| Atrichoblast | - | - | c8 (Unknown): candidate (GL2 0.32/0.04, MYB23), unverified (collation) | - |
| Guard (+ Myrosin_Idioblast) | - | c19: Adopt (0.2%; TGG2 shows myrosin cells co-cluster) | c11: Adopt | - |
| Phloem_Companion | c13: Adopt | c6: Adopt | c10 (Unknown): partly (SUC2, AHA3) | c12 mixed |
| "Phloem parenchyma" → Pericycle / xylem-loading stele | c9: Revise | c7: Revise (PHO1, NPF7.3, HMA4) | - | - |
| Xylem | c12: Revise → differentiating xylem | c11: Adopt | - | - |
| Endodermis | c14 (Unknown): missed (CASP1/2/3/5, UCC1, MYB36); c11: Revise → suberizing endodermis (inferred) | c17: Adopt; c9 (Unknown): suberin/cuticle program (LCR, FAR4/5, KCS2), endodermis or periderm (collation) | c13 (Unknown): suberized endodermis (HORST, ASFT, CASPL1B1) | - |
| Cortex / elongating ground tissue | c15, c7 | c18 "Vascular": Revise (GAST1, EXT1, XTH17/18, DREB26) | c14, c18 (XTH17/18/19, AGPs, DREB26) | c10 |
| Dividing_cells (G2/M) | c10: Revise (state) | c4: Revise (state) | - | - |
| S_Phase / ribosome-rich | c16 "Dividing": Revise | c12 "Mesophyll": Revise | - | c15 "Vascular": **Reject** as a type |
| Stress states | - | c13 (iron deficiency): Unknown, correct | c17 (heat shock): correct | c13 (heat shock): correct |
| Apical_Hook_Cortex (etiolated) | hook dataset only: Adopt as states | - | - | - |
| Cortex, Pericycle, Columella, LRC, QC, SAM | not labeled | not labeled | not labeled | not labeled |

## Cross-study markers

25 rows have support from at least one independent single-cell or spatial study besides Lee 2025 (or, for Atrichoblast GL2 and Myrosin_Idioblast TGG2, from two independent studies). Agreement raised `confidence` one level where the single-study grade was below `high`: CA1, PDF1, AT1G04800, GH9C1, AHA3, PP2-A1. PRP3 was raised for an independent root-hair promoter study plus Lee cluster specificity.

- **Mesophyll:** CA1 (AT3G01500), with Nobori 2025.
- **Epidermis:** ATML1 (AT4G21750; Zhang 2021 reporter), FDH (AT2G26250; Nobori 2025, Zhang 2021), PDF1 (AT2G42840; Tenorio Berrio 2025 reporter, Xu/Zhang).
- **Guard:** FAMA (AT3G24140; Zhang 2021), TGG1 (AT5G26000; Tenorio Berrio 2025), AT1G04800 (Tenorio Berrio 2025 reporter + Lee Table S3).
- **Myrosin_Idioblast:** TGG2 (AT5G25980; reporters in Tenorio Berrio 2025 and Lyu 2025; in the Lee guard cluster).
- **Trichoblast:** COBL9 (AT5G49270), LRL3 (AT5G58010; PHYTOMap), RHD6 (AT1G66470), GH9C1 (AT1G48930), all with Shahan 2022.
- **Atrichoblast:** GL2 (AT1G79840; Shahan 2022, Nobori 2023).
- **Endodermis:** CASP2 (AT3G11550), MYB36 (AT5G57620; Shahan reporter, PHYTOMap).
- **Pericycle / xylem loading:** PHO1 (AT3G23430; Zhang 2021 xylem-parenchyma cluster).
- **Xylem / Procambium:** CESA8 (AT4G18780), MYB46 (AT5G12870), ACL5 (AT5G19530; Lyu 2025 reporter), ATHB8 (AT4G32880; Kim 2021).
- **Phloem_Companion:** SUC2 (AT1G22710), NaKR1 (AT5G02600), AHA3 (AT5G57350), PP2-A1 (AT4G19840).
- **Dividing_cells:** HIK (AT1G18370; Tenorio Berrio 2025).

## Gaps

These expected types have no `function` marker in the draft or the skill's Arabidopsis tables, or no seedling cluster:

- **Mesophyll:** no `function` row anywhere (CA1/PSRP2/NdhS/RBCS are enrichment markers). Palisade vs spongy not resolved.
- **Cortex** (root and hypocotyl): no marker; Lee 2025 did not label cortex. Candidate clusters (3d c15, 6d c18, 12d c14/c18) carry growth genes (XTH17/18/19, EXT1, AGPs), not cortex identity genes.
- **Bundle_Sheath, Hydathode, Columella, Shoot_Meristem, Lateral_Organ_Primordium:** none (SAM genes exist only in the shoot-apex draft).
- **Root tip types** (QC, LRC, columella, stem cell niche): markers exist in `arabidopsis_root.tsv` (WOX5, SMB, PLT1) but none is DE in any seedling cluster; expect no such clusters in whole-seedling nuclei.
- **Atrichoblast:** only GL2 (shared with trichome) and WRKY44 (here in the trichome cluster). Not resolved in Lee 2025.
- **Stomatal_lineage, Phloem_Parenchyma, Sieve_Element, Phloem:** markers in the skill tables (SPCH, MUTE, SWEET11/12, SEOR1, APL), but none is cluster-specific in the seedling DE sheets.
- **Apical_Hook_Cortex:** state markers only (IAA32, GH3.3), etiolated seedlings only, `low`.

## Recommended label reference

Lee 2025 is the only seedling reference. Use its per-cell portal labels (`Lee2025/seedling_6d_labels_from_portal.tsv`, `..._12d_...`, `..._merge_...`) as cluster priors only for the adopted types: mesophyll, shoot epidermis, guard (contains myrosin idioblasts), companion cells, 6 d xylem, trichoblast (add 12d c15 "Xylem" and 6d c10/c15), and 6 d endodermis. Re-label 6d c16/12d c12/merged c9 as Trichome, and 6d c7 as pericycle/xylem-loading stele. Re-annotate root ground tissue, root epidermis and the unlabeled clusters from scratch with `markers_draft.tsv` plus `arabidopsis_root.tsv`. For root-specific benchmarking, Shahan 2022 (arabidopsis_root group) is the better label reference.

## Conflicts and corrections

- **CESA4 accession:** the review's ID check gives A0A068FIL6 (unreviewed TrEMBL). The Swiss-Prot entry is Q84JA6 (CESA4/IRX5, AT5G44030); the draft uses that.
- **RSL4 (AT1G27740):** the UniProt protein name for Q8LEG1 reads "Transcription factor RSL3", but its gene names are RSL4/BHLH54 and the locus is correct.
- **Guard cluster includes myrosin cells:** the review lists TGG1 and "BGLU37" as guard markers. BGLU37 is TGG2 (AT5G25980), a myrosin-idioblast marker by reporter in two independent studies; FAMA is also expressed in myrosin cells (Lyu 2025). So 6d c19/12d c11 = guard + myrosin idioblasts. TGG1 is kept as Guard `medium`.
- **GL2 / TTG2 / MYB23 are shared trichome and atrichoblast genes.** The review lists GL2 as "Trichome / root atrichoblast"; the draft splits it into two rows. TTG2 (WRKY44) is Atrichoblast in `arabidopsis_root.tsv` but sits in the seedling trichome cluster; MYB23 is also a root non-hair gene (Kang et al. 2009). Separate shoot and root clusters before using them.
- **XTH17 (AT1G65310):** `arabidopsis_root.tsv` lists it for Atrichoblast (`low`). In the seedling it is top-specific to 3d c15, 6d c18 and 12d c18 (0.71/0.01), the elongating root/hypocotyl clusters with XTH18/19 and AGPs. Not added; treat it as a growth-zone gene, not an atrichoblast marker.
- **NdhS (AT4G23890):** MERFISH cotyledon mesophyll (Fig 2a), but Lee Table S3 lists it as a stem cortex marker. Kept `low`.
- **GH9B8 (AT2G32990):** hook epidermis by MERFISH, but Lee S1 lists it as root metaphloem, and it is not DE in the light-grown snRNA. Kept `low`.
- **PHO1 naming:** the shoot-apex draft puts PHO1 under `Xylem_Parenchyma`; this draft uses `Pericycle` (the name in `arabidopsis_root.tsv`), because the seedling cluster is root stele (PHO1, NPF7.3, HMA4). Reconcile before merging the drafts.
- **3 d DE sheet:** avg_log2FC values in `Seedling_3d` are implausible (e.g. 245 for RBCS1A), so only pct.1/pct.2 were used from that sheet. In all DE sheets, IDs carry Seurat `make.unique` digits; the first 9 characters were used.
- **Additional unlabeled clusters (collation, inferred from DE only):** 12d c13 = suberized endodermis (HORST, ASFT, CASPL1B1, FAR5); 6d c9, 6d c14 and 12d c16 = suberin/cuticle programs (FAR1/4/5, KCS2, LCR), endodermis or hypocotyl/periderm, unresolved; 12d c8 = possible atrichoblast.

## Not verified

- No second seedling dataset was reviewed, so no seedling-specific cross-study comparison exists.
- 3-d per-cell labels and the hook object (CELLxGENE 3-d view returned a server error; the rds/h5ad objects are 0.56-1.3 GB and were not downloaded). Whether those objects carry a cell-type column is unconfirmed.
- Lee Supp Tables 5/6 (pseudobulk, 27/91 MB) and the GitHub code repo (404).
- Literature citations in `basis` for characterized genes (e.g. Roppolo 2011, Lee 2013, Reyt 2020, Hofer 2008, Lin 2008, Yi 2010) are the standard references for those genes and were not re-read here; specificity values are from the Lee Supp Table 2 DE sheets.
- AT2G12462 and AT1G04800 have only unreviewed UniProt entries (F4ITC9, Q9MAS9).

## Overlap with existing skill tables

- `arabidopsis_leaf.tsv`: 14 (gene, type) pairs shared: CA1, ATML1, FDH, PDF1, CER5, FAMA, GL1, GL2 (Trichome), IRX3, XCP1, XCP2, ATHB8, SUC2, H3.1. The draft raises PDF1 to `high` (leaf table: `medium`).
- `arabidopsis_root.tsv`: 10 shared: COBL9, EXPA7, GH9C1, GL2 (Atrichoblast), CASP1-3, MYB36, PER64, MYB46. The draft raises GH9C1 to `high` (root table: `medium`). TTG2/WRKY44 is Atrichoblast there and Trichome here.
- New relative to both tables: 33 genes, mainly the trichome set (MYB23, MYB106, TTG2), trichoblast TFs (LRL3, RSL2, RSL4, RHD6) and PRP3/PER73, CASP5/UCC1/HORST, PHO1/NPF7.3, CESA4/CESA8/ACL5, companion-cell NaKR1/AHA3/PP2-A1, myrosin TGG2, guard TGG1/AT1G04800, the Lee MERFISH genes (PSRP2, NdhS, AT2G12462, EXPA5, GH9B8), cell-cycle HIK/CDC20.1/CSLD5/TOP2, and hook-state IAA32/GH3.3.
