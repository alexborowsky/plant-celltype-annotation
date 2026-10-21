<!-- Collated from the survey review of sorghum_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# sorghum_root: collated cell-type marker resources

Collated on 2026-10-20 from the two dataset reviews in `survey/merged_reviews.json` (group `sorghum_root`) and their folders `Guillotin2023/` and `Venado2026/` (each has its own README). Nothing in the skill was edited.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Sorghum root-tip cell types, from anatomy (seminal and aerial nodal roots). `function_markers` = `function` rows for the type in `arabidopsis_root.tsv` + `rice_root.tsv` (after Sorghum trait filtering, via homology) + `markers_draft.tsv` |
| `markers_draft.tsv` | 40 rows in the skill schema plus `alt_id`. 36 rows use BTx623 `Sobic.` IDs (`alt_id` = NCBIv3/Ensembl `SORBI_3` ID); 4 rows use RTx430 v2.1 IDs (`SbiRTX430.`), with an empty `alt_id` |

## Datasets

| Dataset | Citation | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Guillotin2023 | Guillotin et al. 2023 *Nature* 617:785, doi:10.1038/s41586-023-06053-0; GEO GSE225118; figshare 22331002 | 10x 3' v3; BTx623 primary-root tips (0.5 cm); 1 protoplast + 3 nuclei libraries; co-integrated with maize and Setaria on single-copy orthologs | 3,510 cells + 7,620 nuclei (paper); 13,299 sorghum barcodes in the GEO metadata; 19 named types | NCBIv3 `SORBI_3` (= `Sobic.`); 1:1 orthologs renamed to maize B73 v4 in the object and the DE tables (conversion in Supp Table 1) | large object: per-cell numeric clusters in a 1.1 MB GEO CSV; the cluster-to-name map is only in the 3.7 GB RData | medium |
| Venado2026 | Venado et al. 2026 bioRxiv, doi:10.64898/2026.09.29.755433; GEO GSE348174 and PRJNA1532956 (both private) | 10x 3' v3.1, FANS nuclei; IS23992 aerial nodal-root tips; 1 dry + 1 wet library | 11,526 nuclei, 15 clusters | RTx430 v2.1 (`SbiRTX430.`), not BTx623 | cluster only (SD2 and Fig 1) | low |

Other papers checked (Europe PMC, 2026-10-20) and excluded: Bojdová et al. 2026 *Plant Biotechnol J* (snRNA-seq of *S. purpureosericeum* embryos, not root); Liu et al. 2026 *Plant Physiol* (sorghum HS1 myosin VIII in leaf protoxylem; a leaf protoxylem lead, not root).

## Per-cell-type verdicts across datasets

A = Adopt, R = Revise, X = Reject, "-" = no such label. Names are the skill's canonical names.

| Canonical type | Guillotin2023 | Venado2026 |
|---|---|---|
| Phloem | A (Phloem; sorghum HCR) ; R (Young_Phloem, early phloem) | R (S1/S5 "Stele/Phloem": no phloem evidence; S5 X) |
| Xylem | A (sorghum HCR, CESA8) | - (missing) |
| Endodermis | A (sorghum HCR, PER72-like) | R (S8, probably mixed with stele/pith; S4 Cortex/Endodermis merged) |
| Pericycle | R (no sorghum validation) | - |
| Procambium / Stele | R (Stele_2 = procambium + protophloem); X (Stele_1, ribosome-biogenesis state) | R (S1 Stele unresolved) |
| Cortex | R (Cortex_1, 3, 4); X (Cortex_2) | R (S3; also S4 merged) |
| Exodermis / hypodermis | - (maybe in Cortex_4, inferred) | - |
| Epidermis | R (Epidermis_2, 3); X (Epidermis_1) | A (S14); R (S15, dry library only) |
| Trichoblast | R (not position-patterned in grasses; shares epidermis markers) | - |
| Lateral_Root_Cap | R (expansins only) | R (S2, S6, S11 "Columella/Root cap", single-library clusters) |
| Columella | R (HCR gene not DE; weak markers) | R (as above) |
| Border_Cell | - | A (S12; sorghum in situ marker) |
| Quiescent_Center | - | R (S7, S9, S10, S13 = 36% of nuclei: meristem/proliferation, not QC) |
| Dividing_cells (state) | R (G2_M kept as state; Young_Stele_2 = S phase) | - (absorbed into "QC") |

Neither dataset has QC, exodermis/hypodermis, sclerenchyma or pith as a validated type. Proto- and metaxylem are not split, and sieve elements and companion cells are not split.

## Cross-study markers

**None by gene ID.** The two datasets use different genome assemblies (BTx623 vs RTx430 v2.1), and the RTx430-to-BTx623 table is on Phytozome behind a login. RTx430 IDs are not in UniProt, SorghumBase or Ensembl. So no `confidence` was raised for cross-study agreement.

