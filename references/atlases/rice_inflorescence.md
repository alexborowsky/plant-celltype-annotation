<!-- Collated from the survey review of rice_inflorescence (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Rice inflorescence (young panicle): collated cell-type marker resources

Collated 2026-10-20 from two dataset reviews (Wang2025, reviewed 2026-10-19; Zong2022, reviewed 2026-10-19).
Desk review only: no data were re-analysed. Per-dataset audits are in `Wang2025/README.md` and `Zong2022/README.md` (left unchanged).

Files written here:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 36 expected types/states (32 from panicle anatomy, IM stage to meiosis, plus 4 added 2026-10-20 for Jing2026's later stages), with `function` marker counts from `markers_draft.tsv` |
| `markers_draft.tsv` | 72 rows, 71 genes after the 2026-10-20 update (39 rows, 38 genes before), skill schema plus `alt_id`. `ref_gene` = MSU7 `LOC_Os`, `alt_id` = RAP-DB (as in `rice_root.tsv`). Field counts validated (13 columns on every line) |
| `README.md` | this file |

`tissue` is `inflorescence` for organ-specific rows and `any` for the 3 cell-cycle rows. `inflorescence` is a new value: the skill README lists only `leaf`, `root`, `any`, so pass `--tissue inflorescence --tissue any` to `map_markers.py`. No `requires`/`excludes` tags were needed. All rows are rice genes, and none is a C3/C4 photosynthesis gene. Grass-only organs (glume, lemma, palea, lodicule) have no counterpart outside grasses, so add `requires=grass` before using these rows across species via homology.

## Datasets

| Dataset | Citation | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Zong2022 | Zong J ... Yuan Z. *New Phytol* 234:494-512 (2022). doi:10.1111/nph.18008; GEO GSE185068 | BD Rhapsody, protoplasts (the survey's "10x" is wrong) | 37,571 after QC, of which ~29,829 are inflorescence (S1 < 2 mm, S2 2-3 mm, 2 reps each). The other 7,742 are a flag-leaf control library | RAP (`Os01g0100100`) | **none** (authors' labels not public). scPlantDB re-annotation (7 labels, 24,028 cells; 51.3 MB h5ad, not downloaded) | medium (review); labels and markers are all inferred because the Wiley full text and SI are behind a bot check |
| Wang2025 | Wang X ... Gu X. *Nature* 644:722-730 (2025). doi:10.1038/s41586-025-09251-0; GEO GSE232863 | 10x Multiome (nuclei, RNA + ATAC) | 44,248 panicle nuclei: SP3 10,931; SP4 9,408; SP6 6,452; SP8 17,457 | MSU7 in the paper; RAP on the portal | **table**, SP8 only (17,457 cells, 10 labels, from the portal Plotly page; 100 barcodes duplicated across replicates). SP3/4/6 not public | low (review) |
| Jing2026 | Jing Y ... Chen F. *Cell* (2026). doi:10.1016/j.cell.2026.09.023; PMID 42838048 | snRNA (DNBelab C4) + Stereo-seq (ZH11 T2T IDs `ZH01G...`) | see the update section below | ZH11 | **table** (`Jing2026/portal/`) | medium (reviewed 2026-10-20; see the update section) |

The two reviewed datasets barely overlap in stage. Zong2022 covers IM to FM (S1-S2, roughly Sp1-Sp6). Wang2025 SP3/SP4 overlap the late end of that window, and SP6/SP8 reach anthers with tapetum and meiocytes.

## Per-cell-type verdict matrix

Rows are canonical names (marker-table names). "-" means the dataset has no label for the type.

| Canonical type | Zong2022 | Wang2025 |
|---|---|---|
| Meristem (umbrella) | Revise: "Meristem" (5,611 cells; LOG/OSH1; cell cycle not excluded) | - |
| Inflorescence_Meristem | Revise: IM subclusters | - |
| Branch_Meristem | Revise: BM (primary, elongated primary, secondary); OsAUX1 | - |
| Spikelet_Meristem | Revise: SM | - |
| Floral_Meristem | Revise, closest to Adopt: floret/FM subclusters 5/7 (DWT1 + dwt1 genetics) | Revise: "Floral meristem" SP3/SP4 (~40-51%; probe is the defensin CAL1 staining the whole floret) |
| Glume | Revise: rg/sl subcluster 9 (YABBY ID ambiguous) | Revise: "Spikelet identity cells" = "Cryptic bract" (one cluster, two names; KCS4 marker taken from Zong) |
| Bract | - | see Glume row ("Cryptic bract") |
| Lemma | Revise: subcluster 0 (OsMADS1 also marks palea) | - (never labelled) |
| Palea | - (only via the dwt1 phenotype) | Revise: "Palea" SP3/SP4 = hull primordia (probe RepA, also the SP8 ovary-wall top gene) |
| Mesophyll (hull chlorenchyma) | Revise: "Leaf" (mostly the flag-leaf library; batch-confounded) | **Reject** as "Ovule" (19.6% SP8, ~37% SP6; CAB/PSBO/RBCS3); probably hull chlorenchyma |
| Epidermis | Revise: meristem subcluster 7 (ROC genes; chitin-response terms) | Revise: "Epidermis" (hull + B-class organ epidermis merged) |
| Lodicule | - | Revise: "Lodicule" (13%; defense genes, no B-class MADS) |
| Stamen (B-class organ) | - | Revise: "Filament" (in situ stains locule contents; B-class MADS) and "Stamen" SP4 (PR3 chitinase probe; ED Fig 8c calls it "Stigma") |
| Tapetum | - | **Adopt at SP8 only** (TDR, EAT1, OsC6, RTS, RAFTIN1; SP8 DE). The paper's SP6 tapetum is not found in the GEO SP3-SP6 nuclei: all five genes <=2.5% in every cluster (skill test L3, 2026-10-22; Wang's SP6 may be earlier than Ikeda Sp6) |
| Meiocyte | - | Revise: "Pollen mother cell" = anther locule cells (no meiosis genes; MEL1/PAIR1 0-3% in SP3-SP6, L3) |
| Carpel / Ovule | - | Revise: "Stigmata/Stigma" = carpel with ovule genes (DL, OsMADS58, OsMADS13) |
| Ovary_Wall | - | Revise: "Ovary wall" (identity uncertain) |
| Ground_Tissue / axis | Revise: "Rachis" (organ label); Reject: "SSC" (spikelet supporting cells, no anatomical counterpart) | - |
| Vascular | - (inside Rachis) | **Reject**: "Vascular" = defense/PR state |
| Other | Revise: "Spikelet" (organ label); Reject: "SIC" (spikelet identity cells, a state) | Adopt as unknown: "Panicle unknown" |

Verdicts are desk review (probe and DE reading); re-check in data. A per-nucleus test on the GEO SP3/SP4/SP6 object (skill test L3, 2026-10-22) confirmed the Ovule, Vascular, Stamen, Lodicule and Floral-meristem doubts, and found:
- **No tapetum or meiocyte programme at SP3-SP6** (see the Tapetum row). Do not expect tapetum before SP8 in these data.
- **The Palea probe OsCP1 (Os11g0255300) marks a cysteine-protease cluster present at all stages** (65% vs 17%). Its programme (MC9-like metacaspase MCP2f 51% vs 3%, BFN1, RD21/CEP1-like proteases) is developmental PCD, but it lacks xylem identity genes (VND7, XCP1/2, CESA4 <5%) and its kNN neighbours are JA/hull clusters: a PCD programme of an unidentified (possibly degenerating) organ, not palea, not senescence and not xylem (re-test with v0.2.0, desk review; re-check in data). **Xylem** in SP3/SP4 is a ~180-cell subset inside the procambium cluster: subclustering it (recomputed, batch-corrected PCA) gives a group with ACL5 35% vs 5%, the XCP2 RBH (Os05g0108600) 15% vs <=2%, WAT1 61%, a VND-like NAC (Os10g0532000) 26%, PXY 39%, LAX2 and LOG1, and no secondary-wall CESA yet (young xylem; user review 2026-10-22).
- SP6 forms a stage island that Harmony did not integrate, with ambient chloroplast RNA (psbA in 54-83% of SP6 nuclei). Subcluster it separately.
- A JA/wound programme (TIFY10C 77-85%) defines about 9% of nuclei: a dissection response state.

No type is labelled in both datasets with agreeing evidence. The same name points to different things in the two studies: Zong's "spikelet identity cells" are a rejected state label, while Wang's "spikelet identity cells" are a bract/glume-like cluster that only reuses a Zong marker (KCS4).

## Cross-study markers

**No gene ID is a validated or cluster-specific marker for the same type in both reviewed single-cell datasets.** Their marker lists share no IDs. They cover different stages, and Zong's markers could not be checked against its own tables. Cross-study agreement here therefore means independent literature localization (in situ, promoter, mutant) plus single-cell enrichment in Wang2025. Nine rows meet that bar:

| Gene | MSU / RAP | Type | Studies | Effect on confidence |
|---|---|---|---|---|
| WDA1/GL1-5 | LOC_Os10g33250 / Os10g0471100 | Epidermis (anther-biased) | Jung 2006 Plant Cell in situ; Wang 2025 in situ + DE | raised medium to high |
| RTS | LOC_Os01g70440 / Os01g0929600 | Tapetum | Luo 2006 PMB promoter; Wang 2025 DE | raised medium to high |
| RAFTIN1 | LOC_Os08g38810 / Os08g0496800 | Tapetum | Wang 2003 PNAS; Wang 2025 DE | raised medium to high |
| TDR | LOC_Os02g02820 / Os02g0120500 | Tapetum | Li 2006 Plant Cell; Wang 2025 DE | already high |
| EAT1/DTD | LOC_Os04g51070 / Os04g0599300 | Tapetum | Niu 2013 Nat Commun; Wang 2025 DE | already high |
| OsC6 | LOC_Os11g37280 / Os11g0582500 | Tapetum | Zhang 2010 Plant Physiol; Wang 2025 DE | already high |
| DL | LOC_Os03g11600 / Os03g0215200 | Carpel | Yamaguchi 2004 Plant Cell; Wang 2025 DE ("Stigmata") | already high |
| OsMADS13 | LOC_Os12g10540 / Os12g0207000 | Ovule | Lopez-Dee 1999; Dreni 2007 Plant J; Wang 2025 in situ + DE | already high |
| OsMADS58 | LOC_Os05g11414 / Os05g0203800 | Carpel | Yamaguchi 2006 Plant Cell; Wang 2025 DE | kept medium (also stamen) |

Not raised, despite appearing in both datasets or in a dataset plus the literature:
- **OsMADS8/24** (Os09g0507200): Zong FM subcluster (inferred), but DE in four Wang SP8 clusters. Kept low.
- **OsMADS16, OsMADS2, OsMADS4**: the literature puts them in lodicule and stamen, while Wang has them in "Epidermis"/"Filament" and not in "Lodicule". Kept medium.
- **KCS4** (LOC_Os02g56860): Wang reused it from Zong, so the two are not independent. Not carried.

## Marker table summary (`markers_draft.tsv`)

- From Zong2022 (11 genes in the review): carried 10. Dropped OsYAB1/FIL1 (Os07g0160100), which is expression-only and ambiguous ("OsYAB1 (TOB1)" conflates two loci) and is DE in Wang's PMC/Lodicule/Stigmata clusters. OsMADS1 is split into Lemma and Palea rows. OsAUX1 was downgraded from the review's `function` to `characterized_enriched`/low: an auxin carrier with a branching phenotype is not BM-specific, and its enrichment is inferred. Zong's single-cell enrichment is unverified for every gene, so these rows are graded on the literature.
- From Wang2025 (29 genes in the review): carried 19 (tapetum, meiocyte, epidermis, carpel, ovule, B-class). The two in-situ-only locule genes (LOC_Os11g34270, SCP61) were lowered from medium to low because the cluster lacks meiosis genes. Not carried: probes for rejected or doubtful types (CAL1, RepA/OsCP1, PIOX, RMC, DFOT1, ASN1, OLP1, AGP41P, PR3 LOC_Os04g41640), LOC_Os01g24790 (not in Oryzabase or UniProt), KCS4 (not independent), and RBCS3 (photosynthesis; **do not use as an ovule marker**).
- Added from the literature to fill gaps named in the reviews (IDs from Oryzabase and checked in UniProt): TAW1 (IM), G1/ELE (sterile lemma), REP1/OsTCP24 (palea), OsMADS3 (stamen), MEL1 and PAIR1 (meiocytes), ROC1 (L1 epidermis). CycB1;1, CDKB2;1 and OsPCNA are copied from `rice_root.tsv` (same IDs) so that meristem/FM clusters can be screened for cell-cycle states.
- Evidence tiers: 30 `function` (16 high, 14 medium) and 9 `characterized_enriched` (3 medium, 6 low). There are no `expression` rows.
- ID checks: every MSU-RAP pair matches Oryzabase (`../../reference/rice/oryzabase_gene_list.tsv`), and UniProt (taxon 39947) confirms the pair for 32 of 38 genes. The other 6 (REP1, LOC_Os06g14350, GELP67, LOC_Os11g34270, SCP61, S40-5) have no UniProt entry carrying the MSU ID. REP1's UniProt entry for Os09g0410500 lacks an MSU ID, so the pair comes from Oryzabase only. All RAP IDs except OsMADS13, OsC6, RTS, RAFTIN1, LOC_Os06g14350 and SCP61 are in the Zong2022 S2-1 matrix gene list. These are late anther/ovule genes, so their absence fits the stage.
- DOIs: every `source` DOI was resolved in Europe PMC. Seventeen recalled DOIs were wrong and were replaced (for example, PAP2 is Kobayashi 2010 *Plant Cell Physiol*, REP1 is Yuan 2009 *Plant Physiol*, and G1 is 10.1073/pnas.0907896106).

## Gaps (expected types with no `function` marker)

Branch_Meristem (OsAUX1 low only), Bract, Mesophyll/hull chlorenchyma, Trichome, Guard, Endothecium, Middle_Layer, Microspore, Filament (and connective), Ovary_Wall, Stigma_Style, Ground_Tissue (rachis, pedicel, rachilla), Procambium, Phloem and Xylem in the panicle. Lemma has only OsMADS1, which is shared with palea. The IM, SM and FM markers are positional and overlap each other.

For Phloem and Xylem, `rice_root.tsv` has OsSUT1 and OsCESA4 (`function`, root context). For leaf types from the flag-leaf library, use the leaf tables via homology.

## Recommended label reference

- **Wang2025 SP8 portal labels, Tapetum only (SP8 stage only)**, as an adoptable per-cell reference (`Wang2025/panicle_SP8_portal_labels.tsv`). Relabel "Stigmata" to Carpel and treat "Epidermis"/"Filament" as B-class organ/epidermis hypotheses. Do not use "Ovule", "Vascular" or "Lodicule".
  - Source: the portal Plotly page http://www.elabcaas.cn/scmr/tissues/tissue_umap/scmr.sp.umap.scatter.html (one Plotly trace per label; each point's `text` is `SP-<label>-<barcode>`, with x/y = UMAP; URL checked 2026-10-22). Barcodes are bare 16-mers with no replicate tag; 100 occur twice (88 with different labels), so drop duplicates before joining.
- **Gene IDs:** paper tables use MSU7, the portal DE plots use RAP-DB. Convert with the skill's `references/annotation/rice_msu_rap.tsv.gz` (from RAP-DB's RAP-MSU file); the Oryzabase list cited below is in the survey folder only.
- **Zong2022 has no usable per-cell labels.** Use its GEO RAP-ID matrices (11-22 MB each) for de novo annotation of early stages with this marker table. Use the flag-leaf library (L) as a negative/contamination reference, and screen meristem/FM clusters for Dividing_cells/S_Phase first. scPlantDB's 7-label re-annotation is a coarse third-party cross-check only.
- For IM-to-FM stages, neither dataset gives reference labels. Rely on the function markers (LOG, OSH1, TAW1, OsMADS34, DWT1, TOB1, G1, OsMADS1, REP1, OsMADS6).
- Once reviewed, Jing2026 may become the better reference: its portal has per-cell labels for inflorescence, spikelet, stamen and pistil, including spatial data. Its curated marker list partly reuses Zong2022 markers (source 10.1111/nph.18008), so it will not be independent of Zong for meristem and bract types.

