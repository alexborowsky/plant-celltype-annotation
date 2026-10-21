<!-- Collated from the survey review of cucumber_inflorescence (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# cucumber_inflorescence: collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill. New group. Input: the
review in `Dong2025/` (`README.md`, `evaluation.tsv`, `markers.tsv`,
`v3_to_v2_blast_markers.tsv`, Supp Tables in `supp/`). No rows in
`survey/characterization/characterized_markers.tsv` mention `cucumber_inflorescence:`,
so no independent characterized-marker support was available. The skill was not edited.

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 28 expected types/states for cucumber female floral buds (S1-S8) and the anthesis (0 DPA) ovary, built from anatomy; `function_markers` counts `function` rows in `markers_draft.tsv` only (Arabidopsis tables not counted) |
| `markers_draft.tsv` | 40 rows, skill schema + `alt_id` + `other_ids`. `ref_species=cucumber`, `tissue=flower`. `ref_gene` = Chinese Long v3 (`CsaV3_...`); `alt_id` = Chinese Long v2 (`Csa1G...`, BLASTn of v3 CDS against v2 CDS); `other_ids` = UniProt accessions (taxid 3659, found by v2 locus name `Csa_1G...`) |

## Datasets

| Dataset | Citation | Platform | Units | Label access | Quality |
|---|---|---|---|---|---|
| Dong2025 | Dong Z, Liu X, Guo X, et al. (2025) Developmental innovation of inferior ovaries and flower sex orchestrated by KNOX1 in cucurbits. *Nature Plants* 11:861-877. doi:10.1038/s41477-025-01950-w (PMID 40169874). CNGB STOmics STDS0000379 | Stereo-seq bin50 (~25 um, several cells per bin), 51 sections of cv. Gy14 female buds S1-S8 + 0 DPA ovary | 186,080 bins, 41 clusters (two 0 DPA sections give ~62k bins) | large_object (per-section h5ad, 4-107 MB each, ~1 GB; not downloaded; list in `Dong2025/ctsta_h5ad_filelist.tsv`) | medium |

Only cucumber was reviewed; the tomato TS69 part of the paper was not.

## Verdicts (Dong2025)

The labels are organ/tissue domains, not cell types, mixed with stage splits and
cell-cycle states. Full reasons are in `Dong2025/evaluation.tsv`.

| Verdict | Labels -> canonical name |
|---|---|
| Adopt | placenta -> Placenta; epidermis -> Epidermis; receptacles primordia + receptacles-early -> Receptacle; petal-2 -> Petal; sepal mesophyll c24 -> Sepal_Mesophyll; provascular -> Procambium; conjunctive tissue-early -> Conjunctive_Tissue; floral intercalary meristem c36 -> Floral_Intercalary_Meristem |
| Revise | FP -> Floral_Meristem (stage domain); receptacles-late, petal primordia, petal-3, conjunctive primordia/late, FIM-2/-3, sepal mesophyll c21 (merge into the adopted domain); ovule (ovary wall) (merged label); sieve element -> Phloem (4.2% of bins); protoxylem -> Xylem (strand domain); trichome-base, thickened epidermis, sepal epidermis -> Epidermis sub-domains; basal sepal abaxial/adaxial (position domains); 0 DPA mesocarp, epicarp -> Exocarp, endocarp + placenta (0 dpa) -> Endocarp (not separable), phloem (0 dpa) |
| Reject | G1/S (largest cluster, 6.1%; top genes CRC and p55), G2/M, G0/G1 (states as clusters); trichome (4.9%, two DE genes); stigma/transmitting tract (one uncharacterized gene); 5 unknown clusters (left unknown by the authors, which is good practice) |

## Markers (`markers_draft.tsv`)

40 rows: 15 `function`, 18 `characterized_enriched`, 7 `expression`; 3 `state` rows
(Dividing_cells). Confidence: 3 high (KNAT2-like1, AG1, PI), 17 medium, 20 low.

- All 37 review rows were carried, merged by gene ID (no duplicates).
- Added by this collation from Supp Table 3 (G2/M cluster): CYCB1;2-like
  (CsaV3_4G029350), CYCB1;4-like (CsaV3_6G038710) and CDC20 (CsaV3_3G032410) as
  `Dividing_cells` state rows. v2 IDs by BLASTn (100% identity), UniProt by v2 name.
- Regraded: WOX9 (Placenta) and PDF1 (Epidermis) lowered from medium to low, because
  they are supported only by bin50 spatial patterns, which are not cell-resolution
  in situ evidence (`literature_search.md`). All other grades follow the review.
- Corrected: the AG1/CAG1 basis cited "Kater et al. 2001 Plant Cell"; the CAG1 paper
  is Kater et al. 1998 Plant Cell 10:171, doi:10.1105/tpc.10.2.171 (Europe PMC
  PMID 9490741).
- Cell-type names: `Floral_primordium` -> `Floral_Meristem`, `Ovary_exocarp` ->
  `Exocarp`, `Ovary_inner_0dpa` -> `Endocarp`, `Stigma_transmitting_tract` ->
  `Transmitting_Tract`, to match existing tables. New names: `Receptacle`,
  `Floral_Intercalary_Meristem`, `Placenta`, `Conjunctive_Tissue`, `Petal`,
  `Sepal_Mesophyll`, `Abaxial_Lateral_Organ`, `Adaxial_Lateral_Organ`.
- **`requires=Cucurbitaceae`** on Receptacle, Floral_Intercalary_Meristem,
  Conjunctive_Tissue and 0 DPA ovary rows: these domains (receptacle-derived inferior
  ovary, carpel-fusion tissue) are cucurbit-specific, and CRC marks carpel/nectary
  in Arabidopsis, not receptacle. `Cucurbitaceae` is a new trait tag; add
  `Cucurbitaceae -> eudicot` to `IMPLIES` in `map_markers.py` before use.
- Every row is a bin50 domain marker. Use them as organ/domain markers in
  single-cell data; they do not resolve cell types inside a domain.

### Cross-study markers

None. This is the only cucumber floral single-cell or spatial dataset reviewed, and no
characterized-marker rows exist for the group, so no confidence was raised. Earlier
cucumber papers characterize some of these genes (CAG1, Kater 1998; CsHAN1, Ding et
al. 2015 J Exp Bot, doi:10.1093/jxb/erv409), but neither was checked for expression in
the same domain, so they are cited, not counted.

## Gaps

Closed (at least one in situ, mutant or function marker): Receptacle, Floral_Meristem,
Floral_Intercalary_Meristem, Carpel, Conjunctive_Tissue, Petal, Epidermis, Procambium,
Xylem, Phloem (domain), Dividing_cells (state). Partly closed (characterized_enriched
only): Sepal_Mesophyll (RCA in situ), Placenta, Abaxial/Adaxial_Lateral_Organ.

Remaining (no `function` marker): Stamen (arrested in female buds), Nectary, Ovule,
Stigma, Transmitting_Tract (expression-only, cluster rejected), Trichome, Guard,
Mesocarp, Exocarp, Endocarp (0 DPA, expression only), Phloem_Sieve_Element and
Phloem_Companion (not resolvable at bin50), S_Phase, sepal and petal epidermis. Male
flowers and the tomato part were not reviewed.

## Recommended label reference

Dong2025, adopted domains only, merged as above (stage splits collapsed into one
domain; cell-cycle clusters dropped). The per-bin labels are in the h5ad objects and
would need a per-sample composition check (Step 3b), because the two 0 DPA sections
supply a third of all bins.

## Conflicts

- ACS2: Supp Table 3 lists CsaV3_UNG054460, but the in situ primers also match
  CsaV3_1G040170; both map to v2 Csa1G580750 (UniProt A0A0A0M1V3). Kept UNG054460,
  with the paralog in `other_ids`.
- AG1: the v2 model Csa6G520410 is a merged gene (UniProt A0A0A0KID6 is annotated as a
  kinase), so AG1, STK-like and SHP-like have no clean `alt_id`.
- CRC is the top gene of both receptacles-early and the rejected G1/S cluster, which
  suggests G1/S is mostly receptacle/ovary bins grouped by state.
- The sieve element (4.2%), protoxylem (2.8%) and trichome (4.9%) fractions are too
  large for those cells at 25 um bins; relabeled as domains or rejected.

## Could not verify

- Main text and Methods (paywalled; not accessed). Cluster-calling methods and the FIM
  definition are known only from tables and Extended Data legends.
- Supp Fig images (PDF text only) and the h5ad objects (not downloaded).
- UniProt entries for STK-like, SHP-like and the thionin-like gene (no clean v2 name);
  CAG1 Q9SBK3 is matched by name only, not by sequence.
- IDs of HB40, SPT, KAN1-2, PP1 and CAB1, shown spatially but not named in Supp Table 3.
