<!-- Collated from the survey review of arabidopsis_leaf (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis leaf: collated cell-type marker resources

Collated 2026-10-20 from the four dataset reviews in
`../../survey/merged_reviews.json` (`group == "arabidopsis_leaf"`). Each
dataset folder keeps its own review README.

Files in this folder:

- `expected_cell_types.tsv`: cell types expected from rosette-leaf anatomy
  (Step 2 format). `function_markers` counts `function` rows in
  `markers_draft.tsv` plus the function rows that exist only in the skill's
  `arabidopsis_leaf.tsv` (the notes say which are which).
- `markers_draft.tsv`: 125 rows after the 2026-10-20 gap-fill update (84 before), skill schema plus `alt_id` (UniProt
  accession). Candidate replacement for or extension of the skill's
  `references/markers/arabidopsis_leaf.tsv`. The skill itself was not edited.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| `TenorioBerrio2025/` | Tenorio Berrío et al. 2025 *New Phytol* 246:840, 10.1111/nph.20446; GSE273033 | Protoplast scRNA-seq (BD Rhapsody), actinomycin D-fixed; 3rd leaf at 14 DAS, well-watered vs mild drought, 2 reps | 50,797 (curated FD atlas) | Per-cell labels without barcodes from the public portal (`portal/portal_cell_labels_no_barcodes.tsv`); barcodes only in the GEO rds (https://ftp.ncbi.nlm.nih.gov/geo/series/GSE273nnn/GSE273033/suppl/GSE273033_seuratObj_for_publication.rds.gz, 828 MB; URL checked 2026-10-22). It is gzipped twice: `readRDS` fails with "unknown input format", so `zcat` it to `.rds` first. `meta.data` has `annotation` (14 labels) and `seurat_clusters` for 50,797 FD cells; cell names `RTB15_nofilter_<BD index>` = well-watered R1 and `RTB19_nofilter_<idx>` = well-watered R2 (counts 14,548 / 13,653; skill test H1, 2026-10-22) | high |
| `Lee2025/` | Lee et al. 2025 *Nature Plants*, 10.1038/s41477-025-02072-z; GSE226097 (rosette part only) | snRNA-seq (10x), whole rosette at 21 d and 30 d, 6 reps each | 22,025 + 37,817 nuclei | Per-nucleus table, corrected by the reviewer (`rosette_21d/30d_labels_corrected.tsv`, column `CellType_SuppTable2`). The portal's own `CellType` column is scrambled | medium |
| `Nobori2025/` | Nobori et al. 2025 *Nature* 638:197, 10.1038/s41586-024-08383-z; GSE226826 | 10x snMultiome (RNA+ATAC) of mature leaves over a Pst DC3000/AvrRpt2/AvrRpm1 time course; MERFISH (500 genes) | 65,061 nuclei; 129,733 MERFISH cells | Only in the 5.2 GB `combined_filtered.rds` (local copy in `Alex/NoboriAtlas/`); 4 coarse classes | medium |
| `Kim2021/` | Kim et al. 2021 *Plant Cell* 33:511, 10.1093/plcell/koaa060; GSE161332 | Protoplast scRNA-seq (10x v2), mature leaves of 6-week plants, vascular-enriched (abaxial epidermis peeled) | 5,230 | Cluster-level only (Supp DS2); GEO matrix is unfiltered (6,300 barcodes) | medium |

## Verdict matrix (published labels, by canonical cell type)

Adopt / Revise / Reject are the reviews' verdicts. "-" = not present or
not resolved.

| Cell type | Tenorio Berrío 2025 | Lee 2025 | Nobori 2025 | Kim 2021 |
|---|---|---|---|---|
| Mesophyll | Adopt (palisade/spongy not split; drought substates inside) | Revise (label transfer from Procko 2022; 30d c6 Adopt) | Adopt (with many immune/JA state clusters) | Revise (11 clusters are states; merge) |
| Palisade / Spongy | - (PAL1/CORI3 gradient only) | - (30d c6 "spongy" tentative) | - | - (FIL weak) |
| Bundle_Sheath | Adopt (CYP83A1 reporter) | Revise (glucosinolate BS/PP: 21d c5, 30d c3) | - (cluster 10 inferred) | Adopt BS-1; BS-2 Revise (merge) |
| Xylem_Parenchyma | - | - | - | Revise (merge XP1/XP2; XP3 hypothesis) |
| Phloem_Parenchyma | Adopt (SWEET12, bZIP9, AT3G11930) | Revise (inside glucosinolate cluster c5) | - (cluster 14 inferred, SWEET11/12) | Adopt PP1 (reporters); PP2 Revise (merge) |
| Phloem_Companion | Adopt | Adopt (21d c8, 30d c7) | Adopt (cluster 6) | Adopt (C15) |
| Sieve_Element | Adopt (developing) | Revise (30d c13 "SE" is G2/M) | - (nuclei) | - |
| Xylem | Adopt (includes precursors) | Revise (21d c17 xylem + procambium) | - (cluster 9 unresolved) | - |
| Procambium | Revise ("Cambium"; weak markers) | Revise (part of 21d c17) | - | Revise (PC-XP, PC-PP unconfirmed) |
| Epidermis / Pavement | Adopt (Pavement; not split by side) | Adopt 30d c1; 21d "Guard" c2 is pavement (Revise) | Revise (GC and trichomes merged in) | Adopt (C13; mostly adaxial) |
| Adaxial / Abaxial epidermis | - | Adopt abaxial (21d c12, 30d c12); 30d c4 Revise to adaxial | - | - |
| Guard | Adopt (6x replicate imbalance) | Adopt (21d c15, 30d c14) | - | Revise (myrosin cells merged in) |
| Stomatal_lineage | Adopt ("Meristemoid") | - | - | - |
| Trichome | - | Adopt 21d c14; 21d c6 Revise (touch state) | - | - |
| Hydathode | Adopt (DIR11 reporter) | - | - | Revise (weak; PUP1 not DE there) |
| Myrosin_Idioblast | Adopt (TGG2/TGG1/NSP1 reporters) | - (TGG1/2 in 21d c10) | - | - (in guard C16) |
| Cell-cycle states | Revise (G1-S 13.4%, G2-M 3.4%) | Revise (4 "Dividing" clusters) | Reject "Unknown" = S-phase | C14 S-phase/endocycle in mesophyll |
| Stress / immune states | drought substates in mesophyll | 21d c6 touch, c13 and 30d c9 defense, Reject 21d c11 multiplets | immune, JA, PRIMER/bystander states (validated as states) | C1 touch, C8 JA, C11 SA, C12 high light; C19 Reject |

## Cross-study markers

32 rows have the same gene ID supported for the same cell type by at least
two of the four datasets, with no conflict. Their `confidence` was raised
one level:

| Cell type | Genes (datasets) |
|---|---|
| Phloem_Companion | SUC2 AT1G22710 (all 4), PP2-A1 AT4G19840 (T reporter, K, N), NaKR1 AT5G02600 (L, N), FTIP1 AT5G06850 (K, N), AHA3 AT5G57350 (T, K), APL AT1G79430 (L, K) |
| Phloem_Parenchyma | SWEET11 AT3G48740 (K reporter, N, L), SWEET12 AT5G23660 (T, N, K), bZIP9 AT5G24800 (reporter in both K and T) |
| Bundle_Sheath | SULTR2;2 AT1G77990 (T, K), BCAT4 AT3G19710 (L, N), MAM1 AT5G23010 (L, N) |
| Guard | FAMA AT3G24140 (L, T, K), MYB60 AT1G08810 (T, K), TGG1 AT5G26000 (L, T), WRKY23 AT2G47260 (L, K), PDR1/ABCG29 AT3G16340 (L, K; see conflicts) |
| Myrosin_Idioblast | TGG2 AT5G25980 (T reporter; top gene of K's guard cluster) |
| Epidermis | ATML1 AT4G21750 (L, K), FDH AT2G26250 (L, N), KCS6 AT1G68530 (K, N), PDF1 AT2G42840 (T reporter, L), CER26 AT4G13840 (L, N), LTP7 AT2G15050 (L, N) |
| Mesophyll | CA1 AT3G01500 (K, N), RBCS1A AT1G67090 (L, N) (both weak in specificity) |
| Spongy_Mesophyll | CORI3 AT4G23600 (L, T gradient; JA-inducible) |
| Procambium | ATHB8 AT4G32880 (L, T, K) |
| States | PCNA1 (L, K), KNOLLE, CYCB1;1, CDKB2;1 (L, T) |

T = Tenorio Berrío 2025, L = Lee 2025, N = Nobori 2025, K = Kim 2021.
Three more genes appear in two or more datasets but conflict or lack
specificity, so they were not raised: KAT1, PUP1 and LHCB1.2/CAB3 (see
below). Lee 2025's 21d and 30d datasets are one study and were not counted
as independent.

## Gaps

- **No `function` marker:** Palisade_Mesophyll, Spongy_Mesophyll,
  Xylem_Parenchyma, Pavement, Adaxial_Epidermis, Abaxial_Epidermis and
  Hydathode. Hydathode has two good reporters (DIR11, PUP1), but neither has
  a hydathode function.
- **Weak:** Mesophyll (only EPFL9 is `function`, and it does not separate
  mesophyll from cycling precursors), Sieve_Element (one gene, protoplasts
  only), Myrosin_Idioblast (one gene).
- **Resolved by only one dataset:** Stomatal_lineage, Hydathode,
  Myrosin_Idioblast, Sieve_Element (all Tenorio Berrío), Xylem_Parenchyma
  (Kim), and adaxial/abaxial epidermis (Lee, using Procko 2022 genes).
- **Not covered by any dataset:** palisade vs spongy (only gradients),
  midrib/petiole collenchyma, and senescing cells (SAG12 comes from the
  skill table only).

## Recommended label reference

1. **Tenorio Berrío 2025** is the best reference for cell types. It has the
   most types (12 plus 2 cell-cycle states), 25 new promoter reporters, a
   digestion-artifact filter, and public per-cell labels. Caveats: these are
   protoplasts of a young (14 DAS) leaf; the labels have no barcodes (use the
   789 MB GEO rds to match); every cell is forced into a label; G1-S/G2-M
   hide 17% of identities; and "Cambium" should be read as procambium.
2. **Lee 2025** is the reference for nuclei data and mature rosettes. Use
   only the corrected labels, and adopt only Guard (21d c15, 30d c14),
   Companion cell (21d c8, 30d c7), abaxial epidermis (c12), adaxial
   epidermis (30d c4), Epidermis (30d c1), Trichome (21d c14) and Mesophyll
   30d c6.
3. **Nobori 2025** gives lineage-level labels only (Mesophyll / Epidermis /
   Vasculature / companion cells) plus validated immune states. Use it as a
   state reference, not for cell types.
4. **Kim 2021** is a marker source (reporter-validated PP, plus CC and BS),
   not a per-cell reference: its labels are cluster-only and few cells are
   vascular.

## Conflicts and corrections

- **Lee 2025 portal labels are scrambled.** The cellxgene `CellType` column
  maps labels to clusters in string order. Use
  `Lee2025/rosette_*_labels_corrected.tsv`.
- **KAT1 (AT5G46240):** guard-specific in Tenorio Berrío (4.8x), but DE in
  the companion-cell clusters of Kim 2021 (C15) and Lee 2025 (21d c8, 30d
  c7), not in their guard clusters. Lowered to `medium` (the skill table
  has `high`).
- **PDR1/ABCG29 (AT3G16340):** guard-cell DE in Lee and Kim, but it is
  characterized as a root endodermis/vascular monolignol transporter, and
  Lee Supp Table 3 lists it for seedling endodermis/vasculature. The
  survey's note that it is a spatially validated guard marker is wrong.
  Kept as `expression`.
- **TGG2 vs guard cells:** TGG2 is the top gene of Kim 2021's guard cluster
  C16. FAMA and TGG1 are expressed in both guard cells and myrosin
  idioblasts, so myrosin cells merge into guard clusters. Use TGG2 and NSP1
  to separate them.
- **PUP1 (AT1G28230):** hydathode reporter (Bürkle 2003) and 5.7x
  hydathode-specific in Tenorio Berrío, but DE in Kim 2021 epidermis C13,
  not in their hydathode C17.
- **SUC2:** Kim 2021 lists it under epidermis C13 DE, not companion-cell
  C15. The other three datasets agree on companion cells.
- **SWEET11:** it marks PP in Kim (reporter) and Nobori (c14), but in Lee
  2025 it is DE in the glucosinolate BS/PP cluster 21d c5. Lee's nuclei do
  not separate BS from PP.
- **Glucosinolate module (BCAT4, MAM1, MYB28/29, CYP79F1, CYP83A1):** placed
  in `Bundle_Sheath` because of Tenorio Berrío's CYP83A1 BS reporter. The
  assignment for Lee c5/c3 and Nobori cluster 10 is inferred. The literature
  places these genes in vascular-associated (phloem/S-cell) tissue.
- **AT1G25230 (PAP4):** a Tenorio Berrío BS reporter gene, but not
  BS-specific in the data (1.2x, highest in Xylem). Left out.
- **EXPA4:** the Tenorio Berrío "cambium" reporter is higher in Xylem than
  in Cambium. Kept as `low`.
- **Kim 2021 named markers that are not DE:** GLR3.6 (XP), PXY, WOX4 and
  REV (procambium). ACL5 is DE in C10, not C4, and HB8 is DE only in C18.
  GLR3.6 and WOX4 were left out.
- **Proliferation labels:** Lee "Dividing" (4 clusters), Lee 30d "SE"
  projection, Tenorio G1-S/G2-M, Nobori "Unknown" and Kim C14 are all
  cell-cycle states. Lee 21d "Guard" c2 (12.5%) is pavement epidermis, and
  21d "Trichome" c6 is a touch-response state.
- **Names:** PREX (AT5G63180) is called AtPLL15 in Tenorio Berrío Table 1
  and "probable pectate lyase 22" in UniProt; the ID is the same. Lee's
  "PKS-like" adaxial gene AT1G18810 is PKS3 in UniProt.

## Overlap with the skill table (`references/markers/arabidopsis_leaf.tsv`, 33 rows)

- **In both tables (22):** CA1, RBCS1A, SULTR2;2, ATML1, PDF1, FDH, LTP1,
  KAT1, FAMA, SPCH, MUTE, GL1, SUC2, SWEET11, SWEET12, SEOR1, APL, XCP1,
  ATHB8, PCNA1, KNOLLE and CYCB1;1. The data support all of them. Changes:
  - KAT1 lowered to `medium` (companion-cell conflict).
  - SULTR2;2 raised from `low` to `medium` (two datasets).
  - PDF1 raised from `medium` to `high`.
  - LTP1 raised from `low` to `medium`.
  - APL moved from `Phloem` (any) to `Phloem_Companion`, because that is
    where it is DE in leaf data.
- **Only in the skill table (no test in these datasets):** RBCS1B, PSBQ-2,
  CER5, LACS2, SLAC1, GL2, XCP2, IRX3, VND7, H3.1 and SAG12. Keep them;
  they are counted in `expected_cell_types.tsv`.
- **New here (62 rows):** the reporter-validated Tenorio Berrío and
  Kim 2021 genes (bZIP9, SWEET13, PP2-A1, PARCL, GRXS2, AT1G04800, MYB60,
  DIR11, PUP1, TGG2, NSP1, FLA12, AT3G10080, CYP83A1, AT3G11930, PREX,
  APG), the BS glucosinolate module, the companion-cell genes NaKR1, FTIP1
  and AHA3, SCL23, xylem parenchyma SULTR2;1/AAP6, and new types
  (Myrosin_Idioblast, Hydathode, Pavement, Adaxial/Abaxial_Epidermis,
  Palisade/Spongy_Mesophyll, Xylem_Parenchyma).
- **New cell-type names** that are not yet in any skill table:
  Myrosin_Idioblast, Hydathode, Pavement, Adaxial_Epidermis,
  Abaxial_Epidermis, Palisade_Mesophyll, Spongy_Mesophyll and
  Xylem_Parenchyma. Add colors for them if the table is adopted.
- **Not added:** immune states (ICS1, ALD1, FMO1, GT-3A/PRIMER from Nobori)
  are validated states, not cell types. They could go in a state table
  later.

## ID checks

Every `ref_gene` in `markers_draft.tsv` was checked against UniProt REST
(taxonomy 3702): gene names and ordered-locus names match, and the
accession is in `alt_id`. Reporter gene IDs were taken from Tenorio Berrío
Table 1 (in the PMC XML) and Kim 2021 Supp DS3 (xlsx). DE numbers come from
the reviews' checks: `Lee2025/portal_checks/`,
`TenorioBerrio2025/portal/portal_marker_check.tsv`, the Kim 2021 DS4-9
tables, and the Nobori ED Fig 2a table. Three IDs have only unreviewed
UniProt entries (AT1G04800 Q9MAS9, AT3G11930 F4J8J5, AT1G09310 C0Z2C6);
those were checked against the paper tables only.

## What could not be verified

- Literature claims in `basis` (Chen 2012, Truernit & Sauer 1995, Cui 2014,
  Takahashi 2000, Bürkle 2003, and others) come from the reviews and general
  knowledge. They were not re-read for this collation, so `source` gives
  DOIs only for the four datasets.
- The Tenorio Berrío barcodes (789 MB rds), Nobori per-cell labels (5.2 GB
  rds) and Lee GEO rds metadata were not downloaded.
- Kim 2021's PscB Shiny app and Nobori's plantpathogenatlas portal were not
  explored.
- The Tenorio Berrío GitHub code repository is not public.
- Procko et al. 2022 (adaxial/abaxial, palisade/spongy genes) was not
  reviewed directly. PKS3, DTX39, IQD22 and CORI3 are cited as Lee 2025 used
  them.
- Whether Nobori's epidermis clusters contain guard cells or trichomes, and
  whether Tenorio Berrío's FAMA-positive myrosin cells overlap the guard
  label, would need the objects.

## Update 2026-10-20: gap-fill reviews

Two reviews were added to fill the palisade/spongy, adaxial/abaxial
epidermis, pavement and hydathode gaps. Each folder keeps its own review
README. DOIs were confirmed in Europe PMC (PMID 35666176, 35512702).

### New datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| `Procko2022/` | Procko et al. 2022 *Plant Cell* 34:3261, 10.1093/plcell/koac167; GSE182414, GSE184511 | FACS of reporter-line leaf protoplasts (IQD22pro:GUS-mCit palisade; JR11-2 lower spongy) + bulk RNA-seq; one 10x 3' v3 protoplast scRNA library; ~45 promoter:GUS-mCit reporters in leaf cross-sections | 23,729 scRNA cells, 17 clusters (no per-cluster counts) | Cluster markers in Supp Data Sets S3-S19 (`supp/SDS3-19_cluster_markers_long.tsv`); per-cell labels only in the 915 MB rds (not downloaded) | medium |
| `Xia2022/` | Xia et al. 2022 *Dev Cell* 57:1299, 10.1016/j.devcel.2022.04.011 | Single-cell Stereo-seq on 10 um transverse sections of mature cauline leaves; cells outlined by hand from a cell-wall stain and labelled by histological position | 13,950 cells, 26 sections | Small per-section tables (`S1-1_labels.tsv`: cell_id, type, x, y). Spatial cells, so they cannot be matched to dissociated barcodes | medium |

### Verdicts

| Cell type | Procko 2022 | Xia 2022 |
|---|---|---|
| Palisade_Mesophyll | FACS IQD22+ Adopt (enrichment only; partially pure, has trichome/petiole genes) | Revise: anatomically right, but DEGs are an adaxial photosynthesis gradient shared with upper epidermis (189/253) |
| Spongy_Mesophyll | FACS IQD22- reference Revise (= spongy + BS; top genes are BS glucosinolate genes); JR11-2 GFP+ Revise; JR11-2 GFP- Reject | Revise: abaxial domain + JA/chitin state + vascular spill-over (213/289 shared with lower epidermis) |
| Mesophyll | scRNA cl1, 3, 4 Revise (palisade and spongy not resolved); cl2 Revise (stress/senescence state) | pooled mesophyll Adopt (ambient photosynthesis genes) |
| Pavement / Epidermis | cl0 Adopt (Pavement, sides not split); cl8 Revise (stress/senescing pavement) | pooled epidermis Adopt (pan-epidermal) |
| Adaxial / Abaxial epidermis | - (only JAL22, PYK10, PDF1.2c reporters at midvein/margin or patches) | Upper and lower epidermis Revise: positions are sound, profiles contaminated by the adjacent mesophyll; not separable on variable genes |
| Bundle_Sheath | cl5 Adopt (THA2, MAM1, ACO3 reporters) | - (merged vascular class) |
| Phloem_Parenchyma | cl6 Adopt (SWEET11/12, AT3G11930) | - (merged) |
| Phloem_Companion | cl9 Adopt (SUC2, APL, SAQR reporter) | - (merged) |
| Vascular (mixed) | cl7 Revise (xylem/procambium mix) | vascular cell Revise (BS, XP, CC, PP merged) |
| Guard | cl12 Adopt (FAMA, MPK12, GASA9 reporter) | Adopt (identity sound; DE table unusable, 5 genes) |
| Hydathode | cl14 Adopt (4 reporters) | - |
| Myrosin_Idioblast | cl15 Adopt (TGG2, TGG1, FAMA) | - |
| States | cl13 "sieve elements" Reject (S-phase: RNR1, TSO2, TK1a, histones; SEOR1/2 not DE); cl10 Reject (JA defense); cl11, cl16 Reject (JA/SA, oxidative stress; left unassigned by the authors); high-light and root samples Reject (treatment, other organ) | none (mature cauline leaves) |

### Markers added and raised

`markers_draft.tsv` went from 84 to 125 rows (41 new). New rows came from
Procko reporters or clusters and from Xia positions. Each ID was checked in
the paper's own table (Procko Supp Data Sets S1/S2/S3-S19; Xia Tables
S2/S3) and in UniProt (`*/uniprot_id_check.tsv`, plus GPAT3, KCS12, KCS20,
RNR1 and TSO2 checked here). TAS3 (AT3G17185) is non-coding and has no
UniProt entry, so `alt_id` is empty.

- **New rows (41):** Palisade_Mesophyll 9 (SPS4, DJC76 medium; AT1G70985,
  TAS3, SQE6, XTH6, ENH1, FAH1, UGT84A2 low); Spongy_Mesophyll 3 (KAN1
  function, YAB3, YAB5; all medium); Abaxial_Epidermis 5 (KAN1, FIL function
  medium; JAL22, PYK10, PDF1.2c low); Adaxial_Epidermis 2 (CER1, CER3 low);
  Bundle_Sheath 3 (THA2, ACO3 medium; EXT21 low); Hydathode 4 (AT3G16670,
  AT3G16660, AT1G62510 medium; AT1G65845 low); Pavement 2 (AT5G28630 medium,
  AT1G04040 low); Guard 1 (GASA9 medium); Trichome 2 (ANL2, ATL15 low);
  Phloem_Companion 1 (SAQR medium); Vascular 1 (DOT1 medium, coarse label);
  Epidermis 6 (AT4G23670, LTP5, PRP4, KCS12, KCS20, GPAT3, all low);
  S_Phase 2 (RNR1, TSO2 low, state).
- **Raised one level by a new independent study (11):** SULTR2;2 BS
  medium->high (Procko cl5, FACS); MAM1 BS medium->high (Procko BS
  reporter); CYP79F1 BS low->medium (Procko vein/BS reporter, Xia vascular);
  DIR11 Hydathode medium->high (Procko cl14 0.93 vs 0.004); AT3G11930 PP
  medium->high (Procko cl6 1.00 vs 0.09); MPK12 Guard medium->high (Procko
  cl12, Xia Fig 3A); DTX39 Abaxial_Epidermis medium->high (Xia position +
  Lee); LTP1 and APG Epidermis medium->high (Xia); AT1G09310 Epidermis
  low->medium (Procko cl0, Xia); FIL Spongy_Mesophyll low->medium (Procko
  FACS, Xia), now `function`.
- **Re-graded on direct evidence (2):** IQD22 Palisade low->medium (the
  Procko reporter itself, now read directly); CORI3 Spongy low->medium
  (Procko reporter + Xia position).
- **Support added without a raise:** SUC2, APL, SWEET11, SWEET12, FAMA,
  KCS6, ATML1, TGG1, TGG2 (already at their ceiling or high). Xia's merged
  vascular class does not resolve BS, XP, CC or PP, so CYP83A1, BCAT4,
  SULTR2;1, AAP6, AAP2 and PP2-A1 were not raised on it.
- **Characterization table** (`survey/characterization/characterized_markers.tsv`,
  `arabidopsis_leaf:` rows): KAN1 (Kerstetter 2001) and FIL (Siegfried 1999)
  give the abaxial-identity function used here. IQD22, FAH1, CORI3 and
  PDF1.2c in that table come from Procko 2022 itself, so they are not
  independent. PDF1.2c is `medium` there but `low` here (patchy and in a JA
  state cluster).

### Gaps closed

- **Spongy_Mesophyll and Abaxial_Epidermis** now have `function` markers
  (KAN1, FIL). Only conditionally closed: these TFs mark the whole abaxial
  domain (Xia ranks them in both lower epidermis and spongy; YAB3 reporter
  in both), so first call epidermis vs mesophyll, then use them to split by
  side.
- **Palisade_Mesophyll, Hydathode, Pavement, Adaxial_Epidermis:** better
  supported (reporters, a second study), but still no `function` marker.

### Gaps remaining

- **No `function` marker:** Palisade_Mesophyll, Xylem_Parenchyma, Pavement,
  Adaxial_Epidermis, Hydathode. Candidates outside this draft: PHB
  (adaxial; characterization table, primordium-stage) and PUP1, PHT1;4,
  NRT2.1 (hydathode; characterization table, `function` medium).
- **Palisade vs spongy is not separable transcriptionally** in either new
  study. Procko's scRNA clusters 1, 3 and 4 merge them, and IQD22 is poorly
  captured; Xia's subtype DEGs mostly describe the adaxial-abaxial axis.
  Treat palisade/spongy calls as a side split within Mesophyll, not as
  cluster identities.
- **Xylem_Parenchyma** still rests on Kim 2021 only (Xia merges it).
- Still not covered by any dataset: midrib/petiole collenchyma, senescing
  cells as a type (Procko cl2/cl8 are mixed stress-senescence states).

### Conflicts and corrections

- **PKS3 and DTX39 attribution:** the existing rows said both were
  "enriched in Procko et al. 2022" (as cited by Lee 2025). Neither gene is
  an adaxial or abaxial epidermis marker in the Procko tables. PKS3 is DE
  only in the unassigned stress cluster 16 (0.39 vs 0.05), and DTX39 only
  as weakly palisade-depleted in FACS (S2, -1.23). The Procko attribution
  was removed. The rows now rest on Lee 2025 + Xia 2022.
- **CORI3, FIL, KAN1, YAB3, YAB5 are abaxial-domain genes**, not spongy
  markers: Xia finds them in lower epidermis as well as spongy, and the
  YAB3 reporter is in both. CORI3 is also in BS (Procko reporter) and is
  JA-inducible.
- **Procko FACS "reference" (palisade-down) list ≠ spongy.** Its top genes
  are BS glucosinolate genes (SULTR2;2, MYB28, MAM1, THA2). Do not use S2
  as a spongy list.
- **Procko cl13 "sieve elements" is an S-phase cluster** (RNR1, TSO2,
  TK1a, histones; SEOR1/2 not DE). APL is also DE there, so it may be
  dividing phloem precursors. This adds to the proliferation-mislabel list
  above (Lee "SE", Nobori "Unknown").
- **GASA9 (AT1G22690):** a stomata-specific reporter in Procko 2022, but
  Lee 2025 21d c2 was called "Guard" from this gene alone and is pavement.
  Require FAMA before calling guard cells.
- **Palisade FACS genes with conflicting reporters:** UGT84A2 (top FACS
  gene, but the reporter is brightest in epidermis) and XTH6 (palisade +
  epidermis, epidermal in scRNA) kept `low`. ANL2 and ATL15 in the palisade
  list are trichome reporters (sort contamination). They were placed under
  Trichome.
- **Xia 2022 data quality:** about 100-300 UMI per cell, transcript
  spill-over between neighbours (plastid genes top the upper-epidermis
  DEGs; SWEET11/SUC2 in abaxial cells), Table S2 log2FC values are broken
  (up to 226), and the guard DE table is unusable. Only within-epidermis
  side genes absent from the neighbouring mesophyll list were used as
  positional support.
- **GEO sample titles for Procko JR11-2 populations are swapped or
  misleading** (GFP+ titled "Reference cells", GFP- titled "Palisade
  cells").
- **Name:** Procko's "LEB" is PYK10/BGLU23 (AT3G09260) in UniProt.

### Recommended label reference (revised)

The order above is unchanged: Tenorio Berrío 2025, then Lee 2025 for
nuclei. Neither new study is a better per-cell reference. Procko 2022 has
a single scRNA library and its labels are only in the 915 MB rds. Xia 2022
labels are spatial and cannot be matched to dissociated barcodes. Add:

5. **Procko 2022** is the reporter reference for Bundle_Sheath, Hydathode,
   Guard (GASA9), Pavement and PP/CC vein genes, and the only sorted-palisade
   data. Use its cluster markers, not its labels, and ignore cl13's name.
6. **Xia 2022** is the positional reference for leaf side (adaxial vs
   abaxial), for checking markers only.

### Could not verify

- The Procko 915 MB rds (per-cell labels, per-cluster cell counts) was not
  downloaded. Cluster sizes are unknown.
- Reporter images were not re-inspected for this collation. Reporter
  localizations come from the Procko review, which read the figures and
  supplementary PDF.
- Literature function claims for KAN1 and FIL come from the
  characterization table, whose DOIs were checked there. They were not
  re-read here.
- Xia's per-section h5ad files beyond `S1-1` and its raw data were not
  examined.
