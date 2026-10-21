<!-- Collated from the survey review of arabidopsis_fruit (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Arabidopsis fruit (silique): collated marker resources

Collated 2026-10-20 from the one review in `survey/merged_reviews.json` for group `arabidopsis_fruit`
(Lee et al. 2025, silique part). The per-dataset review is in `Lee2025/README.md` and was not changed.
This folder adds:

- `expected_cell_types.tsv`: 41 expected types and states for siliques at stages 2-10 (pericarp,
  replum/septum, vasculature, seeds, and unfertilized-ovule and pollen contaminants). It was built from
  anatomy, not from the published labels. `function_markers` is counted from `markers_draft.tsv`; markers
  in the skill's leaf/root tables are given as "(+n)" in `notes`.
- `markers_draft.tsv`: 103 rows (95 type, 8 state; 46 `function`, 50 `characterized_enriched`,
  7 `expression`; 28 high, 57 medium, 18 low) in the skill marker-table schema plus `alt_id` (UniProt accession).
  `tissue` = `fruit`, a new value (`map_markers.py --tissue` matches it as free text). Seed-compartment
  rows also use `fruit`, because a silique sample contains the seeds.

Nothing in the skill was edited.

## Datasets

| Dataset | Platform | Cells | Label access | Quality |
|---|---|---|---|---|
| **Lee TA, ... Ecker JR 2025** *Nat Plants* 11:1960 "A single-cell, spatial transcriptomic atlas of the Arabidopsis life cycle", silique part. DOI 10.1038/s41477-025-02072-z; GEO GSE226097 (GSM7063688-95) | 10x 3' HT v3.1 snRNA-seq (nuclei; 50 g spin removes pollen), plus MERSCOPE MERFISH (140-gene silique panel, 3 siliques) | 71,829 nuclei, 27 clusters, 8 runs; Col-0 siliques stages 2-10 | `table`: per-cell labels from the public cellxgene API (`Lee2025/silique_labels_from_portal.tsv`). Full objects: silique.h5ad 6.6 GB, silique.rds 7.1 GB, GEO rds 2.0 GB (not downloaded) | low for labels (4 of 27 clusters adoptable); high as a marker source (MERFISH layer markers) |

Lee 2025 is the only silique single-cell dataset reviewed. To test agreement between studies for the seed
compartments inside the silique, I used three independent seed datasets reviewed in other groups (read
only; their folders were not changed):

| Dataset (group) | Platform | Use here |
|---|---|---|
| Picard CL ... Gehring M 2021 *Nat Plants* 7:730, DOI 10.1038/s41477-021-00922-0 (`arabidopsis_endosperm/Picard2021`) | Smart-seq2 snRNA, 4 DAP seeds | in situ for CZE (AT2G44240, MEE56, GA20OX5, CYCD4;2), HMGB13 |
| Martin CA ... Gehring M 2026 *Nat Plants*, DOI 10.1038/s41477-026-02295-8 (`arabidopsis_seed/Martin2026`) | 10x snRNA, 3/5/7 DAP seeds | HCR in situ (AGO3, SWEET10, GLIP6, NPF4.5, AT3G49307, PDF1); seed-coat layer markers |
| Rombi KLB ... Kim JY 2026 bioRxiv, DOI 10.64898/2026.07.27.741042 as recorded by its review (`arabidopsis_seed/Rombi2026`) | BD Rhapsody protoplast scRNA + MERFISH on silique sections | MERFISH for seed-coat layers, chalazal unloading domain, abscission zone |

The Lee 2025 seed part (`arabidopsis_seed/Lee2025`) is the same atlas and does not count as independent.

## Verdict matrix (canonical type x dataset)

A = Adopt, R = Revise, X = Reject, - = not resolved. Only Lee 2025 has silique labels. The seed columns say
whether the independent seed studies resolved and validated the type.

| Canonical type | Lee 2025 silique | Seed studies (Picard / Martin / Rombi) | Note |
|---|---|---|---|
| Guard (+ Myrosin_Idioblast) | A (c16) | - | FAMA, TGG1, ABCG29. TGG2 is rank 2, so myrosin cells are probably inside c16 |
| Exocarp | A (c9 "Epidermal") | - | AT4G23670 (MERFISH) is the top DE gene |
| Mesocarp | - | - | MERFISH genes are not DE in any cluster; possibly inside c2 or c0 |
| Endocarp | R (c18, c22, c25; c12 = endocarp b?) | - | MERFISH endocarp genes are top DE genes; c18 also has nucellus genes (see Conflicts) |
| Secondary-wall cells (Xylem / endocarp b / valve margin) | R (c4 "Xylem", c12 "Vascular") | - | CESA4/7/8, IRX8, XCP2 in c4; exocarp MERFISH genes also in c4 |
| Procambium | R (c12) | - | ATHB8 (used for the label) |
| Phloem_Companion | A (c20) | funiculus CC (Martin) | SUC2, FT, AHA3, AAP2 |
| Glucosinolate_Producing (state) | R (c3 "Vascular") | - | MYB29, BCAT4, IMS3 |
| Valve_Margin, Replum, Septum, Transmitting_Tract, Funiculus | - | - | no FUL/IND/SHP/RPL/NTT expression in any cluster |
| Seed_Coat_Epidermis (oi2) | R (c7 "Phloem (embryo)") | V / V / V | GL2 rank 2, MUM4 |
| Endothelium (ii1) | R (c11 "Epidermal") | V / V / V | BAN, LDOX, DFR, GSTF12 ranks 2-10 |
| Subepidermal_Outer_Integument / Chalazal_Seed_Coat (suberin) | R (c13 "Unknown") | - / V / V | ASFT, MYB107; oi1 vs chalaza not resolved |
| Inner_Integument (ii1') | R (c17 "Phloem") **new reading** | - / V / V | UMAMIT12 rank 3, UMAMIT25 rank 13, SIAR1 rank 12 (Rombi ii1' and abscission zone) |
| Nucellus | - (c18?) | - / V / V | SWEET15 and AGO3 weakly DE in c18 |
| Chalazal_Endosperm | R (c14) | V / V / - | AT2G44240 rank 3 |
| Micropylar_Endosperm (+ Suspensor) | **R (c15 "Unknown"; review said Reject)** | V / V / V | RGP3 rank 1, ALE1, GLIP6, ZOU, KRS; WOX8 rank 33 |
| Peripheral_Endosperm | - | - | no specific marker |
| Embryo (maturation) | A (c5) | - | cruciferins, 2S albumins, oleosins |
| Dividing_cells (state) | R (c6 "Embryo (dividing)") | HMGB13 in situ (Picard) | CDC20.1, TOPII, HMGB13 |
| Heat_Stress (state) | X (c8 "Unknown", c10 "Embryo") | - | HSFA2; HSP101, HSP70B |
| Senescing (state) | R (c25) | - | SAG12 with CAD8 (endocarp) |
| Female gametophyte (Synergid/Egg_Cell) | R (c23, c24) | - | DEFL/ECA1 programs; MYB98, EC1.1 not DE |
| Pollen / Sperm_Cell (contaminants) | X (c19 "Phloem"), R (c21) | - | AGP6, AGP11 in c19; MGH3 in c21 |
| Unresolved | X (c1, c26), R (c0, c2) | - | c0 = mixed seed coat per the paper's subclusters; c2 = ground tissue? |

V = validated (in situ, reporter or MERFISH) or a cluster marker in that study.

## Cross-study markers

Agreement here means the same AGI is validated in one independent study and cluster-specific (or validated)
in another, for the same cell type. Lee 2025 DE counts only when the paper did not label the cluster with that
gene.

| Gene | AGI | Type | Evidence A | Evidence B | Confidence |
|---|---|---|---|---|---|
| BAN/ANR | AT1G61720 | Endothelium | reporter (Debeaujon 2003); marker in Picard, Martin, Rombi | Lee c11 rank 2 (labeled "Epidermal") | high |
| LDOX/TT18 | AT4G22880 | Endothelium | mutant (Abrahams 2003); Rombi list | Lee c11 rank 3 | medium -> high |
| DFR/TT3 | AT5G42800 | Endothelium | reporter (Debeaujon 2003); Rombi list | Lee c11 rank 9 | medium -> high |
| GSTF12/TT19 | AT5G17220 | Endothelium | Kitamura 2004; Rombi list | Lee c11 rank 10 | medium -> high |
| GL2 | AT1G79840 | Seed_Coat_Epidermis | mutant (Western 2001); marker in Picard, Martin, Rombi | Lee c7 rank 2 (labeled "Phloem") | high |
| UMAMIT14 | AT2G39510 | Chalazal_Seed_Coat | reporter (Muller 2015) | Rombi MERFISH; Martin marker | high |
| CALS8/GSL04 | AT3G14570 | Chalazal_Seed_Coat | Rombi MERFISH | Le 2010 LCM; Martin marker | medium -> high |
| AGO3 | AT1G31290 | Nucellus | Martin HCR | Jullien 2020 promoter; Rombi cluster | medium -> high |
| AT2G44240 | AT2G44240 | Chalazal_Endosperm | Picard in situ | Martin marker; Lee MERFISH probe and c14 rank 3 | medium -> high |
| MEE56/HIPP18 | AT4G13380 | Chalazal_Endosperm | Picard in situ | Le 2010 LCM; Martin; Lee c14 | medium -> high |
| ZOU | AT1G49770 | Micropylar_Endosperm | mutant + ESR expression (Yang 2008) | Picard, Martin, Rombi; Lee c15 | high |
| ALE1 | AT1G62340 | Micropylar_Endosperm | Tanaka 2001 | Lee c15 rank 18 (unlabeled); Martin, Rombi | high |
| RGP3 | AT3G08900 | Micropylar_Endosperm | Fourquin 2016 (via Martin) | Lee c15 rank 1 (unlabeled) | medium -> high |
| AHA3 | AT5G57350 | Phloem_Companion | promoter-GUS (DeWitt 1995) | Lee c20 rank 17 (not used for label) | medium -> high |
| AAP2 | AT5G09220 | Phloem | promoter-GUS in silique vasculature (Hirner 1998) | Lee c20 rank 1 | medium -> high |
| XCP2 | AT1G20850 | Xylem | Avci 2008 | Lee c4 rank 15 (c4 labeled from XCP1) | high |
| AGP6 / AGP11 | AT5G14380 / AT3G01700 | Pollen | Levitin 2008 | Lee c19 (labeled "Phloem") | high |
| HMGB13 | AT4G11080 | Dividing_cells | Picard in situ | Lee c6 rank 13 | medium -> high |
| FUL | AT5G60910 | Carpel_Valve | in situ (Gu 1998) | Lee 2025 flower carpel MERFISH | high |

Noted but not raised: GLIP6 (Martin HCR was one experiment; Lee c15 rank 28) and NPF4.5 (Martin HCR in a
figure I did not view; Lee c14 rank 101). UMAMIT12, UMAMIT25 and SIAR1 match Rombi's ii1'/abscission-zone
MERFISH in Lee c17, but Lee labeled c17 with UMAMIT12/SIAR1 (as phloem), so they are not counted.

## Gaps (expected types with no `function` marker in the draft)

- **Pericarp:** Exocarp, Mesocarp, Endocarp (only MERFISH-validated uncharacterized genes; endocarp a and b
  cannot be told apart). Mesocarp can borrow chlorenchyma genes from `arabidopsis_leaf.tsv`.
- **Fruit structures:** Septum, Funiculus. Valve_Margin, Replum and Transmitting_Tract have classic function
  markers, but none is expressed in any Lee 2025 cluster, so these types are probably not resolved in that data.
- **Seed:** Nucellus, Chalazal_Endosperm (both have `high` characterized_enriched rows), Peripheral_Endosperm,
  Protoderm, Central_Cell.
- **Vascular:** Phloem (AAP2 is characterized_enriched; APL is in the leaf table), Sieve_Element (absent in
  nuclei), Myrosin_Idioblast (TGG2 only).
- **States:** Heat_Stress and Glucosinolate_Producing have only characterized_enriched rows.

## Recommended label reference

Lee 2025 is the only silique dataset, and its labels are weak. Adopt only c16 (Guard, with a myrosin-cell
check), c9 (Exocarp), c20 (Phloem_Companion) and c5 (Embryo, maturation). Relabel these, using the markers
above: c7 to Seed_Coat_Epidermis, c11 to Endothelium, c14 to Chalazal_Endosperm, and c15 to
Micropylar_Endosperm (+ suspensor). Treat c6, c8, c10 and c25 as states, and c19 and c21 as contaminants.
For the seed compartments, the independent seed atlases (Martin 2026 snRNA with HCR; Rombi 2026 with
MERFISH) are better label references than Lee 2025. A second silique-wall (pericarp) atlas is needed before
the pericarp labels can be treated as ground truth.

## Conflicts and corrections

- **Correction to the review: c15 is micropylar endosperm (ESR), not a reject.** RGP3 is its top DE gene, and
  ALE1 (rank 18), GLIP6 (28), WOX8 (33), ZOU (65) and KRS (113) are also DE. Lee's own annotation text
  names RGP3 as an endosperm marker for c15, but the final label is "Unknown". WOX8 suggests suspensor cells
  co-cluster. SWEET11 (rank 10) is also DE here, which fits seed-coat/endosperm sugar transport (Chen 2015)
  better than phloem parenchyma.
- **New reading of c17 ("Phloem"):** UMAMIT12 (rank 3), UMAMIT25 (13) and SIAR1/UMAMIT18 (12) are Rombi
  2026 MERFISH markers of ii1' and the seed abscission zone. The review called c17 "unresolved (vascular
  parenchyma vs guard-like)". It is more likely inner-integument/chalazal seed coat. MYB60 and SLAH3 are
  still unexplained.
