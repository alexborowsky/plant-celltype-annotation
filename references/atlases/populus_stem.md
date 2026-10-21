<!-- Collated from the survey review of populus_stem (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Populus stem: collation of single-cell datasets and draft marker table

Collated 2026-10-20 for the `plant-celltype-annotation` skill (group `populus_stem`). This is a desk collation of four reviews (Chen 2021, Li 2021, Schmidt 2025, Wei 2026) plus the Tung 2023 dataset that Wei 2026 reuses. No data were re-analysed. Nothing here has been added to the skill; the draft table needs the user's review first.

## Files

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Step 2 list for a woody poplar stem, from anatomy. `function_markers` counts `function` rows in `markers_draft.tsv` (all rows pass `eudicot` filtering) |
| `markers_draft.tsv` | 96 rows, 95 genes, 16 cell types/states (78 rows before the 2026-10-20 update). Skill schema plus `alt_id` |
| `build_markers_draft.py` | Script that writes `markers_draft.tsv` (curated rows, automatic `alt_id`) |
| `xref_cluster_markers_by_potri.tsv` | Lookup built from the papers' own tables: every cluster-enriched gene of Chen 2021 (Table S2), Li 2021 (Dataset S3), Schmidt 2025 (Additional file 2, both replicates), Wei 2026 (Dataset S2 "Up") and Tung 2023 (Additional file 3 cluster DEGs, Additional file 15 LCM DEGs), keyed by Potri ID. Used for every specificity number in `basis` |
| `Tung2023_viaWei/` | Tung et al. 2023 full text (Europe PMC) and Additional files 3 (cluster DEGs) and 15 (LCM fiber/vessel/ray DEGs), downloaded 2026-10-20 from `static-content.springer.com/esm/art%3A10.1186%2Fs13059-022-02845-1/MediaObjects/13059_2022_2845_MOESM{3,15}_ESM.xlsx` |
| `Tung2023/`, `Qi2026/` | Gap-fill reviews added 2026-10-20 (see the update section at the end) |
| `Chen2021/`, `Li2021/`, `Schmidt2025/`, `Wei2026/` | The per-paper reviews (their own README, supplements, curated marker lists); left unchanged |

## Datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Chen et al. 2021 *Genome Biol* 22:319, 10.1186/s13059-021-02537-2 | *P. alba* var. *pyramidalis*, 4-month stem below internode 3, bark and wood separately; 3 plants pooled, 1 library per tissue | Protoplasts, 10x 3' v2 | 6,796; 20 clusters | `pou` (P. alba genome) with best Potri and AGI hits | cluster only (Table S4) | medium |
| Li et al. 2021 *J Integr Plant Biol* 63:1906, 10.1111/jipb.13159 | 84K (*P. alba* x *P. glandulosa*) debarked stem-differentiating xylem; probably 1 sample | Protoplasts, Drop-seq | 9,798; 12 clusters | 84K `Pop_A/G` with Potri (v3-era) and AGI | cluster only (rebuilt from supplements; ray cluster numbering inferred) | low |
| Schmidt et al. 2025 *Genome Biol* 26:258, 10.1186/s13059-025-03728-x | *P. trichocarpa* Nisqually-1, 6-week, whole internode LPI 4-5 (primary-to-secondary transition); 2 replicates | Nuclei (FANS), 10x 3' v3.1 | 11,673; 26 clusters | Potri v4 | inside a 358 MB Seurat RDS (Figshare 28392170); cluster-to-type map in GitHub code | medium |
| Wei et al. 2026 *Genome Biol*, 10.1186/s13059-026-04007-z | 84K, 5-month, debarked SDX below internode 15; 2 trees | Nuclei (FACS), 10x 3' v3.1, plus protoplast-nuclei control and the Tung 2023 protoplasts | 26,925 nuclei | Potri v4.1 | none for nuclei (cluster only); Tung per-cell table available | low |
| Tung et al. 2023 *Genome Biol*, 10.1186/s13059-022-02845-1 (reused by Wei; not given a full review) | *P. trichocarpa* debarked SDX | Protoplasts, 10x; plus LCM RNA-seq of fibers, vessels and rays (3 reps each) | 4,705; 10 K-means clusters | Potri v4.1 | small barcode-to-cluster table (Zenodo 7477911; copy in `Wei2026/Tung2023_Ptr_Barcode_Cluster.csv`) | medium for Ptr7 fiber and Ptr8 ray (LCM-correlated); other clusters are stage hypotheses |

Independence: the five datasets come from four groups. Tung 2023 and Wei 2026 share a lab (Lin/Li) and Wei reuses Tung's protoplasts, but Wei's nuclei and in situ data are new. Li 2021 and Wei 2026 share an author (Q. Li). Tung's "known fiber markers" (IRX15-L, PtAP66) and its ESK1a/ABR1 in situ images are cited from Chen 2021, so those claims are not independent of Chen; Tung's own LCM and scRNA data are.

## Per-cell-type verdicts across datasets

Verdicts are the reviews' Step 3a calls (A = Adopt, R = Revise, X = Reject), mapped to canonical names. "-" = tissue not sampled; "absent" = sampled but no cluster.

| Canonical type | Chen 2021 (bark+wood) | Li 2021 (xylem) | Schmidt 2025 (young stem) | Wei 2026 (xylem nuclei) | Tung 2023 (xylem) |
|---|---|---|---|---|---|
| Epidermis | A cl12 | - | R c6 (+c16, c23), labelled "epidermal & peridermal" | - | - |
| Phellem | A cl11 | - | absent (too young) | - | - |
| Phellogen | absent | - | R c15 is endodermis, not phellogen | - | - |
| Cortex / chlorenchyma | R cl0 ("photosynthetic"), R cl7 ("endodermal", likely bark parenchyma) | - | R c2, c9 (root cortex markers) | - | - |
| Endodermis (starch sheath) | R cl17 (labelled CEI) | - | R c15 (labelled phellogen) | - | - |
| Phloem (developing) | R cl6 ("phloem mother cell") | - | R c17 (PMC) | - | - |
| Sieve_Element | A cl19 | - | X c14 (organellar transcripts) | - | - |
| Phloem_Companion | A cl13 | - | A c18 | - | - |
| Phloem_Parenchyma | A cl18; R cl3 | - | A c12 | - | - |
| Cambium | R cl1, cl2, cl10 ("cambium region", 33% of cells) | R cl4 (unlabelled) | R c10 (S-phase genes co-enriched) | - | R Ptr3, Ptr6 ("organizers") |
| Xylem_Mother_Cell | R cl5 | R cl4, cl10 | A c4, c5 | - | R Ptr2, Ptr4 |
| Vessel_Element | merged in cl4 | R cl7, cl10 (disputed) | R c25 (best vessel cluster, PCD stage); c13 merged | merged in 11-L1 | R Ptr1 (24% of cells, too many) |
| Xylem_Fiber | merged in cl4 | A cl2; R cl6 | R c3 (fiber-biased SCW) | merged in 11-L1 | A Ptr7 |
| Xylem (SCW, fiber+vessel) | R cl4 | R cl6, cl7 | R c13; X c22 | R 11-L1 (SCW/PCD state); X 12 (98% catch-all) | - |
| Xylem_Parenchyma | A cl9; R cl8 (stress) | R cl5 (stress), cl11 | A c7 (vessel-associated cells) | absent | - |
| Ray_Parenchyma | possibly cl10 (TIP1-like ray LCM gene is specific there) | R cl3, cl5, cl11 | absent | hidden in 12 | A Ptr8 |
| Pith | absent | - | probably in unidentified c0/c1 | - | - |
| Phloem_Fiber, Collenchyma, Crystal_Idioblast, Trichome | absent (cl16 = crystal cells is a guess) | - | absent | - | - |
| Dividing_cells / S_Phase | state cl14, cl15 (unlabelled, correct) | state cl9 | state c8, c19 | - | - |
| Rejected | cl16 | cl0, cl1, cl8 | c14, c21, c22 | 12 | Ptr9, Ptr10 |

## Recommended label reference

- **Whole stem (bark + wood, young internodes): Schmidt 2025.** It is the only replicated dataset, is in Potri v4 IDs, has in-species promoter::GUS for three markers and a knockout, and leaves unknown clusters unlabelled. Adopt c4/c5 (XMC), c7 (xylem parenchyma), c12 (PP), c18 (CC). Relabel c15 as Endodermis, c25 as Vessel_Element (PCD stage), c3 as fiber-biased Xylem; reject c14, c21 and c22. Per-cell labels need the 358 MB RDS (read `meta.data` in a job).
- **Bark of older stems (sieve elements, phellem, epidermis): Chen 2021**, at cluster level only (no per-cell table). Its SE cluster (cl19) is the only clean one in poplar.
- **Xylem cell types (fiber, vessel, ray): Tung 2023**, because its fiber and ray clusters are backed by LCM of the same cell types and its per-cell table is small and public. Ptr1 "vessel" is over-sized; use the vessel LCM genes below to split it.
- Do not use Li 2021 or Wei 2026 labels as ground truth: Li has pseudotime-only and photosynthesis/stress-defined clusters and no per-cell table; Wei assigns 98% of nuclei to one catch-all cluster.

## How the draft table was graded

- `ref_gene` = *P. trichocarpa* v4 Potri locus. Every ID was taken from a paper's own table (Chen Table S2/S4 best Potri hit, Li Dataset S3/S7 JGI column, Schmidt Additional file 2, Wei Dataset S2/S3, Tung Additional files 3/15) and checked in UniProt (taxon 3694, `gene:POPTR_<id>`); exceptions are listed under "Could not verify".
- `alt_id` mixes three genomes, chosen in this order: Chen `pou` ID (*P. alba* var. *pyramidalis*), else Li `Pop_A/G` ID (84K), else Schmidt `PtXaAlbH` (717 HAP2 v5.1); empty for 7 rows. The prefix tells the genome. These are best-hit pairings from the papers, not curated orthologs; with `--id-column alt_id` only rows from the matching genome will hit.
- `tissue` = `stem`, a new value (the README of the marker tables lists only leaf/root/any).
- `requires=eudicot` on Cambium, Xylem_Mother_Cell, Ray_Parenchyma and Phellem rows (secondary growth and periderm do not exist in grass stems) and on Endodermis/GL2 rows (shoot starch sheath and GL2 epidermal patterning are eudicot features; SCR orthologs mark bundle sheath in grasses). A `secondary_growth` trait tag would be more precise; adding it needs a change to `IMPLIES` in `map_markers.py` and was not made.
- Grades follow `literature_search.md`. In-species validation = RNA in situ (Chen, Wei; Li's probes count only weakly because the images were not seen), promoter::GUS (Schmidt) or LCM of the cell type (Tung). Agreement raised confidence one level when the same Potri ID was validated in one study and cluster-specific in another, or, for `function` genes, cluster-specific in two independent studies. Enrichment that is broad (pct.out > ~0.2) or lands in a different cell type did not count.
- No row is a dataset-only DE pick: the six `expression` rows are uncharacterized genes that are LCM-specific in Tung 2023 and cluster-specific in at least two other datasets.

## Cross-study markers (45 rows with independent agreement)

| Cell type | Markers (confidence) | Studies agreeing |
|---|---|---|
| Vessel_Element | XCP2 Potri.005G256000 (high), XCP2-like Potri.002G005700 (high), XCP1 Potri.004G207600 (high), MAN6 Potri.016G138600 (high), LAC17-like Potri.001G401300 (high), WAT1-like Potri.002G029100 (medium), ACL5 Potri.006G222200 and Potri.008G151800 (medium), pectate lyase Potri.003G131700 and polygalacturonase Potri.001G463000 (medium, expression) | Tung vessel LCM + Schmidt c25 + Li cl7 for the PCD-stage genes; Wei in situ for XCP2 and WAT1; ACL5 enriched in early xylem in all four RNA datasets |
| Xylem_Fiber | IRX15-L Potri.005G141300, FLA12 Potri.009G012200, CTL2 Potri.010G141600, CslA1 Potri.008G026400, F5H Potri.005G117500, SND1-A1 Potri.011G153300 (all high); Potri.010G121800, Potri.008G112300 (medium, expression) | Tung fiber LCM and Ptr7; Wei in situ (CTL2 fiber arrow, FLA12); Chen cl4; Li cl2/6; Schmidt c3 |
| Xylem (SCW) | ESK1a, CesA4, CesA8-A, MYB46, MYB83-like, KNAT7 (high); GUX1 (medium) | Chen in situ (ESK1a), Schmidt GUS (KNAT7); all four RNA datasets |
| Xylem_Parenchyma | MYB48-2 Potri.009G027300 (high) | Schmidt VAC c7 + Tung ray LCM |
| Ray_Parenchyma | TIP1-like Potri.001G235300 (medium) | Tung ray LCM + Chen cl10 |
| Phloem | APL Potri.010G174100, SMXL5 Potri.006G073800 and Potri.018G140900 (high) | Chen in situ (APL) + Chen cl6/13/19 + Schmidt c17/c18 |
| Phloem_Companion | PP2-A1 Potri.012G120400, PP2-A9/A10-like Potri.015G120100 (high) | Chen cl13 + Schmidt c18 |
| Phloem_Parenchyma | four UMAMITs: Potri.006G082700, Potri.001G032500, Potri.005G176100, Potri.002G085100 (medium) | Chen cl18 + Schmidt c12 |
| Endodermis | SCR/SGR1 Potri.006G114200, LAZY1 Potri.001G059100 and Potri.003G168700 (high) | Chen cl17 + Schmidt c15 (both mislabelled by the authors) |
| Dividing_cells / S_Phase | CDKB2;1, CDKB1;1, KNOLLE, CYCB2;4, H2A, PCNA (high) | Chen cl14/15, Li cl9, Schmidt c8/c10 |

## Gaps (expected types without a validated `function` marker)

- **Phellem and phellogen.** Only Chen 2021 has cork (cl11, peroxidases and ABCG32); its ASFT (pou01365 / Potri.001G326300) is in Table S4 but not among the cluster-enriched genes. No phellogen cluster exists anywhere.
- **Phloem_Companion and Phloem_Parenchyma** have strong cross-study markers but no `function` row: the poplar SUC2 orthology is unclear (see conflicts) and Arabidopsis SWEET11/12 have no enriched poplar ortholog in either bark dataset.
- **Ray_Parenchyma**: only LCM-backed, uncharacterized-function rows. Ray vs axial parenchyma is resolved in no dataset.
- **Cortex, collenchyma, pith, phloem fibers, crystal idioblasts, trichomes**: no marker in any dataset.
- **Vessel vs fiber at the SCW stage** in nuclei data: Schmidt c13 and Wei 11-L1 merge them; use the LCM-backed rows to split.

## Conflicts and corrections

- **SCR vs SCL23.** Potri.006G114200 is called SCL23 by Chen 2021 (best AGI hit AT5G41920) and SCR by Schmidt 2025. UniProt A0A385JI69 (*P. tomentosa*) names this locus SGR1, i.e. SCARECROW. Kept as SCR/SGR1. Chen's separate "SCR" Potri.T138100 is a v3 scaffold ID absent from UniProt; Schmidt's c15 has a second SCR, Potri.016G143833, also absent from UniProt. These may be the same gene in v3 and v4 (not verified; needs Phytozome).
- **Cluster labels corrected.** Chen cl17 "cortex/endodermis initial" and Schmidt c15 "phellogen" are both shoot endodermis (SCR, LAZY1, PIN3/LAX3). Stems have no CEI, and periderm is unlikely at LPI 4-5.
- **Same symbol, different gene.** "MYB46": Chen used Potri.001G258700 (PtrMYB2), Li and Schmidt used Potri.009G053900; the table carries the latter. "SUC2": Chen Potri.013G115200 vs Schmidt Potri.019G085800. "PP2-A10": Chen Potri.012G120300 vs Schmidt Potri.015G120100. "PXY": Chen/Schmidt Potri.001G126100 vs Li Potri.003G107600. "CESA8": Potri.004G059600 (Chen) vs Potri.011G069600 (Schmidt). "ACL5": Li Potri.008G151800 vs Wei Potri.006G222200. "ASFT": Chen Potri.001G326300 (cork) vs Schmidt Potri.015G100800 (epidermis).
- **Schmidt "SUC2" Potri.019G085800 is not companion-cell-specific**: it is also enriched in SCW xylem (Chen cl4, Schmidt c3) and in fiber LCM (Tung). It may be a wood-fiber SUT (PttSUT3-like); kept as `low` with the caveat.
- **Vessel vs fiber for Li cluster 7.** Chen et al. 2024 (*Genome Biol* 10.1186/s13059-024-03227-5) argued Li's "vessel" markers track fibers. Tung's own vessel LCM puts XCP2 (V 2332 vs F 40 TPM), XCP2-like, MAN6 and LAC17-like in vessels, and so does Schmidt's c25, which supports Li's vessel call for those genes. In Tung's protoplast clusters the same genes land in Ptr7 (fiber), so protoplast clusters mix late vessels with fibers.
- **AHA5 (Potri.006G275000)**: Li 2021's in situ probe for "ray I" cl11, but specific to companion cells in Chen (cl13, 0.93/0.02) and Schmidt (c18). Not carried.
- **ABR1 (Potri.005G087200)**: in situ xylem parenchyma in Chen 2021; Tung 2023 reuses the same image as "organizer cell location"; Li's agreeing cluster is a wound/ethylene state. Kept at `medium`, not raised.
- **CAD7**: Chen's review cited "Li 2021 JIPB" for CAD7 as a xylem parenchyma marker; the gene is not in the Li 2021 (*jipb.13159*) tables. Kept `low` on Chen data alone.
- **Wei 2026 naming errors** (from its review): ACL5 is called a methyltransferase and "GH1" Potri.011G047700 is a glycosyltransferase. Potri.011G047700 is also vessel-LCM-specific (Tung: V 63 vs 0) and in Schmidt c25 (0.50/0.005); not carried because it has no characterized function.
- **Schmidt Additional file 2**: sheet "Cluster 21" duplicates cluster 24, so the CEID cluster has no marker table.

## Overlap with existing skill tables

There is no poplar table in `references/markers/`, so there is no same-species overlap. By homology, the draft shares genes with the Arabidopsis tables: APL (Phloem), SEOR1 (Sieve_Element), XCP1/XCP2 (Arabidopsis `Xylem`; here `Vessel_Element`), MYB46 (Xylem), SCR (root Endodermis; here shoot endodermis), FDH (Epidermis), KNOLLE and PCNA (states). Two naming differences: Arabidopsis leaf lists GL2 under `Trichome` (here `Epidermis`), and ATHB8 under `Procambium` (here PttHB8 under `Xylem_Mother_Cell`). New cell-type names introduced: `Cambium`, `Xylem_Mother_Cell`, `Vessel_Element`, `Xylem_Fiber`, `Xylem_Parenchyma`, `Ray_Parenchyma`, `Phellem` (plus `Phellogen`, `Collenchyma`, `Pith`, `Phloem_Fiber`, `Crystal_Idioblast`, `Trichome` in the expected list only).

## Could not verify

- **Phytozome** (v4 annotation) needs a login, so v3-to-v4 renames could not be checked. Potri.T138100, Potri.016G143833, Potri.006G114200, Potri.009G102700 (Li's LAC22 in situ probe) and Potri.006G181900 (CesA7-A) are not in UniProt under `POPTR_` names. Only Potri.006G114200 is used, on the strength of the *P. tomentosa* SGR1 entry.
- The `pou` (Chen) and `Pop_` (Li) IDs in `alt_id` could not be checked in a genome database (GWH and the 84K genome are large downloads); they are the papers' own pairings.
- Li 2021 in situ images and the main text are paywalled (Wiley 403; jipb.net login), so Li's probe genes were not used as validation.
- Tung 2023 was not given a full Step 3a review: only its cluster DEG and LCM DEG tables and the relevant text were read. Its Additional file 13 (known xylem genes) link returned a 466-byte non-Excel file.
- Literature functions cited in `basis` (e.g. Kucukoglu 2017, Etchells 2015, Zhu 2013, Milhinhos 2013, MacMillan 2010) were taken from the reviewed papers and general knowledge, not re-read; DOIs in `source` are for the single-cell datasets only.
- CNCB GSA pages (Chen CRA004476, Wei CRA038282/CRA038285) are behind a bot check and were not accessed. Large objects (Schmidt RDS 358 MB / 1.24 GB, GEO RAW tars, Liang 2024 Zenodo 182 MB) were not downloaded.

## Update 2026-10-20: gap-fill reviews

Two reviews were merged: a full Step 3a review of **Tung 2023** (until now used only through its tables) and a new review of **Qi 2026**. Both target the `Ray_Parenchyma` gap. Rows were merged by Potri ID. `build_markers_draft.py` now carries them in a block marked "Update 2026-10-20", and the table was rebuilt from it (78 to 96 rows).

### New datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Tung et al. 2023 *Genome Biol* 24:3, 10.1186/s13059-022-02845-1 (full review; folder `Tung2023/`) | *P. trichocarpa* debarked stem-differentiating xylem | Protoplasts, 10x 3' (batch 1, K-means k=10), plus LCM RNA-seq of fibers, vessels and rays (3 reps each) | 4,705 labelled (of 25,166 profiled) | Potri v4.1 | small per-cell table (`Tung2023_Ptr_Barcode_Cluster.csv`) | medium |
| Qi et al. 2026 *Plant Cell* 38(9):koag275, 10.1093/plcell/koag275, PMID 42725656 (DOI confirmed in Europe PMC; folder `Qi2026/`) | *P. tremula x alba* 717, 10 um tangential sections of the cambial zone, 3 sections | BMK S3000 spot-based spatial (2.5 um spots), image-segmented pseudo-single cells; RNA in situ for each cluster marker | 22,597 segmented cells, 19 clusters | Potri (version not determined) | none (no accession, no table seen) | medium for the XRP_2 marker, low for the "initial" labels |

Independence: Qi 2026 is a different lab and new data (Q. Li is a co-author, as on Li 2021 and Wei 2026). Tung 2023 was already a source of the draft, so its full review adds no independent support for rows that already cited it.

### Verdicts

| Dataset | Cluster | Verdict | Canonical | Reason |
|---|---|---|---|---|
| Tung 2023 | Ptr8 R (136, 2.9%) | Adopt | Ray_Parenchyma | best match to ray LCM; 48 genes up in both |
| Tung 2023 | Ptr7 F (433) | Revise | Xylem_Fiber + maturing vessels | vessel-LCM PCD genes (XCP1/2, MAN6, LAC17-like) are also Ptr7 DEGs |
| Tung 2023 | Ptr1 V (1,140, 24%) | Revise | early/expanding xylem incl. young vessels | too large; lacks strong vessel-LCM genes |
| Tung 2023 | Ptr2-6 organizers/precursors | Revise | Xylem_Mother_Cell (hypotheses) | UMAP order and HD-ZIP III only; Ptr4/Ptr5 carry CDKB2;1, MCM3 and histones (partly dividing) |
| Tung 2023 | Ptr9, Ptr10 (54) | Reject | - | unlabelled, no DEGs |
| Qi 2026 | FIC, RIC_1, RIC_2 | Revise | Cambium (dividing state) | markers are CDKB2-like, histone H2B and a CHI-family gene, all in the dividing clusters of Chen, Li and Schmidt; fusiform vs ray initials are told apart by position only |
| Qi 2026 | XRP_1 | Revise | Xylem_Mother_Cell / early xylem ray | marker ACL5-2 (Potri.008G151800) marks vessels/XMC elsewhere |
| Qi 2026 | XRP_2 | Adopt (marker level only) | Ray_Parenchyma (developing) | LTP-like Potri.001G121900 in situ in ray cells and the top Tung Ptr8 gene |
| Qi 2026 | XRP_3 | Revise | contested | marker ACLA Potri.013G004400 is fiber-enriched in Tung Ptr7, Li cl6, Schmidt c3 |
| Qi 2026 | XMC/XPC, PRP, PMC, PHC_1-5, ECC_1/2 | Revise | positional / merged | no markers seen; PHC and ECC merge types |

Revised cross-dataset row: **Ray_Parenchyma** is now Tung Ptr8 (A) plus Qi XRP_2 (A, marker level only). **Cambium**: Qi FIC/RIC are dividing-state clusters.

### Markers added (18 rows)

- **Ray_Parenchyma (12)**: LTP-like/HyPRP Potri.001G121900 (`characterized_enriched`, medium: Qi in situ plus Tung Ptr8; would be high once the Qi in situ and ID are confirmed from the paper). Eleven `expression`/low rows, all ray LCM plus Ptr8: Potri.014G162800, Potri.002G223100, Potri.003G111400, Potri.001G416500 (also in Chen cl10 or Li cl3/8/11, but broad in whole stem), and Potri.003G131200, Potri.001G276200, Potri.012G140700, Potri.002G068300, Potri.001G332800, Potri.005G143200, Potri.009G156900 (LCM ray vs fiber/vessel about 0; single study). The single-study rows break the earlier rule that `expression` rows need two other datasets. They were added because ray had no other candidates and the LCM is a cell-type measurement, not a cluster DE pick. Drop them if a stricter table is wanted.
- **Xylem (1)**: PtrCesA7-A Potri.006G181900 (`function`, high). It is in the Chen cl4, Li, Schmidt c13/c3 and Tung fiber-LCM tables. Earlier it was left out only because UniProt has no POPTR_ entry for it.
- **Xylem_Fiber (3)**: aspartic protease Potri.019G002100 (medium: fiber LCM plus Chen, Li and Schmidt SCW clusters); two FLAs, Potri.019G121200 and Potri.013G151300 (low: fiber LCM about 200-fold over vessel, weak elsewhere). These help split fiber from vessel.
- **Dividing_cells (1)**: CHI-family Potri.007G057800 (`expression`, medium: Chen cl14/15 plus Schmidt c8). **S_Phase (1)**: histone H2B Potri.008G030600 (`function`, medium: Li cl9 plus Schmidt c8; not in UniProt).
- **Edited, not raised**: the PtACL5-2 (Potri.008G151800) and CDKB2;1 (Potri.005G257500) basis lines now note the Qi in situ. **No confidence was raised.** Qi's evidence is from a summary of the article page, and its two overlapping markers either are already high (CDKB2;1) or are not specific to the row's cell type (ACL5-2 in developing rays as well as vessels).

### Not carried

Photosynthetic ray-LCM genes LHCB1-like Potri.005G239300, RBCS Potri.017G114600 and NADP-MDH-like Potri.008G031700: they mark cortex/chlorenchyma in Chen cl0/cl7 and Schmidt c0/c2/c9, so they would mislabel bark in whole-stem data. Also not carried: peroxidase Potri.005G195600 (weak in Ptr8, enriched in XMC/xylem parenchyma elsewhere); ACLA Potri.013G004400 (Qi ray in situ conflicts with fiber enrichment in three datasets); Fb34 Potri.011G122700 (broad, pct.out 0.5-0.7); 4CL Potri.003G188500 (also Schmidt c25 vessels); and expansin Potri.001G240900 (broad cambium/XMC, pct.out about 0.45).

### Characterized-marker survey (non-single-cell studies)

Rows tagged `populus_stem:` in `survey/characterization/characterized_markers.tsv` are Arabidopsis genes (SUC2, SWEET11/12, GPAT5, MYB67, SGNH, WOX4, MYB68, GL1, GL2) with no Potri ID, so they map by homology only, plus one poplar row. That row is **PtSHR2B Potri.017G019900**: promoter::GUS in phellogen and overexpression increases bark (Miguel et al. 2016 *J Exp Bot*, 10.1093/jxb/erv547; ID from a secondary summary, id_checked False). It has the same ID as the draft's Endodermis row PtSHR2b (`characterized_enriched`, low). It was not moved to Phellogen because no single-cell dataset has a phellogen cluster and the ID is unchecked. Treat it as a candidate Phellogen marker in older stems.

### Gaps closed

- **Ray_Parenchyma: partly.** It now has one cross-validated developing-ray marker (Potri.001G121900) and a ray-LCM gene set. There is still no `function` marker.

### Gaps remaining

- Ray_Parenchyma has no `function` marker. Ray vs axial/contact parenchyma, and mature vs developing rays, are still not separated, and phloem rays (Qi PRP) have no marker.
- No new data for Phellem, Phellogen (PtSHR2B candidate only), Cortex, Collenchyma, Pith, Phloem_Fiber, Crystal_Idioblast, Trichome, or the CC/PP `function` gap. Qi's phloem and bark clusters are positional and merged.

### Conflicts

- Qi "fusiform/ray initial" markers are cell-cycle genes (CDKB2-like, H2B, CHI-family). They are listed here as Dividing_cells/S_Phase, not as initial identities.
- ACL5-2 Potri.008G151800: Qi in situ in developing ray cells, vessel/XMC in Tung, Schmidt and Chen. Kept as Vessel_Element `medium` (early xylem).
- ACLA Potri.013G004400: Qi calls it a developing-ray marker, but it is fiber-enriched in Tung, Li and Schmidt. Not carried.
- Tung's Ptr7 "fiber" includes maturing vessels and Ptr1 "vessel" is early xylem. This agrees with the existing note on Li cluster 7.

### Recommended label reference

Unchanged. Qi 2026 has no public labels or data, and the Tung 2023 review confirms Ptr8 (ray) and supports Ptr7 (fiber, with maturing vessels) at the levels already recommended above.

### Could not verify

- Qi 2026 full text, figures (Fig. 5h in situ, Fig. S10) and Supplementary Data Sets S1-S13 (S12 = 227 ray-lineage candidates): the OUP page returns a Cloudflare bot check and is behind a subscription. It was not bypassed. The six Qi IDs come from a summary of the page. They exist in the Li, Schmidt and Tung tables and, except H2B, in UniProt, but whether they are the genes Qi used is unconfirmed. With Stanford access, the user can download the article and Data Set S12 into `Qi2026/` to confirm them.
- No accession was found for Qi's spatial data. Potri.006G181900 and Potri.008G030600 have no UniProt entry, and Phytozome needs a login.
