<!-- Collated from the survey review of arabidopsis_seed (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis seed single-cell datasets: collated review

Date: 2026-10-20. Built from the four dataset reviews in this folder (`Martin2026/`, `Rombi2026/`, `Liew2024/`, `Lee2025/`, each with its own README) and the `arabidopsis_seed` entries of `survey/merged_reviews.json`. This is a paper-only review. No in-data check (Step 3b) was run.

Files:
- `expected_cell_types.tsv`: the cell types to expect, written from seed anatomy (ovule at fertilization through 7 DAP, plus imbibed and germinating seed), not from the published labels. `function_markers` counts `function` rows in the skill's existing tables (`references/markers/*.tsv`) that apply to Arabidopsis (traits eudicot, Brassicaceae, C3) under the same cell-type name. `notes` gives the count in the draft below.
- `markers_draft.tsv`: 121 rows (119 genes) in the skill's marker schema plus `alt_id`. `ref_gene` is the TAIR AGI. `alt_id` is the UniProt accession (reviewed entry when one exists), as in the other Arabidopsis drafts. `tissue = seed` is a new value; the skill README lists only leaf/root/any. Field counts were validated (13 fields on every line).
  - Tiers: 43 `function` (29 high), 60 `characterized_enriched`, 18 `expression` (17 of them `medium`, which needs agreement between two or three independent atlases).
  - `requires=Brassicaceae` is set on seed-coat layer rows whose layer anatomy (oi1/oi2/ii1'/ii2, mucilage, pigment strand) is Brassicaceae-type, and `requires=eudicot` on the endothelium proanthocyanidin genes and the chalazal endosperm rows. `excludes=C4` is set on RBCS2B and the plastid cortex gene.

## Datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Martin et al. 2026 *Nat Plants* 10.1038/s41477-026-02295-8 (GEO GSE295007) | whole Col-0 seeds at 3, 5 and 7 DAP, 2 replicates per stage | snRNA-seq, 10x 3' v3.1, FANS nuclei; HCR in situ for 10 genes | 54,210 nuclei (~64% seed coat, 23% endosperm, 10.5% embryo) | AGI, TAIR10/Araport11 | large objects only: Seurat RDS 1.3-3.9 GB on GEO. Cluster-to-label table in Supp Table 3 (also GitHub `Gehring-Lab/seed_atlas_2025`) | high |
| Rombi et al. 2026 bioRxiv 10.64898/2026.07.27.741042 (preprint) | heart-stage seeds, detached from the funiculus | protoplast scRNA-seq (BD Rhapsody), 2 replicates; MERFISH; 3 GFP reporters | 20,097 cells, 21 clusters (93.5% seed coat) | gene symbols as features (AGI only for unnamed genes) | cluster-level only (Table S1). The GEO accession is a placeholder; no data released | high (seed coat); embryo/endosperm merged |
| Liew et al. 2024 *Nat Plants* 10.1038/s41477-024-01771-3 (E-MTAB-12532) | embryos only (seed coat and endosperm removed) at 12/24/48 h after stratification | protoplast scRNA-seq, 10x 3' v2 | 12,798 cells, 15 clusters (13 named) | AGI, TAIR10/Araport11 | small table: per-cell `meta.tsv` (2.2 MB), saved as `Liew2024/labels.tsv`. No count matrix deposited | medium |
| Lee et al. 2025 *Nat Plants* 10.1038/s41477-025-02072-z (GSE226097), seed part | imbibed seed (0 d) and germinating seed (1.25 d) | snRNA-seq, 10x; Curio spatial on a 1.25 d section | 13,149 (0 d) + 87,207 (1.25 d) nuclei | AGI, TAIR10/Araport11 | small table: per-nucleus labels from the cellxgene portal (`Lee2025/seed_*_labels_from_portal.tsv`). The 0 d portal numbering does not match Supp Table 2 | medium |

The four studies come from four labs and are independent. Martin and Rombi cover the developing seed (3-7 DAP; heart stage). Liew and Lee cover the mature, imbibed and germinating seed. Only Martin and Lee captured endosperm, and only Martin resolved it into domains.

Related groups not collated here: `arabidopsis_endosperm` (Picard 2021) and `arabidopsis_ovule` (Hou 2021). The chalazal endosperm rows cite Picard 2021 through Martin's marker table.

## Verdicts by expected cell type

A = Adopt, R = Revise, X = Reject, - = not annotated or not sampled. Verdicts come from the dataset reviews, with the corrections listed below.

| Expected type | Martin 2026 (3-7 DAP) | Rombi 2026 (heart) | Liew 2024 (germ. embryo) | Lee 2025 (0 d / 1.25 d) |
|---|---|---|---|---|
| Funiculus | A (FUN epidermal; FUN companion cells, 3 DAP) | - (seeds detached) | - | - |
| Seed_Abscission_Zone | A (FUN hilum, ADPG1); FUN epidermal at 5 DAP is probably hilum too (see corrections) | A (c17) | - | - |
| Outer_Integument_2 | A (oi2 general, VLCFA, LTP); R (WRKY40/JA stress, S-phase) | A (c9) | - | - |
| Outer_Integument_1 | A (oi1 MYB11, basal, polyester, micropylar oi); R (high-PCD, S/G2M states) | R (c1 + c12 merge; c6 micropylar and c8 chalazal are subdomains) | - | - |
| Inner_Integument_1_Prime | A (3/5 DAP); R (merged with ii2 at 7 DAP) | R (c3, c4, c5, c11: merge) | - | - |
| Inner_Integument_2 | A (ii2 general) | R (c0, c2, c10, c20, called from dVPE/STK only) | - | - |
| Endothelium | A (ii1 endothelium); R (S-phase) | A (c7; c14 micropylar) | - | - |
| Pigment_Strand | R (merged into "ii1 basal") | A (c15) | - | - |
| Chalazal_Seed_Coat | A (CZSC general, 3 DAP) | R (c8 chalazal oi1 subdomain) | - | - |
| Chalazal_Unloading_Domain | A (CZSC placentochalazal phosphate and callose clusters) | R (c19 ULD; contains vascular-terminus xylem) | - | - |
| Nucellus | A (CPT persistent and transient nucellus) | A (c18) | - | - |
| Endosperm (pan; germinating) | A (PEN general, AGL62) | R (c13 merges embryo and endosperm) | - (removed by design) | R (1.25 d cl6 "Seed coat" = endosperm); X (cl16) |
| Micropylar_Endosperm (MCE + ESR) | A (MCE, MCE_ESR); R (ESR high-PCD state) | R (c13 subclusters only) | - | - |
| Peripheral_Endosperm | A (PEN; collapse I-IV); R (G2/M, S, dehydrin states) | R (called from G2/M genes) | - | - |
| Chalazal_Endosperm | A (nodule, basal and apical cyst); R (nodule-like, cyst photosynthetic, disaccharide) | - (absent) | - | - |
| Embryo (proembryo) | A (3 DAP upper protoderm); X (EMB unknown I/II, G2/M) | R (c13 subcluster 2) | - | - |
| Suspensor | R (score threshold) | - | - | - |
| Epidermis (protoderm) | A (upper and lower protoderm) | - | A (cl6, cl10) | A (1.25 d cl7); R (0 d; 1.25 d cl10 = root/hypocotyl epidermis) |
| Abaxial_Epidermis | A (lower protoderm, KAN1) | - | - | R (1.25 d "abaxial leaf primordia" = abaxial cotyledon epidermis) |
| Ground_Tissue / Cortex / Endodermis | A (ground tissue and cortical initials) | - | R (cl1/5/7 cortex split by replicate; cl2 cortex/endodermis merged) | R (1.25 d "Root stele" cl1; top gene GA3OX2 points to ground tissue) |
| Pericycle | - | - | - (probably inside cl12) | - |
| Procambium | A (7 DAP vascular primordium); R (5 DAP merged with hypophysis; EMB unknown IMK2) | - | R (cl12 provascular catch-all) | A (1.25 d Vascular) |
| Xylem | - | R (inside c19) | A (cl9 protoxylem) | R (0 d xylem precursors) |
| Phloem / Phloem_Companion | A (funicular companion cells) | - | A (cl15 protophloem) | A (1.25 d Phloem); R (0 d) |
| Mesophyll | A (7 DAP inner cotyledon, XYL4) | - | R (cl3, cl13: merge) | R (1.25 d cl0/2/9/11) |
| Shoot_Apical_Meristem | - (not captured) | - | - | - |
| Root_Cap / QC / Stem_Cell_Niche | A (7 DAP hypophysis, SMB) | - | R (cl14 mixed root tip; cl4 "QC/columella" histone-driven, near Reject) | R (1.25 d radicle cl5) |
| Dividing_cells / S_Phase | R (state clusters: merge into parents) | R (c16, labelled as a state) | - | R (0 d and 1.25 d cl13 G2/M); X (1.25 d cl12, no cell-cycle genes) |
| Seed_Maturation (state) | R (PEN dehydrin) | - | X (cl8) | X (1.25 d cl14) |
| Senescing (state) | A (unfertilized ovules, non-seed) | - | - | - |
| Unassigned | - | - | X (cl11) | X (0 d Unknown 73.5%; 1.25 d cl3) |

## Markers supported by more than one dataset (by gene ID)

Matched by AGI across Martin Supp Table 3 (top 15 per cluster), Rombi Table S3 (symbols mapped to AGI through UniProt gene names, plus direct lookups), Liew Supp Table 4 and Lee Supp Table 2. Rombi and Liew/Lee values are pct.1/pct.2.

| Type | Gene | Support | Draft |
|---|---|---|---|
| Endothelium | BAN AT1G61720 | Martin ii1 rank 1-8 (3/5/7 DAP); Rombi c7 1.00/0.05; BAN promoter (Debeaujon 2003) | function, high |
| Endothelium | TT12 AT3G59030; DFR AT5G42800; LDOX AT4G22880; TT19/GSTF12 AT5G17220 | Martin ii1 top-15; Rombi c7 (0.47-1.00 vs 0.02-0.05) | function, high |
| Endothelium | STP14 AT1G77210 | Rombi MERFISH; Martin 5 DAP ii1 top-15 | characterized_enriched, high |
| Endothelium | CYP86A2 AT4G00360; AT5G51950 | Martin ii1; Rombi c14/c7 | medium |
| Pigment_Strand | AT2G42860 | Martin ii1-basal (5/7 DAP); Rombi c15 0.75/0.02 | expression, medium |
| Outer_Integument_2 | GL2 AT1G79840 | Martin oi2; Rombi c9 0.26/0.02 | function, high |
| Outer_Integument_2 | ATML1 AT4G21750 | Rombi MERFISH; Martin oi2 (also embryo epidermis in Liew, Lee) | characterized_enriched, high |
| Outer_Integument_2 | LTPG6 AT1G55260; AT5G45670; EXL3 AT1G75900; KCS6 AT1G68530 | Martin oi2 top-15; Rombi c9 | medium |
| Outer_Integument_1 | ELA1 AT5G24910 | Creff 2015 seed coat; Martin oi1; Rombi c12 | characterized_enriched, high |
| Outer_Integument_1 | SWEET12 AT5G23660 | Rombi GFP reporter (micropylar oi1); Martin "oi micropylar" rank 1 | function, high (domain conflict noted) |
| Outer_Integument_1 | NRT1.6 AT1G27080; MYB11 AT3G62610; NMT3 AT1G73600; UMAMIT15 AT5G13670 | Martin oi1/micropylar oi; Rombi c1/c6 (NRT1.6 also MERFISH) | medium |
| Chalazal_Seed_Coat | ARR22 AT3G04280 | Horak 2008 reporter; Martin CZSC rank 1-3; Rombi c19/c8 | characterized_enriched, high |
| Chalazal_Unloading_Domain | UMAMIT14 AT2G39510 | Rombi MERFISH; Martin placentochalazal rank 1; Muller 2015 | function, high |
| Chalazal_Unloading_Domain | bZIP9 AT5G24800; CALS8 AT3G14570; SWEET10 AT5G50790 | Rombi reporter/MERFISH or top DE; Martin placentochalazal rank 1-2 (SWEET10 HCR) | characterized_enriched, high |
| Chalazal_Unloading_Domain | AT1G26450; HIPP09 AT5G24580; AT1G73850 | Martin placentochalazal; Rombi c19 | medium |
| Nucellus | AGO3 AT1G31290 | Martin HCR, rank 1; Rombi c18 0.92/0.00 | characterized_enriched, high |
| Nucellus | AT5G46300; AT1G51030; AT1G20730 | Martin CPT top-15 (3/5 DAP); Rombi c18 (0.63-0.82 vs 0.00-0.01) | expression, medium |
| Seed_Abscission_Zone | ADPG1 AT3G57510 | Rombi c17 0.21/0.001; Martin FUN hilum | function, high |
| Inner_Integument_1_Prime | UMAMIT12 AT2G37460; UMAMIT29 AT4G01430 | Rombi MERFISH; Martin ii1' rank 1/12 | characterized_enriched, high |
| Inner_Integument_2 | OFUT4 AT1G14970; SBT3.15 AT4G21640 | Martin ii2 rank 1-2; Rombi c10/c0 | expression, medium |
| Micropylar_Endosperm | ZOU AT1G49770 | Martin ESR; Rombi c13 0.14/0.00 | function, high |
| Chalazal_Endosperm | AT2G44240 | Picard 2021 CZE; Martin apical cyst | expression, medium |
| Epidermis | PDF1 AT2G42840 | Martin HCR; Liew cl6 0.77/0.15 | characterized_enriched, high |
| Epidermis | FDH AT2G26250; ATML1 AT4G21750 | Liew cl6; Lee 1.25 d cl7; Martin protoderm | function, high |
| Epidermis | ABCG15 AT3G21090 | all Martin protoderm clusters; Liew cl6 0.45/0.04; Lee cl4/cl7. Absent from seed-coat clusters | expression, medium |
| Ground_Tissue | AT3G23470 | Martin cortical initials rank 1; Liew cl2; Lee 1.25 d cl1 | expression, medium |
| Procambium | ATHB8 AT4G32880; JUL1 AT3G15680; XYP2 AT2G13820 | Martin vascular primordium (JUL1 HCR); Lee 1.25 d cl8; Liew cl12 | high/high/medium |
| Xylem | XCP1, IRX3/CESA7, IRX5/CESA4, IRX1/CESA8, VND6, VND2 | Liew cl9; Lee 0 d cl15 | function, high (VND2 medium) |
| Phloem | APL AT1G79430; PD1 AT3G01950 | Liew cl15; Lee 1.25 d cl15 | high |
| Phloem_Companion | SUC2 AT1G22710; PP2-A1 AT4G19840 | Martin funicular CC; Liew cl15; Lee cl15 | high |
| Phloem_Companion | AHA3 AT5G57350; NaKR1 AT5G02600 | Liew cl15; Lee cl15 | characterized_enriched, high |
| Root_Cap | SMB AT1G79580 | Martin 7 DAP hypophysis rank 3; Liew cl14 | function, high |
| Quiescent_Center | RGF8 AT2G03830 | Martin hypophysis; Liew cl4 0.29/0.01 | expression, medium |
| Dividing_cells / S_Phase | CDC20.1, TOPII; HMGB6, TSO2 | Martin G2/M and S clusters; Lee cl13; Rombi c16 | state rows |

## Gaps

- No validated marker in any dataset: **Funiculus** (apart from its phloem), **Shoot_Apical_Meristem** (not captured; CLV3/STM/WUS not detected), **Pericycle**, **Stomatal_lineage** (germination only, not annotated), **Endodermis** separate from cortex (SCR is filed under Ground_Tissue; CASPs not detected in embryos).
- Only `expression` or `low` rows: **Peripheral_Endosperm** (IQD16 only; PEN was called from AGL62 and G2/M genes), **Quiescent_Center** (WOX5 not detected; RGF8 only), **Cortex** (one plastid gene), **Seed_Maturation** and **Senescing** (states).
- **Inner_Integument_2** has no layer-specific validated gene (dVPE is shared with ii1'), and **Nucellus** has one validated gene (AGO3).
- Adaxial cotyledon epidermis (AS2) and the suspensor (WOX8 seen in only 31 nuclei) rest on one literature gene each.
- Developmental coverage stops at 7 DAP. The maturation phase (8 DAP to dry seed) has no single-cell dataset in this group.

## Recommended label reference

- **Developing seed (globular to torpedo, nuclei):** Martin 2026. It is the only dataset covering embryo, endosperm domains and all seed-coat layers, with replicates and HCR checks. Use the L2 (tissue/layer) labels and collapse the L3 states listed above (S/G2M, high-PCD, WRKY40, dehydrin, numbered PEN subclusters). Per-nucleus labels must be read from the GEO RDS (`GSE295007_ATLAS_merged_annotated_sigmods.rds`, 1.3 GB) in a compute job. Use Rombi 2026 Table S1 and its MERFISH genes to check the seed-coat layers, the ULD, the nucellus and the abscission zone. Rombi has no released data and cannot serve as a per-cell reference.
- **Germinating seed:** Lee 2025 1.25 d (nuclei, public per-nucleus labels, endosperm included) for Phloem, Epidermis and Procambium. Relabel its cl6 "Seed coat" as Endosperm and its cl14 as a maturation state. Liew 2024 (protoplasts, embryo only) is the reference for Xylem and Phloem, with time as a covariate. Its cl8 and cl11 are states, and its cortex and mesophyll clusters split by replicate.

## Conflicts and corrections

1. **ID swap in Liew 2024 Supp Table 3:** the table lists AT5G05290 as RGL2 and AT3G03450 as EXPA2. UniProt gives AT5G05290 = EXPA2 (Q38866) and AT3G03450 = RGL2 (Q8GXW1). The draft uses AT5G05290 for EXPA2. Lee 2025 lists EXPA2 under the correct ID.
2. **SWEET15 (AT5G13170) correction to the Rombi review:** the review says SWEET15 is "not in S3 (filtered)". It is in Table S3 under its alias **SAG29**, in ii1' c11 (0.24/0.02) and c13 (0.15/0.02), not in the nucellus (c18). This conflicts with the paper's pSWEET15:SWEET15-GFP nucellus call, so SWEET15 is left out of the draft.
3. **Rombi IDs were not checked in its review** (`id_checked=false`). All 119 draft AGIs now resolve in UniProt (taxon 3702), and the symbols match. Some genes have no symbol in UniProt (UMAMIT12/14/15/18/25/29, PLL24, JUL1, OLEO1, PD1); for these the AGI comes from the papers' own tables (Martin S1, Liew S3, Rombi Table S1).
4. **Same domain, different names:** Martin's "CZSC placentochalazal" clusters and Rombi's "unloading domain" (c19) share bZIP9, CALS8, UMAMIT14, SWEET10, HIPP09, AT1G73850 and AT5G49320. Both are filed as `Chalazal_Unloading_Domain`. Rombi's c19 also holds vascular-terminus xylem (ACL5) and phloem (GTR2, SHR, PXY).
5. **Martin "FUN epidermal (CER3)" at 5 DAP** has ADPG1 in its top 15, and CER3 is also in Rombi's abscission zone (c17). It is probably hilum/abscission tissue rather than general funiculus epidermis.
6. **SIAR1 (AT1G44800):** abscission zone by MERFISH in Rombi, but rank 4 of Martin's 5 DAP "oi micropylar". The micropyle sits next to the hilum, so both may be right. Kept `medium`.
7. **UMAMIT25 (AT1G09380):** ii1' by MERFISH in Rombi, but micropylar endosperm/ESR in Martin, and endosperm in earlier work. Kept `low`. MES10 (spatial endosperm vs scRNA ii1') was left out.
8. **Epidermal genes mark two lineages:** ATML1, FDH, LTP1, KCS6 and AT5G45670 mark both the embryo epidermis and the seed-coat oi2, and DCR/PEL3 is oi2 in Rombi but embryo protoderm in Martin. In whole-seed data, use ABCG15 and PDF1 for the embryo, and GL2, LTPG6 and EXL3 for oi2.
9. **SWEET12:** micropylar oi1 by reporter (Rombi) and by cluster (Martin), but placentochalazal early (Li 2024, as cited by Martin), and equally in chalazal oi1 in Rombi's scRNA. The skill's leaf table has it as Phloem_Parenchyma.
10. **NRT1.6:** oi1 in both atlases, but Almagro 2008 reported silique and funicular vasculature expression. Kept at `medium` instead of being raised.
11. **DIR20:** protoxylem by in situ (Liew), but also in provascular cl12 (Liew) and procambium cl8 (Lee). It marks provasculature plus protoxylem.
12. **Lee 2025 labels:** 1.25 d cl6 "Seed coat" is endosperm (EXPA2, a germinating-endosperm marker per Sanchez-Montesino 2019; the testa is dead at maturity). 1.25 d cl1 "Root stele" has GA3OX2 as its top gene, which is expressed in cortex and endodermis by in situ (Yamaguchi 1998). It is filed under Ground_Tissue.
13. **Left out for conflicts:**
    - GRP5 (AT3G20470): radicle tip by in situ in Liew, but oi2 in Martin and Rombi.
    - WOX9: hypophysis per Martin's marker table, but its DE is in PEN general IV.
    - PLL22 (AT5G63180): in both micropylar oi and transient nucellus.
14. **Rombi naming:** it calls oi2 "adaxial epidermis". In standard usage oi2 is the outer (abaxial-facing) epidermis. The draft uses layer names only.

## Overlap with existing skill tables (Arabidopsis)

- `arabidopsis_leaf.tsv`: 11 genes are shared (13 draft rows).
  - Same cell type: ATML1, FDH, PDF1 and LTP1 (Epidermis), ATHB8 (Procambium), XCP1 and IRX3 (Xylem), APL (Phloem), SUC2 (Phloem_Companion).
  - Different cell type: GL2 (Trichome in leaf; Outer_Integument_2 here) and SWEET12 (Phloem_Parenchyma in leaf; Outer_Integument_1 here).
  - Confidence: the draft raises PDF1 (medium to high) and ATHB8 (medium to high) for agreement across seed studies. LTP1 goes from low to medium.
- `arabidopsis_root.tsv`: 7 genes are shared.
  - Same cell type: MYB46 (Xylem), APL (Phloem), PLT1 (Stem_Cell_Niche).
  - Different cell-type name: GL2 (Atrichoblast vs Outer_Integument_2), SCR (Endodermis vs Ground_Tissue), SHR (Stele vs Procambium), SMB (Lateral_Root_Cap vs Root_Cap).
- All seed-coat, endosperm, nucellus, abscission-zone and unloading-domain rows are new. The skill has no seed table.
- If the draft is added, either use `Root_Cap` in the skill or rename to `Lateral_Root_Cap`/`Columella`, so the counts match.

## Not verified

- **Martin 2026:**
  - Per-nucleus labels were not extracted (RDS 1.3-3.9 GB).
  - Not downloaded: the Supp Information PDF (68 MB, HCR images in Supp Fig 5) and Supp Table 4 (125 MB, full DE).
  - "Not in top 15" in this README is not evidence of absence.
- **Rombi 2026:**
  - No data are released.
  - The Supp Figs PDF was not parsed, and the main text was read only through a summarizer (cluster calls come from Table S1).
  - Per-cluster cell counts are not tabulated in the paper.
  - The symbol-to-AGI matching used UniProt names. Genes with no UniProt symbol rely on the reviewer's reading of Table S3 (checked directly here for UMAMIT12/29/14, RR22, SIAR1, ADPG1, SAG29 and RGE1).
- **Liew 2024:**
  - No count matrix is deposited.
  - The interactive atlas was not mined, and the Extended Data images were not viewed.
- **Lee 2025:**
  - The h5ad/rds objects were not downloaded.
  - The match between the 0 d portal and Supp Table 2 numbering is unconfirmed. The 0 d cluster numbers above follow Supp Table 2.
  - The GitHub repository returns 404.
- **Literature basis lines:** these use the reviews' citations and Martin/Liew marker tables. Primary papers were not re-read. DOIs are given only when they came from a paper's table; other citations are named in `basis`. These are Sagasser 2002, Tanaka 2001, Ogawa 2009, Tian 2010, Dinant 2003, Motose 2004, Kang 2008, Almagro 2008, Debeaujon 2001, Yamaguchi 1998 and Sanchez-Montesino 2019 (the last DOI is from Liew Table S3).