Where the two studies touch the same gene through maize orthologs (Ensembl Compara, 2026-10-20), they **disagree**:
- Venado's sorghum "endodermis" gene SbiRTX430.01G515100 is described as the ortholog of their maize in situ endodermis marker Zm00001eb005460. That maize ID is **ZmSUT1** (UniProt C4J697/A0A804LEF3, Gramene transcripts), not a glutaredoxin, and its BTx623 ortholog is SORBI_3001G488700 (SbSUT1). In Guillotin, SbSUT1 is weakly enriched in **Phloem** (pct 0.16 vs 0.06) and pericycle, not endodermis. The draft keeps SbSUT1 as `Phloem_Companion` and flags the Venado row with `REVIEW:`.
- Venado's root-cap callose synthase SbiRTX430.04G115800 has maize orthologs Zm00001eb148030 and Zm00001eb367780, which map to BTx623 SORBI_3003G355200. That gene has no cap-specific DE in Guillotin (its maize v4 IDs are absent from Markers_Sorghum). This is a candidate mapping only.

Agreement with other skill tables (same sorghum ID, not an independent single-cell study): Sobic.003G296400 (CESA8/IRX1) and Sobic.009G008800 (XCP1) are xylem markers in `sorghum_leaf.tsv` too.

## Draft marker table summary

| Cell type | Rows | function | characterized_enriched | expression | Best marker |
|---|---|---|---|---|---|
| Phloem | 10 | 2 | 3 | 5 | Sobic.002G066400 (sorghum HCR); APL Sobic.004G058700 |
| Phloem_Companion | 1 | 1 | 0 | 0 | SUT1 Sobic.001G488700 (weak in root) |
| Xylem | 5 | 3 | 2 | 0 | CESA8 Sobic.003G296400 (sorghum HCR + function), XCP1 Sobic.009G008800 |
| Procambium | 1 | 1 | 0 | 0 | HD-ZIP III (CNA/ATHB15) Sobic.003G028300 |
| Stele | 1 | 1 | 0 | 0 | SHR2 Sobic.002G357800 (weak) |
| Pericycle | 3 | 1 | 0 | 2 | HMA2 Sobic.010G250900 |
| Endodermis | 6 | 1 | 1 | 4 | PER72-like Sobic.006G079300 (sorghum HCR) |
| Cortex | 2 | 0 | 1 | 1 | GH17 Sobic.009G119200 (expression) |
| Epidermis | 2 | 0 | 0 | 2 | MUR3-like Sobic.001G229000 (expression) |
| Lateral_Root_Cap | 2 | 0 | 0 | 2 | EXPA17-like Sobic.003G112100 |
| Columella | 1 | 0 | 0 | 1 | FUT Sobic.004G125300 (ID ambiguous) |
| Root_Cap | 3 | 0 | 2 | 1 | PMI Sobic.003G087900 (HCR); CalS SbiRTX430.04G115800 (in situ) |
| Border_Cell | 1 | 0 | 1 | 0 | SbiRTX430.05G002900 (in situ; RTx430 ID) |
| Dividing_cells (state) | 2 | 1 | 0 | 1 | CCS52B/FZR-like Sobic.003G444100 |

Grading followed `literature_search.md`: sorghum in situ + function = `function` high; sorghum in situ alone = `characterized_enriched` medium; characterized ortholog with scRNA enrichment only = `function` medium or `characterized_enriched` low; uncharacterized DE genes = `expression`, medium only if specific to one lineage. `requires=grass` only on SUT1 (grass SUT1 clade). No `excludes` was needed: no row is C3- or eudicot-specific.

## Gaps (no validated sorghum marker)

- **No `function` marker at all** (any table): Border_Cell, Epidermis, Atrichoblast, Cortex, Protoplasting_stress. Step 4 search targets.
- **Only by homology from Arabidopsis or rice** (nothing sorghum-validated): Columella, Lateral_Root_Cap, Quiescent_Center, Stem_Cell_Niche, Trichoblast, Exodermis, Sclerenchyma.
- **Weak**: Pericycle and Procambium (scRNA enrichment of characterized orthologs only), Phloem_Companion (SUT1 weak), Stele_Parenchyma/pith (SHR only).
- **Not resolved anywhere**: protoxylem vs metaxylem; sieve element vs companion cell; QC.

## Recommended label reference

**Guillotin et al. 2023**, for primary/seminal root tips of BTx623-based data. It is the only sorghum root atlas with sorghum in situ validation (phloem, xylem, endodermis), with BTx623 IDs and public per-species DE tables. Adopt Phloem, Xylem and Endodermis. Collapse Cortex_1-4 to Cortex and Epidermis_1-3 (+ Trichoblast) to Epidermis. Treat G2_M and Young_Stele_2 as states and reject Stele_1. Per-cell names need the 3.7 GB RData (`GSE225118_Maize_Sorghum_Setaria_Cells_Nuclei_Seurat_Obj.RData.gz`); export its metadata in a job.

**Venado et al. 2026** only for border cells and the aerial-root cap (S12 Border cells), once GSE348174 is public and RTx430 IDs are mapped to BTx623. Do not reuse its QC labels.

