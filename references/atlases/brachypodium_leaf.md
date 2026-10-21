<!-- Collated from the survey review of brachypodium_leaf (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Brachypodium leaf single-cell datasets: group collation

Date: 2026-10-20. Paper-only review (Steps 1-3a); no in-data check yet.
Input: one dataset review (Berg et al. 2026), in `Berg2026/` (its own README, supplements, GitHub files and `id_check.tsv`; left unchanged).

Files in this folder:

- `expected_cell_types.tsv`: written from the anatomy of a C3 pooid grass leaf base plus the vegetative shoot apex (the sampled material), not from the published labels. `function_markers` counts the `function` rows in `markers_draft.tsv` (all rows apply to Brachypodium, which is `grass,C3`).
- `markers_draft.tsv`: 36 rows (36 genes), skill schema plus `alt_id`. **`ref_gene` = Bd21-3 v1.2 (`BdiBd21-3.`, the IDs in the GEO features.tsv); `alt_id` = Bd21 v3 (`Bradi`).** For data aligned to the Bd21 v3 reference, run `map_markers.py --id-column alt_id`. `tissue` is `leaf`, or `shoot_apex` for the 4 SAM/primordium rows.

## Datasets

| Dataset | Material | Platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Berg et al. 2026 *Plant Cell* koag172, 10.1093/plcell/koag172 (PMC13291820; GEO GSE307277, bulk GSE306756) | Bd21-3 WT + *sid/bdmute-1*; basal 3-5 mm of the growing leaf (7 libraries) + vegetative SAM with primordia (2 libraries); 3 sites/years | protoplast scRNA, 10x 3' v3.1, Cell Ranger 7.0.1 (introns), SoupX, DoubletFinder, STACAS integration guided by the authors' own labels | 69,687 (epidermis 15,034; stomatal 8,406) | Bd21-3 v1.2 + Bradi v3 (Table S3) | cluster only (RenameIdents in GitHub R script); per-cell table only for 4,581 stomatal cells (MINI-EX input); GEO RAW 910 MB, not downloaded | medium: strong for epidermis (13 genes by HCR RNA-FISH, 4 by reporters, sid genetic control); coarse merged ground/vascular/SAM labels |

Only one single-cell dataset exists for this group. The cross-study evidence comes from earlier Brachypodium reporter and mutant papers (Raissig 2016/2017, McKown 2023, Zhang 2022, Spiegelhalder 2024, Nunes 2023), not from a second atlas.

## Verdicts by expected cell type

A = Adopt, R = Revise, X = Reject, - = not annotated. From the Berg 2026 review.

| Expected type | Berg 2026 label (% of subset) | Verdict |
|---|---|---|
| Mesophyll | Mesophyll (44.7% of atlas; includes dividing ground tissue 9/14) | R |
| Bundle_Sheath, Mestome_Sheath | - (inside Mesophyll/Vasculature; script privately labels cluster 10 "bundle sheath") | - |
| Epidermis | Epidermis (21.6%) | A |
| Epidermis (protoderm state) | Stage 0-2 (29.8% of epidermis; 11.9% of stomatal) | R (state) |
| Pavement | Inter-specialized cells (13.9% of epidermis) | R (young, heterogeneous) |
| Stomatal_lineage | Stomatal lineage (12.2% of epidermis); Early GMCs (4.8%); Dividing GMCs (7.1%) | A |
| Stomatal_lineage (SMC) | SMCs (10.5% of stomatal) | X (tracks batch and the SMC-less *sid* genotype) |
| Guard | Early GCs (7.1%), Late GCs (7.7%) | A |
| Subsidiary | SCs (10.4%) | A |
| Trichome (prickle hair) | Hair cell lineage (17.6% of epidermis) | A |
| Silica | Silica cell lineage (21.2% of epidermis) | R (too large; only cluster 9 SLP-enriched) |
| Cork, Bulliform, Sclerenchyma | - | - |
| Xylem, Phloem, Procambium | Vasculature (9.5%); SAM/Vasculature (4.5%) | R (merged) |
| Sieve_Element, Phloem_Companion, Phloem_Parenchyma | - (not split) | - |
| Shoot_Meristem, Leaf_Primordium | SAM/Primordium (8.5%) | R (homolog markers, barley spatial support; batch = tissue) |
| Ligule | - | - |
| Dividing_cells | kept inside tissue labels (G2/M scored) | A as a state |
| Unassigned | Unclear (~11% of atlas; ~5% of epidermis) | X (correctly left unassigned) |

## Cross-study markers (same gene ID, independent studies)

| Cell type | Gene (Bd21-3 / Bradi) | Studies | Confidence |
|---|---|---|---|
| Stomatal_lineage | BdMUTE BdiBd21-3.1G0240400 / Bradi1g18400 | Raissig 2017 *Science* and Spiegelhalder 2024 *Development* (YFP reporters, *sid* mutant); Berg 2026 (RNA-FISH, Dividing GMC cluster) | high (raised from medium) |
| Guard | BdFAMA BdiBd21-3.2G0300000 / Bradi2g22810 | McKown 2023 *Plant Cell* (YFP-BdFAMA reporter, mutant); Berg 2026 (transcriptional reporter, GC clusters) | high (raised from medium) |
| Trichome | BdPOX/BdPRX76 BdiBd21-3.2G0467800 / Bradi2g37000 | Nunes 2023 *Curr Biol* (transcriptional and translational reporters only in prickle hairs, mutant); Berg 2026 (Fig 2f, cluster 27 lfc 7.6, pct 0.47 vs 0.005) | high (already high) |

That is 3 cross-study genes. All of these studies come from the Raissig lab or its collaborators, but each is a separate experiment with its own reporters, so I counted them as independent. BdPAN1 (Zhang 2022 *eLife* reporter) was not counted: Berg 2026 enriches it only weakly (pct 0.11), and only in the rejected SMC cluster.

## Gaps (expected types with no `function` marker)

- **Mesophyll, Bundle_Sheath, Mestome_Sheath:** the main gap. Berg 2026 did not split the ground tissue, and its only mesophyll marker (STOMAGEN-1) is weak and broad. Step 4 search targets. For C3 BS, look for Bd or wheat/barley reporter work.
- **Pavement, Cork, Bulliform, Sclerenchyma:** no validated marker. Bulliform and mature pavement cells are lost to protoplast size limits.
- **Silica:** only SLP1-like3 (RNA-FISH, but it moves to hair cells at stage 6). Use with BdPOX/SLP1-like5 absent.
- **Xylem, Sieve_Element, Phloem_Companion:** only homolog-named, unvalidated genes (TED4-like, XCP1-like). SE vs CC was not split. No Bd SUT1 row.
- **Leaf_Primordium, Ground_Meristem, Ligule, S_Phase:** no Bd marker. CRC and FCP1 rest on barley spatial data.
- **Thin:** Guard, Subsidiary, Phloem, Phloem_Parenchyma, Procambium, Shoot_Meristem and Dividing_cells have one `function` row each. The PP, Procambium and SAM rows are `low`.

## Recommended label reference

Use Berg 2026 only for the epidermis. Its GMC, GC, SC and hair-cell labels and the in situ-validated markers are well supported, and the *sid/bdmute-1* libraries are a built-in negative control for subsidiary cells. Treat its tissue-level labels (Mesophyll, Vasculature, SAM/Vasculature, SAM/Primordium) and the Silica, Inter-specialized and Stage 0-2 labels as hypotheses to split in Part B. Do not use its SMC label. Per-cell labels are not public, so it serves as a marker source and cluster-level hypothesis, not as a per-cell benchmark. The exception is the 4,581-cell stomatal subset table on GitHub, which could benchmark GMC/GC/SC calls if the barcodes match.

## Conflicts and corrections

- **Correction to the review: Table S5 is not a list of 1,812 genes.** It is the full DESeq2 table (12,878 genes, protoplasted vs intact), of which 1,812 have log2FC > 3 (induced) and 809 < -3. Three marker rows are strongly protoplasting-affected: **BdSWEET13 (9.2), BdHDG2-like (9.1) and BdPME53-like (6.9)**. This is noted in their `basis`. The HDG2-like and PME53-like rows still hold because they rest on reporter and RNA-FISH evidence; SWEET13 stays `low`.
- **BdPAN1 grading (review said `function`, kept, but `low`).** Zhang 2022 shows that the BdPAN1-YFP reporter is in *all* young protodermal cells, and only the protein polarizes in SMCs. It is not a transcript marker for SMCs.
- **BdSLP1-like3: silica or hair.** RNA-FISH marks silica precursors at stage 5 and hair cells at stage 6, and it is enriched in HC clusters 14/23. Kept as Silica (`medium`); the conflict is in `basis`.
- **Cluster 19: xylem or procambium.** TED4-like (xylem-like) is its top gene, but the authors' script labels it Procambium. TED4-like is kept as Xylem (`low`).
- **Grading changes from the review:** BdWOX3B and BdAPL were raised from `characterized_enriched` to `function` (`medium`), because their orthologs have defining functions (OsWOX3B for trichomes, AtAPL for phloem). BdKN1, BdWOX4 and BdSWEET13 were set to `function` but `low`, because none is enriched in Berg Table S4.
- **Added at collation:** BdPOX/BdPRX76 (BdiBd21-3.2G0467800). Berg 2026 uses it as a hair-cell marker (Fig 2f) but leaves it out of Table S3. Its ID comes from the Nunes 2022 bioRxiv full text (figure legend and results), and I confirmed it in the Phytozome synonym file (Bradi2g37000) and UniProt (I1HM77, peroxidase).
- **Not carried:** expression-only genes (BdLHCA6, BdTMO6-like, BdSLAH2, BdSLP1-like9) and broad receptor genes (ERECTA, SERKs), following the skill rule against data-picked rows. BdERL1 is kept as `low` support only.
- **Figure percentages:** Fig 3a and Fig 5n disagree for the same stomatal UMAP (e.g., Stage 0-2 51.4% vs 11.9%). The script and Table S4 also label clusters 4 and 17 differently.

## ID checks

All 36 `ref_gene`/`alt_id` pairs match both Berg Table S3 (35 genes; BdPOX is not in it) and the Phytozome Bd21-3 v1.1 → Bradi synonym file (`Berg2026/github/`). The review also checked the 35 Table S3 genes against UniProt through the `BRADI_*v3` cross-reference (`Berg2026/id_check.tsv`). I re-queried UniProt for BdMUTE (I1GRC8) and BdPOX (I1HM77). The prior-study IDs agree: Spiegelhalder 2024 gives BdMUTE as BdiBd21-3.1G0240400, McKown 2023 gives BdFAMA as Bradi2g22810, and Zhang 2022 gives BdPAN1 as BdiBd21-3.3G0526300 / Bradi3g39910.

## Overlap with existing skill tables

There is no Brachypodium table in `references/markers/`, and none of the skill tables contains a `BdiBd21-3` or `Bradi` ID. Related rows exist by name and function only (not checked by BLAST):

- `sorghum_leaf.tsv`: CST1 (Subsidiary), SLP1 (Silica), SWEET13 (Phloem_Parenchyma) and XCP1 (Xylem) have homologous rows here. SbSLP1 has nine Bd SLP1-like paralogs, and only SLP1-like3 (silica) and SLP1-like5 (hair) are validated, so a homology transfer of SbSLP1 may land on the wrong paralog.
- `arabidopsis_leaf.tsv`: MUTE and SPCH (Stomatal_lineage), FAMA (Guard), PDF1 (Epidermis), APL (Phloem) and XCP1 (Xylem) have homologs here.

The Bd table adds what neither has: validated GMC stage markers (TMM, SDD1, LRR kinase), a second SC marker (DUF567), and prickle-hair markers (BdPOX, 2cRR, SLP1-like5, WOX3B). These are the first grass hair-cell markers with in situ support in the collection.

## Could not verify

- **Raissig et al. 2016 *PNAS*:** the full text is not available through Europe PMC or NCBI (abstract only). The reporter details for BdSPCH1/2 and BdSCRM2 were not checked, so those rows stay `medium`, with no cross-study raise.
- **Raissig et al. 2017 *Science*:** no open full text. The BdMUTE reporter claim rests on the abstract plus Spiegelhalder 2024 (open, checked).
- **Nunes et al. 2023 *Curr Biol*:** the journal version was not read. I used the bioRxiv preprint (10.1101/2022.07.03.498611), which is publicly readable.
- **No in-data check:** the GEO matrices (910 MB) were not downloaded, and the per-cluster cell counts are not published. Percentages are from the figures.
- **Sign convention of Table S5:** Fig S4c defines up/downregulation at |log2FC| > 3, and the sheet name is "wholevsproto". I read positive values as induced by protoplasting, consistent with the review's 1,812-gene count, but the column header does not state the direction.
