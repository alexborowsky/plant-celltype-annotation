<!-- Collated from the survey review of selaginella_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Selaginella moellendorffii root: collated marker resources

Group collation for the plant-celltype-annotation skill, 2026-10-20. Built from the one review in `survey/merged_reviews.json` (group `selaginella_root`) and its folder `Yang2023/` (that review's own README is left unchanged). IDs were re-checked against the paper's Data S1A table and UniProt REST (taxid 88036).

## Files

| File | Content |
|---|---|
| `markers_draft.tsv` | 19 rows (17 genes; SmSCRa and SmSCRb each have two NCBI loci, so each gets two rows). Skill schema plus `alt_id`. `ref_gene` = NCBI RefSeq `LOC` ID, `alt_id` = PLAZA/JGI `SMO` ID (empty for SmPLTe) |
| `expected_cell_types.tsv` | 11 types and states from root anatomy, with function-marker counts taken from `markers_draft.tsv` |
| `Yang2023/` | dataset review, supplementary files, point locations, and the region-label table |

## Datasets

| Dataset | Platform | Cells | Label access | Quality |
|---|---|---|---|---|
| Yang X et al. 2023 *Curr Biol* 33:4069 (10.1016/j.cub.2023.08.030) | Targeted smFISH, 97 genes (probably Resolve Molecular Cartography, not confirmed), plus HCR RNA-FISH, colorimetric in situ, and Arabidopsis complementation | No cells and no segmentation. 2,261 hexagon regions from one 0-day and one 3-day root; 444,598 transcripts | `cluster_only` (region labels, Data S2) | medium as a marker source; low as a label source |
| (supporting, not independent) Hawinkel et al. 2026 *Genome Biol* (10.1186/s13059-026-03976-5, PMC12951914) | Reanalysis of the Yang 2023 points (smoppix) plus two new HCR RNA-FISH experiments on gene pairs (BioStudies S-BIAD1942) | none | none | Same lab and samples. Tests whether gene pairs co-localize; it makes no tissue calls |

I found no Selaginella or lycophyte root scRNA-seq or snRNA-seq dataset (Europe PMC search, 2026-10-20). **There is only one independent study, so no marker meets the cross-study tier.**

## Per-cell-type verdicts across datasets

| Cell type | Yang 2023 (region cluster) | Yang 2023 (gene pattern) | Hawinkel 2026 |
|---|---|---|---|
| Root_Cap | none | Adopt (SmWOX13a, SmBRN by HCR) | - |
| Stem_Cell_Niche | inside the meristem clusters (Reject) | Revise (SmPLTe zone) | - |
| Dividing_cells (state) | Meristem 1-4 / 1-3 = proliferation state (Reject as types) | SmCYCB2;4, SmCYCA1;1a | - |
| Endodermis / ground tissue | none | Adopt (SmSCRa/b) | SCRb anti-localized with SHRa (consistent) |
| Cortex | Cortex 1 (0d): Revise, no specific gene | none | - |
| Epidermis | Cortex-epidermis 1-2 (3d): Revise, merged; cluster 3: Reject (artifact) | SmPINV outer layers (inferred) | - |
| Pericycle | merged into vasculature | none (Reject) | - |
| Stele | Vasculature clusters: Revise to Stele | SHRa plus stele-wide genes | most panel genes are central/vascular |
| Xylem | merged | Adopt, low n (SmTMO5b, SmVND1) | - |
| Phloem | merged | Revise (SmVND2 only) | - |

## Cross-study markers

None. Hawinkel 2026 reused the same smFISH data, and its HCR experiments test pairwise co-localization, so it does not count as independent validation. It did not raise any confidence level. The only result that bears on cell types is that SmSHRa and SmSCRb are anti-localized by HCR, which fits SHR in the stele and SCR in the ground tissue. I cited it in `basis` and did not upgrade either row.

## Strongest markers

- **Root_Cap:** SmWOX13a `LOC9660776` (function, high: HCR, plus cap induction in Arabidopsis) and SmBRN `LOC9638368` (medium).
- **Endodermis / inner ground tissue:** SmSCRa `LOC9638011`/`LOC112344873` and SmSCRb `LOC9635947`/`LOC9652292` (function, medium; in situ, plus scr-4 complementation). The domain may include the inner cortex.
- **Xylem:** SmTMO5b `LOC9640581` (medium).
- **Dividing_cells:** SmCYCB2;4 `LOC9635280` (high) and SmCYCA1;1a `LOC9650624` (medium).

## Gaps (no validated marker)

Cortex, Pericycle, Epidermis (only SmPINV, marked `REVIEW:`), Phloem (only SmVND2, low, and it conflicts with the family's role in seed plants), Procambium, and apical initials as distinct from the surrounding zone. All of these are Step 4 search targets. For a Selaginella target, map `arabidopsis_root.tsv` by homology (CASP1-4/MYB36 for endodermis, APL/SEOR-like genes for phloem) with care: there are no companion cells, and the epidermis is not patterned like the eudicot root.

## Recommended label reference

None for labels. The Yang 2023 region clusters are hexagon bins, not cells. They come from one root per time point, merge tissue layers, and are dominated by cell-cycle genes, so do not import them. Use Yang 2023 only as a marker source: for root cap, endodermis/ground tissue, xylem and dividing-cell markers; and for stele vs outer tissue.

## Conflicts and corrections to the review

- **Naming traps (compare by ID):** UniProt names differ from the paper's. SmWOX13a = "WOX8-1" (D8QUI1), SmVND2 = "VND4-2" (D8RAM9), SmVND1 = "VND2-1" (D8QQ16), and SmCYB2;4 = "CYCB1-1" (D8R4N3; the paper writes "SmCYB2;4"). NCBI calls SmBRN, SmVND1 and SmVND2 all "NAC domain-containing protein 105".
- **SmBRN orthology:** UniProt D8S100 (SELMODRAFT_451784) annotates SmBRN as ANAC012/NST3/SND1-like, a secondary-wall NAC clade, not BRN1/2. I kept it as Root_Cap at medium because the HCR pattern is in the cap, and recorded the caveat in `basis`.
- **Merged UniProt entries:** D8QUI1 (WOX13a: GeneIDs 9660776 and 9634901), D8R529 (AHP6b: 9652598 and 9657836) and D8R4N3 (CYCB2;4: 9635280 and 9640078) each cover two NCBI loci, probably the two haplotypes of the v1.0 assembly. Only the paper's LOC is in the table. Expression data on the other locus may also need mapping.
- **SCR genes span two loci:** Data S1A lists two LOC IDs per SCR gene, and both are rows in the table.
- **Correction to the review:** the review says Hawinkel 2026 HCR shows SmSGNb and SmPINS in the central vascular tissue. The Hawinkel text says "central vascular tissue" only for SmBIRDa and SmCYCD3;3a. For SGNb-PINS it reports co-localization in smFISH but a negative correlation by HCR. I removed that claim from the SGNb and PINS rows.
- **SmVND2 (phloem) vs the VND family (xylem in seed plants):** I kept it as Phloem, low, `requires=lycophyte`. Check that it does not overlap SmTMO5b before using it.
- **Evidence-tier changes:** SmVND2 changed from `expression`/medium to `characterized_enriched`/low (it has cell-resolution smFISH, but the conflict above). SmSCRa changed from medium-high to medium (its domain is broader than the endodermis).
- **Dropped:** SmAUX1a and SmPINR. Both are top genes of the 0d cortex cluster as well as the stele/apical region, so they are not specific. SmPINR's "apical initials region" was never shown to be a cell type.

## Trait tags

The rows use a new tag, `lycophyte`, on patterns that should not transfer to seed plants: WOX13a and BRN in the cap, VND2 in phloem, SGNb in the stele, and PINV in the outer layers. `lycophyte` is not yet in the skill vocabulary or in `IMPLIES` in `map_markers.py`. It must be added before the table is installed. Until then, these rows only apply when the target is given `--target-traits lycophyte`.

## Overlap with existing skill tables

There is no Selaginella table in `references/markers/`. The overlap is by homology only: SCR, SHR and CASP1 match the Endodermis/Stele rows in `arabidopsis_root.tsv` and `rice_root.tsv`; SmPLTe matches PLT1 (Stem_Cell_Niche); and the cyclins match rice Dividing_cells. SmWOX13a and SmBRN have no counterpart in the cap rows (Arabidopsis uses SMB for the lateral root cap).

## Could not verify

- Main text, STAR Methods and main-figure captions of Yang 2023: cell.com and sciencedirect returned a bot check or 403, which I did not bypass. Tissue calls not stated in the supplementary legends (SmCASP1, SmPINV, SmPLTe zone, the stele genes) come from the figure images only.
- The SmSCRb in situ pattern is taken from the Fig S2 legend; the image was not inspected.
- The platform identity (Resolve) and the hexagon size.
- The BioStudies S-BIAD1942 HCR images were not viewed.

## Update 2026-10-20: gap-fill reviews

One new review was added: `Liu2023/`. That review's own README and `markers_candidate.tsv` are left unchanged. `markers_draft.tsv` now has 27 rows: 19 existing rows (all kept, 11 annotated) and 8 new rows. The column set is unchanged. `ref_gene` is still the *S. moellendorffii* NCBI LOC ID, and `alt_id` is still the SMO ID, which is empty for the 8 new rows because they are not in the Yang panel. The *S. kraussiana* IDs (SK..G.....) are given in `basis`. `survey/characterization/characterized_markers.tsv` has no `selaginella_root:` rows.

### New dataset

| Dataset | Platform | Cells | Label access | Quality |
|---|---|---|---|---|
| Liu W et al. 2023 *Curr Biol* 33:4085 (10.1016/j.cub.2023.08.061, PMID 37716350) | *S. kraussiana* root-tip protoplast scRNA-seq, 10x 3' v3, plus colorimetric in situ for SkeuANTa/b, SkWOX13b, SkSHRa and SkSCRb | 3,969 cells, one pooled library, no replicates, 9 clusters | `cluster_only` (Table S2 DE plus cluster names; no barcode labels; raw reads at GSA CRA007853) | medium |

This is the only lycophyte root single-cell dataset found. It is a different species and lab from Yang 2023, so it counts as independent. Every Sk-to-LOC mapping is inferred by reciprocal blastp against UniProt taxid 88036 (`Liu2023/orthology/`), so `id_checked` is false. I raised confidence only where the reciprocal-best hit was unambiguous. Where blastp tied between two LOC loci (often the two haplotypes of the v1.0 assembly), I did not raise.

### Verdicts (Liu 2023 clusters)

| Cluster | Published label | Verdict | Use as |
|---|---|---|---|
| 0 (~51) | RAM initiation? | Reject | lignin/suberin profile; label rests on dot-plot genes not in Table S2 |
| 1 | Root cap stem cells + derivatives | Adopt | Root_Cap (cap stem cells merged with cap) |
| 2 | Root apical cell + proximal merophytes | Revise | proximal meristem zone, not Stem_Cell_Niche (hundreds of cells; LEA/HSP stress genes) |
| 3 | ? | Reject | low quality / transitional |
| 4 | ? (SkTRN1) | Reject | unresolved differentiating cells (epidermis, cortex or xylem) |
| 5 + 6 | Vasculature | Revise | Stele (merged); cluster 6 mixes in expanding cells |
| 7 | Endodermis (Ground tissues?) | Revise | Endodermis / inner ground tissue; also HD-ZIP III |
| 8 (~37, ~1%) | Dividing cells | Adopt | Dividing_cells (state) |

### Cross-species agreement and confidence raises

Four Liu in situ genes are reciprocal-best orthologs of Yang 2023 in situ/smFISH genes, and both species give the same tissue:

- **SmSCRa** `LOC9638011` / `LOC112344873` (Endodermis): medium to **high**. SkSCRb is in the endodermis by in situ and is the most specific cluster-7 gene.
- **SmPLTe** `LOC9639077` (Stem_Cell_Niche): medium to **high**, and evidence changed to `function`. SkeuANTa is in situ across the whole RAM and partly rescues Arabidopsis plt3 plt5 plt7. It still marks the meristem zone, not the initials alone.
- **SmSHRa** `LOC9657352` (Stele): low to **medium**. SkSHRa is in the vasculature by in situ.
- **SmWOX13a** `LOC9660776` (Root_Cap): already high. SkWOX13b in situ in the cap stem cells and cap, plus cluster-1 enrichment, adds support.

Supported but not raised:

- SmCYCB2;4: already high.
- SmBRN: Liu enrichment is only weakly specific, and its orthology is doubtful.
- SmSCRb (both loci): Liu has the dot plot only, not Table S2.
- SmCYCA1;1a: the blastp tie with SmCYCA1;1b `LOC9651297`.

There are now 4 high-confidence marker genes (5 rows) and 2 independent datasets, so the group stays **secondary** (primary needs 9 high-confidence markers with 2 datasets).

### Markers added (8 rows, all from Liu 2023)

- Stem_Cell_Niche: SkeuANTb `LOC9638168` (characterized_enriched, low; mapped via a 157-aa fragment).
- Stele: SkBAM1 `LOC9660218` and SkCLERK `LOC9663247` (characterized_enriched, low; scRNA only; CLERK blastp ties with LOC9658791).
- Endodermis: SkSGNa `LOC9653216` (low; conflict below) and `REVIEW:` HD-ZIP III `LOC9645025` (expression, low).
- Dividing_cells (state): CDKB1-like `LOC9661534` and NACK1/TES-like kinesin `LOC9661086` (function, medium; blastp ties with LOC9633858 / LOC9651829), and TPX2-like `LOC9644795` (characterized_enriched, low).

### Gaps closed / remaining

- **Partly closed:**
  - Stele now has a medium in situ marker (SmSHRa), backed by two species. It still has no `function` row.
  - The Stem_Cell_Niche zone now has a `function` marker (SmPLTe), but the zone is broader than the initials.
- **Remaining:**
  - Epidermis, Cortex, Pericycle and Procambium: never labeled in either study.
  - Xylem and Phloem: not resolved in the Liu stele clusters. Only the Yang smFISH rows exist, at medium and low.
  - Apical initials as distinct from the meristem zone.
  - Cap stem cells as distinct from the cap.

### Recommended label reference (revised)

Liu 2023 is the only true single-cell label set for a lycophyte root, but it is cluster-only with no barcode labels. Only clusters 1 (Root_Cap) and 8 (Dividing_cells) are adoptable, and 5+6 can be used as merged Stele. Use it as a cluster-level reference for those three groups. Yang 2023 is still the better marker source for xylem, phloem and outer tissues. Neither gives a label reference for epidermis, cortex or pericycle.

### Conflicts

- **SCR a/b names are swapped:** SkSCRb = SmSCRa (`LOC9638011`) and SkSCRa = SmSCRb (`LOC9652292`/`LOC9635947`). Compare by ID.
- **SGN:**
  - Liu's SkSGNa is called SGN1-like in the text, but its best hit in the paper's table is GSO1/SGN3.
  - Its blastp ties between `LOC9653216` and `LOC9652543`, which is Yang's SmSGNb, and SmSGNb is stele by smFISH.
  - I kept SmSGNb in Stele and added `LOC9653216` as Endodermis low. Do not use either alone.
- **HD-ZIP III in endodermis cluster 7:** HD-ZIP III is a stele/procambium gene in seed plants, so Liu cluster 7 may include inner stele cells. The row is marked `REVIEW:`.
- **SkBRN:** the paper's own table gives ANAC007/VND4 as best Arabidopsis hit. This adds to the existing doubt about SmBRN's orthology to BRN1/2.
- **Dividing cells are about 1% of Liu cells.** That is low for a root tip, and it fits the Yang finding that cell-cycle genes dominate the meristem regions.

### Could not verify (Liu 2023)

- GSA CRA007853: blocked by a JavaScript browser check, which I did not bypass.
- The xulinlab genome portal did not respond, so the Sk IDs could not be checked in an organism database.
- The in situ images were not rendered. Patterns come from the legends and text.
- Several dot-plot genes (SkeuANTb, SkSHRa, SkSCRa, SkSGNa, SkTRN1, SkACR4, SkRGI1) are absent from Table S2.
- Cluster sizes are inferred from the pct values.
