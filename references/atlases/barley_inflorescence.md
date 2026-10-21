<!-- Collated from the survey review of barley_inflorescence (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Barley inflorescence (spike): collated cell-type resources

Collated 2026-10-20 for the plant-celltype-annotation skill. Inputs: the one review for this group in
`survey/merged_reviews.json` (Demesa-Arevalo 2026; the review is in `DemesaArevalo2026/README.md`), plus
targeted checks of earlier barley in situ papers. These checks supply the cross-study evidence. The skill was not edited.

Files here:
- `expected_cell_types.tsv`: the cell types expected at W3.5, from spike anatomy. `function_markers` counts the `function` rows in `markers_draft.tsv`. The notes name skill-table markers that can be used via homology.
- `markers_draft.tsv`: 42 rows in the skill schema plus `alt_id`. `ref_gene` is the Morex V3 ID (`HORVU.MOREX.r3.*`) and `alt_id` is the Morex V1 ID (`HORVU*Hr1G*`) where a paper table gives one. Field counts were validated with awk.
- `DemesaArevalo2026/`: the dataset review, downloaded tables and derived ID checks (not modified).

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| DemesaArevalo2026 | Demesa-Arevalo E ... Usadel B, Simon R. *Nature Plants* 12:107–124 (2026). doi:10.1038/s41477-025-02176-6. PMC12830361 | Protoplast scRNA-seq (BD Rhapsody WTA). Resolve Molecular Cartography (MC): 100-gene panel, 86 genes detected, 81 used as anchors | 16,528 high-quality cells from WT Golden Promise W3.5 spikes, 3 experiments. 27 clusters. 22,082 MC cells | `table`, with caveats. The scRNA-only labels exist at cluster level only (Fig 2b map; transcribed in `DemesaArevalo2026/derived/`). The public per-cell labels come from the 81-gene scRNA+MC integration (BARVISTA static files): `DemesaArevalo2026/barvista/D1-5_res1.3_percell_labels.tsv` | medium for labels, high for spatial markers |

This is the only single-cell dataset for barley inflorescence. The `barley_shoot_apex` group reviews the vegetative SAM (vSAM) part of the **same paper** (919 cells, a separate MC section). It is not an independent study, so it was not used to raise confidence.

No count matrices or other large objects were downloaded. The review README lists them: RSEC matrices of 366–503 MB per replicate, an imputed CPM matrix of 1.74 GB and a 404 MB rds, all in the DataPLANT ARC at git.nfdi4plants.org/ceplas/Barvista_ARC.

## Per-cell-type verdicts (one dataset)

Source A is the 27 scRNA clusters. Source B is the vascular and corpus subclusters. Source C is the BARVISTA integrated labels.

| Expected cell type | DemesaArevalo2026 label(s) | Verdict |
|---|---|---|
| Epidermis | L1 – epidermis (A7) | Adopt |
| Epidermis (sub-states) | L1 – epidermis TSM/LSM/FM (A11, 22, 1); G1 transition – Epidermis (A20) | Revise: merge into Epidermis |
| Shoot_Meristem (corpus) | Meristem – IM,TSM (A2, 18); Meristem – SM,LSM (A8); Meristem (A3, 26); IM/TSM ground, Meristem ground/rachis (B) | Revise: positional domains of one corpus. Cluster 26 is close to Reject |
| Inflorescence_Meristem / Spikelet_Meristem | A2, A18 / A8 (as above) | Revise: no IM- or SM-specific marker |
| Floret_Meristem | Corpus subcluster 9 | Adopt |
| Stamen_Primordium | Corpus subclusters 1, 8; most of "Meristem – FM, F organs" (A4) | Adopt (B) / Revise (A4: FM and organs merged) |
| Lemma | Corpus subcluster 4 | Adopt (medium) |
| Lemma + Palea | Corpus subclusters 6, 7 | Revise: merged |
| Lodicule + Carpel_Primordium | Corpus subcluster 17 "Lodicules/Gynoecium" | Revise: merged |
| Rachilla | Corpus subcluster 16 (5 is merged with meristem base) | Adopt 16 (medium) / Revise 5 |
| Glume | Corpus subclusters 10, 14, 15 "Meristem base/Glumes" | Revise: merged |
| Organ_Boundary, Suppressed_Bract, Lateral_Spikelet | not a cluster (spatial and imputation data only) | missing |
| Meristem_Central_Zone, Organizing_Center | not assigned | missing |
| Ground_Tissue | "Vascular tissue: Pith" (A14) | Revise: ground tissue, not vascular |
| Chlorenchyma | "Pith (two veins)" (A21); Green_Rachis-1/-2 (B) | Revise: a photosynthetic ground state |
| Procambium | Procambium (B); "Cambium" (B); G1 transition – Vascular (A19) | Adopt / Revise (grasses have no cambium) / Revise |
| Xylem | Xylem (B); "Pith + Xylem" (A24) | Adopt (medium) / Revise |
| Phloem (Phloem_Companion, Sieve_Element) | Phloem (B) | Adopt (medium). SE and CC are not split |
| unresolved | Vascular tissue/Meristem base (A16, 17); Vascular tissue (A25, ABA/stress); Spikelet/Floret_base (B) | Revise |
| S_Phase, Dividing_cells | S (A0, 5, 9, 13), G2 (A10, 15, 23), M (A12) | Reject as types; keep as a state flag (about half the cells) |
| – | G1 transition – Meristems (A6); Unknown (B2, 11) | Reject (no signature / left unknown by the authors) |
| (all) | BARVISTA 22 integrated labels (C) | Revise: positional hints only. "Meristem – FM" and "Vascular tissue/Meristem" act as catch-all bins for scRNA cells |

## Cross-study markers

Six rows had their confidence raised because independent barley studies agree on the same gene ID. Each case is the Demesa MC smRNA-FISH or cluster result plus independent RNA in situ. I took the in situ statements from the full-text XML (Europe PMC), and matched IDs through Morex V1 IDs in the papers' own tables.

| Cell type | Gene (V3) | Symbol | Studies |
|---|---|---|---|
| Shoot_Meristem | 4HG0339120 | HvKN1 | Demesa 2026 MC (non-L1 corpus); Zhong et al. 2021 PNAS in situ (non-L1 IM/TMM) |
| Meristem_Tip_L1 | 5HG0502720 | HvLOG1 | Demesa 2026 MC; Zhong 2021 in situ (L1 of IM/TMM) |
| Organ_Boundary | 5HG0479720 | COM1 | Demesa 2026 MC; Poursarebani et al. 2020 Nat Commun in situ (IM-to-SM boundary). V1 HORVU5Hr1G061270 in both papers |
| Floret_Meristem | 6HG0604360 | HvMADS50 (= HvMADS6) | Demesa 2026 MC; Kuijer et al. 2021 Front Plant Sci in situ (FM). V1 HORVU6Hr1G066140 in both |
| Lemma | 4HG0396400 | HvMADS33 (= HvMADS1) | Demesa 2026 MC and subcluster; Kuijer 2021 in situ (lemma primordium and FM); Zhong 2021 in situ (SM, lemma/palea). V1 HORVU4Hr1G067680 |
| Stamen_Primordium | 7HG0721170 | HvMADS76 (= HvMADS16) | Demesa 2026 cluster 4 and stamen subclusters; Selva et al. 2023 J Exp Bot in situ (stamen and lodicule primordia at W3.5). V1 HORVU7Hr1G091210 (Kuijer 2021 table) |

Not raised (agreement is only partial):
- HvMADS20/HvMADS3: Zhong 2021 places it in stamens and pistils, but Selva 2023 confines it to the ovule at W6.
- INT-M, HvLFY and HvMADS42: both studies agree only that expression is broad.
- VRS4: Koppolu 2013 did in situ, but I could read only the abstract, so the pattern is unchecked.

Same-symbol traps: this paper's HvMADS numbers follow the newer nomenclature, while Kuijer, Zhong and Selva use the legacy names. HvMADS33 = HvMADS1, HvMADS50 = HvMADS6, HvMADS76 = HvMADS16, HvMADS24 = HvMADS2, HvMADS7 = HvMADS4, HvMADS20 = HvMADS3, and HvMADS4 (new) = HvMADS13 (legacy). The links come from Demesa Supp Tables 4 and 6 and Kuijer 2021 Table 1. **Compare by ID only.**

## Gaps

These expected types have no `function` marker:
- Meristem_Central_Zone: no barley CLV3/FCP1 ID in any source.
- Glume: VRS4 is shared with LSM/TSM founder cells; the only cue is "HvMADS33-negative bract".
- Palea: no W3.5-specific marker. HvMADS50 and COM1 appear in palea only later.
- Lodicule: HvMADS76 is shared with stamen. Barley CLY1/HvAP2 has no ID here.
- Ground_Tissue: HvMND1 is the only marker and is characterized_enriched.
- Chlorenchyma: only photosynthesis genes, which are LC models and were not carried.
- Sieve_Element.
- Stomatal_lineage: not expected at this stage.

Several types rest on low-confidence rows only:
- Organizing_Center: HvWUS1 was not detected in MC.
- Inflorescence_Meristem: all its markers are broad.
- Carpel_Primordium: HvMADS58.
- Procambium: ortholog function only.
- Phloem_Companion: HvSUT1 is protoplasting-induced.

For the vascular, epidermal and cycling types, the skill's leaf and root tables can be used through homology. The `expected_cell_types.tsv` notes list which ones.

## Recommended label reference

Use **DemesaArevalo2026**, since it is the only dataset.
- Use the **Fig 2b cluster map together with Supp Table 3** markers as cluster-level hypotheses.
- Use the **corpus subclusters** (Fig 4a) for floral organs: stamen, FM, lemma and rachilla.
- Re-derive per-cell labels from the public RSEC matrices. Do not import the BARVISTA 81-gene integration labels as ground truth; use them as positional hints only.
- Treat the 11 cell-cycle and G1-transition clusters as states, and recover their lineage from the type markers.

## Conflicts and corrections

Corrections to the review:
- **HvVND1, HvHB8, HvFOS1, HvSMXL3 and HvAPL:** the review's Ensembl check gave `NOT_FOUND` because of REST rate-limiting. A re-check with throttled requests shows all five are Morex V3 HC protein-coding genes. HvPSAN (2HG0113750) and LHCB2;3 (5HG0499400) are truly absent from Ensembl HC (LC models) and were left out.
- **"HvSUC2" (4HG0403620) is HvSUT1.** The predicted protein matches UniProt Q9M422 (barley SUT1) at 521 of 523 residues. UniProt auto-names both "SUT3", and the paper calls it "HvSUC2". It is also **induced by protoplasting** (Supp Table 2, log2FC +5.1), so it is graded low.
- **Protoplasting-repressed genes** (Supp Table 2, log2FC about −3.3): TRD, INT-M and VRS1. Expect these to be under-detected in protoplast data. The authors removed protoplasting DEGs from the HVG selection.
- **VRS1 (2HG0184740)** was added from Supp Table 4. The ID matches the UniProt Vrs1 protein through the HD-ZIP region. Its C-terminus diverges because Morex is six-rowed and carries a vrs1 allele. Golden Promise is two-rowed. In situ: lateral-spikelet primordia only (Komatsuda 2007 PNAS abstract).
- Added rows not in the review: PDF1-like 3HG0286190 (Epidermis, low), the extra S-phase histones and cyclin A (Supp Table 3), HvMADS58 (1HG0031260) and HvMADS13 (1HG0024860). The MADS rows come from Supp Tables 5 and 6, with in situ or organ data from Kuijer 2021 and Selva 2023.

Conflicts recorded in `basis`:
- **HvMADS42 and HvLFY:** the paper calls them IM/TSM genes, but in MC they are in more than half of the cells. HvMADS42 is also a green-rachis DE gene (cluster 21).
- **HvMADS20 (AG):** MC places it in stamens and gynoecium; Selva 2023 confines it to the ovule at W6. It is also a top L1 cluster-7 gene.
- **HvMADS24 (PI):** broad in early floral organs (Selva 2023).
- **PDF1-like:** marks both L1 cluster 7 and the Xylem subcluster.
- **HvVND1:** also DE in FM-centre cells (Supp Table 19).
- **The paper's ABCE class assignments by pseudotime** (Supp Table 6) contradict phylogeny in several cases. The draft uses phylogenetic identity.
- **HvWOX3 has two IDs** in the paper (main text vs Supp Table 5), so it was excluded.

Naming: "Pith" is renamed Ground_Tissue, "Green rachis" is Chlorenchyma, and "Cambium" is Procambium.

## Overlap with existing skill tables

- The skill has **no barley table and no inflorescence or shoot-apex table**, so no rows overlap for the same species.
- The draft uses `tissue = inflorescence`, a new value; `markers/README.md` lists `leaf`, `root` or `any`.
- Lineage tags use `grass` for the spikelet organs (lemma, palea, glume, rachilla, LSM, bract suppression, COM1 and SUT1). VRS1 is Triticeae-specific, but the skill's trait vocabulary has no Triticeae or Hordeum tag. Adding one would need an `IMPLIES` entry in `map_markers.py`.
- Through homology, the draft's generic types share cell-type names with the skill tables: Epidermis, Procambium, Xylem, Phloem, Phloem_Companion, S_Phase and Dividing_cells.
  - Barley HvAPL and the rice/sorghum SUT1 rows are the same orthogroups as arabidopsis APL and rice OsSUT1 / sorghum SUT1.
  - CDKB2 and the histones match the rice_root cycling rows.
- The meristem type names (Shoot_Meristem, Organizing_Center, Organ_Boundary, Lateral_Organ_Primordium) follow the unpublished `datasets/arabidopsis_shoot_apex/markers_draft.tsv`.

## Could not verify

- Koppolu 2013 (VRS4) and Whipple 2010 (TRD): I read only the abstracts, so the in situ patterns are not checked. Neither row's confidence was raised by agreement.
- Zhong 2021 does not list Morex IDs for HvKN1 or HvLOG. The link to the V3 IDs rests on Demesa Supp Table 4, which cites Zhong 2021 for those genes. INT-M (HORVU5Hr1G112440) and COM1 IDs are in the papers themselves.
- The MC images for single genes (Supp Figs) were read only through their legends, both in the review and here.
- The paper does not describe the MC pattern for HvMADS58 or HvMADS13.
- Barley CLY1/HvAP2 (lodicule), HvLG1 (boundary, V1 HORVU2Hr1G111620) and HvAPO1 (IM/FM) have expression evidence, but I did not map them to V3 IDs, so they are not in the draft.
- Not accessed (from the review): per-cell labels for the scRNA-only clusters, the authors' code (on request), and FASTQs for replicate 3. I contacted no one.
