<!-- Collated from the survey review of pepper_fruit (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# pepper_fruit: collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill (new group). The input is the
review in `Han2026/` (`README.md`, `markers_Han2026.tsv`, `fruit_celltype_counts_ExtDataFig1c.tsv`).
The skill was not edited.

Outputs in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 21 expected types/states for *Capsicum annuum* fruit, 0-45 DPA, built from anatomy first. `function_markers` counts the `function` rows in `markers_draft.tsv`; counts in the skill's Arabidopsis/tomato tables are in `notes` |
| `markers_draft.tsv` | 39 rows (38 genes), skill schema + `alt_id` + `other_ids`. `ref_species=pepper`, `tissue=fruit`. `ref_gene` = NCBI RefSeq LOC IDs on UCD10X v1.1 (`LOC1078xxxxx` / `LOC1248xxxxx`); `alt_id` = CM334/Zunla `T459_` locus tag where known; `other_ids` = UniProt |

## Datasets

| Dataset | Citation | Platform | Cells (fruit) | Label access | Quality |
|---|---|---|---|---|---|
| Han2026 | Han J, Tang Y, Yue Z, Ji W, ... Yang S, Li B. Laminar patterning transcription factors orchestrate spatial metabolite partitioning in *Capsicum* fruit. *Nat Plants* (online 2026-05-05). doi:10.1038/s41477-026-02293-w, PMID 42086737 (DOI confirmed in Europe PMC). BioProject PRJNA1259216 | snRNA-seq (BMKMANU DG1000, BGI DNBelab C4); sequencing-based spatial (BMKMANU S1000/S3000, cell-bins <1000 um2); smFISH (ISSeq); RNA ISH. Line CA59, genome UCD10X v1.1 | 36,261 nuclei (0, 7, 16, 25, 35, 45 DPA); 29,828 ST cell-bins (10, 16, 25, 35, 45 DPA). Whole atlas 332,468 cells / 57 samples, Harmony 37 clusters / 17 types | cluster_only (no per-cell labels, no processed object; portal is a viewer) | medium |

This is the only pepper fruit single-cell/spatial dataset reviewed. No `pepper_fruit:` rows exist in
`survey/characterization/characterized_markers.tsv`, so there is no independent characterized-marker support.
Two characterization papers were cited in `basis` for the gland function rows (DOIs confirmed in Europe PMC):
Stewart et al. 2005 *Plant J* (Pun1, doi:10.1111/j.1365-313x.2005.02410.x) and Zhu et al. 2019 *New Phytol*
(MYB31, doi:10.1111/nph.15853). They support the `function` grade but did not raise confidence (both rows are already `high`,
and their gene-ID mapping to UCD10X LOC IDs rests on NCBI aliases, not on a table in those papers).

## Verdicts (Han2026)

A = Adopt, R = Revise, X = Reject. Counts: SN nuclei / ST cell-bins (ED Fig 1c).

| Published label | n | Verdict | Mapped to |
|---|---|---|---|
| Gland | SN 1254 (16 DPA only); ST 366 (25 DPA) | A | Capsaicinoid_Gland |
| Metabolically active gland | small subcluster | A (as a state) | Capsaicinoid_Gland, 25 DPA maturation state |
| Pre-metabolic gland | small | R | Capsaicinoid_Gland, early state (defined by absence of expression) |
| Subglandular parenchyma | small | R | Placenta (placental parenchyma) |
| Placenta (+ PlacentaParenchyma, PlacentaPlacenta) | SN 13185; ST 8287 | R | Placenta / Ovule / Vascular / Capsaicinoid_Gland (catch-all, 0-67% of nuclei by stage) |
| Exocarp | SN 10563; ST 916 | R | Exocarp (35 DPA cluster contains seed oleosins: bin contamination) |
| Epidermis (fruit) | SN 648; ST 1684 | R | Exocarp |
| Chlorenchyma / storage parenchyma (35 DPA) | - | R | Exocarp / Mesocarp layers |
| Collenchyma / Parenchyma / Outer, Inner epidermal cells (25 DPA ST) | - | R | Hypodermal_Collenchyma / Mesocarp / Exocarp / Endocarp |
| Mesocarp (Mesocarp1/2) | SN 5817; ST 11507 | R | Mesocarp (tissue label only, no marker) |
| Endocarp | ST 2165; SN 0 | R | Endocarp |
| Vascular tissue | SN 935; ST 1396 | R | Vascular (xylem and phloem merged) |
| Seed / Seed coat | ST 3264 | R | Seed_Coat / Endosperm / Embryo (merged) |
| Embryo | ST 70 (35 DPA) | A | Embryo |
| Septum | ST 293 | R | Septum (gland epidermis mixed in) |
| Meristem (fruit SN) | SN 3686 (2928 at 35 DPA) | X | forced cross-organ label (possibly Dividing_cells in part) |
| Mesophyll (7 DPA fruit SN) | SN 173 | X | forced leaf label (probably photosynthetic exocarp) |

## Markers (`markers_draft.tsv`)

39 rows on 38 genes: 2 `function`, 22 `characterized_enriched`, 15 `expression`; 3 `state` rows.
Confidence: 2 high, 11 medium, 26 low.

- Taken from the review's 38 JSON markers, merged by LOC ID. LOC107876119 (PCR8-like, the paper's "PDF1" ISH) has two rows,
  Exocarp and Endocarp, because the ISH shows both layers.