- **c18 ("Phloem (tip)"): endocarp a or nucellus.** The MERFISH endocarp gene AT1G23520 is rank 2, but the
  nucellus markers SWEET15 (Rombi reporter, rank 47) and AGO3 (rank 87, weak) are also DE. Both tissues
  undergo PCD (MC9, BFN1, alphaVPE). Not resolved.
- **c16 Guard includes myrosin cells (probably).** TGG2 (myrosin cells only, Barth & Jander 2006) is rank 2.
  KAT1 is DE in c20 (companion cells), not in c16, and SLAC1 is not DE anywhere.
- **FDH (AT2G26250)** is DE only in c11 (endothelium), not in exocarp c9. Kept as Epidermis (medium) with this
  note.
- **Lee MERFISH layer genes vs snRNA clusters:** exocarp genes FPP7 and TPXL6 are DE in c4 ("Xylem"); the
  endocarp genes NSP2 (c5 embryo), AT4G21895 (c21, male germline) and AT2G23910 (c11, endothelium) are DE
  in other compartments; ALD1 is "Endocarp" in Supp. Table 3 but "seeds" in Extended Data Fig. 6e (not
  carried). AT2G37540 is mesocarp in the silique but sepal/petal epidermis in the flower. All are `low`.
- **The 17 MERFISH "Embryo" genes in Supp. Table 3** (AT1G56045 ... AT5G64310) are not DE in the embryo
  cluster c5. Several are cell-cycle or methylation genes (AT3G20150 kinesin, DDM2/MET1). None was carried.
