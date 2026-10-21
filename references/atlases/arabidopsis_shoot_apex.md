<!-- Collated from the survey review of arabidopsis_shoot_apex (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis shoot apex: collated cell-type marker resources

Collated 2026-10-20 from the two dataset reviews in this folder (`Zhang2021/`, `Xu2025/`; their own READMEs are left as they were) for the plant-celltype-annotation skill. This is a draft. The skill itself was not edited.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 28 expected types/states, written from the anatomy of the vegetative SAM plus young leaves and hypocotyl top, and of the inflorescence apex. `function_markers` = the union of `function` rows in `markers_draft.tsv` and `arabidopsis_leaf.tsv` for that name (the split is in `notes`). |
| `markers_draft.tsv` | 82 rows, 82 genes, 19 cell types/states. Skill schema plus `alt_id`, which holds the UniProt accession. `tissue` = `shoot_apex` (`any` for the cell-cycle states). Every row has 13 fields (checked with awk). |
| `Zhang2021/`, `Xu2025/` | Per-dataset reviews, supplementary tables, and the UniProt ID checks |

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Zhang2021 | Zhang TQ, Chen Y, Wang JW. *Dev Cell* 56:1056 (2021), doi:10.1016/j.devcel.2021.02.021. CNCB GSA CRA002977; EBI SCEA E-CURD-83 | Protoplast scRNA-seq, 10x 3' (v2: shoot1 and leaf3; v3: shoot4). Col vegetative apex at 7 and 14 d, **plus a third-leaf sample** | 36,643 cells; 23 clusters, 9 populations | `cluster_only`: the cluster→population map is in Fig S2, and there are no per-cell labels. The SCEA object (2.04 GB) has only SCEA clusterings | medium. It has a curated, referenced marker list, about 20 in situ probes and 5 promoter reporters, and it recovers SE, CC, SEn, GC and stomatal-lineage cells. Weaknesses: the VC label merges 4 identities, and SMC cluster 1 is a glucosinolate program |
| Xu2025 | Xu X ... Jackson D. *Dev Cell* (2025), doi:10.1016/j.devcel.2025.07.024. SRA PRJNA1039492/PRJNA1039493 | Protoplast scRNA-seq, 10x 3' v3. *ap1;cal* (Col) inflorescence apex, 2 reps | 20,482 cells; 18 clusters | `table`: Table S1 has a barcode→cluster table; the names come from Fig 1F (`Xu2025/labels.tsv`) | medium. It recovers CLV3+ and WUS+ cells, and the replicates are balanced. Weaknesses: both "OC" clusters are heat-shock/starvation states, the "rib zone" is photosynthetic, "trichome" is epidermis, and there is no in situ of cluster identity |

The two datasets are from independent labs, genotypes and apex types (vegetative wild type vs. *ap1;cal* inflorescence). Both use TAIR10 AGI IDs, so no ID conversion was needed.

## Verdict matrix (canonical type × dataset)

Verdicts are from the dataset reviews. `-` = no such cluster.

| Canonical type | Zhang2021 (cluster: verdict) | Xu2025 (cluster: verdict) |
|---|---|---|
| SAM_Central_Zone | - (not resolved) | inside c2/c3 (CLV3+ cells; no cluster) |
| Organizing_Center | - | c1, c10 "OC": **Reject** (heat-shock / starvation states, WUS not DE) |
| Shoot_Meristem (CZ+PZ, inner) | c13 SMC: Adopt (mixed with boundary); c1 SMC: Revise (glucosinolate) | c2: Adopt |
| Organ_Boundary | inside c13 (LSH3, KNAT6) | - |
| Lateral_Organ_Primordium | - | c0: Revise (weak FIL) |
| Epidermis (L1 / protoderm) | c2: Adopt; c14: Revise (JA/defense) | c3 (meristem L1): Adopt; c8 (organ epidermis): Adopt; c4 "Trichome": Revise → Epidermis |
| Stomatal_lineage | c18: Revise (co-driven by G2/M); part of c12 | - |
| Guard | c11: Adopt (heat-shock co-signature) | - |
| Trichome | - | c4 label rejected as trichome |
| Mesophyll | c0, c4: Adopt; c3: Revise (stress); c16: Revise (S phase) | c6 "Rib zone": Revise → Mesophyll/chlorenchyma |
| Bundle_Sheath (shoot endodermis) | c20 SEn: Adopt | - |
| Cortex | - | c7, c9 "Cortex": Revise (stress/defense; marker AT1G62510 not DE) |
| Procambium / Xylem | c10: Revise → xylem precursor/procambium | c5 "Xylem": Revise (weak TMO5/TED4 support; see corrections) |
| Xylem_Parenchyma | c6: Revise | - |
| Phloem (early / phloem pole) | c7: Revise | c12: Adopt (low) |
| Phloem_Companion | c15: Adopt | c16: Adopt |
| Sieve_Element | c22: Revise (label VC → SE) | c17: Adopt |
| Dividing_cells / S_Phase (states) | c5, c9, c17, c19 PC; c12, c16, c18 co-driven | c11, c13 (S), c14, c15 (G2/M) |
| Stress states | c8: Reject (undefined) | c1, c10 (and partly c7, c9) |
| Unknown | c21 (LTP cluster; hydathode?) | - |

## Cross-study markers

43 genes are cluster-specific in **both** atlases for the same type. Most are also validated by in situ or reporter in Zhang 2021 or the literature. Agreement raised `confidence` one level, as in `literature_search.md`. The pct.1/pct.2 values are in `basis`.

- **Shoot_Meristem / SAM_Peripheral_Zone:** STM (AT1G62360); CYP78A5 (AT1G13710).
- **Epidermis:** ATML1 (AT4G21750), PDF2 (AT4G04890), PDF1 (AT2G42840), FDH (AT2G26250), DCR (AT5G23940), LTPG1 (AT1G27950), LTP6 (AT3G08770), HDG2 (AT1G05230).
- **Xylem:** TMO5 (AT3G25710), TED4 (AT3G18280).
- **Phloem:** bZIP9 (AT5G24800), TMO6 (AT5G60200), CLE25 (AT3G28455), SMXL5 (AT5G57130), AT4G39190, APL (AT1G79430).
- **Phloem_Companion:** SUC2 (AT1G22710), AHA3 (AT5G57350), FTIP1 (AT5G06850), PP2-A1 (AT4G19840), NAKR1 (AT5G02600), AAP4 (AT5G63850).
- **Sieve_Element:** SEOR1 (AT3G01680), SEOR2 (AT3G01670), CALS7 (AT1G06490), ENODL9 (AT3G20570), AT1G63310, GATA20 (AT2G18380), DOF6 (AT3G45610), DOF5.6 (AT5G62940).
  - AT1G63310 is the most specific SE gene in both atlases (0.98/0.01 and 0.97/0.00).
- **Dividing_cells (state):** KNOLLE, CDKB2;1, CYCB1;1, SCL28 (AT1G63100), ENODL13 (AT5G25090), IMK2 (AT3G51740), AT5G56120.
- **S_Phase (state):** H3.1 (AT5G10400), HIS4 (AT2G28740), HTA6 (AT5G59870), HTB1 (AT1G07790).

The single-study rows stay at the grade their evidence alone supports: guard cells, the stomatal lineage, Bundle_Sheath, xylem parenchyma, ACL5/PXY/ATHB8, CLV3/WUS/LOG7/PAN, and the meristem in situ genes.

## Gaps

These expected types have no `function` marker in the draft or in `arabidopsis_leaf.tsv`:

- **SAM_Peripheral_Zone:** CYP78A5 only (characterized_enriched). Neither atlas splits the PZ from the CZ.
- **Rib_Meristem, Pith:** no marker. Xu's "rib zone" is not rib meristem.
- **Floral_Meristem:** not relevant to the vegetative apex. In *ap1;cal*, the AP1 and CAL markers are mutant.
- **Cortex (hypocotyl/stem):** no marker. AT1G62510, Xu's cortex marker, is an `expression` row in `arabidopsis_root.tsv`, and in Xu it is DE in c6, not in c7/c9.
- **Hydathode, Myrosin_Idioblast:** no marker. Zhang c21 is unassigned (a hydathode candidate, unverified).
- **Protoplasting_stress:** state, not captured in this table.
- **Thin coverage (1 function marker):** SAM_Central_Zone (CLV3), Organizing_Center (WUS), Organ_Boundary (CUC3), Mesophyll (EPFL9), Xylem_Parenchyma (PHO1).
  - CLV3 and WUS are not cluster DE genes in either atlas, because these cells are too rare. Find them by expression, not by cluster.
- **Trichome, Phloem_Parenchyma:** covered only by `arabidopsis_leaf.tsv` (GL1/GL2, SWEET11/12). Neither atlas has a trichome or a separate phloem-parenchyma cluster.

## Recommended label reference

- **Markers: Zhang2021.**
  - Its curated Table S2 list has references, and its in situ and reporter validations cover the vascular sub-types, the stomatal lineage, guard cells and the shoot endodermis.
  - It matches a wild-type vegetative apex.
  - Remove its leaf3 sample, or treat it separately, when comparing to apex-only data.
  - Its labels are cluster-only, so reuse means re-clustering E-CURD-83 or the raw reads.
- **Per-cell labels: Xu2025, clusters 2, 3, 8, 12, 16 and 17 only.**
  - Use these for an inflorescence-apex benchmark (inner meristem, L1, organ epidermis, early phloem, CC, SE).
  - Treat 11/13/14/15 as states.
  - Do not reuse the OC, rib zone, cortex, trichome or xylem labels.
  - Allow for the *ap1;cal* background.
- **Rare types:** neither dataset has validated CZ/OC clusters. Use CLV3/WUS expression plus STM for those.

## Conflicts and corrections to the reviews

1. **H3.1 locus.** Three IDs are in use for H3.1, and all three encode the same H3.1 protein (UniProt P59226). All three are DE in the S-phase clusters of both atlases, and reads can multimap among them.
   - The Xu review used AT5G10390 (HTR13).
   - The Zhang in situ probe is AT5G10400 (HTR9).
   - `arabidopsis_leaf.tsv` uses AT5G65360 (HTR1).

   The draft uses AT5G10400, the gene probed by in situ.
2. **AT5G59870.** Zhang names it "H2A6". UniProt lists it as "Probable histone H2A.7 (HTA6)", and Zhang's own Table S1 calls it h2a.w.6. Same gene; the symbol in the draft is HTA6/H2A.W.6.
3. **Xu c5 "Xylem".** The Xu review said there are no supporting DE genes. That is too strong: TMO5 (AT3G25710, 0.25/0.07), TED4 (AT3G18280, 0.29/0.02) and AT5G46730 (Zhang in situ) are DE in c5. TMO5-LIKE1 (AT1G68810) is indeed not DE. Weak xylem-precursor support; the verdict stays Revise.
4. **Xu c6 "Rib zone".** KNAT1/BP is DE in c6 (0.29/0.10) and not in the meristem clusters. BP is expressed in the inflorescence-stem cortex. Together with the photosynthesis genes and EPFL9, this supports stem cortex/chlorenchyma rather than rib meristem.
5. **AT5G57785.** Zhang's SAM in situ gene is also DE in Zhang epidermal and leaf clusters (c2, c4, c14) and in Xu epidermal c4. Graded `low`; use only with STM.
6. **ANT.** The Xu in situ (Fig 2C) is labelled CHO1/EMK/AIL5, but the Table S5 probe is ANT (AT4G37750); this is from the Xu review. In Zhang, ANT is DE only in the G2 procambium cluster c19.
7. **Gene in more than one cluster.**
   - LSH3: DE in Zhang c13, but only weakly in Xu lateral-organ c0.
   - NAKR1: CC in both atlases, but also DE in the Xu stress cluster c10.
   - AAP4: CC in both atlases, also Zhang c6.
8. **SEn naming.** Zhang's "shoot endodermis" is filed as `Bundle_Sheath`, to match `arabidopsis_leaf.tsv`.
   - The `basis` lines say when a gene is more a stem starch-sheath/gravitropism gene (LAZY1, SGR6).
   - Shoot endodermis has no Casparian strip, so do not use the root `Endodermis` CASP rows for it.
9. **Overlap with the skill tables.**
   - The draft shares 11 genes with `arabidopsis_leaf.tsv`: ATML1, PDF1, FDH, SPCH, FAMA, ATHB8, APL, SUC2, SEOR1, KNOLLE and CYCB1;1.
     - The cell-type names agree.
     - PDF1 and SEOR1 are raised to `high` here, from cross-study agreement.
     - The leaf table's SEOR1 lacks the `eudicot` tag that the draft adds (the SEO family is eudicot-specific).
   - It shares 2 genes with `arabidopsis_root.tsv`: APL, and DOF5.6. The root table lists DOF5.6 as `Phloem`; it is `Sieve_Element` here.
   - New cell-type names, not in any skill table: SAM_Central_Zone, Organizing_Center, SAM_Peripheral_Zone, Shoot_Meristem, Organ_Boundary, Lateral_Organ_Primordium, Xylem_Parenchyma.
10. **Excluded on purpose.**
    - Ribosomal RPS14C (AT3G52580) and RPL29B (AT3G06680): Xu in situs, but these are housekeeping/growth genes.
    - MCM2-7: S-phase genes that Xu presented as "conserved meristem markers".
    - Zhang SMC c1 glucosinolate genes.
    - Heat-shock and stress genes.
11. **Trait tags.**
    - `requires=eudicot` on SEOR1, SEOR2 and SUC2 (clade-specific).
    - Also on POLAR and BASL (no grass orthologs known).
    - Also on FIL and YAB3, where abaxial YABBY expression is not conserved in grasses.

## Not verified

- **Zhang 2021 images.** Main Figs 1-8 were behind Cloudflare/403 and were not circumvented. The in situ and reporter images were not viewed for most genes; only the AT1G13650 reporter image was seen. The in situ results are taken from the primer table (Table S2: purpose and figure panel). Rows that rest on an unseen image say "image not inspected".
- **Zhang SEn vs. bundle sheath.** The paper's exact SEn/bundle-sheath definition and the STAR Methods were not read.
- **Xu supplements.** The PMC supplements (bot check), bioRxiv (429) and the ShinyCell portal (403) were not accessed. Table S4 (138 MB) was not downloaded.
- **Literature citations.** The citations in `basis` were written from the reviews and from knowledge of the literature. They were not re-fetched; check them before moving rows into the skill.
  - This applies especially to SGR6 (no year given), TED4 (characterization), SCL28 and IMK2 (only Zhang's in situ is cited).
- **Gene IDs.** Every `ref_gene` was checked against UniProt and against at least one paper table: Zhang Table S1/S2 or Xu Table S1/S2.
  - Unreviewed UniProt entries: AT1G13650, AT5G57785, AT5G61660, AT5G46730, AT4G39190, AT5G56120.
  - AT3G28420 was checked but is not used in the draft.
- **Wording of pct values.** The pct.1/pct.2 values in `basis` come straight from the two Table S1 DE sheets (Seurat FindAllMarkers; Zhang uses natural-log avg_logFC, Xu uses log2). They show enrichment, not validated specificity.