- Left out: BTF3 (LOC107877801; weakly specific, housekeeping-like; it is in `markers_Han2026.tsv` but not in the review JSON),
  and every paper ID whose NCBI description contradicts its name (LOC107866983 "CCS", LOC107843685 "PP2-B10",
  LOC107874941 "SWEET10", LOC107869855 "RAB28", LOC107859921 "SHN1", LOC107860847 "SPT"). For CCS, PP2-B10 and SWEET10 the correct-looking
  locus from the DE tables was used instead (LOC107875664, LOC107871262, LOC107856014).
- Symbols follow the NCBI description of the ID, not the paper's symbol; the paper's symbol is noted in `basis` when it differs.
- Grading follows `literature_search.md`. ST cell-bins are near-cellular but show neighbour contamination, so ST-only enrichment
  of a characterized gene is `characterized_enriched` low-medium, as graded in the review. Only Pun1/AT3 and MYB31 (capsaicinoid
  function plus smFISH) are `function` high.
- Cell-type names: `Capsaicinoid_Gland` (review: Gland_capsaicinoid), `Carotenoid_Ripening` (state; review: Exocarp_ripening and
  Pericarp_ripening), `Hypodermal_Collenchyma` (review: Collenchyma_hypodermis), `Phloem_Parenchyma` (review: Vascular_phloem_parenchyma),
  `Sieve_Element` (SEOR; review: Vascular_phloem), `Phloem` (SWEET10), `Ovule` (STK; review: Placenta_ovule). Reused names:
  `Exocarp`, `Endocarp`, `Septum`, `Embryo`, `Vascular`, `Phloem`, `Ovule`. New names not yet in skill tables:
  `Capsaicinoid_Gland`, `Carotenoid_Ripening`, `Hypodermal_Collenchyma`, `Placenta`.
- Trait tags: `requires=Capsicum` on the gland rows and on Ccs (capsanthin is Capsicum-specific). **`Capsicum` is a new trait tag:**
  add `Capsicum -> Solanaceae` to `IMPLIES` in `map_markers.py` before using these rows. `requires=Solanaceae` on expression-only
  fleshy-fruit layer rows, PSY1/BCH1 and prosystemin (a Solanaceae-specific gene). Conserved genes (SEOR, SWEET10, UMAMIT14, STK, oleosins,
  peamaclein) have no tag.

## Gaps

- **Closed:** Capsaicinoid_Gland (2 function + 11 supporting rows, smFISH), Embryo (expression/characterized_enriched, small cluster).
- **Partial:** Exocarp (WRKY6 smFISH; ISH 'PDF1' probe unconfirmed), Endocarp (candidates only, ID-corrected PP2-B10),
  Hypodermal_Collenchyma, Phloem / Phloem_Parenchyma / Sieve_Element / Vascular (ST only, merged in the paper),
  Placenta and Ovule (catch-all label), Septum (weak), Carotenoid_Ripening state (broadly expressed genes).
- **Remaining (no pepper marker):** Mesocarp, Guard, Xylem, Phloem_Companion, Procambium, Seed_Coat, Endosperm, Dividing_cells.
  Of these, Guard, Xylem, Phloem_Companion, Procambium, Endosperm and Dividing_cells have function rows in the Arabidopsis/tomato
  tables to map by homology. No cell type except Capsaicinoid_Gland has a pepper `function` marker.

## Recommended label reference

Han2026 is the only option. Use its Gland call (and the 25 DPA ST gland subclusters) as a reference. Treat its pericarp
layer, placenta, septum, vascular and seed labels as tissue-level hints, re-derived from markers; never transfer Meristem or
Mesophyll. Per-cell labels are not public, so label transfer is not possible; use the markers and the cluster counts.

## Conflicts

- **Gene-ID/name mismatches in the paper** (checked against NCBI Gene in the review): CCS -> LOC107866983 is a copper chaperone
  (real Ccs LOC107875664); PP2-B10 -> LOC107843685 is 40S ribosomal S14-2 (real PP2-B10 LOC107871262, endocarp-specific);
  PDF1 -> LOC107876119 is PCR8; SWEET10 (ED1j) -> LOC107874941 is a glutaredoxin; ABI3 -> LOC107862571 is oleosin H2;
  RAB28 -> sugar carrier C; SHN1 -> ALDH3F1; SPT -> probable TF At4g00390; WRKY6 -> NCBI WRKY31-like; AGL6 -> MADS3 (AG clade);
  ZAT10 is listed under two IDs. The ISH/smFISH validations of CCS, PDF1 and PP2-B10 therefore cannot be attributed to a locus.
- The 35 DPA "Exocarp" ST cluster contains seed oleosins (oleosin L pct .82), so its DE genes include contamination; the oleosin rows
  are assigned to Embryo only.
- Pun1 is DE in the Septum cluster, and Placenta includes ovule (STK), vascular and gland cells: these clusters are mixtures.
- The paper's text conflicts on which 35 DPA exocarp subcluster is the epidermis.

## Could not verify

- Supplementary Table 1 (MOESM3, 92.5 MB .xlsb, over the download limit;
  https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41477-026-02293-w/MediaObjects/41477_2026_2293_MOESM3_ESM.xlsb):
  curated marker table, QC and ISH/smFISH primers. Needed to resolve which loci the ISH probes targeted.
- Per-cell labels and processed objects: not deposited (raw reads only in PRJNA1259216; code at github.com/SuLea-IT/Pepper has no labels).
- Peer review file: downloaded in `Han2026/`, not text-searched.
- The stage assignment of SuppTable2 sheets 1-c (35 DPA ST) and 4-c (25 DPA ST) is inferred by the review.
- LOC-ID mapping of the Pun1 and MYB31 loci in Stewart 2005 / Zhu 2019 to UCD10X v1.1 was not checked beyond NCBI aliases.
