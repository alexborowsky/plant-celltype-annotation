<!-- Collated from the survey review of strawberry_fruit (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# strawberry_fruit: collated cell-type marker resources

Collated 2026-10-20 for the plant-celltype-annotation skill. Inputs: the review in
`Ma2026/` (merged_reviews.json entry, `Ma2026/README.md`, `markers.tsv`, `evaluation.tsv`)
plus two characterized-gene papers fetched for gap filling (`literature/`). The skill was not edited.

Outputs in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | 27 expected types/states for whole *F. vesca* fruit, stages 2-5, built from anatomy; `function_markers` counts the `function` rows in `markers_draft.tsv` (Arabidopsis-table counts in `notes`) |
| `markers_draft.tsv` | 45 rows, skill schema + `alt_id` (`ref_species=strawberry`, `tissue=fruit`, IDs *F. vesca* v4.0.a2 `FvH4_` with underscore; `alt_id` = v2.0.a2 `gene#####` where a paper gives it) |
| `literature/` | Full text of Feng et al. 2019 J Exp Bot (PMC6322568) and Guo et al. 2022 Nat Commun (PMC9271072), downloaded 2026-10-20 from Europe PMC |

## Datasets

Only one single-cell/spatial dataset exists for strawberry fruit. A Europe PMC search on
2026-10-20 (`(strawberry OR Fragaria) AND (single-cell OR single-nucleus OR snRNA-seq OR scRNA-seq OR spatial transcriptom*)`, 1,469 hits, top 40 read) found no other fruit atlas; the other hits were reviews or other species/tissues.

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Ma2026 | Ma Z ... Zhou J. *Nat Commun* 17:10447 (2026), doi:10.1038/s41467-026-77874-6, PRJNA1311706 | "snRNA-seq" on BMKMANU DG1000 (protocol and 3-7% intronic reads suggest whole cells), plus 10x Visium (55 µm spots) and spatial metabolomics | 32,017 cells (6 libraries, st2/3/5; one library, SC_2_2, missing from SRA); 7,654 Visium spots | cluster_only (cluster→type map only in the Results text; no per-cell labels, no processed object) | low-medium |

Characterized-gene sources (not atlases, used for endosperm/embryo gaps):
- Feng J ... Kang C. *J Exp Bot* 70:563 (2019), doi:10.1093/jxb/ery384: promoter-GUS lines for FveTAR1/2 and FveYUC4/5/10/11 in seeds, fveyuc10 CRISPR.
- Guo L ... Liu Z. *Nat Commun* (2022), doi:10.1038/s41467-022-31656-y: FveAGL62/80 endosperm auxin induction; lists v2/v4 IDs for all YUC/TAR genes.

## Verdict matrix per cell type

One dataset, two modalities. A = Adopt, R = Revise, X = Reject, - = not called.

| Expected type | Ma2026 snRNA | Ma2026 Visium | Notes |
|---|---|---|---|
| Epidermis | A (cl15,16) | A (Fruit-Epidermis) | receptacle and achene epidermis not split |
| Guard, Trichome | - | - | not resolved |
| Cortex | R (in Parenchyma cl13,14,20) | R (Cortex-1); X (Cortex-2, technical) | conflicting markers |
| Pith | R (in Parenchyma) | A (Pith domain) | expression-only markers |
| Receptacle_Parenchyma | R (cl13,14,20) | R (Diamond, Bundle-Sheath) | spot domains, not cell types |
| Procambium / Xylem / Phloem / Sieve_Element | R (all in cl8) | R (Fruit-Bundle st5 only; Pedicel-Bundle) | sub-types not separated |
| Vascular_Bundle | R (cl8) | R (Fruit-/Pedicel-Bundle, Fruit-Bundle-Adjacent) | PIN1/PIN5 GUS, GDH1/PP2 in situ |
| Seed_Coat / Endosperm / Embryo | R (Seed cl4,10,19 merged) | R (Seed = whole achene) | cl18 'Carpel' at st5 expresses FveYUC4/YUC10 (see below) |
| Ovary_Wall, Endocarp | - | - (inside Seed spots) | not resolved |
| Carpel / Style / Carpel_Epidermis | R (cl12,18) | R (Carpel) | stigma/style/ovary merged |
| Pollen | X ('Others' cl6; identifiable as pollen) | - | stage 2 only |
| Nectary, Petal | - | - | |
| Sepal | R (Sepal&Pedicel cl5,7,17) | A (Sepal); X (Sepal-Tip) | organ-level |
| Mesophyll | - | (Pedicel st5 photosynthetic) | |
| Dividing_cells / S_Phase (states) | X as 'Carpel' cl3 / cl2 → state | R (FBA, see below) | |
| (stress state) | cl7 WRKY33/53/NLR | - | in 'Sepal&Pedicel' |
| (unassigned) | cl1, cl11; 'Others' cl9, cl21 | - | |

## Markers (`markers_draft.tsv`)

45 rows: 9 `function`, 22 `characterized_enriched`, 14 `expression`; 3 `state` rows.
- Taken from the review's 40 rows, merged by gene ID. No gene appears twice; the two different metallothioneins (FvH4_3g36020 vascular, FvH4_3g36040 pith/Diamond) are kept as separate genes.
- Added 6 characterized seed genes (FveYUC4/5/10/11, FveTAR1, FveAGL62) from Feng 2019 and Guo 2022 to fill the Endosperm and Embryo gaps.
- Regraded against `literature_search.md`: Visium spot projections are not cell-resolution, so genes supported only by them are `low`. The review's `medium` for VPE was lowered to `low`. FDH, NACK1 and CYCB2;4 were raised to `function`, following the Arabidopsis tables.
- `requires=Rosaceae` is set on expression-only receptacle/carpel/sepal rows; these only make sense for a strawberry-type receptacle fruit. **`Rosaceae` is a new trait tag:** add `Rosaceae → eudicot` to `IMPLIES` in `map_markers.py` before using these rows.
- New cell-type names, not yet used in skill tables: `Vascular_Bundle` (unresolved bundle, analogous to `Stele`), `Pith`, `Receptacle_Parenchyma`, `Seed`, `Seed_Coat`, `Endosperm`, `Embryo`, `Carpel`, `Style`, `Carpel_Epidermis`, `Sepal`, `Pollen`. Reused names: `Epidermis`, `Cortex`, `Phloem`, `Sieve_Element`, `Procambium`, `Dividing_cells`, `S_Phase`.

### Cross-study markers

Only one marker qualifies for the cross-study confidence raise:

| Gene | Cell type | Study 1 | Study 2 | Result |
|---|---|---|---|---|
| FvH4_4g17980 FveYUC11 | Endosperm | Feng 2019: promoter-GUS throughout the endosperm after fertilization | Ma 2026: enriched in Seed cl4 at st5 (0.13/0.02) | function medium → **high** |
| FvH4_2g24750 FveYUC10 | Endosperm | Feng 2019: GUS in endosperm (weak) + CRISPR lowers auxin | Ma 2026 text: "Seed" at st2 (Supp Fig 25), but its only DE hit is cl18 'Carpel' st5 | not raised (partial) |

The ID of every YUC/TAR gene is the same in Feng 2019, Guo 2022 and Ma 2026 (v2↔v4 tables in both papers).

### Gaps (no validated marker)

- No strawberry marker at all: Guard, Trichome, Xylem, Phloem_Companion, Ovary_Wall, Endocarp, Nectary, Petal, Mesophyll. Use the Arabidopsis tables via homology for Guard, Xylem, Phloem_Companion and Mesophyll.
- Expression-only markers: Cortex, Pith, Receptacle_Parenchyma, Carpel, Style, Carpel_Epidermis.
- No `function` marker (other rows only): Seed_Coat, Embryo, Sepal, Pollen, Vascular_Bundle.

## Recommended label reference

Ma2026 is the only reference. Its labels are cluster-level only, so to reuse them, re-cluster the SRA reads (v4.0.a2) and map clusters with SD2-SD5.
- Adopt only **Epidermis** (cl15/16) as a type label.
- Treat cl8 as Vascular_Bundle (to split), cl2/cl3 as S_Phase/Dividing_cells, cl6 as Pollen, and cl7 as a stress state.
- Use the Visium domains as positional hints, not cell types.

For seed tissues, the Feng 2019 reporters (YUC4 embryo, YUC5 chalazal endosperm, YUC10/11 and TAR1 endosperm) are a better guide than the merged Seed label.

## Conflicts and corrections to the review

- **Fruit-Bundle-Adjacent is not a dividing zone by its markers.** In SD10 its "top" genes CYCB2;4 (FvH4_2g16590) and CYCA1;1 (FvH4_2g27590) have pct.1 < pct.2 (0.23 vs 0.41; 0.39 vs 0.52). Their high avg_log2FC comes from a few spots, so they do not mark FBA. The review's "likely a dividing, cambium-like zone" is unsupported. Its only well-detected top gene, NRAMP6 (FvH4_6g28670, 0.99/0.51), is also broad. Only PIN5 in situ + GUS supports the domain.
- **cl18 ('Carpel') probably holds seed cells at st5 (inference).** FveYUC4 (embryo reporter) and FveYUC10 (endosperm reporter) are DE only in cl18 at st5 (0.25/0.003 and 0.25/0.009). The review assigned FveYUC10 to "Seed/endosperm (st2)" without noting this.
- **SLP3 (FvH4_3g01740) annotation.** SD10 says subtilisin-like serine protease 3 and SD13 says "peptidase inhibitor 19". These agree: the I9 domain is the subtilase prodomain. The cell-type conflict (Cortex / Fruit-Bundle / Bundle-Sheath) remains.
- **VPE (FvH4_6g36630).** The text says ALPHA-VPE and SD5 says GAMMA-VPE, but the listed AGI, AT3G20210, is delta-VPE. Delta-VPE is the seed-coat VPE in Arabidopsis, which fits cl19, so the row is labelled Seed_Coat.
- **Specificity values.** Several values in the review differ from SD13 (PP2 cl8 st5 is 0.66/0.16 in SD13, not 0.33/0.02; FvH4_4g05050 is 0.53/0.31, not 0.96/0.54). The draft uses the SD13/SD5 values.
- **SD12 errors (confirmed).** The homolog column is copy-pasted (AT3G25710 = TMO5 is given for FvH4_2g34420, and AT5G59810 recurs). FvH4_5g24020 (VIM1) is listed as a receptacle-epidermis "TT12" marker. The stigma gene is FvH4_3g08671 in SD12 but FvH4_3g36671 in Supp Fig 13.
- The review's FvH4_3g24570 specificity comes from cl15/16. SD13 lists it for cl16 (0.75/0.23) and cl17 (0.81/0.19); cl17 is part of 'Sepal&Pedicel'.

## Overlap with existing skill tables

- **Same species:** there is no strawberry or Rosaceae table in `references/markers/`, so there is no direct overlap.
- **Orthologous rows in the Arabidopsis tables:** PDF1 (AT2G42840, Epidermis), FDH (AT2G26250, Epidermis), APL (AT1G79430, Phloem), SEOR1 (AT3G01680, Sieve_Element).
- Using `map_markers.py` with homology for strawberry data would bring in these and the other Arabidopsis rows. The strawberry-ID rows here would add Endosperm/Embryo/Seed_Coat/Pollen/receptacle types that the leaf/root tables lack.

## What could not be verified

- **IDs not confirmed in any gene database.** GDR (rosaceae.org) and PLAZA dicots 5.0 (vandepoelelab.be) are behind Cloudflare bot checks, which I did not try to get around. UniProt indexes no FvH4 IDs, and the Ensembl REST service returned errors/not-found.
- **IDs were checked only within and across papers.** Every ID was confirmed to occur in Ma 2026's own tables or text (SD5, SD10-SD13, Methods), with a consistent annotation. The YUC/TAR/AGL62 IDs also match across Feng 2019, Guo 2022 and Ma 2026.
- **Arabidopsis ortholog assignments are the paper's own** (APL, PXY, TMO5, SEOR1, PDF1, FDH, CER1, STK, DOG1, PER1, PRK2A, RALF). They were not checked by BLAST, and SD12's homolog column is unreliable.
- No per-cell labels, processed matrices, or per-type cell counts exist publicly.
- FveAGL62's ghost specificity comes from dissected-tissue bulk RNA-seq, not cell resolution.
