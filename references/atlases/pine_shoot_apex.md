<!-- Collated from the survey review of pine_shoot_apex (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Pine shoot apex: collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill from the one review in this group (`Xue2025/`, whose own README holds the full desk review). Nothing here has been added to the skill.

Files:
- `expected_cell_types.tsv`: expected types for a *Pinus* vegetative shoot apex (SAM, needle primordia, young stem with resin ducts), built from conifer anatomy first and then matched to the Xue 2025 clusters. `function_markers` counts only pine-native `function` rows in `markers_draft.tsv`. Arabidopsis homology candidates are named in `notes` but not counted: homology from Arabidopsis to a gymnosperm is distant, and some angiosperm markers (SUC2, SEOR1, CLV3/WUS-type) are not expected to transfer.
- `markers_draft.tsv`: 11 rows in the skill schema plus `alt_id` and `other_ids`. `ref_gene` = *P. tabuliformis* genome v1.0 IDs (`Pt<chr>G<nnnnn>`; X = chr10, J = chr11, Q = chr12, 0 = unplaced contigs; Niu et al. 2022 Cell). `alt_id` is empty because there is no second gene-ID system for these loci: UniProt has none of them, and the de novo transcriptome was not mapped to them. `other_ids` = the locus coordinates in the v1.0 GFF3 (figshare 10.6084/m9.figshare.16847146). `tissue` = `shoot_apex`.
- Trait tags: rows use `requires=gymnosperm` (resin duct rows use `requires=conifer`). Neither tag is in the skill vocabulary yet. To use the table, `conifer → gymnosperm` must be added to `IMPLIES` in `map_markers.py`, and `--target-traits gymnosperm conifer` must be passed. Because the IDs are pine v1.0, these rows are for same-species use (`--no-blast`) or for other *Pinus* species by homology.
- No rows in `survey/characterization/characterized_markers.tsv` mention `pine_shoot_apex:`, so there is no independent support from characterization studies.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Xue2025 | Xue HC, Xu ZG, Liu YJ, ... Mao YF, Wang JW (2025) A unified cell atlas of vascular plants reveals cell-type foundational genes and accelerates gene discovery. Cell 188(22):6370-6390.e29. doi:10.1016/j.cell.2025.07.036 (Europe PMC; PMID 40829588). BioProject PRJNA1188718 | Protoplast scRNA-seq: 10x (pt-1, 5,247 cells) + BD Rhapsody (pt-2, 9,122 cells), DNBSEQ-T7 | 14,369 (per-cluster counts only in figures) | cluster_only (DE table + label summary in Table S1; no per-cell labels or processed object) | medium |

This is the only annotated pine (or gymnosperm) single-cell atlas found. The full text and figures are paywalled.

## Verdict matrix (one dataset, 12 clusters)

| Canonical type | Xue 2025 label (verdict) | Pine markers |
|---|---|---|
| Epidermis | EC Epidermal Cell (Pavement Cell) (Adopt) | none (no pine RISH probe) |
| Mesophyll (+Cortex) | MC Mesophyll/Cortex (Revise: merged layer) | PtJG24650 (low); Pt2G27100, Pt0G10370 (expression, not specific) |
| Phloem_Companion (Strasburger-like) | VC Phloem Cell Type I (Revise: CC-like by cross-species mapping only) | Pt3G16430, Pt5G23680, Pt9G23400 (medium) |
| Sieve_Element | VC Phloem Sieve Cell / Sieve Element (Revise) | Pt1G05200 (expression, low; conflict) |
| Xylem (tracheids) | VC Xylem Tracheid / Tracheary Element (Adopt) | Pt5G55730 (medium) |
| Xylem_Parenchyma | VC Xylem Cell Type I (Pan-Vascular Parenchyma) (Revise: rename) | Pt0G26330 (medium) |
| Procambium? | VC Vascular Cell Type I (Revise: undefined; Pan maps it to sieve elements) | none |
| S_Phase | PC S Phase (Revise: keep as state) | none curated |
| G2_M | PC G2/M Phase (Revise: keep as state) | none curated |
| Resin_Duct_Epithelium | Resin Duct Secretory Cell (Adopt) | PtCYP720B1 Pt6G36960, PtTPS_mo20 PtXG48400 (function, high) |
| - | Unknown (Reject) | - |
| - | Unknown II (vascular-associated) (Reject; re-examine) | - |

No cluster was forced into a type: the authors left two Unknown, and named the proliferation clusters as states. No SAM/meristem, guard-cell, hypodermis, endodermis, transfusion-tissue or pith cluster was resolved.

## Markers

- `function`, high (2): Pt6G36960 PtCYP720B1 (a diterpene resin-acid oxidase, by GFF3 name; the CYP720B1 enzyme is characterized in loblolly pine by Ro & Bohlmann 2006 Phytochemistry, 10.1016/j.phytochem.2006.01.011, but orthology of this locus was not checked) and PtXG48400 PtTPS_mo20 (a monoterpene synthase, by GFF3 name). Both are RISH probes for the resin duct and cluster-specific (pct 0.67 vs 0.06 and 0.44 vs 0.02). I re-checked the DE values against sheet 14.
- `characterized_enriched`, medium (5): three phloem RISH genes in the CC-like cluster (Pt3G16430, Pt5G23680, Pt9G23400); Pt5G55730 (tracheary element); Pt0G26330 (xylem parenchyma, pct 0.59 vs 0.01). None has an annotated function, so "characterized" here means in situ-validated, not functionally known.
- `characterized_enriched`, low (1): PtJG24650 (mesophyll/cortex).
- `expression`, low (3): Pt2G27100 and Pt0G10370 (mesophyll; weak or higher in epidermis), and Pt1G05200 (sieve element; see Conflicts).
- Cross-study raises: none. There is only one dataset, and no characterization-study rows match.
- Name changes from the review's `markers.tsv`: `Companion_Cell_like` became `Phloem_Companion` and `Xylem_TE` became `Xylem`, to match the existing skill tables. The original labels are kept in square brackets in `basis`. The coordinates moved from `alt_id` to `other_ids`.

## Gaps

Closed (partly) by Xue 2025:
- Resin duct epithelium (secretory cells): filled, with function-grade markers.
- Companion-cell-like (Strasburger) cells: partly filled. There are three in situ phloem genes, but CC identity is inferred from SAMap/SATURN mapping.
- Xylem tracheary element and xylem parenchyma: one in situ gene each.
- Phloem cluster genes: present (see above).

Remaining:
- No pine `function` marker for any type except the resin duct. Every vascular marker is an unannotated gene.
- SAM central and peripheral zones, needle primordia, guard cells, hypodermis, endodermis, transfusion tissue, pith and cortex (separate from mesophyll): no cluster and no marker.
- Epidermis: adopted cluster, but no pine gene. Use HD-ZIP IV (ATML1/PDF2/HDG2) homologs and check them in the data.
- Sieve element: only the conflicted Pt1G05200.
- Proliferation states: no pine IDs curated. Use Arabidopsis histone, PCNA and CYCB homologs.
- "VC Vascular Cell Type I" and "Unknown II": identity unresolved (possibly procambium/cambium).

## Recommended label reference

Xue 2025 is the only option. Use it as a marker source and as a guide to which clusters to expect, not as a label source: there are no per-cell labels, and re-deriving them needs the raw reads (SRR31541693, 10x, 40.4 GB; SRR31827612/3, BD, about 94 GB each) to be reprocessed in a compute job. Its most reliable anchors are Resin_Duct_Epithelium, Xylem, Xylem_Parenchyma and the CC-like phloem cluster.

## Conflicts

- Pt1G05200: Table S1 sheet 1 labels its RISH probe "Resin Duct Secretory Cell", but in sheet 14 it is DE only in VC Phloem Sieve Element (log2FC 6.3, pct 0.39 vs 0.022) and VC Phloem Cell Type I (weak). It is not DE in the Resin Duct cluster. It is kept as Sieve_Element, `expression`, low, until Fig. 1 can be seen.
- Pt0G10370: labeled a middle-layer (mesophyll/cortex) probe, but it is DE more strongly in epidermis (0.19 vs 0.07) than in MC (0.13 vs 0.07).
- VC Vascular Cell Type I: the Pan label (Pan-Phloem Sieve Element) conflicts with its name and with the separate SE cluster.

## Could not verify

- The in situ images, per-cluster cell counts and dot plots: the full text and figures are paywalled (cell.com and sciencedirect return 403; there is no OA copy).
- The Arabidopsis homologs of the unannotated pine genes: PLAZA Gymno is behind a Cloudflare challenge, which I did not try to get past.
- Whether Pt6G36960 is the ortholog of the characterized *P. taeda* CYP720B1, and which product PtTPS_mo20 makes.
- The full v1.0 GFF3 (155 MB, above the download limit). Only targeted range reads were done.
