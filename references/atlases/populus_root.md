<!-- Collated from the survey review of populus_root (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Populus root: cell-type marker resources (group review, 2026-10-20)

Collated from the two dataset reviews in `survey/merged_reviews.json`
(group `populus_root`); per-dataset details are in `Li2025/README.md` and
`Lv2024/README.md`. Files here:

- `expected_cell_types.tsv`: types expected from poplar root anatomy (primary
  root tip, lateral and adventitious root formation, secondary growth in older
  roots). `function_markers` counts `function` rows in the skill's root tables
  (`arabidopsis_root.tsv` + `rice_root.tsv`, eudicot trait filter); the
  `notes` column gives the rows this draft adds.
- `markers_draft.tsv`: 15 rows, skill schema plus `alt_id`. Field counts
  validated (13 per line).

## Datasets

| Dataset | Citation | Material / platform | Cells | Gene IDs | Label access | Quality |
|---|---|---|---|---|---|---|
| Li2025 | Li J, ... Zhang D. Plant Physiol 2025, kiaf432 (10.1093/plphys/kiaf432; PMC12526957). CNCB GSA CRA012587 (raw reads only) | *P. simonii* root tips (2 cm), with and without lateral roots; protoplast 10x 3' v2, Seurat SCT/CCA, 12 clusters | 19,875 (Tables S8/S12; text says 10,000). One library per condition, no replicates | *P. simonii* `Psi##G######` (genome version not stated; not in UniProt; no Potri map) | cluster only (rebuilt in `Li2025/cluster_to_celltype.tsv`) | low |
| Lv2024 | Lv K, ... Li B. Hortic Res 2024; 11: uhae237 (10.1093/hr/uhae237; PMC11540759). CNCB GSA CRA014595, CRA014319 | Base of in-vitro stem cuttings of 84K poplar (*P. alba* x *P. tremula* var. *glandulosa*) forming adventitious roots; BMKMANU S1000 spatial, 50 um bins | 6,505 + 10,210 bins (multi-cell) | 84K haplotype genome `PAxG..`; Potri IDs only for the 3 in situ genes (Table S5) | cluster/domain only, in text and figures | low |

Neither dataset is a root atlas of the quality of the Arabidopsis or rice
references. Lv2024 is not root tissue at all, apart from the AR primordia, and
its bins are tissue domains, not cells.

## Verdict matrix (published labels mapped to skill names)

| Cell type | Li2025 (scRNA, root tip) | Lv2024 (spatial, cutting base) |
|---|---|---|
| Columella | Revise (cl 7, 2.6%; specific DE, expression only) | - |
| Lateral_Root_Cap | Revise (cl 3, 6; cl 6 ubiquitous markers) | - |
| Quiescent_Center | absent | - |
| Meristem / Dividing_cells | Revise (cl 9, 1.9%; best supported, maybe a proliferation state) | Revise (S3 c2 "AR": translation genes, proliferative state) |
| Trichoblast | Reject (cl 11, 78 cells) | - |
| Atrichoblast / Epidermis | Revise (cl 0, 4; 32%, implausible; treat as epidermis) | Revise (S2 c1 outer ring, mixed bins) |
| Cortex | Revise (cl 2, 5) | Revise (S2 c2+c4, merge); Adopt at domain level (S3 c3) |
| Endodermis | Revise (cl 8, 10; cl 10 suberizing layer, cl 8 differs) | - |
| Stele / Xylem / Phloem / Pericycle | Reject (cl 1, no enriched markers) | Revise (S2 c0 xylem+pith; S2/S3 cambium+phloem merged) |
| Cambium | - | Revise (merged with phloem, but good WOX4/PXY pattern) |
| Pith | - | Adopt at domain level (S3 c5; stem tissue) |
| Periderm | - | Revise (S3 c0, unlikely in a 1-month in-vitro stem) |
| Adventitious_Root_Primordium | - | Adopt at domain level (S2 c5); S3 c2/c4 Revise |

No published label from either study is usable as per-cell ground truth.

## Cross-study markers

**None.** The two studies use different species and genome ID systems
(*P. simonii* Psi vs 84K PAxG), neither provides a Potri mapping for its
single-cell markers, and they share no validated gene. The only shared symbol
is WOX4, and it is not the same gene: PsiWOX4 = `Psi02G012270` (chr 2; Li2025
calls it atrichoblast) and the Lv2024 WOX4 = `PAxG14Gg0018000` (chr 14;
cambium domain). These are most likely the chr2/chr14 salicoid paralogs
(PttWOX4a/b; Kucukoglu et al. 2017), which I could not confirm without the
proteomes. No confidence was raised for cross-study agreement.

## Marker draft summary

| Cell type | Rows | Best row |
|---|---|---|
| Cambium | 1 | WOX4 `PAxG14Gg0018000`, `function` medium (Populus WOX4 RNAi cambium phenotype, Kucukoglu 2017 New Phytol 10.1111/nph.14631) |
| Meristem (kind=state) | 4 | `Psi03G016300` and PsiSKP2B `Psi05G016630` (in situ, low); SAC56/LOS1 (housekeeping, low) |
| Columella | 3 | `Psi04G004010` (expression, low) |
| Root_Cap | 1 | `Psi01G034580` (LRC + columella clusters) |
| Epidermis | 1 | `Psi14G013520` (in situ, low; published as atrichoblast) |
| Cortex | 1 | `Psi06G013570` (weak) |
| Endodermis | 3 | `Psi04G002720` (CCR-like), `Psi01G004800` (KCS-like), `Psi19G006550` (conflict, below) |
| Adventitious_Root_Primordium | 1 | WOX13a `PAxG05Ag0085100` (in situ, low) |

`ref_species` is `populus_simonii` (Li2025) or `populus_84K` (Lv2024). For a
*P. trichocarpa* (Potri) or 717 dataset these IDs do not match directly; they
need homology mapping, and no Psi or 84K proteome is wired into
`map_markers.py`. Only SAC56 and LOS1 carry a Potri `alt_id`.

Left out on purpose:
- PsiWOX4 `Psi02G012270` and PsiZHD9 `Psi04G011440`: Li2025 calls them
  atrichoblast genes from weak, uncontrolled in situs and weak UMAP signal;
  WOX4 is a cambium regulator, so the epidermal call conflicts with the biology.
- `Psi11G003270` (rejected trichoblast cluster; also a meristem marker in S13).
- `PAxG01Ag0017800` (stem-cutting outer layer "periderm"; not root).
- Figure-only Lv2024 genes with no ID (WOX5a, LBD16, WOX11/12a, PLT3,
  PXYa/b, WAT1a/b, STM, CCoAOMT1, C4H, PRX52, EOD1, MT2A).
- The Arabidopsis BLAST homologs in Li2025 Table S10 are documented in
  `basis`, not used as `alt_id` (not the same gene).

## Gaps

No Populus-validated marker for: Quiescent_Center, Stem_Cell_Niche,
Trichoblast, Atrichoblast (as distinct from epidermis), Exodermis,
Pericycle, Xylem, Phloem (companion cells, sieve elements), Procambium,
Periderm, Lateral_Root_Primordium. Cortex, Columella, Root_Cap and Endodermis
have only `expression`-tier rows. For all of these, use the Arabidopsis root
table via homology (`arabidopsis_root.tsv`: SCR, CASP1, SHR, WOX5, PLT1, SMB,
EXPA7, ...). A targeted literature search for Populus reporter lines
(PtoWOX5a, PtrLBD16, PtrSCR, Populus CASP or SUC2 orthologs) is the next step
if a Potri table is wanted; it was not done here.

## Recommended label reference

None for per-cell labels. Use **Li2025** as the cluster-level hypothesis for
a Populus root-tip dataset (it is the only Populus root scRNA atlas): its
cluster 9 (meristem/proliferative), cluster 7 (columella) and cluster 10
(suberizing endodermis or exodermis) markers are the most specific.
Reprocess from raw reads and annotate de novo with Arabidopsis homology
markers. Use Lv2024 only as qualitative spatial support for cambium (WOX4,
PXY) and adventitious-root-primordium genes in stem-cutting samples.

## Conflicts and corrections to the reviews

- **Psi19G006550 (endodermis, cluster 10):** its only Table S10 homolog,
  AT5G66230, is annotated as a dividing-cell/proximal-meristem/root-cap marker,
  not endodermis. Kept as `low` with the conflict in `basis`.
- **Psi01G034580:** the Li2025 review gave its homologs as AT1G53130/AT4G26880.
  In Table S10 the strongest hits are AT1G50720 (e=3e-40), AT5G55110 and
  AT4G26880 (STIG1-like, columella/LRC); AT1G53130 (GRI) is weak (e=6e-13).
  It is DE in both LRC cluster 3 and columella cluster 7, so it is filed as
  `Root_Cap`.
- **Psi09G013700:** strongest Table S10 hits are AT5G54370 and AT5G60530
  (e<1e-75); the review's AT3G19430 is a weak hit (e=9e-6).
- **Psi05G006900:** AT5G10130 is an Ole e 1-like protein listed as a columella
  marker in Li2025's database; the review's "DFC" name is not used.
- **Evidence regraded:** the review graded Psi04G002720 (CCR2-like)
  `characterized_enriched`; the Psi gene itself is uncharacterized and only
  scRNA-enriched, so it is `expression` here.
- **SAC56/LOS1:** in Lv2024 Table S3 they are DE in stage-2 *cluster 2*
  (pct 0.91 vs 0.54 and 0.93 vs 0.69), which the figure calls cortex, which
  fits the review's finding that the S3 stage-2 cluster numbers do not match
  Fig. 1D. They are near-ubiquitous translation genes (UniProt B9IIY9 uL4;
  B9HH10 EF-2, both confirmed via their Potri IDs), filed as `Meristem`
  kind=state, `low`.
- **WOX13a:** Lv2024 Table S5 gives it LOS1's Potri ID (Potri.007G065700),
  so its Potri ID is unknown (confirmed in the raw xlsx).
- **WOX4 (Lv2024):** confirmed in Table S3 (stage 2 cluster 3, log2FC 1.18,
  pct 0.26 vs 0.10, "WUSCHEL-related homeobox"). Raised to `function` medium
  from the Populus WOX4 RNAi phenotype (Kucukoglu et al. 2017); that is
  literature, not this paper, and which 84K/Potri WOX4 copy Kucukoglu's
  PttWOX4a/b correspond to was not mapped by ID.
- **Cell counts:** Li2025 text says 10,000 cells; Tables S8/S12 sum to 19,875.

## Not verified

- No Psi ID could be confirmed in a database: the *P. simonii* genome behind
  them is not stated and they are not in UniProt. All Psi IDs and statistics
  were confirmed only against the paper's own tables (S9, S10, S13) and the
  accession list in the text (PsiSKP2B, PsiWOX4, PsiZHD9).
- 84K PAxG IDs are not in UniProt; checked only against Tables S3/S5. Potri IDs
  for SAC56/LOS1 were checked in UniProt (taxonomy 3694).
- UniProt has no Potri locus for Populus WOX4/WOX5 entries (A0AAU0, Q2A0M2), so
  no Potri ID was added for WOX4.
- The WOX4 paralog assignment (chr2 vs chr14) is inferred from chromosome
  numbers, not from sequence.
- CNCB GSA pages (CRA012587, CRA014595, CRA014319) are behind a JavaScript
  bot check that I did not bypass. File lists and sizes are unknown.
  CRA026966/CRA026969 (Li2025 bulk/transgenic) are embargoed until 2027-06-19.
  The Lv2024 lab server was unreachable.
- Lv2024 Fig. S6 (WOX13a in situ) was not inspected in detail.

## Overlap with existing skill tables

There is no *Populus* table in
`~/.claude/skills/plant-celltype-annotation/references/markers/`, so no
rows overlap by ID. The closest relevant table is `arabidopsis_root.tsv`
(homology). Cell-type names follow the skill tables (Columella, Root_Cap,
Epidermis, Cortex, Endodermis). Three names are new: `Meristem` (kind=state;
not cell-cycle-validated, so not filed as `Dividing_cells`), `Cambium` and
`Adventitious_Root_Primordium`.