## Overlap with existing skill tables (sorghum)

- `sorghum_root_Guillotin2023.tsv` (1,187 rows, all `expression`, the paper's cross-grass common markers projected from maize): 15 of the 36 BTx623 draft genes are in it. The draft adds the sorghum HCR genes (Sobic.002G066400, .003G296400, .006G079300, .003G087900), the sorghum-specific DE markers, the TF/characterized orthologs (APL, SCR1, SHR2, HMA2), grading and `basis`. Cell types disagree for **Sobic.001G217200 (REV)**: Columella in the skill table, but top sorghum enrichment is Xylem (0.31 vs 0.03; columella 0.14 vs 0.04).
- `sorghum_leaf.tsv`: shares Sobic.003G296400 (IRX1, Xylem), Sobic.009G008800 (XCP1, Xylem) and Sobic.001G488700 (SUT1, Phloem_Companion). The cell types agree.
- The skill's sorghum tables use `Sobic.` IDs; the draft keeps that in `ref_gene` and puts `SORBI_3` IDs in `alt_id`.

## Conflicts and corrections to the reviews

1. **Venado endodermis marker** (above): Zm00001eb005460 is ZmSUT1, not a glutaredoxin. Either the ID or the description in the paper is wrong. The Venado review carried "glutaredoxin" from the text.
2. **"HB8-like" Sobic.003G028300**: Ensembl Compara gives a one-to-one ortholog AT1G52150 (CORONA/ATHB15), not ATHB8. Still HD-ZIP III and procambial, so the row is kept as Procambium with the corrected symbol.
3. **VND-like NAC Sobic.006G160900**: the review marked the clade as inferred. Ensembl Compara places it with VND4/5/6 (AT1G12260, AT1G62700, AT5G62380), so it was upgraded to `characterized_enriched`.
4. **CDC20/FZR-like Sobic.003G444100** is the one-to-one ortholog of AT5G13840 (FZR3/CCS52B).
5. **Ambiguous IDs** (in Guillotin Supp Table 1, one maize gene maps to several sorghum genes): nsLTP Zm00001d003757 → Sobic.006G074200/.074300; FUT Zm00001d053327 → Sobic.004G124800/.125100/.125300. Kept at `low`, and the ambiguity is noted in `basis`.
6. **Guillotin endodermis HCR gene** appears twice in Markers_Sorghum: as SORBI-3006G079300 (pct 0.166 vs 0.023) and as its maize alias Zm00001d003707 (0.088 vs 0.003). The review's numbers are from the first.
7. **Venado internal inconsistencies** (from the review, confirmed in the XML): the root-cap probe is 04G115800 in the text but 03G383000 in SD1; SD1 claims a cortex in situ for villin 01G385000 that the text contradicts. Villin was not carried forward.
8. **PPR Sobic.007G033900**: phloem in Guillotin (maize HCR), but endodermis-enriched in maize bulk data (Ortiz-Ramirez 2021). Kept as Phloem, `low`.

## ID checks done

- All 35 Guillotin BTx623 genes were re-derived from the paper's own tables: maize v4 ID → sorghum through Supp Table 1 ("Orthologs Gene Used", both single and two-homeolog blocks), and pct/log2FC from Supp Table 4 `Markers_Sorghum`. All matched the review.
- 30 genes were confirmed in UniProt (taxonomy 4558, `SORBI_3` ordered-locus names), with protein names that agree with the review's symbols. SbSUT1 (SORBI_3001G488700) was also confirmed (UniProt C5WVY0; named SUT1 in A0A0H4AWF3).
- Arabidopsis/rice orthologs were checked in Ensembl Compara: APL, SCR, SHR, REV, CESA4, CESA8, FZR3, VND clade, PER72, OsHMA2 (one-to-one with Sobic.010G250900).

## Could not verify

- RTx430 v2.1 IDs (all Venado rows): no public mapping to BTx623 (Phytozome needs a login), and they are not in UniProt or Ensembl. These 4 rows will not match BTx623 data until mapped.
- Ensembl Compara timed out (HTTP 503 / HTML) for XCP1 (Sobic.009G008800) and CalS7-like (Sobic.003G179600). Their identities rest on the paper's annotation, UniProt protein names (CalS7: 1,3-beta-glucan synthase; XCP: uncharacterized) and the sorghum_leaf curation (XCP1).
- Per-type cell counts for Guillotin: these need the 3.7 GB RData (not downloaded).
- Venado Supp Figs 5, 6, 9 and 10 (media-2.pdf, over 50 MB) and Fig 3: not read. The in situ images for border cells and root cap were assessed from Fig 2 only.
- No sorghum CASP, MYB36, WOX5/QHB, SMB, SUC2-type or root-hair gene has been validated in a sorghum root single-cell study. Their sorghum orthologs come into play only through `map_markers.py` homology from `arabidopsis_root.tsv` and `rice_root.tsv`.
