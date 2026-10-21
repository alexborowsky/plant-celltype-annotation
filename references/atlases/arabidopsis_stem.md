<!-- Collated from the survey review of arabidopsis_stem (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# arabidopsis_stem: collated cell-type marker resources

Collation done 2026-10-20 for the plant-celltype-annotation skill. It draws on the one dataset review
in this group (`Lee2025/`, done 2026-10-19), a full-text check of one unreviewed stem-relevant
paper (`MorenoRamirez2026_unreviewed/`), UniProt look-ups, and the sibling `arabidopsis_*`
collations, which were used to find independent studies that agree on a marker. No expression data
were re-analysed.

Files in this folder:

| File | What it is |
|---|---|
| `expected_cell_types.tsv` | Cell types expected from inflorescence-stem anatomy (base to apex, nuclei). `function_markers` counts the `function` rows in `markers_draft.tsv`; the notes add the counts from the skill's `arabidopsis_leaf.tsv`/`arabidopsis_root.tsv` |
| `markers_draft.tsv` | 84 rows (83 genes) after the 2026-10-20 update (53 before), skill schema + `alt_id` (UniProt accession). `tissue` = `stem` |
| `build_markers_draft.py` | Writes and validates the Lee 2025 based 53 rows (rows are hand-curated in the script) |
| `update_markers_shi2021.py` | Re-runs `build_markers_draft.py`, then merges the Shi 2021 review (edits 34 rows by gene ID, adds 31). Run this one to regenerate the table |
| `Shi2021/` | Dataset review of Shi et al. 2021 (FANS + LCM stem tissue profiles; README, supplementary tables, figures, UniProt check) |
| `Lee2025/` | Dataset review (its own README, supplementary extracts, portal labels, UniProt check) |
| `MorenoRamirez2026_unreviewed/PMC13281799.xml` | Full text of Moreno-Ramirez et al. 2026 Sci Adv (Europe PMC, open access), read for stem reporter genes only |

## Datasets

| Dataset | Platform | Cells | Label access | Quality | Notes |
|---|---|---|---|---|---|
| Lee TA ... Ecker JR 2025 *Nat Plants* 11:1960 (10.1038/s41477-025-02072-z), stem part; GEO GSE226097 (GSM7063702-14) | 10x 3' HT v3.1 snRNA-seq (part CellPlex by region) + MERFISH (1,000 genes, one stem apex section) | 17,114 nuclei, 16 clusters; median 913 UMI | `table`: per-cell labels from the public CELLxGENE portal API, saved as `Lee2025/stem_labels_from_portal.tsv`; full objects 687 MB h5ad / 1.6 GB rds not downloaded | low for labels; medium as a marker source (MERFISH) | 3 of 16 clusters adoptable (10.6% of nuclei); 60% of nuclei in single-library clusters; no run/region column |
| Moreno-Ramirez S ... Jonsson H 2026 *Sci Adv* (10.1126/sciadv.aee2988), PMC13281799; SRA PRJNA1438735 | 10x 3' v3 snRNA-seq of dissected inflorescence meristems (top 200-300 um, including the youngest primary stem) | 10,025 nuclei, 3 replicates | not checked (code/objects at gitlab.developers.cam.ac.uk/slcu/teamhj/publications/Moreno-Ramirez_etal_2026) | **not reviewed** (survey lists it under `arabidopsis_inflorescence`) | Reporter lines for stem cortex (AED3, JKD, C/VIF2), procambium (ATHB8, PFA3/PFA5), stem epidermis (MLP28). Used here only for AED3, JKD, ATHB8 and PXY rows |

No second Arabidopsis inflorescence-stem single-cell dataset with stem cell-type labels was found
(Europe PMC query: arabidopsis AND ("inflorescence stem" OR hypocotyl) AND single-cell/nucleus AND
cambium/xylem; 365 hits screened by title). The Greb-lab stem tissue profiles (Shi et al. 2021) are
FACS-sorted bulk, not single-cell; they were reviewed later (see "Update 2026-10-20: gap-fill reviews" below).

## Verdict matrix (cell type x dataset)

Lee 2025 verdicts are from the review (Step 3a, cluster level). "-" = not present or not identifiable.

| Expected cell type | Lee 2025 stem (cluster, %, verdict) | Moreno-Ramirez 2026 (apex; unreviewed) |
|---|---|---|
| Epidermis (pavement) | c10, 3.3%, **Adopt** | stem epidermis cluster (MLP28 reporter) |
| Guard | c5 'Guard', 5.8%, **Revise** (guard + myrosin; no KAT1/SLAC1) | - |
| Trichome | c15 'Trichome', **Reject** (pollen) | - |
| Cortex | c6 'Unknown', 5.3%, **Revise** -> cortex chlorenchyma; MERFISH cortex domain | cortex cluster (AED3, JKD, C/VIF2 reporters) |
| Endodermis (starch sheath) | - | - |
| Interfascicular fiber | maybe inside c4 / c13 (**Revise**) | - |
| Pith | - (maybe in batch clusters c0/c1/c2, **Reject**) | rib zone (AED3) |
| Procambium / cambium | c11 'Cambium', 2.3%, **Revise** (root markers only); MERFISH 'procambium' domain | procambium cluster (ATHB8 reporter), cambium trajectory (PXY) |
| Xylem (differentiating vessels) | c8, 3.8%, **Adopt**; c3 'Xylem' **Reject**; c13 'Xylem' **Revise** | xylem trajectory (TMO5, ATHB8, ACL5) |
| Xylem parenchyma | - | 'xylem parenchyma' cluster (GH3.6, FAF1/3) |
| Phloem companion cells | c9, 3.5%, **Adopt** | phloem trajectory (CALS8, OBP2, PEAR2) |
| Sieve elements (developing) | inside c9 and c4 (**Revise**) | - |
| Phloem parenchyma | - | - |
| Myrosin idioblast | merged into c5 (**Revise**) | - |
| Mixed vascular | c4 'Vascular', 11.1%, **Revise** (secondary wall + developing phloem + TGG1) | - |
| Shoot meristem | - | CZ/OC cluster (CLV3, WUS) |
| Dividing cells | c7 'Unknown' (POK2), **Reject** as labelled | S and G2-M clusters |
| Contaminants | c14 'Phloem' = floral/ovule (**Reject**); c15 = pollen; c12 'Epidermal' = seed-coat flavonoid cells (**Revise**) | - |

## Recommended label reference

**Lee 2025, clusters 8 (Xylem), 9 (Phloem_Companion) and 10 (Epidermis) only**, imported from
`Lee2025/stem_labels_from_portal.tsv`. Everything else in that object must be re-derived: cortex
(c6) from the cortex markers, guard vs myrosin (c5) with KAT1/SLAC1 vs TGG2, and the
single-library clusters (c0, c1, c2, c3, c7, c13) only after the library suffixes `_1`-`_4` are
mapped to GEO runs and stem regions (needs the 1.6 GB rds). Drop or flag c14, c15 and c12 as
floral/seed contaminants. Use the MERFISH genes as stem markers rather than the cluster labels.
Moreno-Ramirez 2026 covers only the apex and has not been reviewed, so it is not a label reference.

## Markers (`markers_draft.tsv`)

53 rows, all `kind=type`: 29 `function`, 23 `characterized_enriched`, 1 `expression` (a pollen
flag). Confidence: 19 high, 19 medium, 15 low. Every AGI was checked in UniProt (accession in `alt_id`):
the Lee rows against `Lee2025/uniprot_id_check.tsv`, Supp. Table 3 and the DE sheet; the literature rows
by `gene:<AGI>` REST queries on 2026-10-20 (SCR, NST1, SND1, WOX4, PXY, SMXL5, JKD, AED3, TGG1,
SEOR1, NaKR1, ATHB8). DE percentages quoted in `basis` come from `Lee2025/stem_cluster_DE_SuppTable2.tsv`
(pct.1 vs pct.2). Literature DOIs were checked in Crossref.

Grading rules applied:
- Lee 2025 MERFISH genes count as in situ evidence. Genes shown in an Extended Data panel *and* DE
  in the matching adopted cluster are `characterized_enriched` medium (AT1G67870). Genes listed only
  in Supp. Table 3 or not DE are `characterized_enriched` low. MERFISH comes from one section (n = 1).
- Rows added from the literature for gaps (SCR, NST1, SND1, WOX4, PXY, SMXL5) are `function` medium:
  they have stem reporter or mutant evidence but no enrichment in the stem snRNA data.
- Contaminant flags (Pollen, Seed_Coat_Endothelium) are kept so that floral material in stem samples
  can be recognised.

### Cross-study agreement

Only one stem dataset exists, so no marker is supported by two *stem* single-cell studies. For
organ-independent cell types (vascular, epidermal, guard, myrosin), agreement with an independent
Arabidopsis study in another organ was counted, following the sibling collations. Lee 2025 rows in
other organs are the same atlas and do not count. **20 rows** have such agreement; confidence was
raised for 18 of them:

| Gene | Cell type | Lee 2025 stem | Independent study |
|---|---|---|---|
| SUC2 AT1G22710 | Phloem_Companion | c9 DE | Nobori 2025, Tenorio Berrio 2025, Zhang 2021 |
| AHA3 AT5G57350 | Phloem_Companion | MERFISH + c9 DE | Kim 2021, Tenorio Berrio 2025 |
| PP2-A1 AT4G19840 | Phloem_Companion | MERFISH + weak c9 DE | Tenorio Berrio 2025 (reporter), Kim 2021 |
| NaKR1 AT5G02600 | Phloem_Companion | weak c9 DE | Nobori 2025 |
| APL AT1G79430 | Phloem | MERFISH | Shahan 2022, Zhang 2021 |
| CALS7 AT1G06490 | Sieve_Element | c9 DE | Zhang 2021, root secondary-growth atlas 2025 |
| SEOR1 AT3G01680 | Sieve_Element | c4 DE | Zhang 2021, Tenorio Berrio 2025 |
| VND6 AT5G62380 | Xylem | c8 DE | root secondary-growth atlas 2025 |
| IRX3, IRX1, IRX5 (AT5G17420, AT4G18780, AT5G44030) | Xylem | MERFISH / c4 DE | Shahan 2022 |
| MYB46 AT5G12870 | Xylem | c8/c13 DE | Shahan 2022 |
| FDH AT2G26250 | Epidermis | weak c10 DE | Nobori 2025, Zhang 2021 |
| FAMA AT3G24140 | Guard | c5 DE | Kim 2021, Tenorio Berrio 2025 |
| TGG2 AT5G25980 | Myrosin_Idioblast | c5 DE (weak) | Tenorio Berrio 2025, Kim 2021 |
| ABCG29 AT3G16340 | Guard | c5 DE | Kim 2021 |
| BAN AT1G61720 | Seed_Coat_Endothelium (contaminant) | c12 DE | independent seed atlases |
| ATHB8 AT4G32880 | Procambium | not DE | Moreno-Ramirez 2026 (reporter) |
| ACL5 AT5G19530, ENODL9 AT3G20570 | Xylem, Sieve_Element | conflicting in stem | Shahan 2022/Zhang 2021; **not raised** (see conflicts) |

## Gaps (no validated `function` marker for the stem)

- **Cortex**: only MERFISH genes from one section (BBX15, AT1G64500, LHB1B1) and apex reporters
  (AED3, JKD). Lee 2025 never assigned a cortex cluster.
- **Pith**: no marker in any source.
- **Xylem parenchyma** and **phloem parenchyma**: no stem evidence. The skill's SWEET11/12 rows are
  leaf rows; SWEET11/12 are reported in stem xylem parenchyma (Le Hir et al. 2015 Plant Cell), but
  this was not verified here.
- **Phloem cap / phloem fibers**: no marker.
- **Trichome**: only the leaf GL1/GL2 rows; stem trichomes are sparse.
- **Endodermis (starch sheath)**, **interfascicular fibers**, **vascular cambium**: literature
  `function` rows only (SCR; NST1, SND1; WOX4). None is enriched in any stem snRNA cluster.
- Shoot meristem and dividing cells: covered by the `arabidopsis_shoot_apex` draft and the skill's
  state rows, not repeated here.

## Conflicts and corrections to the review

1. **ACL5 (AT5G19530)**: the review lists it as a xylem marker (weak DE c3). In the DE sheet it is
   more enriched in the companion-cell cluster c9 (0.85 vs 0.36) than in the 'Xylem' c3 it was used
   to call (0.53 vs 0.36). Kept as Xylem but at medium.
2. **ENODL9 (AT3G20570)**: the Ext. Data Fig. 4c legend spells it "ENDOL9"; the review's mapping to
   AT3G20570 is confirmed by its presence in the MERFISH panel. It is a known sieve-element gene
   (Khan 2007) and is placed here as Sieve_Element, against Lee's 'procambium' domain. The same
   domain holds AT5G22090, which is DE in the CC cluster c9. The stem MERFISH 'procambium' domain is
   probably cambium plus developing phloem, so its genes were downgraded to low.
3. **LAC17 (AT5G60020)**: the review says "DE c4", but pct is 0.43 vs 0.49 there (not enriched). The
   row rests on MERFISH and Berthet 2011.
4. **MYB46**: enrichment in c8 is weak (0.61 vs 0.53). FDH in c10 is weak too (0.85 vs 0.68), and
   PP2-A1 in c9 (0.31 vs 0.16).
5. **Evidence tiers changed from the review**: XCP1/XCP2 `characterized_enriched` -> `function`
   (matches the skill table); AHA3 `function` -> `characterized_enriched` (matches the sibling
   collations: CC-enriched H+-ATPase, also in SE); AT1G67870, bHLH112, PR-1-like, GLP10, AT1G03106,
   UMAMIT11, bHLH68, BBX15, AT1G64500 `expression` -> `characterized_enriched` (MERFISH counts as
   in situ), with low confidence except AT1G67870.
6. **bHLH68 (AT4G29100)** is a root pericycle marker in Shahan 2022 (arabidopsis_root draft).
   **ABCG29 (AT3G16340)** is listed for root endodermis in the Lee 2025 root review. Both conflicts
   are noted in `basis`.
7. **FAMA** is listed twice, as Guard (high) and Myrosin_Idioblast (medium, `requires=Brassicaceae`).
   Lee c5 likely mixes the two types.
8. Supp. Table 3 lists **AS2 (AT1G65620)** as a stem phloem gene and **AGL20/SOC1** and **ARK3** as
   cortex genes. These are developmental regulators with no known tissue restriction of that kind.
   Not carried.
9. The Lee 2025 stem review did not mention Moreno-Ramirez 2026, which has stem cortex and
   procambium reporters. It is in the survey's unreviewed list (assigned to `arabidopsis_inflorescence`).

## Overlap with the skill tables (`references/markers/arabidopsis_leaf.tsv`, `arabidopsis_root.tsv`)

11 genes (12 rows) are already in the skill: XCP1, XCP2, IRX3, ATHB8, APL, SUC2, SEOR1, FAMA (leaf
table, Guard), FDH (leaf), MYB46 and SCR (root table, root Endodermis). The cell types agree; the
draft adds stem-specific evidence in `basis`. New relative to the skill: Myrosin_Idioblast (FAMA,
TGG1, TGG2), Interfascicular_Fiber (NST1, SND1), Vascular_Cambium (WOX4), stem Cortex rows,
stem-MERFISH phloem/xylem genes, CALS7, VND6, and contaminant flags. The skill's root Endodermis
`function` rows (CASP1-4, MYB36, PER64) should **not** be applied to stem: the shoot endodermis has
no Casparian strip.

## Could not verify

- Library suffix -> GEO run/stem region mapping for Lee 2025 (needs the 1.6 GB rds or 687 MB h5ad;
  not downloaded).
- Stem MERFISH images and cell segmentation: Extended Data Fig. 4 was read from the legend only (no
  PDF/image rendering on this node), and the public MERFISH transcript table has no cells. So
  MERFISH specificity is as the authors report it.
- Moreno-Ramirez 2026: supplementary tables S1-S16 and the GitLab repository were not opened, so its
  cluster sizes, labels and per-cell metadata are unknown. Only reporter statements in the main text
  were used.
- Literature rows (SCR, NST1, SND1, WOX4, PXY, SMXL5, SWEET11/12 in stem) rely on the cited papers'
  reported expression. The papers were not re-read here; only their DOIs were checked in Crossref.
- Lee 2025 Supp. Tables 5-6 (pseudobulk, 27/91 MB) were not downloaded.

## Update 2026-10-20: gap-fill reviews

One new review was merged: `Shi2021/` (done 2026-10-20). The table is now regenerated by
`update_markers_shi2021.py`, which re-runs `build_markers_draft.py` and then edits rows by gene ID
and appends the new rows. The FANS and LCM values quoted for **existing** rows (marked "Shi 2021 Plant Cell
FANS (SDS5 ...)" in `basis`) were read here from Supplemental Data Set 5 (mean normalized counts per
population, 17 libraries) and Data Set 7 (LCM Wald tests). Values for the new rows come from the review's
`Shi2021/Shi2021_markers.tsv`.

### New dataset

| Dataset | Platform | Cells | Label access | Quality | Notes |
|---|---|---|---|---|---|
| Shi D ... Greb T 2021 *Plant Cell* 33:200 (10.1093/plcell/koaa019, PMC8136906; confirmed in Europe PMC); GEO GSE142034 | FANS of 7 promoter::H4-GFP nucleus populations (Smart-seq2, n = 2-3) + LCM of phloem cap, pith and bundle control (n = 2); second basal internode; TAIR10/Araport11 | no single cells; 10 populations | `population_level` (no per-cell labels; 219 MB RAW tar not downloaded) | medium (the review rates it medium-high as a marker source) | Only stem resource that separates starch sheath, epidermis, fibers, vessels, phloem, pith and phloem cap; 19 of 34 promoter reporters validated in stem sections |

### Verdicts (Shi 2021, population level)

| Population | Canonical name | Verdict | Main reason |
|---|---|---|---|
| NST3pro nuclei | Interfascicular_Fiber (+ xylem fibers) | Revise | merges xylem and IF fibers; LHCB genes and photosynthesis GO peak here (possible chlorenchyma) |
| VND7pro nuclei | Xylem (developing vessels) | **Adopt** | VND6, XCP1 peak; VND1/2, XCP2, BFN1 VND7-specific |
| PXYpro nuclei | Procambium / Vascular_Cambium + early xylem | Revise | merged domain, 54 specific genes; PXY mRNA only 1.07x |
| SMXL5pro nuclei | Phloem (developing) / distal cambium | Revise | 5 specific genes, overlaps APL |
| APLpro nuclei | Phloem (CC + developing SE) | Revise | SE and CC merged; SUC2, PP2-A1 do not peak |
| SCRpro nuclei | Endodermis (starch sheath) | **Adopt** | SCR 2.7x, PIN3 peak, WRKY28 reporter |
| LTP1pro nuclei | Epidermis | **Adopt** | FDH, CER6, CER1, LTPG1 peak; AT5G28630 reporter |
| LCM phloem cap | Phloem_Cap | Revise | includes adjacent phloem (APL 3.6x, SEOR1 2.2x) and, as found here, pollen RNA |
| LCM pith | Pith | **Adopt** | ANAC074, PER22 up; AGP26, CLE46 reporters |
| LCM vascular bundle | - | Reject | mixed control sample |

Updated verdict-matrix entries: Endodermis (starch sheath) now has an adopted population (Shi SCR); Pith has
Shi LCM pith (Adopt); Phloem_Cap has Shi LCM cap (Revise); Xylem and Epidermis each have a second adopted
source (Shi VND7, Shi LTP1). Cortex, xylem parenchyma and phloem parenchyma were not profiled by Shi.

### Markers added (31 rows; all IDs from the paper's tables, UniProt-checked in `Shi2021/uniprot_id_check.tsv`)

| Cell type | Added (evidence, confidence) |
|---|---|
| Epidermis | CER6 AT1G68530 (function, high), CER1 AT1G02205 (function, high), LTPG1 AT1G27950 (function, high), AT5G28630 (char., high) |
| Endodermis | PIN3 AT1G70940 (function, medium), WRKY28 AT4G18170 (char., medium) |
| Interfascicular_Fiber | AT2G31930 (char., medium) |
| Xylem | VND7 AT1G71930 (function, high), VND2 AT4G36160 (function, high), VND1 AT2G18060, BFN1 AT1G11190, LBD30 AT4G00220 (function, medium) |
| Vascular_Cambium | ANT AT4G37750 (function, high), HIPP35/ATHMP10 AT1G56210, DOF2.2 AT2G28810 (char., low) |
| Phloem | PEAR1 AT2G37590 (function, high), PEAR2 AT5G02460 (function, medium), AT1G29520 (char., high), AT1G24575, FMO GS-OX-like 2 AT1G12200 (char., medium) |
| Sieve_Element | NAC086 AT5G17260, NAC045 AT3G03200 (function, high) |
| Phloem_Cap | LHT7 AT4G35180, MIPS3 AT5G10170, MYB29 AT5G07690, CYP83A1 AT4G13770 (char., medium), CYP79F1 AT1G16410 (char., low); the 3 glucosinolate genes `requires=Brassicaceae` |
| Pith | ANAC074 AT4G28530 (function, medium), PER22 AT2G38380, AGP26 AT2G47930 (char., medium), CLE46 AT5G59305 (char., low) |

Seven new rows sit one level above the review's grade because an independent study in a sibling draft agrees
(named in `basis`): CER1 (Xia 2022 leaf Stereo-seq), LTPG1 (Zhang 2021, Xu 2025 shoot apex), AT5G28630
(Procko 2022 reporter), VND2 (Liew 2024 seed, Lee 2025 inflorescence), ANT (Eswaran 2024 Science;
10.1126/science.adj8752 confirmed in Europe PMC), PEAR1 (Shahan 2022, Lyu 2025 root), AT1G29520 (Lee 2025 stem c9).

### Existing rows raised (12) and annotated

Raised one level, with the reason in `basis`:
- medium -> high: SCR/SGR1 (Endodermis), SND1/NST3 (Interfascicular_Fiber), WOX4 (Vascular_Cambium),
  SMXL5 (Phloem; with Zhang 2021 and Shahan 2022, because Shi and Wallner 2017 are the same lab),
  ENODL9 (Sieve_Element), IRX8, LAC17, ACL5, UXS6 (Xylem), FAR3/CER4 (Epidermis), NaKR1 (Phloem_Companion).
- low -> medium: GLP10 (Xylem).

Not raised, with the Shi values noted in `basis`: NST1 (1.3x in NST3 nuclei), PXY (1.07x; high in pith),
ATHB8 (tops in VND7 nuclei), and rows already at high (APL, SEOR1, CALS7, VND6, XCP1, XCP2, IRX1/3/5, MYB46,
FDH, AHA3). TGG1 also gets Husebye 2002 (the only `characterized_markers.tsv` row whose ID matched the draft);
it stays medium because it also marks guard cells.

Totals: 84 rows (83 genes; FAMA twice): 44 `function`, 39 `characterized_enriched`, 1 `expression`;
41 high, 25 medium, 18 low (before: 19 / 19 / 15).

### Gaps closed

- **Pith**: closed. ANAC074 (`function`, medium) plus PER22, AGP26, CLE46.
- **Phloem_Cap**: partly closed. Five `characterized_enriched` rows (LHT7 and MIPS3 are the cap-specific
  reporters); still no `function` marker.
- **Endodermis (starch sheath)**: now has an adopted stem population and three rows (SCR high, PIN3, WRKY28).
- Also strengthened: Epidermis (5 `function`), Vascular_Cambium (WOX4 high, ANT high), Sieve_Element (NAC086,
  NAC045), Phloem (PEAR1/2), Xylem (VND7, VND1, VND2, BFN1, LBD30).

### Gaps remaining

- **Cortex**: not profiled by Shi; still only low/medium characterized_enriched rows.
- **Xylem_Parenchyma**, **Phloem_Parenchyma**: no stem evidence. `characterized_markers.tsv` lists
  NRT1.8, HKT1 (xylem parenchyma) and SWEET11/12 (phloem parenchyma) for this group, but from leaf/root work;
  they were not added as stem rows.
- **Trichome** (GL1/GL2 only in the characterized table, leaf evidence), **Shoot_Meristem** (STM in the
  characterized table; use the `arabidopsis_shoot_apex` draft), dividing and S-phase states: unchanged.
- **Phloem_Cap** `function` marker and a clean companion-cell signal in stem sorted data.

### Conflicts

1. **Evidence tier changed from the review**: MYB29, CYP83A1 and CYP79F1 were graded `function` in the review;
   here they are `characterized_enriched`. Their function marks an aliphatic-glucosinolate program, not the cap,
   and it is also high in Shi PXY/NST3 nuclei. The leaf draft puts the same genes in Bundle_Sheath and the fruit
   draft in Glucosinolate_Producing.
2. **Pollen RNA in the LCM phloem cap libraries** (found here, not in the review): VGD1 and LAT52-like are up
   log2FC 6.1 and 6.8 in cap vs bundle (SDS7). Phloem_Cap genes without a reporter (CYP79F1, and SDS15
   membership alone) should be checked against pollen markers before use.
3. **Myrosinases in starch-sheath nuclei**: TGG2 (2.4x) and TGG1 are highest in SCR nuclei and up in LCM cap.
   Either the SCR promoter is active in myrosin cells or myrosin cells sit next to the starch sheath. TGG1/2
   cannot separate Endodermis from Myrosin_Idioblast in stem data.
4. **Companion-cell genes**: SUC2 and PP2-A1 do not peak in Shi APL nuclei (FANS under-samples CC, or the APL
   population is SE-biased). Their high grades rest on Lee 2025 and other organs; not lowered.
5. **Conflicts resolved**: ACL5 (VND7 4.1x, not APL) supports xylem over the Lee c9 signal; ENODL9 (APL 10.7x)
   supports Sieve_Element over the Lee MERFISH 'procambium' domain.
6. **AT1G64500 (Cortex, low)**: tops in Shi NST3 nuclei and is up in LCM pith, so it is not cortex-specific.
   Kept low. The NST3 population may carry chlorenchyma (review), which would also explain it.
7. **PXY and SCR in pith**: PXY mRNA is highest in LCM pith among LCM samples; SCR is up in pith (log2FC 1.27).
   Both are kept, with notes.
8. **NST3 population contamination**: LHCB3/LHCB2.2 peak there, so NST3-nucleus enrichment alone is weak evidence
   for fiber identity.

### Recommended label reference

Unchanged: Lee 2025 clusters 8, 9 and 10 (per-cell labels). Shi 2021 has no per-cell labels and cannot be a
label reference, but it is now the **recommended marker reference** for naming stem clusters that Lee 2025
left unlabelled: starch sheath (SCR, PIN3, WRKY28), pith (ANAC074, PER22, AGP26), phloem cap (LHT7, MIPS3)
and fibers vs vessels (NST3/NST1 vs VND7/VND6/XCP).

### Could not verify

- `GSE142034_RAW.tar` (219 MB) and per-sample bigWigs were not downloaded; the supplementary tables were used.
- Shi Supp. Figs 1, 6 and 7 were read from legends only. The cited localization papers (Nintemann 2018 for
  CYP83A1, Fujimoto 2018 for ANAC074, Schurholz 2018 for PER22) were not re-read.
- The SDS5/SDS7 values for existing rows are my own reading of the tables (population means; no new
  statistics). With n = 2-3 per population they are ratios, not tests.