- **UMAMIT25 (AT1G09380):** ii1' by Rombi MERFISH, but Picard 2021 in situ shows micropylar endosperm plus
  seed coat, and Besnard 2018 describes it as a seed-loading exporter. Kept `low`.
- **NaKR1 (AT5G02600)**, a companion-cell gene, is DE in c24 (DEFL/synergid-like) and c14, not c20. `low`.
- **bZIP9 (AT5G24800)**: Lee used it as a leaf phloem marker (Kim 2021). Rombi's reporter places it in the
  chalazal unloading domain, which is the phloem end in the seed. Graded as Chalazal_Seed_Coat (medium).
- **Citation corrections made while building the table:** the LDOX endothelium evidence is Abrahams et al.
  2003 (tds4), not Pourcel 2005 (that paper is TT10). XCP2 function is Avci et al. 2008 (Funk 2002 is
  XCP1). ZOU is Yang et al. 2008 *Development*, KRS is Moussu et al. 2017 *Plant Cell*, and ARR22 is Horak
  et al. 2008 *BMC Plant Biol*. Every DOI in `source` was resolved through Crossref or Europe PMC, except the
  Rombi 2026 preprint DOI (see below).
- **ID hygiene:** 522 Lee DE IDs carry `make.unique` suffixes (e.g. `AT2G395101`). Matching used the 9-character
  `agi` column. DE `pct.2` is ~0.5 for almost every gene, so only within-cluster ranks are quoted, as "rank
  r/n". These are not ordinary enrichment statistics.