## Conflicts and corrections to the reviews

- Platform: Zong2022 is BD Rhapsody, not 10x (survey entry wrong; the GEO text also mentions Cell Ranger).
- Zong2022 cell count: 37,571 includes the 7,742-cell flag-leaf library, so the inflorescence total is ~29,829.
- "OsYAB1 (TOB1)" (secondary summaries of Zong) conflates TOB1/OsYABBY5 (Os04g0536300) and OsYAB1/FIL1 (Os07g0160100). Only TOB1 is carried.
- Name collisions: "REP1" is both the palea TCP (Os09g0410500, carried) and a cysteine protease (Os01g0907600). "RepA/OsCP1" (LOC_Os11g14900, Wang's palea/ovary-wall probe) is a third, unrelated gene. "OsAUX1"/"OsLAX1" are synonyms of RAU1 (Os01g0856500), not LAX1 (Os01g0831000). "OsSCL1" matches 3 loci and was not carried. ZEP1 is ambiguous in Oryzabase (ABA1/ZEP vs the synaptonemal ZEP1) and was not added.
- Wang2025 labels: "Spikelet identity cells" and "Cryptic bract" are one cluster; SP4 "Stamen" is "Stigma" in ED Fig 8c; the floral-meristem probe is LOC_Os02g41904 in the figures but LOC_Os02g41940 in the primer table.
- Grading changes from the reviews: OsAUX1 function to characterized_enriched/low; Wang locule genes medium to low; RTS and RAFTIN1 medium to high (literature + single-cell agreement); WDA1 medium to high.
- DL is also expressed in the leaf and lemma midrib, so flag-leaf cells can express it. OSH1 is also expressed in axis ground tissue: Jing2026's portal lists it for "spikelet supporting cells".

## Overlap with existing skill tables

The only rice table in `references/markers/` is `rice_root.tsv`. The overlap is 3 genes, all cell-cycle states copied on purpose: CycB1;1 (LOC_Os01g59120), CDKB2;1 (LOC_Os08g40170) and OsPCNA (LOC_Os02g56130). No organ-specific gene is shared. The root Epidermis, Phloem and Xylem rows use different genes and were not copied. Every inflorescence cell type here is new to the skill. The skill was not edited.

## Could not verify

- Zong2022 full text, figures and Supporting Information (Wiley Cloudflare check): every Zong cluster label, its markers and its in situ gene list are inferred. Its rows are graded on the literature, not on the paper.
- Wang2025 SP3/SP4/SP6 labels and DE (not deposited), and the 5.1 GB `GSE232863_scRNA_omics.Rds` (not downloaded).
- The localization statements in `basis` for the literature genes come from paper titles and abstracts (titles checked in Europe PMC) plus recalled content; the primary figures were not re-read. This matters most for PAIR1 (PMC expression), REP1 (palea primordium in situ), ROC1 (L1 in situ) and FOS1 (no localization claimed).
- RAP-DB (refuses scripted access). Oryzabase and UniProt were used instead.
- Jing2026 was not reviewed; its portal files are in `Jing2026/portal/`.

## Update 2026-10-20: gap-fill reviews

One new review was merged: Jing2026 (`Jing2026/README.md`, `Jing2026/evaluation.tsv`, `Jing2026/markers_carried.tsv`). The sections above are kept as written for the first two datasets. Where they conflict with this section, this section wins (file counts, the Jing2026 row of the datasets table, gaps, recommended reference). The last "Could not verify" line above ("Jing2026 was not reviewed") is superseded.

### New dataset

| Dataset | Citation | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Jing2026 | Jing Y, Chen Q, Chen Y, Yan W ... Xu X, Chen F. A spatiotemporal lifecycle atlas decodes spatial coordination in rice. *Cell* (2026), online 2026-10-06. doi:10.1016/j.cell.2026.09.023 (checked in Europe PMC, PMID 42838048). CNGB CNP0008591; STOmicsDB STDS0000421 | snRNA-seq (DNBelab C4 / DNBSEQ-T7) + Stereo-seq. Stamen sections use cell-boundary bins; inflorescence and pistil sections use square bins. ZH11 T2T genome | In-scope snRNA: Inflorescence Formation 102,586 (0.1 to 3-5 mm panicles); Spikelet 79,484 (sp6, sp7, sp8e, sp8L); Stamen 49,685 (S6-S12); Pistil 120,519 (P1-P7). Stereo-seq: a few hundred bins per label | ZH11 (`ZH01G...`); no RAP/MSU crosswalk in the paper. Carried rows were mapped by portal symbol + Oryzabase + UniProt + same chromosome within ~1 Mb (no BLAST) | **table**: per-cell labels for snRNA (`Jing2026/portal/ZH11_SC_per_cell_labels.tsv.gz`, 2.9 MB) and Stereo-seq; h5ad files not downloaded (sizes in `Jing2026/portal/h5ad_files_sizes.tsv`) | medium. Stamen strongest; early panicle and spikelet labels weak; full text not accessible |

Stage coverage now extends past meiosis. Jing2026 reaches mature pollen (S12) and pistil P7, so four types were added to `expected_cell_types.tsv`: Pollen, Connective, Carpel_Epidermis and Abscission_Zone. Filament no longer includes the connective.

### Verdicts (Jing2026), mapped to canonical names

| Canonical type | Jing2026 label(s) | Verdict |
|---|---|---|
| Inflorescence_Meristem | Inflorescence_meristem_1 (462; 42 ST bins) | Revise: right stage (0.1 mm panicle), but spatial DE markers only (OsPLT1, OsEm) |
| (none) | Inflorescence_meristem_2 (5,332) | **Reject**: grows to 2,886 nuclei at 3-5 mm, after IM abortion; marker SHAT1 is an abscission-zone gene |
| Branch_Meristem | Branch_meristem_1 (+ ST Branch_meristem_2) (1,474) | Revise: markers copied from Zong 2022 |
| Dividing_cells (state) | Spikelet_primordia (5,947) | Revise: a proliferation state labelled as a type (CDKB2;1, CycB1;1, CDKB1;1, CYCA2;1, KCH1) |
| Bract | snRNA Bract (21,254; 20.7%) | Revise, not usable: merged; markers copied from Zong mix cuticle, meristem-identity and WOX3 genes |
| Bract / Trichome | ST Bract_primordia (26 bins) / Bract_hair_1-3 (684 bins) | Revise: Bract_primordia has OSH6, PLA1, PLA2; bract hairs are a DE-only trichome candidate |
| Ground_Tissue (axis) | Rachis_I/II, Branch_3, ST Rachis/Branch/Branch_basal (24,980) | Revise: organ and axis labels |
| Other | Spikelet (39,695; 38.7%) | Revise: catch-all organ label |
| Ground_Tissue | Pistil_supporting_cell (= "Spikelet_supporting_cell" in the marker table; 22,517) | Revise: OSH1, OSH15, OsMADS6 point to axis or receptacle ground tissue |
| Epidermis | Pistil_identity_cell (17,376) | Revise: implausible at Sp6-Sp7; its marker WDA1 suggests epidermis |
| Lemma | Lemma (11,887) | Revise: DE-only markers |
| Palea | Palea (4,465) | Revise: DE markers plus CycB1;1; no REP1 |
| Glume | Cryptic_bract (10,197) | Revise: too large; FZP plus DE genes (and the meiocyte gene OsCMT3a) |
| Glume | Steril_lemma-Rudimentary_glume (214) | Revise: merges two glume organs; TOB1/TOB2 plus S-phase genes |
| Lodicule | Lodicule (7,257) | Revise: DE markers only; no B-class MADS |
| Floral_Meristem | Floral_primodium (2,849) | Revise, close to Adopt: DWT1, FON2, OsMADS58, OsMADS13; merges FM with carpel and ovule primordia |
| Stamen / Carpel | Stamen / Ovary (sp8; 478 / 283) | Revise: under-represented |
| Tapetum | Tapetum (13,563; 27.3% of stamen) | **Adopt**: TDR, EAT1, OsABCG15, OsC6; all 6 stamen samples plus cell-segmented Stereo-seq |
| Epidermis (anther) | Epidermis (9,022) | **Adopt**: WDA1; spatially placed |
| Endothecium | Endothecium (5,948) | Revise: spatially placed, but markers are photosynthesis genes |
| Middle_Layer | Middle_layer (1,905) | Revise: spatially placed, absent at S12 as expected; OsTGA10 not layer-specific |
| Connective | Vascular_bundle-Connective_tissue (5,807) | Revise: merges two tissues that the Stereo-seq separates; OsJAR1, OsTAR2 |
| Meiocyte | Microscope_mother_cell / Meiotic_cell (829 / 532) | Revise: one sample each; merge as Meiocyte |
| Meiocyte (states) | Dyad_cell / Tetrads (ST; 26 / 22 bins) | Adopt: stage-specific states in the locule; DE markers only |
| Microspore | Microspore (761) | **Adopt**: right stages (S9-S10), placed in the locule; MTR1 marks the whole male germline |
| Pollen | Biceullar_pollen / Mature_pollen (3,540 / 7,693) | **Adopt**: stage-defined (S11, S12); OsSPS1, OsPLL6 in situ in this study, plus OsGCS1, OsNek3 |
| Ovary_Wall | Ovary_wall_1/2 (34,263; 28.4% of pistil) | Revise: OsNAC6 (stress) and CAB1R (photosynthesis), square bins |
| Carpel_Epidermis | Ovary_wall_epidermis / Style_epidermis (14,031 / 3,830) | Revise: both share GELP24 (from Li 2023): treat as carpel epidermis |
| Stigma_Style | Style / Stigma (5,623 / 1,447) | Revise: OsPME24 copied from Li 2023; Stigma "TPP5" maps to the wrong chromosome |
| Dividing_cells (state) | Dividing_cell_1-3 (pistil; 16,318) | Adopt: proliferation labelled as a state |
| (rice_ovule group) | Integument / Nucellus / Chalaza / Germ (42,468) | Revise; out of scope here, belongs to rice_ovule |
| Other | Stamen_residue / Unknown (379 / 3,777) | Adopt: contamination and unassigned cells kept separate |

### Markers added and raised

`markers_draft.tsv` went from 39 rows (38 genes) to 72 rows (71 genes). The 13-column set and ID convention are unchanged (`ref_gene` = MSU7 `LOC_Os`, `alt_id` = RAP-DB). ZH11 IDs are given at the end of `basis` for the Jing-derived rows. Every new MSU-RAP pair was checked against `../../reference/rice/oryzabase_gene_list.tsv` (all 33 new pairs agree). Field counts validated (13 on every line of `markers_draft.tsv`, 6 on every line of `expected_cell_types.tsv`).

- **29 new rows from Jing2026** (all 29 non-overlapping rows of `Jing2026/markers_carried.tsv`):
  - Tapetum: OsABCG15 (function, high).
  - Endothecium: CP24 (characterized_enriched, medium), CAB1R, Lhca4/DYE1 (low). Photosynthesis genes, so use them only inside anther clusters.
  - Middle_Layer: OsTGA10 (low).
  - Microspore: MTR1 (function, medium; whole male germline).
  - Meiocyte: OsCMT3a (function, medium), OsUGP1 (low).
  - Dividing_cells (state): OsCDC20.1 (medium), OsCDC20/WD40-109 (low).
  - Pollen: OsGCS1/HAP2 (function, medium), OsSPS1, OsPLL6, OsNek3 (medium), OsHAK26, OsGEX1, OsGEX3 (low).
  - Connective: OsJAR1 (low).
  - Stigma_Style: OsPME24 (low). Carpel_Epidermis: GELP24 (low). Ovary_Wall: OsNAC6 (expression, low).
  - Floral_Meristem: FON2/FON4 (function, medium).
  - Glume: FZP (low). Ground_Tissue: OSH15 (low). Bract: OSH6, PLA1, PLA2 (low).
  - Inflorescence_Meristem: OsPLT1 (expression, low). Abscission_Zone: SHAT1 (low; flags the rejected IM_2 label).
- **4 new rows from the characterized-marker survey** (`survey/characterization/characterized_markers.tsv`, rows with `rice_inflorescence:` gaps; rice genes only, DOIs already checked there): LAX1 (Branch_Meristem, function, medium), Oshox1 (Procambium, function, high), GLR1/OsWOX3B (Trichome, function, medium), OsSUT1 (Phloem, function, medium). None of these IDs matches a Jing marker, so they give no cross-study raise. The survey's TAW1 row (BM) cites the same Yoshida 2013 study as the existing TAW1 row, so it is not independent and TAW1 was not raised. The Arabidopsis survey rows (MYB26, NST1, NST2 for endothecium; FATA1, KAS2 for middle layer; STY1 for stigma/style) and the Brachypodium BdFAMA row (guard cells) are homology leads only. They were not added to this rice table.
- **Grading changes to Jing's carried rows:** FON2 was lowered from high to medium, because it is expressed at the apex of every aerial meristem and is not FM-specific. CP24 lost `requires=grass`: it is a photosynthesis gene, not a grass trait. OsCDC20/WD40-109 was moved from Meiocyte (kind=state) to Dividing_cells, so that kind and type agree.
- **Existing rows updated (11; basis and source only):** TDR, EAT1, OsC6, WDA1, OsMADS13, DWT1, OsMADS58, CycB1;1, CDKB2;1, OsPCNA, TAW1.
- **Raised: none.** TDR, EAT1, OsC6, WDA1 and OsMADS13 now have a third independent study (Jing: cluster-specific in all stamen samples plus cell-segmented Stereo-seq), but they were already high. Three rows were not raised:
  - DWT1 stays medium: Jing copied its panicle markers from Zong 2022, so they are not independent.
  - OsMADS58 stays medium: Jing lists it for the merged Floral_primodium, not for a carpel cluster.
  - OsMADS8/24 stays low: Jing lists it for the proliferation-driven Spikelet_primordia.
- `requires=grass` is now set on the Bract, Glume (FZP), Abscission_Zone, Branch_Meristem (LAX1), Trichome and Phloem (OsSUT1) rows added here. The earlier rows still carry no tags (see the note at the top).
- Tier totals: 39 `function` (18 high, 21 medium), 31 `characterized_enriched` (8 medium, 23 low), 2 `expression` (low).

### Gaps

- **Closed** (an expected type now has a `function` marker):
  - Microspore: MTR1 (Jing2026).
  - Branch_Meristem: LAX1. Trichome: GLR1. Procambium: Oshox1. Phloem: OsSUT1. These four come from the characterized-marker survey.
  - Pollen, a newly expected type: OsGCS1.
- **Partly filled** (weak markers only, no `function` marker): Endothecium (CP24, CAB1R, Lhca4), Middle_Layer (OsTGA10), Ovary_Wall (OsNAC6), Stigma_Style (OsPME24), Bract (OSH6, PLA1, PLA2), Ground_Tissue (OSH15), Connective (OsJAR1), Carpel_Epidermis (GELP24), Abscission_Zone (SHAT1). The review listed Endothecium, Middle_Layer, Ovary_Wall and Stigma_Style as filled. They have spatially placed labels now, but none has a type-defining gene.
- **Remaining** (no `function` marker): Bract, Mesophyll/hull chlorenchyma, Guard, Endothecium, Middle_Layer, Filament, Connective, Ovary_Wall, Stigma_Style, Carpel_Epidermis, Ground_Tissue, Xylem, Abscission_Zone. Lemma still has only OsMADS1, which is shared with palea. The IM, SM and FM markers still overlap.

### Recommended label reference (revised)

- **Jing2026 stamen labels are now the best per-cell reference for anthers** (`Jing2026/portal/ZH11_SC_per_cell_labels.tsv.gz`). They replace Wang2025 SP8 for Tapetum: all 6 stamen samples, cell-segmented Stereo-seq, and a tapetum count (27.3% of stamen nuclei) that fits a multinucleate layer.
  - Adopt Tapetum, anther Epidermis, Microspore, Biceullar_pollen and Mature_pollen (as Pollen states), and Dyad/Tetrad (ST).
  - Endothecium, Middle_layer and Vascular_bundle-Connective_tissue can serve as positional labels, but do not take markers from them.
  - Merge Microscope_mother_cell with Meiotic_cell as Meiocyte.
  - Convert the ZH11 IDs with the MSU/RAP pairs in `Jing2026/markers_carried.tsv` or a positional/BLAST crosswalk. Jing2026 itself gives none.
- **Jing2026 pistil labels:** use Dividing_cell_1-3 as a state. Treat Ovary_wall, Style, Stigma and the two epidermis labels as hypotheses: they come from square bins and copied markers. Ovule tissues belong to rice_ovule.
- **Do not use Jing2026 inflorescence or spikelet labels as reference.** Bract, Spikelet and Pistil_supporting_cell are implausibly large, Spikelet_primordia is a proliferation state, IM_2 is rejected, and Pistil_identity_cell is probably epidermis. Floral_primodium is the one usable label (FM plus carpel/ovule primordia).
- For IM-to-FM stages the earlier advice is unchanged: no dataset gives reference labels, so rely on the function markers. Add LAX1 (AM boundary) and FON2 (meristem apex) to that set.
- Wang2025 SP8 Tapetum stays a valid second reference for SP8-stage nuclei.

### Conflicts and corrections

- Jing2026 is not independent of Zong2022 for panicle types (BM, Bract markers), and not independent of Li 2023 Dev Cell for pistil types (OsPME24, GELP24). No row was raised on Jing evidence for those types.
- Label names: "Pistil_supporting_cell" in the cell table is "Spikelet_supporting_cell" in Jing's marker table. Jing's spelling errors ("Microscope_mother_cell" = microspore mother cell, "Biceullar_pollen", "Floral_primodium", "Steril_lemma") are kept only where the Jing label itself is quoted.
- Portal symbol errors: "CAB2R" is CAB1R (Os09g0346500); Oryzabase CAB2R is Os01g0600900. "TPP5" (ZH03G21440, chr3) does not match Oryzabase TPP5 (Os04g0554000, chr4) and was not carried. MTR1 here is the chr2 fasciclin (Os02g0491300), not the chr7 "MTR1". OsGEX1 and OsGEX3 have no portal symbol; their symbols were inferred from the DOIs Jing cites plus position.
- Jing lists OsCMT3a for spikelet Cryptic_bract as well as meiocytes, and WDA1 for Pistil_identity_cell as well as anther epidermis. Both are recorded in `basis`.
- Jing's use of OSH1/OSH15 for "supporting cells" fits the existing OSH1 caveat (axis ground tissue).
- The Jing2026 review corrects the rice_seed review's label-access call for this paper: it is `table`, not `large_object`.

### Could not verify (Jing2026)

- The *Cell* full text, STAR Methods, figures and supplementary tables (not open access; not retried). Not seen as a result: the OsSPS1/OsPLL6 in situ images, the label-calling procedure, and any RAP/MSU crosswalk.
- The ZH11-to-MSU/RAP mapping is positional plus symbol (no BLAST). For CP24, ABCG15, Lhca4, OsTGA10, the CDC20s, MTR1, PLL6, GEX1/3, PME24, GELP24 and PLT1, the MSU half comes from Oryzabase only (UniProt carries the RAP ID but no MSU ID).
- Not downloaded (size rule): the h5ad files, so the match between label-table barcodes and h5ad barcodes is untested.
- Localization claims for FZP, PLA1, PLA2, OSH6, OsJAR1 (Jing review) and for LAX1, Oshox1, GLR1, OsSUT1 (characterized survey) come from abstracts and the survey's `validation` column. Primary figures were not re-read.
