<!-- Collated from the survey review of arabidopsis_endosperm (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis endosperm: collated cell-type marker resources

Date: 2026-10-20. Desk collation for the plant-celltype-annotation skill. No re-analysis, and the skill itself was not edited.

Inputs:
- the one review in this group, `Picard2021/` (its README is the full Step 1–3a audit);
- for cross-study agreement, three independent sources:
  - two endosperm-containing datasets reviewed under `datasets/arabidopsis_seed/`: Martin 2026 and Rombi 2026;
  - the Belmonte 2013 / Le 2010 LCM seed-region profiles. Their domain marker list is in Picard Supp Data 2, sheet "Belmonte marker genes".

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Cell types expected in an early (3–7 DAP) Arabidopsis seed sample enriched for endosperm, written from anatomy. `function_markers` is the count in the current skill tables; the draft counts are in `notes`. |
| `markers_draft.tsv` | 58 rows (42 original + 16 from the 2026-10-20 update below), skill schema plus `alt_id` (empty; Arabidopsis uses AGI only). Field counts validated. `tissue` = `seed`, as in `rice_seed/markers_draft.tsv`. |
| `Picard2021/` | Review files: supplements, per-nucleus label table, cluster table, GitHub files, and README. |
| `Belmonte2013/` | Review files for the Belmonte 2013 LCM study (paper PDF, PMC XML, GEO GSE12404 series matrix and sample table, README). Added in the 2026-10-20 update. |

## Datasets

| Dataset | Platform | Nuclei | Label access | Quality | Role here |
|---|---|---|---|---|---|
| **Picard CL et al. 2021** *Nat Plants* 7:730 (10.1038/s41477-021-00922-0); GEO GSE157145 | Plate-based snRNA Smart-seq2. FANS of 4 DAP whole seeds gated on 3C/6C; reciprocal Col×Cvi F1 | 1,437 (966 endosperm, 464 seed coat, 7 embryo); 1,091 in the Fig. 1 label table | `table`: per-nucleus SC3 clusters (Supp Data 1 / GitHub), cluster→label mapping (Supp Data 2). Derived files: `Picard2021/published_labels_4DAP.tsv`, `published_cluster_table.tsv` | medium (medium-high for the chalazal endosperm) | the group's only review; the in situ-validated chalazal and ESR markers come from it |
| Martin CA et al. 2026 *Nat Plants* (10.1038/s41477-026-02295-8), reviewed in `arabidopsis_seed/Martin2026` | 10x 3' v3.1 snRNA, FANS 2C–16C, Col-0 whole seeds at 3/5/7 DAP | 54,210 (23.4% endosperm) | see that review | not graded here | independent cluster-level agreement; HCR for RALFL3, AT3G49307 and GLIP6 |
| Rombi KLB et al. 2026 bioRxiv (preprint), reviewed in `arabidopsis_seed/Rombi2026` | Protoplast scRNA (BD Rhapsody) + MERFISH, heart-stage seed | 20,097 (embryo+endosperm 2.7%) | see that review | not graded here | seed coat agreement; UMAMIT25 and MES10 conflicts |
| Belmonte MF et al. 2013 *PNAS* (10.1073/pnas.1222061110); Le BH et al. 2010 *PNAS* (10.1073/pnas.1003530107) | LCM microarrays of seed regions | n/a | n/a | n/a | domain-level (CZE, MCE, PEN, CZSC, GSC) enrichment, counted as an independent study |

Martin 2026 is from the same lab as Picard 2021 (Gehring). It is still counted as independent because it is a separate experiment with a different platform, genotype and stages. Where Martin named a cluster from Picard's markers (CYCD4;2, AT2G44240), that cluster call is **not** counted as agreement.

## Verdict matrix per expected cell type

A = Adopt, R = Revise, X = Reject, – = not annotated. Picard verdicts are from `Picard2021/README.md`; Martin and Rombi verdicts are from the `arabidopsis_seed` reviews (in `survey/merged_reviews.json`).

| Expected type | Picard 2021 (4 DAP) | Martin 2026 (3/5/7 DAP) | Rombi 2026 (heart) |
|---|---|---|---|
| Micropylar_Endosperm / ESR | A (CxV E9, renamed ESR); R (VxC E3, 4 nuclei); R (M-/S-phase "micropylar") | A (MCE_ESR general / sheath-promoting); R (high-PCD state) | R (inside merged embryo+endosperm cluster 13) |
| Peripheral_Endosperm | R (about 10 clusters: cell-cycle phases and "energy-generating" programs, to be merged); X ("inactive" low-quality bin) | PEN general clusters (not graded individually in the seed review) | R (called from G2/M genes) |
| Chalazal_Endosperm_Cyst | A (CxV E13 6, VxC E6 24; in situ) | A (basal cyst RALFL3; apical cyst MEE56); R (7 DAP "photosynthetic" and "disaccharide" cyst) | – |
| Chalazal_Endosperm_Nodule | A (CxV E12 6, VxC E1 32; in situ) | A (nodule CYCD4;2) | – |
| Chalazal_Endosperm (nodule-like) | R (CxV E14, MEA) | R (nodule-like MEA; pseudotime says PEN→CZE transition) | – |
| Cellularizing_Endosperm | only inside M-phase clusters | – | – |
| Dividing_cells (state) | labelled as domains in 8/14 CxV and 4/11 VxC endosperm clusters | PEN G2/M and S-phase clusters | G2/M genes used to call "peripheral endosperm" |
| Embryo | X (7 nuclei by % maternal reads) | many types (see seed review) | merged with endosperm |
| Seed_Coat_Outer_Epidermis (oi2) | A | (oi2 markers) | A/R (oi2 by ATML1 MERFISH) |
| Seed_Coat_Endothelium (ii1) | A (VxC S7+S8); R (S4 "possible") | A | A (general, micropylar, pigment strand) |
| Seed_Coat_Inner_Integument | R (ii1'+ii2 merged, S5) | (ii1'/ii2 markers) | R (over-split) |
| Chalazal_Seed_Coat | R (merged chalazal region) | A (placentochalazal clusters) | A (pigment strand, ULD) |
| Seed coat, other | R (flavonol S1); X (photosynthetic S6/S3: prep artifact) | | R (oi1 subdomains) |

## Cross-study markers (independent agreement; confidence raised)

The marker IDs below agree in at least two independent sources. Each ID was checked in the source table:
- Picard 2021: Supp Data 2 symbol sheet, Supp Data 5 enrichment scores (ES);
- Martin 2026: Supp Tables 1 and 3;
- LCM: the Belmonte marker sheet;
- UniProt (taxon 3702): 46 loci checked (the 45 draft or candidate loci plus AT5G23420), every AGI resolves to the expected gene. Four uncharacterized loci are in UniProt unreviewed only: AT2G44240, AT3G49307, AGL33, AGL40.

| Cell type | Gene | Agreement |
|---|---|---|
| Micropylar_Endosperm | ZOU AT1G49770 | function (Yang 2008); ESR cluster in Picard and Martin |
| Micropylar_Endosperm | ALE1 AT1G62340 | function (Xing 2013); top ESR gene in Picard (ES 12.3/10.6) and Martin (5 and 7 DAP) |
| Micropylar_Endosperm | RGP3 AT3G08900 | Picard ESR (8.8/7.5); Martin 5/7 DAP top; Fourquin 2016 |
| Micropylar_Endosperm | ARF13, CSY1, AT1G71250, ENODL10 | Picard ESR clusters + Martin MCE/ESR (ARF13 also LCM MCE) |
| Micropylar_Endosperm | GLIP6, UMAMIT25 | agreement, but each has a conflict (see below) |
| Chalazal_Endosperm_Cyst | MEE56 AT4G13380, AT2G44240 | Picard in situ + LCM CZE + Martin 5 DAP apical cyst |
| Chalazal_Endosperm_Cyst | AGL33 AT2G26320 | most cyst-specific gene in Picard (ES 17.9/16.5) + LCM CZE |
| Chalazal_Endosperm_Cyst | ARR21 AT5G07210 | Picard cyst + Martin 7 DAP cyst + reporter (Jeong 2025) |
| Chalazal_Endosperm_Nodule | GA20OX5 AT1G44090 | Picard in situ + LCM CZE + Martin 3 DAP (nodule-like) |
| Chalazal_Endosperm_Nodule | HDG8, BGAL7, AGL40, LCR46 (AGL28 with LCM only) | Picard nodules + Martin nodule top markers (+ LCM CZE) |
| Chalazal_Endosperm | AT3G49307, GA3OX4, PHE2, MEA | Picard + Martin; nodule vs cyst split inconsistent, so pan-chalazal |
| Endosperm | MYB118 | Picard broad endosperm + LCM MCE |
| Dividing_cells | 3xHMG-box1 AT4G11080, 3xHMG-box2 AT4G23800, TOPII | Picard (in situ for 3xHMG-box1) + Martin G2/M top markers |
| Seed coat | GL2, BAN, TT1, DELTAVPE, UMAMIT14, ARR22 (TT2 with LCM) | Picard + Martin + Rombi and/or LCM |

**34 of the 42 draft rows** have independent agreement. The other 8 rest on one study plus the literature: AGL62, FIS2, KRS, ICE1, CYCD4;2, SUVH7, RALFL3 and CDKB2;1.

Grading notes:
- Expression-only rows (uncharacterized genes) start at `low`, and agreement raises them to `medium`, never to `high`.
- Agreement was **not** used to raise four rows:
  - KRS and AGL62: stage-restricted, and not DE in Picard at 4 DAP;
  - GLIP6: also in the cyst;
  - RALFL3: Martin assigned its basal-cyst nuclei by hand on RALFL3 expression.

## Gaps

- **Peripheral_Endosperm:** none of the datasets has a validated specific marker. Every peripheral cluster is a cell-cycle phase or a photosynthesis/metabolic program. In Part B, call it by elimination (endosperm markers + no micropylar or chalazal markers).
- **Chalazal_Endosperm_Cyst and _Nodule:** no `function`-tier marker. The in situ genes have no known role in these domains, so they are `characterized_enriched`.
- **Cellularizing_Endosperm:** no marker; it is visible only inside mitotic clusters.
- **Aleurone** (mature persistent endosperm layer): out of scope at 3–7 DAP. No data.
- **Seed_Coat_Outer_Integument (oi1)** and **Funiculus:** no validated marker in the reviewed datasets. Martin and Rombi list candidates (MYB11, FLS1, NRT1.6, SWEET12, SUC2); those belong to the `arabidopsis_seed` collation.
- **Embryo:** not covered here. Picard has only 7 embryo nuclei. Use the `arabidopsis_seed` (Martin 2026) markers.
- **Pan-endosperm** markers are weak after cellularization. AGL62 and FIS2 are switched off around 4 DAP (except FIS2/MEA in the cyst), and MYB118 peaks at maturation.

## Recommended label reference

**Picard 2021 per-nucleus labels for the chalazal cyst (CxV E13, VxC E6), the chalazal nodules (CxV E12, VxC E1) and the ESR (CxV E9).** These are small public tables whose IDs match the GEO CPM matrix columns, and the labels are backed by in situ (cyst, nodule) or by function markers (ZOU/ALE1 for the ESR).

- Collapse the cell-cycle and "energy-generating" clusters into Peripheral_Endosperm with a Dividing_cells/S-phase state.
- Reject VxC E5 ("inactive") and seed coat CxV S6/VxC S3.
- Do not transfer proportions: the 3C/6C gating and plate sampling distort them.

For droplet data, or for stages other than 4 DAP, use **Martin 2026**. It is much larger (54k nuclei), covers 3/5/7 DAP and includes the embryo, and its labels are reviewed under `arabidopsis_seed`. Its chalazal subdomain calls partly re-use the Picard markers.

## Conflicts and corrections

1. **UMAMIT25 (AT1G09380):** placed in different tissues by different studies.
   - Picard in situ: micropylar endosperm plus seed coat and cellularization front;
   - Martin: 5 DAP MCE top marker;
   - Rombi MERFISH: seed coat ii1';
   - Picard data: seed coat S5 (ES 6.0).

   It is kept as a medium Micropylar_Endosperm marker. Use it only after endosperm identity is established.
2. **MES10 (AT3G50440):** Rombi's MERFISH endosperm marker, but it peaks in seed coat ii1' in Rombi's own scRNA. In Picard it is spread over ESR, S-phase and seed coat clusters. Not included.
3. **HDG8 (AT3G03260):** Martin's curated table lists it as a chalazal *cyst* gene (Nakamura 2006). In both Picard and Martin's snRNA data it is a top *nodule* gene, with lower cyst signal. Filed as nodule, medium, with the conflict in `basis`.
4. **AT3G49307:** Martin's HCR shows the apical cyst, but the gene is a top marker of Martin's 3 DAP nodule cluster. In Picard it is cyst-enriched. Filed as pan-chalazal.
5. **GA20OX5:** Picard in situ puts it in the nodules, but in Martin it is a top marker of the *nodule-like (MEA)* cluster, not the CYCD4;2 nodule cluster. It is still chalazal endosperm; the nodule call rests on Picard's in situ.
6. **Picard VxC E3 ("canonical micropylar endosperm", 4 nuclei):** its top genes include ARF13 (14.9) and MINI3/WRKY10 (10.5). It also has TT1 (14.1), an endothelium gene that Rombi places in the *micropylar endothelium*. This cluster may contain seed coat nuclei or doublets, which strengthens the Review verdict's "Revise". This is new here and was not in the Picard review.
7. **Symbol traps:**
   - TAIR "3xHMG-box2" (AT4G23800) is "HMGB6" in UniProt, while TAIR "HMGB6" is AT5G23420 (UniProt HMGB7). Martin's "PEN S-phase (HMGB6)" cluster refers to AT5G23420. Compare by AGI.
   - Martin calls AT3G14570 "CALS8"; Rombi calls it "GSL04". Same locus.
8. **ICE1:** enriched in the ESR, but also in seed coat CxV S6 and in stomatal lineages, so it is `medium` and must be used together with ZOU or ALE1.
9. **Correction to the Picard review:** the review graded ZOU, ICE1, MYB118, BAN, TT2, TT8 and GL2 from prior knowledge. Here each function claim was matched to a primary paper found through Europe PMC: Yang 2008 Development, Kondou 2008 Plant Physiol, Denay 2014, Barthole 2014, Debeaujon 2003, Windsor 2000. The DOIs are in `source`. The abstracts were read, not the full texts. TT8 was dropped because it is not layer-specific: it is in oi2 S2 and in the endothelium S7/S8.

## Overlap with existing skill tables (Arabidopsis)

- **No skill table covers seed or endosperm.** All 42 rows are new cell types for the skill, except `Dividing_cells`.
- **Only one gene is shared:** GL2 AT1G79840. In the skill it is Trichome in `arabidopsis_leaf.tsv` and Atrichoblast in `arabidopsis_root.tsv`; here it is Seed_Coat_Outer_Epidermis. Its cell-type meaning depends on the tissue.
- **`Dividing_cells`** rows here (CDKB2;1, TOPII, 3xHMG-box1/2) add to the `arabidopsis_leaf.tsv` rows with `tissue=any`: CYCB1;1 and KNOLLE (Dividing_cells), H3.1 and PCNA1 (S_Phase). Picard's data confirm that CYCB1;1 and KNOLLE mark its M-phase endosperm clusters (ES 10.2 and 4.7).
- **Naming:** Micropylar_Endosperm here plays the same role as `Embryo_Endosperm_Interface` in `rice_seed/markers_draft.tsv`. If the skill wants one shared name across species, rename one of them.

## Could not verify

- Figure images were not viewed: Picard Fig. 2 in situ panels, Martin HCR panels and Martin Supp Fig. 5 (NPF4.5). Localization claims come from legends, text and the earlier reviews.
- Full texts of these papers were not re-read: Fourquin 2016 (RGP3 as an ESR gene, via Martin's citation), Rademacher 2011 (ARF13 micropylar endosperm), Nakamura 2006 (HDG8), Sagasser 2002 (TT1) and Western 2001 (GL2). For Kang 2008, Luo 2000, Moussu 2017, Xing 2013, Denay 2014, Jeong 2025, Nakaune 2005, Horák 2008 and Pedersen 2011, only the abstracts were read. The Müller 2015 DOI was taken from Martin's Supp Table 1.
- Expression conclusions from Martin 2026 rest on its top-15 marker lists per cluster (Supp Table 3), not on full DE tables. A gene missing from a top-15 list was not taken as evidence against it.
- No GEO matrices were downloaded, and no in-data (Part B) check was done.
- The Picard count discrepancy (802 endosperm nuclei in the text vs 748 in the table) remains unexplained.

## Update 2026-10-20: gap-fill reviews

### New dataset

| Dataset | Platform | Populations | Label access | Quality | Role here |
|---|---|---|---|---|---|
| **Belmonte MF et al. 2013** *PNAS* 110:E435 (10.1073/pnas.1222061110, confirmed in Europe PMC); GEO GSE12404; review in `Belmonte2013/` | LCM + Affymetrix ATH1 on paraffin sections, Ws-0, 2-3 replicates | 31 subregion x stage populations: EP, SUS (globular only), MCE, PEN, CZE, CZSC, SC across pre-globular to mature green | `population_level` | medium | pseudo-bulk correlation reference for scoring clusters, and the only reference that reaches maturation. SI Datasets S1-S4 (the gene lists) returned 403 from PNAS and were not read. |

Before this update, Belmonte 2013 was already counted as an independent source through Picard's "Belmonte marker genes" sheet. Rows that already cite it were **not** raised a second time. GA3OX4 (AT1G80330) is one: the review proposed raising it to medium, but it was already medium with Belmonte cited, so only a note was added to `basis`.

### Verdicts (Belmonte 2013)

| Population | Verdict | Canonical type here | Why |
|---|---|---|---|
| EP (pg-mg) | Adopt | Embryo | anatomically clean; at mature green it shares the maturation program with the endosperm |
| SUS (globular) | Adopt | Suspensor | YUC3, PIN7 and ARF16 are higher in SUS than in EP by ATH1 and qRT-PCR |
| MCE (pg-mg) | Adopt | Micropylar_Endosperm | includes the ESR; has its own W-box-enriched gene set |
| PEN (pg-h) | Revise | Peripheral_Endosperm (weak) | few PEN-specific genes; its photosynthesis terms come from sets shared with EP and MCE |
| PEN / cellularized endosperm (lc, mg) | Revise | Endosperm | 0 subregion-specific mRNAs at mature green; this is a maturation state, not aleurone |
| CZE (pg-mg) | Adopt | Chalazal_Endosperm | the most distinct endosperm domain (788 specific mRNAs). Cyst and nodules are merged, so it supports the pan-chalazal type only |
| CZSC | Revise | Chalazal_Seed_Coat | maternal chalazal tissues merged |
| SC | Revise | seed coat (all layers merged) | split it into the Seed_Coat_* layers in Part B |

### Markers added (16 rows; 42 → 58)

From the Belmonte 2013 review. Each ID was confirmed in UniProt (taxon 3702, reviewed). Picard enrichment scores (ES) were read from Picard Supp Data 5; Martin hits were read from `arabidopsis_seed/Martin2026/SuppTable3_cluster_annotations.tsv`.

| Cell type | Gene | Evidence / confidence | Support |
|---|---|---|---|
| Suspensor | PIN7 AT1G23080 | characterized_enriched / medium | Friml 2003 (basal-cell localization) + Belmonte SUS>EP + Martin 3 DAP suspensor cluster label |
| Suspensor | YUC3 AT1G04610 | characterized_enriched / medium | Belmonte SUS>EP + Martin 3 DAP suspensor top-15 (raised from low) |
| Suspensor | ARF16 AT4G30080 | characterized_enriched / low | Belmonte only |
| Chalazal_Endosperm_Cyst | GA3OX3 AT4G21690 | characterized_enriched / medium | Belmonte CZE + Picard cyst in both crosses (ES 16.8/11.6, no nodule signal); raised from low |
| Chalazal_Endosperm | NCED6 AT3G24220 | characterized_enriched / medium | Lefebvre 2006 (endosperm-only reporter and in situ) + Belmonte CZE + Picard nodules and cyst; raised from low |
| Chalazal_Endosperm | NCED9 AT1G78390 | characterized_enriched / low | Belmonte CZE, also high in the embryo; not DE in Picard |
| Micropylar_Endosperm | MINI3/WRKY10 AT1G55600 | characterized_enriched / low | Belmonte "primarily MCE" (Luo 2005 reporter is pan-endosperm); Picard signal is only in the doubtful 4-nucleus VxC E3 and in the endothelium, so not raised |

From `survey/characterization/characterized_markers.tsv` (rows tagged `arabidopsis_endosperm:`; IDs and DOIs were already checked there and re-checked in UniProt here). Confidence was adjusted for this tissue using the Picard data:

| Cell type | Gene | Evidence / confidence | Note |
|---|---|---|---|
| Chalazal_Endosperm | FH5 AT5G54650 | function / medium | Ingouff 2005 in situ at the chalazal pole; the first `function` row for any chalazal type; not DE in Picard |
| Seed_Coat_Endothelium | TT16 AT5G23260 | function / high | Nesi 2002 |
| Seed_Coat_Endothelium | TT12 AT3G59030 | function / high | Marinova 2007 + Picard VxC S7/S8 (5.9/5.7) + Martin ii1 basal |
| Seed_Coat_Outer_Epidermis | INO AT1G23420 | function / high | Villanueva 1999 (ovule stage, medium), raised by Martin 3 DAP oi2 top-15 |
| Seed_Coat_Outer_Epidermis | MUM4 AT1G53500 | function / low | lowered from medium: Picard has it up in several endosperm clusters, and Belmonte GSC |
| Seed_Coat_Inner_Integument | ATS/KAN4 AT5G42630 | function / medium | ovule-stage evidence; the Belmonte marker sheet lists it as EP (conflict) |
| Seed_Coat_Outer_Integument | SWEET15 AT5G13170 | function / medium | Chen 2015; the first oi1 row; see conflict 2 below |
| Micropylar_Endosperm | SWEET15 AT5G13170 | characterized_enriched / low | Picard ESR in both crosses (8.7/8.6) |
| Funiculus | STK AT4G09960 | function / low | lowered: also in integuments, Belmonte CZSC, Picard chalazal seed coat; Funiculus is absent from Picard |

Existing rows annotated (no confidence change):
- ALE1: Tanaka 2001 in situ added to `basis`/`source` (already high);
- AGL62: the characterized row rests on the same Kang 2008 paper, so not raised;
- GA3OX4: Belmonte Fig 5B note added.

ZOU and BAN characterized rows cite the same papers already in the draft. No existing row was found to be wrong.

### Gaps closed

- **Suspensor** (the embryo part of the "Embryo" gap): 2 medium + 1 low row. The name matches `arabidopsis_seed`.
- **Chalazal_Endosperm**: the first `function` row (FH5), plus NCED6 at medium.
- **Chalazal_Endosperm_Cyst**: GA3OX3 adds a third, LCM-backed cyst gene at medium.
- **Seed_Coat_Outer_Integument** (oi1) and **Funiculus**: one row each, but both are weak. SWEET15 is also an ESR gene, and STK is low.
- Seed coat layers: TT16, TT12 and INO strengthen the endothelium and oi2.

### Gaps remaining

- **Peripheral_Endosperm**: still no specific marker. Belmonte confirms this independently: PEN has the fewest subregion-specific mRNAs (0 at mature green). Keep calling it by elimination.
- **Chalazal_Endosperm_Cyst / _Nodule**: still no `function`-tier marker, and the LCM cannot separate them.
- **Cellularizing_Endosperm**, **Aleurone**: no markers. Belmonte mature-green PEN is a maturation state shared with the embryo, not an aleurone reference.
- **Embryo proper**: not covered here. Use `arabidopsis_seed` (Martin 2026). LEC1 (AT1G21970, characterized table) was **not** added, because Picard 2021 has it up in endosperm clusters (VxC E4 ES 6.1, CxV E3 3.4) and seed coat CxV S6 (5.0). In endosperm-enriched data it would mislabel endosperm.
- **Chalazal_Seed_Coat** subdomains (pigment strand vs unloading zone): Belmonte CZSC merges them, and its CZSC-specific genes (trehalose, cytidine metabolism) are only in the inaccessible Dataset S3.
- Belmonte SI Datasets S1-S4 (PNAS 403): no named per-domain gene lists beyond the figures and Picard's marker sheet.

### Conflicts

1. **The gap search was wrong about PEN.** It claimed Belmonte supplies PEN-specific genes, but the paper contradicts this (see Gaps remaining). Its PEN "photosynthesis" terms are CZE-delayed sets shared with EP and MCE.
2. **SWEET15 (AT5G13170):** placed in different tissues by different sources.
   - Chen 2015: outer integument, then endosperm;
   - Picard 4 DAP: ESR in both crosses, with little seed coat signal.

   It was filed in both places. Trust the seed coat row only in nuclei already identified as seed coat.
3. **ATS/KAN4 (AT5G42630):** McAbee 2006 places it in the ovule inner integument, but the Belmonte marker sheet puts it in the embryo proper. Kept at medium.
4. **GA3OX3 vs GA3OX4 symbol trap:** UniProt Q9SVS8 (AT4G21690, GA3OX3) lists "AtGA3ox4" as an alias. In Picard, GA3OX3 is cyst-only, while GA3OX4 (AT1G80330) is nodule plus cyst. Compare by AGI.
5. **MINI3:** Belmonte calls it MCE-primary, but Luo 2005's reporter is pan-endosperm (plus the globular embryo). In Picard it is in the 4-nucleus VxC E3 and the endothelium S8. Kept at low.
6. **NCED9:** CZE-high in LCM, but also embryo, and not DE in Picard. Kept at low; do not use alone.

### Recommended label reference

**Unchanged.** Use Picard 2021 per-nucleus labels for the chalazal cyst, nodules and ESR, and Martin 2026 for droplet data and other stages. Belmonte 2013 is population-level only, so it cannot be a label reference. It is still useful in two ways:
- as a pseudo-bulk correlation reference for domain-level calls (EP, SUS, MCE, CZE, CZSC, SC), especially for maturation stages that no single-cell dataset covers. Matrix: GEO GSE12404 series matrix, saved in `Belmonte2013/` (ATH1 probe sets; map to AGI before use);
- as independent support for chalazal and suspensor markers.

### Could not verify (this update)

- Belmonte SI Datasets S1-S4: the PNAS supplementary links returned 403, and this was not worked around.
- Belmonte figure images were not viewed. The Fig 4C-E and 5B claims come from the review's reading of the author-hosted PDF.
- For Friml 2003, Lefebvre 2006 and Luo 2005, only the abstracts were read (via Europe PMC).
- The characterized-table rows (Nesi 2002, Marinova 2007, Villanueva 1999, McAbee 2006, Western 2004, Chen 2015, Pinyopich 2003, Ingouff 2005, Tanaka 2001) rest on that table's `validation` text. Their DOIs were checked there, and the papers were not re-read here.
- PIN7 suspensor localization is inferred from Friml 2003's "basal cell" localization, and the review did not check it further.