## IDs checked

Every AGI in `markers_draft.tsv` (103 rows, 103 distinct genes) was confirmed with the UniProt REST API
(taxon 3702). The accession is in `alt_id`, and the gene names matched the symbol in every case. Thirteen
genes have only unreviewed (TrEMBL) entries: AT4G23670, AT5G37478, AT5G18310, AT2G37540, AT1G23520,
AT3G26440, AT1G62225, AT5G50130, AT4G21895, AT2G23910, AT2G44240, AT3G49307 and MYB107 (AT3G02940).
Lee 2025 genes were matched to Supp. Table 2 (DE) or Supp. Table 3 (MERFISH). The seed-study genes were
taken from those reviews' primary-table checks. UMAMIT12/25/29 have no UMAMIT name in UniProt ("WAT1-related
protein"), so their numbers come from the Rombi and Martin tables and the Lee DE description field.

## Rows not in the fruit review's marker list

35 of the 103 rows come from the Lee 2025 silique review (36 genes; ALD1/AT2G13810 was dropped because Supp.
Table 3 and Extended Data Fig. 6e disagree on it). The other 68 rows come from three sources:

- **37 rows from the seed reviews** (Picard 2021, Martin 2026, Rombi 2026), added because the silique
  contains seeds: seed-coat layer, nucellus, endosperm, suspensor and protoderm genes, plus ATML1, CESA7 and
  HMGB13. Each was checked against the Lee 2025 silique DE table.
