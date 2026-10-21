<!-- Collated from the survey review of cotton_ovule (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Cotton ovule: collated cell-type marker resources

Collated 2026-10-20 from the four Part A reviews in this folder (`Qin2022/`, `Wang2023/`, `Zhang2025/`, `Sun2025/`; each has its own README). This was a desk collation. No single-cell data were reanalysed. I re-read the published tables (Qin 2022 Tables S3A-D, Wang 2023 Table S2, Chen 2025 Table S14/S11/S12) with pandas to check IDs and specificity. The scripts are in a maintainers' folder (scratch, so they will be purged).

Files:
- `expected_cell_types.tsv`: cell types expected from the anatomy of a *Gossypium hirsutum* ovule at -2 to +5 DPA, plus the boll tissues that appear only in whole-boll sections. I wrote it from anatomy, not from the published labels. `function_markers` counts the `function` rows in `markers_draft.tsv`.
- `markers_draft.tsv`: 68 rows in the skill schema (`ref_species=cotton`, `tissue=ovule`).
  - `ref_gene` is the HAU TM-1 v1/v1.1 ID (`Ghir_A01G000010`). Qin 2022 and Wang 2023 use it, and so does `cotton_anther/markers_draft.tsv`.
  - `alt_id` is the ZJU TM-1 v2.1 ID (`GH_A01G0001`) used by Zhang 2025 and Chen 2025, where a pairing could be made. It is empty otherwise.
  - CRI-TM1 `Gh_` IDs from Sun 2025 are given in `basis` only.
  - `requires=Gossypium` (a new trait tag) is set on the Fiber and Pavement rows.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Qin2022 | Qin Y ... Tu L. *Plant Biotechnol J* 20:2372 (2022). doi:10.1111/pbi.13918; PRJNA600131 (FASTQ only) | Protoplast scRNA-seq, 10x 3' v2. Outer integument (OI) only: the digestion released only OI cells. LF line at -1.5, -1, -0.5 and 0 DPA, plus Xu142 WT and fibreless fl at 0 DPA. One library per sample | LF_0d 1,703; LF combined 5,137; Xu142 731 + fl 1,465 | **Table**: Table S6 gives barcode→cluster for the 4 LF libraries, and the text gives cluster→type. Xu142/fl are cluster-level only | Medium (fibre: high). The only per-cell labels |
| Wang2023 | Wang D ... Wang K. *Genome Biol* 24:49 (2023). doi:10.1186/s13059-023-02886-0; PRJNA847210 | Protoplast scRNA-seq, 10x v2 + v3, one library each per genotype. Partial OI digestion (PTED), -2 to +2 DPA pooled. Xu142 WT vs fl | WT 18,064; fl 19,634 clustered | None. Cluster-level only (Table S2, Fig 1c) | Medium (fibre: high). Fibre C3 is validated by fl loss, XTH ISH and LCM |
| Zhang2025 (+ Chen2025) | Zhang J ... Zhang T. *Plant J* 121:e70064 (2025). doi:10.1111/tpj.70064 (paywalled). Audited through the open-access sister paper Chen R ... Zhang T. *Plant Commun* 6:101281 (2025), doi:10.1016/j.xplc.2025.101281. scRNA data PRJNA869296 (link to Zhang 2025 inferred) | Protoplast scRNA-seq, 10x, slices of whole 0-DPA ovules, J668 WT and fibreless #mml3s. The spatial platform is unknown (paywalled) | WT 7,566 + #mml3s 6,057 (12 clusters) | Cluster-level only. The cluster→type calls are in Chen 2025's text; the WT markers are Chen Table S14 | Low as a label source (fibre cl3: good) |
| Sun2025 | Sun X ... Ma X. *Nat Commun* 16:858 (2025). doi:10.1038/s41467-025-55869-z; PRJNA800600 | 10x Visium on whole boll cross-sections (8 sections, -1.5 to 5 DPA, 55 µm spots) plus protoplast scRNA-seq of ovules, 10x v3, one library per stage (-1.5, -1, 0, 1 DPA) | ST ~24.6k spots; scRNA 27,765 cells | Cluster-level only (Suppl. Data 2, Suppl. Table 10) | Low. Region-level spatial context; scRNA labels are mostly stage, stress or cell-cycle clusters |

ID systems: Qin and Wang use HAU (Wang 2019 *Nat Genet*). Zhang and Chen use ZJU v2.1 (Hu 2019 *Nat Genet*). Sun uses `Gh_` + 6 digits, which matches the CRI-TM1 format (inferred) even though Sun cites the HAU genome. Only Qin and Wang share IDs, so only their agreement is ID-exact.

## Per-cell-type verdict matrix

Key: A = Adopt, R = Revise, X = Reject, `-` = not reported, n/a = not captured by design.

| Expected type | Qin2022 | Wang2023 | Zhang2025/Chen2025 | Sun2025 |
|---|---|---|---|---|
| Fiber | A (LF_0d C5, combined C5, Xu142 C4; ISH, fl mutant, CRISPR) | A (C3; fl loss, XTH ISH, LCM) | A (cl3; absent in #mml3s). R cl1 "early fibre" (broad markers) | R: ST cl3/10/19 fibre region at 3-5 DPA (spots mix fibre and OI); scRNA cl13 is the 0-DPA fibre-initial candidate |
| Pavement (non-fibre epidermis) | A (LF_0d C2, combined C1/C3, Xu142 C0/C2/C3); R C3 (stress) | - (inside C4 catch-all) | R cl0/8 (~90% mutant cells, hypoxia/stress) | R scRNA cl3/15/10 ("outer integument", HD-ZIP IV ANL2, cuticle genes) |
| Outer_Pigment_Layer | A (LF_0d C0, combined C2, Xu142 C1); R C1/C4/C7 | R: C2 (flavonoid program, but mixed with phloem and G2/M cells; published as "intermediate fibre lineage") | - (unlabelled cl10 has CHI/LDOX/DFR/F3H; inferred OPL) | R scRNA cl7 (possible OI parenchyma) |
| Outer_Integument_Inner_Epidermis | - | - | - | - |
| Inner_Integument | n/a | n/a | - | R scRNA cl4/8 (no identity marker); X cl12 (sHSP stress); R ST cl4/8 (whole-ovule spots) |
| Nucellus | n/a | n/a | - | R scRNA cl2/5; X cl11 (S phase); X ST cl5; R ST cl13 |
| Chalaza / Funiculus | n/a | n/a | - | R scRNA cl14 (published "diaphragm"; funiculus/placenta candidate) |
| Vascular (Xylem, Sieve_Element, Phloem_Companion, Procambium) | - (Xu142 0-DPA C1 holds SUC2/IRX10/KOR, not called) | - (one SEOB gene in C2) | - | R: ST cl18 is phloem (published "Exocarp_3"); scRNA cl16 is a possible phloem cluster (PP2-A9) |
| Guard | - | - | - | - |
| Embryo_Sac / Endosperm | n/a | n/a | - | - (inside ST "nucellus" at 3-5 DPA) |
| Dividing_cells / S_Phase | R: C6 (S), C8 (G2/M) and combined C4 (S) were labelled OPL | X as a type: C1 "early fibre lineage" is S phase | cl2 (S) and cl9 (G2/M) correctly called proliferating, but used as the trajectory root | X scRNA cl11 "nucellus" (S phase) |
| Placenta / Pigment_Gland / Exocarp / Mesocarp (boll sections only) | n/a | n/a | n/a | R ST cl11 placenta; A ST cl15 gland (tentative); R ST cl17 exocarp; X ST cl12 (B-class MADS, so petal/stamen); X ST cl2/6/9/14 mesocarp (one section each) |
| Stress clusters (not types) | LF_0d C3, combined C1 (dehydration) | C5 (wound/ABA; possibly a state) | cl5 (HSP), cl6/7 (GST/WRKY) | scRNA cl1, 6, 9, 12 |

## Cross-study markers

Forty-one rows in `markers_draft.tsv` are supported by two or more datasets (rows whose second dataset is only a bulk table or a weak enrichment, such as HOX3_At, MYB109, FLA1 and PDF2_Dt, are not counted; neither are the eight `low` rows with conflicts or doubtful pairings). How each kind of support counts:

- Qin + Wang agreement is ID-exact (same HAU locus) and counts as independent support.
- Agreement with Chen 2025 (ZJU) or Sun 2025 (CRI) rests on an inferred pairing: same subgenome chromosome, collinear ordinal position (HAU number/10 vs ZJU number, offsets within ~0-160 positions) and the same annotation or AGI. It was not sequence-checked (see Could not verify).

Confidence was raised one level for cross-study agreement. It was not raised where all the support was weak enrichment (GhSCP2D) or where the pairing was doubtful (SVB A13, DET2).

Strongest (validated in one study, specific in another):

| Cell type | Gene (HAU / ZJU) | Evidence |
|---|---|---|
| Fiber | GhMYB25 Ghir_D04G020730 / GH_D04G2108 | Function (RNAi); fibre-specific in Qin, Wang and Chen; lost in both fibreless mutants |
| Fiber | E6 Ghir_D05G016260 / GH_D05G1629 | Qin ISH; Wang C3 FC 6.1; Chen cl3; Sun ST fibre region (E6.4) |
| Fiber | XTH Ghir_D11G006540 | Wang ISH; Qin fibre 0.45/0.05 and Xu142 0.64/0.06 |
| Fiber | DUF (glycine-rich) Ghir_D07G016770 / GH_D07G1684 | Qin ISH; Wang C3 marker (but expressed in fl C2); Chen cl3 |
| Fiber | GhHOX3_Dt Ghir_D12G028680 | CRISPR (Qin); specific in Qin and Wang |
| Fiber | GhHD1 Ghir_A06G015820 / GH_A06G1710 | Reporter + RNAi (literature); Qin and Chen fibre clusters |
| Fiber | alpha-expansins Ghir_D10G012330 / GH_D10G1269 and Ghir_A10G015240 / GH_A10G1626 | Specific in all four datasets (Wang: fl = 0), no ISH, so `medium` |
| Epidermis | GhPDF1 Ghir_D04G004030 / GH_D04G0386 | Reporter + RNAi (literature); pan-epidermal and fibre-biased in all four datasets |
| Outer_Pigment_Layer | CHI Ghir_D13G002250 / GH_D13G0214, CHI Ghir_A13G001970, LDOX Ghir_D08G019350, CHS, ANR | Qin OPL plus Wang C2 plus Chen cl10. None has ISH, so all are `medium` |
| Sieve_Element | SEOB-like Ghir_D03G018170 | Wang C2 marker plus Sun ST phloem cluster (SEOB.21, pairing inferred) |
| Dividing_cells / S_Phase | CYCB1;2 Ghir_A11G033420, TOP2, HTA12, H4 | Qin plus Wang (plus Chen cl9 for CYCB) |

The other cross-study Fiber rows are cuticle and wall genes enriched in fibre initials in Qin, Wang and usually Chen: CER1, the DCR homeologs, HOTHEAD, the APG-like GDSL lipases, DUF642, glycine-rich proteins, GASA4, AnxGb6 and the SVB/SVBL DUF538 family. Their evidence is `characterized_enriched` or `expression`, at `medium`.

## Grading notes

- `function`: genes with a cotton loss-of-function or reporter result that defines fibre or epidermis (MYB25, MYB25-like, HOX3, HD1, PDF1, PDF2, TCP14, MML4, MYB109, FLA1, MYB2). It is also used for FDH, SUC2, IRX10 and the G2/M genes, whose defining function is known from Arabidopsis.
- Two `function` fibre-fate genes are not cluster markers in any dataset, so they are `medium`/`low`: MYB25-like At (broad OI ISH) and Dt.
- Within Qin, the LF_0d and Xu142 libraries were not counted as independent studies. Neither were Zhang 2025 and Chen 2025 (same lab, same scRNA data).
- Rows added at collation, i.e. not in the reviews: the Qin∩Wang fibre genes (HOTHEAD x2, APG x3, DUF642, glycine-rich x2, eggshell-like, GASA4, DCR D08, the SVB/SVBL HAU loci), CHI x2, LDOX x2, SEOB-like, SUC2-like, IRX10-like, the PDF2 Dt alt_id and FDH. Each was found by intersecting Qin Table S3 with Wang Table S2, or by AGI in Wang Table S2.
- New cell-type names: `Fiber`, `Pavement` (used in the sense of non-fibre epidermis), `Outer_Pigment_Layer`, `Outer_Integument_Inner_Epidermis`, `Funiculus`, `Embryo_Sac` and `Placenta`. These names are already used by other tables or drafts: `Epidermis`, `Guard`, `Xylem`, `Sieve_Element`, `Phloem_Companion`, `Dividing_cells`, `S_Phase`, `Inner_Integument`, `Nucellus`, `Chalaza`, `Endosperm`, `Pigment_Gland`, `Exocarp` and `Mesocarp`.
- `requires=Gossypium` is a new trait tag (cotton_anther uses it for Pigment_Gland). If the table enters the skill, add `Gossypium → eudicot` to `IMPLIES` in `map_markers.py`. `tissue=ovule` is new too.

## Gaps (no validated `function` marker)

Pavement, Outer_Pigment_Layer, Outer_Integument_Inner_Epidermis, Inner_Integument, Nucellus, Chalaza, Funiculus, Guard, Embryo_Sac, Endosperm, Procambium, Sieve_Element, S_Phase, Placenta, Pigment_Gland, Exocarp, Mesocarp. Phloem_Companion and Xylem have only a `low` function row each.

- The non-fibre epidermis is defined only negatively (L1 genes without fibre genes) plus the weak Erg6 ISH.
- No dataset resolves inner-integument layers or nucellus with identity markers.
- Vascular types are unannotated everywhere except Sun's ST phloem cluster.

For these types, use the Arabidopsis seed/ovule drafts via homology: `arabidopsis_ovule`, `arabidopsis_seed` (Inner_Integument, Endothelium, Nucellus, Chalaza) and the skill's Arabidopsis tables (Guard, Sieve_Element, Phloem_Companion, Xylem).

## Recommended label reference

**Qin 2022** is the label reference. Its labels are the only per-cell ones (Table S6 barcodes, 4 LF libraries), and its fibre call has ISH, a fibreless-mutant scRNA control and CRISPR support. It covers only the outer integument. Use it as follows:
- Adopt Fiber (LF_0d C5 / combined C5), Pavement (C2, merging C3 as a stress state) and Outer_Pigment_Layer (C0/C1).
- Relabel C6/combined C4 as S_Phase and C8 as Dividing_cells.
- Treat C7 (terpene synthases) as an unresolved candidate (possible secretory cells).
- Barcodes need re-running Cell Ranger on the SRA FASTQ. The SRA stage names (LF_0d/12h/24h/36h) do not match the paper's stages, so check the cell numbers against Table S1.

Wang 2023 is the best source for the fibre marker set and the WT/fl contrast (cluster-level only; C1 is S phase, C2 is mixed, C4 is a catch-all). Chen 2025 Table S14 adds 0-DPA whole-ovule clusters (fibre cl3; cl10 is probably the pigment layer; cl2/cl9 are cell-cycle states). Sun 2025 is useful only for region-level spatial hypotheses.

## Conflicts and corrections to the reviews

- **GhRDL1.** Chen's GH_A05G0505 is fibre cl3, but the positional HAU counterpart Ghir_A05G005110 (RD22-like) is a Wang C5 marker (2141 vs 31 in C3), in Qin LF_0d C4 (an OPL substate) and in Xu142 C5. Kept as Fiber `low` with the conflict in `basis` (the Zhang review had `medium`). Wang C5 and Qin LF_0d C4 share RD22/BURP + GASA genes and may be the same population.
- **GhMYB2.** Wang 2023 names Ghir_A06G008810, while Chen 2025 S11 names GH_A08G1934 (different chromosome). Lowered to `low` (barely detected).
- **GhFLA1.** Wang 2023 names Ghir_A01G008090 (A01), while Chen 2025 S11 names GH_D09G1182 (D09). Kept at `medium`, with the conflict in `basis`.
- **AGI disagreements for the same pair.** These are paralogs within one family, not errors, but they mean the AGI cannot be used to pair IDs:
  - MYB25: AT5G15310 (Wang) vs AT3G01140 (Chen).
  - HD1: AT4G21750 vs AT4G04890.
  - SVB family: AT1G56580 vs AT1G09310.
  - DUF642: AT2G41800 vs AT2G41810.
- **SVB/SVBL** were `function` in the Zhang review on the strength of a VIGS result seen only in the abstract. Here they are `characterized_enriched`. The SVBL genes are near-ubiquitous in Chen (pct_out 0.6-0.85), but fibre-biased in Qin and Wang.
- **GhMYB25-like Dt** was `function`/`medium` in the Qin review. It is `low` here, because it is not fibre-enriched in any dataset.
- **Wang C2** holds the flavonoid program (CHS, CHI, LDOX, ANR), a SEOB gene (255 vs ≤18) and CYCB1;2. It is a mix of pigment-layer, phloem and dividing cells, which supports the review's Revise.
- **Qin Xu142 0-DPA C1** (Table S3C) enriches SUC2, IRX10, KOR and IRX14 along with Erg6. This possible vascular admixture was not noted in the Qin review.
- **Chen cl10 and cl9** (unlabelled in the Zhang review) carry CHI/LDOX/DFR/F3H and cyclin B. I infer Outer_Pigment_Layer and Dividing_cells.
- **PDF1 citation.** The Qin review gives Deng 2012 *Plant Cell Physiol*; the Wang review gives *Plant Physiol*. I used *Plant Physiol* (GbPDF1), but did not re-check it.
- **E6.** Qin's ISH probe is the D05 copy (Ghir_D05G016260). Wang's C3 marker list instead has the A05 copy (Ghir_A05G016440), while the D05 copy is C3-enriched (FC 6.1) but not in Wang's list. Both copies are in the table.
- These review flags are carried over unchanged:
  - Wang Table S2 cites the GaMYB2 DOI for GhHOX3.
  - The HbdA SP6 primer in Qin Table S12 is named for Ghir_D01G020590.
  - Wang lists GhMYB25 as a C3 marker in one sheet but as a C4 DEG in another.

## Markers not in the table (no HAU ID could be paired)

These are kept out of `markers_draft.tsv` so that `ref_gene` stays a single ID system. They are worth pairing by BLAST when a cotton proteome is available:

| Cell type | Gene | Notes |
|---|---|---|
| Fiber | GhMYB106 GH_A04G1759 (ZJU) ≈ Gh_A04G171200 (CRI) | Fibre-enriched in Chen cl3 (0.65/0.17) and Sun ST cl19 (0.53/0.04); a cross-study pair between ZJU and CRI |
| Fiber | GhPPO7 GH_A06G2011 (ZJU) | Chen annotation marker (expression) |
| Fiber (3-5 DPA elongation) | Gh_A10G219300 KCS19.4, Gh_D01G000600 HOS3.7/ELO, Gh_A03G153800 KCR1.2, Gh_D04G007600 LRX2.1, Gh_D09G117000 FLA11.3, Gh_D12G200300 bZIP43.11 (CRI) | Sun ST fibre region only |
| Pavement/Epidermis | Gh_A11G092100 ANL2.3 (CRI) | Sun scRNA cl3 |
| Sieve_Element | Gh_A03G010200 SEOB.3, Gh_A03G009800 SEOB.1 (CRI) | Sun ST cl18 |
| Placenta | Gh_A09G062900 BEE3.1, Gh_D09G057400 BEE3.6 (CRI) | Sun ST cl11; BEE3 OE/RNAi alters fibre initiation |
| Pigment_Gland | Gh_D05G199000 CYP82A3.12, Gh_D13G235800 AOP1.30 (CRI) | Sun ST cl15 |
| Exocarp | Gh_A07G148100 WSD1.5, Gh_A04G109500 GPAT6 (CRI) | Sun ST cl17 |
| Petal/stamen (contaminant) | Gh_D02G087300 GLO, Gh_A02G084500 PMADS2.1 (CRI) | Sun ST cl12 |
| Outer integument, focal (likely its vascular bundle) | Gh_A09G193100 DOX2, Gh_D11G090900 SBT4.14, Gh_A03G188900 GH3.6.2, Gh_D04G160000 SWEET15 (CRI) | Sun ISH |
| Dividing_cells / S_Phase | GH_A07G1334 UBC20 (cl9 0.51/0.01), GH_D08G0035 HTA (ZJU) | Chen |

Also excluded: Qin LF_0d C7 terpenoid cyclase Ghir_D09G000800 (0.73/0.04). It is a possible secretory or gland-like subtype, but the identity is unknown. GhACTIN1 Ghir_A11G006130 is broadly expressed and is not a marker.

## Overlap with existing skill tables

There is no cotton or ovule table in `references/markers/`. By Arabidopsis best hit:
- PDF1 (AT2G42840), ATML1 (AT4G21750, the HAU best hit of GhHD1) and FDH (AT2G26250) are Epidermis rows in `arabidopsis_leaf.tsv`.
- SUC2 (AT1G22710) is Phloem_Companion.
- SEOR1 (AT3G01680), the best hit of SEOB-like Ghir_D03G018170, is Sieve_Element.

Cell-type assignments agree in all five cases.

Against the not-yet-merged `datasets/cotton_anther/markers_draft.tsv`, the same HAU loci appear with the same cell types: Ghir_D04G004030 PDF1 and Ghir_A13G020120 FDH (Epidermis), Ghir_A11G033420 CYCB1;2 and Ghir_D01G009690 CDKB2;2 (Dividing_cells). A combined cotton table could merge these rows.

## Could not verify

- **Database ID checks.** UniProt returns 0 hits for Ghir_, GH_ and Gh_ locus names (tested Ghir_D04G020730, GH_D04G2108, Gh_D04G040400). CottonGen (including the `cottongen_downloads` path) returns 403 behind Cloudflare, and cottonfgd.net returns a redirect to a bot check; I did not try to get around either. NCBI has no annotated HAU, ZJU or CRI assembly (only the HudsonAlpha v2.1/v3 and UTX assemblies with LOC/Gohir IDs). So every ID rests on the papers' own tables, which I re-read by script.
- **Cross-system pairings** (HAU ↔ ZJU ↔ CRI) are inferred from chromosome, collinear position and annotation, not from sequence. A BLAST of the proteomes (HAU v1.1, ZJU v2.1, CRI v1 from CottonGen in a browser) would settle them.
- **Zhang 2025's own text, figures, supplements and spatial data** are paywalled, and no spatial accession was found. Its SVB/SVBL VIGS and spatial results are unverified.
- **Sun 2025's gene-ID system** is unstated: CRI by format, although HAU is cited.
- **Other searches.** I did not run a new literature search beyond the four reviews: other cotton ovule single-cell datasets, e.g. Zhao 2026 JXB 1-DPA Visium (PRJNA1074265), were not reviewed.
- **No per-cell data was examined.** Specificity numbers are pct.1/pct.2 or cluster means from the published tables. Wang WT clusters carry ambient fibre RNA, so judge fibre specificity against fl.
- **Literature citations in `source`** are given by author and year (Machado 2009, Walford 2011/2012, Shan 2014, Deng 2012, Wang 2013, Suo 2003, Pu 2008, Huang 2013, Luo 2007, John & Crow 1992, Wu 2018, Bedon 2014, Ji 2003, Li 2007). Their DOIs were not looked up.