- **4 more Lee 2025 MERFISH genes** from Supp. Table 3 (AT3G28270, AT1G80170, AT4G21895, AT2G23910), all `low`.
- **27 classic or literature rows.** Some cover types the data do not resolve: FUL, IND, SHP1, SHP2, ALC,
  RPL, NTT, LEC1, MYB98 and EC1.1, none of which is DE in Lee 2025. The rest are characterized genes that are
  DE in a Lee 2025 cluster: TGG2, CESA4, CESA8, ATHB8, SWEET11, NaKR1, ABI3, CRA1, SESA4, AGP6, AGP11, TOPII,
  SAG12, HSFA2, HSP101, MYB29 and BCAT4.

## Overlap with existing skill tables (same species)

There is no fruit or seed table in the skill. The same gene with the same cell type appears in
`arabidopsis_leaf.tsv` for FAMA (Guard), ATML1 and FDH (Epidermis), SUC2 (Phloem_Companion), SWEET11
(Phloem_Parenchyma), XCP2 and IRX3/CESA7 (Xylem), ATHB8 (Procambium) and SAG12 (Senescing). GL2 is
Trichome in `arabidopsis_leaf.tsv` and Atrichoblast in `arabidopsis_root.tsv`, but Seed_Coat_Epidermis here.
PDF1 is Epidermis in the leaf table and Protoderm here. These are the same genes in different tissue
contexts, not conflicts. The other 92 rows (genes) are new to the skill's Arabidopsis tables. Myrosin_Idioblast, Valve_Margin, Carpel_Valve,
Transmitting_Tract, Synergid, Egg_Cell and Pollen rows also exist in the unmerged
`arabidopsis_inflorescence/markers_draft.tsv` (tissue `flower`).

## Could not verify

- The Rombi 2026 preprint DOI (10.64898/2026.07.27.741042) did not resolve in Crossref. It is kept as
  recorded by that review. Rombi IDs were marked `id_checked: false` in its review; I confirmed them in
  UniProt, but did not open the preprint's tables.
- Martin 2026 Supp. Fig. 5 (NPF4.5 HCR) and Lee 2025 Extended Data figures were not viewed. Their evidence is
  taken from legends and the reviews.
- The silique MERFISH cell table (13 GB raw Vizgen folder only) and the full h5ad/rds objects were not
  downloaded. Cluster specificity here comes from the paper's DE ranks, not from re-analysis.
- Literature expression claims for classic rows (FUL, IND, SHP, ALC, RPL, NTT, TT genes, AGL62, LEC1, etc.)
  are cited from the original papers by title and DOI. I did not reread their figures.
