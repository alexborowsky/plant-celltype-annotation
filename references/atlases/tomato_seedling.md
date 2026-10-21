<!-- Collated from the survey review of tomato_seedling (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# tomato_seedling: etiolated apical hook and hypocotyl (Solanum lycopersicum)

Group collation for the plant-celltype-annotation skill. Written 2026-10-20 from the
dataset review in `Huang2026/` plus cross-checks against the other tomato reviews in this
resources folder (`../tomato_other/Song2023/`, `../tomato_root/Kajala2021/`,
`../tomato_root/CantoPastor2024/`). No data were re-analysed. The skill was not edited.

Files in this folder:

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Cell types expected from hypocotyl/hook anatomy (skill Step 2 format); `function_markers` = `function` rows in `markers_draft.tsv` |
| `markers_draft.tsv` | 27 graded markers, skill schema + `alt_id` (NCBI RefSeq gene symbol, e.g. `LOC101254107`; empty where UniProt/NCBI has no cross-reference) |
| `Huang2026/` | Dataset review (README, curated markers, paper, supplementary tables, UniProt ID check) |

## Datasets

Only one single-cell dataset of this organ exists in the survey.

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Huang2026 | Huang W, Yang L, ... Tan C (2026) *Hortic Res* 13:uhag044, doi:10.1093/hr/uhag044 (CNGB CNP0007766) | Nuclei, BGI DNBelab C4 (not 10x); Micro-Tom, 72 h dark; mock/ACC/Torin2 | 117,929 nuclei (hook 38,751; hypocotyl 79,178) | cluster_only (no per-cell labels, no processed object; GitHub repo 404) | low |

Independent tomato datasets used only to test cross-study agreement of gene IDs (different
organs, reviewed under other groups):

| Dataset | Organ / platform | Used for |
|---|---|---|
| Song et al. 2023 *PNAS* (10.1073/pnas.2310163120) | Shoot-regenerating cotyledon callus; Stereo-seq (cell resolution), S1000 and Visium spots, 10x snRNA | Dataset S1 per-cluster DE, read here for every Huang marker ID |
| Kajala et al. 2021 *Cell* (10.1016/j.cell.2021.04.024) | Root tip TRAP-seq of promoter-defined populations | Table S1 "Cell type lists" (CTEGs), checked for every Huang marker ID |
| Canto-Pastor et al. 2024 *Nat Plants* (10.1038/s41477-023-01567-x) | Root scRNA-seq | Marker table in its review README |

## Per-cell-type verdicts

Verdicts are from the Huang2026 review (Step 3a), corrected where noted. Song 2023 is shown
only where it supports the same signature in another tissue.

| Expected type | Huang hook | Huang hypocotyl | Song 2023 (callus) support |
|---|---|---|---|
| Epidermis | Revise ("epidermis", ~48%, too large) | Revise ("epidermis", ~47%) | air-side epidermis (iv:5; ii:4) has ML1, GPAT4, KCS2a |
| Epidermis, cuticle-producing | Revise ("exodermis-like" 15,16) | Revise ("exodermis-like" 18,19) | same GPAT4/KCS2a signature in surface spots |
| Guard, Trichome, Glandular_Trichome, Collenchyma, Pith, Pericycle | absent | absent | absent |
| Cortex | Reject ("cortex" cl 12 is phloem) | Revise ("cortex", weak markers) | none |
| Endodermis | Revise ("endodermis-like" 3; PIN3 is not specific) | Adopt, provisional (MYB36 0.32 vs 0.02) | none |
| Phloem / Sieve_Element | Reject "phloem" (G2/M); hook "cortex" = SE/CC signature | Revise: "procambium" cl 15 = developing SEs (SEOa/b); "phloem" (21%) unresolved | Stereo-seq vascular i:4 and snRNA iv:8, iv:15 share SEOa/b, PP2-A9-like, HMA |
| Procambium | Reject ("procambium" = S phase) | Revise (relabel cl 15 as phloem) | snRNA iv:6 (HD-ZIP III) |
| Xylem | Revise (~30%, oversized) | Adopt (CAD 0.35 vs 0.07) | snRNA iv:19, spots ii:8 (IRX1/5, XCP, VND, UXS6, CAD) |
| Dividing_cells / S_Phase | present as hook "phloem" (G2/M) and "procambium" (S) | not separated | snRNA iv:18 (CDC20, CYCB2;4), iv:20 (H2A) |

## Cross-study markers

Rule used (from `literature_search.md`): confidence is raised one level when the same
Solyc ID is cluster-specific for the same cell type in two independent datasets and at least
one of them gives localization support. Here that support is Song 2023 spatial data (Stereo-seq
cells or spots) or a Kajala 2021 promoter-defined TRAP population. Huang 2026 claims that are
only in its dotplot (not in Tables S2/S3) were not counted as specificity. 13 rows were raised:

| Gene | Symbol | Cell type | Studies | Final |
|---|---|---|---|---|
| Solyc03g111810 | SlSEOa | Sieve_Element | Huang hyp cl15 0.66/0.03; Song Stereo-seq i:4, snRNA iv:15 | function high |
| Solyc05g013850 | SlSEOb | Sieve_Element | Huang 0.55/0.01; Song i:4, iv:15; Kajala PH | function high |
| Solyc02g031740 | PP2-A9-like | Phloem | Huang hook "cortex" 0.65/0.03, hyp cl15 0.52/0.04; Song i:4, iv:8, iv:15; Kajala PH | characterized_enriched medium |
| Solyc10g085910 | HMA/NaKR-like | Phloem | Huang hook "cortex" 0.61/0.05; Song iv:8 0.83/0.13, Visium vascular | expression medium |
| Solyc02g072240 | SlCESA8/IRX1 | Xylem | Song iv:19 0.87/0.08, ii:8; Kajala V; Canto-Pastor xylem | function high |
| Solyc09g072820 | SlCESA4/IRX5 | Xylem | Song iv:19 0.88/0.09, ii:8 0.51/0.02; Kajala V; Canto-Pastor | function high |
| Solyc04g082710 | SlXCP1/2-like | Xylem | Song iv:19 0.41/0.01; Kajala V; Canto-Pastor | function high |
| Solyc05g054590 | SlUXS6 | Xylem | Song iv:19, ii:8; Canto-Pastor | characterized_enriched medium |
| Solyc01g107590 | CAD | Xylem | Huang hyp xylem 0.35/0.07; Song iv:19, ii:8 | characterized_enriched medium |
| Solyc01g094700 | SlGPAT4 | Epidermis (hypocotyl) | Huang hook "exodermis-like" 0.41/0.07; Song ii:4, iii:10, iv:5 | characterized_enriched medium |
| Solyc09g083050 | SlKCS2a | Epidermis (hypocotyl) | Huang hook 0.42/0.10, hyp 0.43/0.09; Song ii:4, iii:10, iv:5 | characterized_enriched medium |
| Solyc03g096870 | SlCDC20 | Dividing_cells | Huang hook "phloem" 0.29/0.05; Song iv:18 0.80/0.05 | function high |
| Solyc04g082430 | SlCYCB2;4 | Dividing_cells | Huang hook "phloem" 0.30/0.02; Song iv:18 0.74/0.04 | function high |

Caveat: Song 2023 is callus, and Kajala and Canto-Pastor are root. Agreement shows that the
gene marks the lineage across organs, not that it was localized in the hypocotyl. No marker
in this group was localized in hook or hypocotyl tissue by any study.

## Orthology and ID checks done here

- Every Solyc ID was taken from Huang 2026 Tables S2/S3 or text and re-checked in
  ITAG4.0_descriptions.txt and UniProt (`Huang2026/uniprot_id_check.tsv`), plus UniProt GeneID
  cross-references and NCBI Gene symbols for `alt_id`.
- All 27 marker proteins (ITAG4.0_proteins.fasta, SGN) were BLASTed against Arabidopsis
  Swiss-Prot, and the Arabidopsis reference genes back against the ITAG4.0 proteome
  (ncbi-blast+ 2.16.0; working files in /tmp/abor_tomseed, not copied here). Reciprocal best hits:
  ATML1 = Solyc10g005330; MYB36 = Solyc07g006750; CESA8/IRX1 = Solyc02g072240;
  CESA4/IRX5 = Solyc09g072820; CDC20.1 = Solyc03g096870; GPAT4 = Solyc01g094700;
  VND1 = Solyc02g084350 (also the best tomato hit of ANAC076/VND2).

## Conflicts and corrections to the review

- **SlMYB36 ID conflict.** Huang uses Solyc07g006750 (ITAG "blind-like8"). The tomato root
  review (Canto-Pastor, citing Li et al. 2018) lists Solyc04g077260 (ITAG "blind-like3") as
  SlMYB36-like. By BLAST, Solyc07g006750 is the reciprocal best hit of AtMYB36 (54% over
  367 aa). Solyc04g077260 matches AtMYB36, RAX3 and MYB68 equally, and only over the
  ~120-aa MYB domain. NCBI names LOC101254107 (Solyc07g006750) "transcription factor MYB36".
  The table uses Solyc07g006750, and the root group should re-check its ID.
- **CASP symbols.** Huang/Li 2018 call Solyc06g074230 SlCASP1, Solyc10g083250 SlCASP2 and
  Solyc09g010200 SlCASP3. NCBI calls LOC101263718 (Solyc06g074230) "CASP3-like" and
  LOC101255546 (Solyc10g083250) "CASP1". Compare by ID. All three CASPs are in the Kajala 2021
  meristematic-zone (MZ) list, not its endodermis (EN) list.
- **"SWEET11"** (Solyc03g097610) is a clade III SWEET whose best Arabidopsis hit is SWEET10.
  It is not the SWEET11 ortholog, so it is kept at `low` as a generic phloem row.
- **"XCP2"** (Solyc04g082710) is equally close to AtXCP1 and AtXCP2. Named XCP1/2-like.
- **HD-ZIP III** Solyc02g024070 is ATHB-14/PHB-like, not ATHB-9/PHV as Huang named it. It is
  moved from Xylem to Procambium (Song procambium cluster iv:6), at `low`.
- **4CL3** Solyc03g117870: the ITAG4.0 model is a 4CL2-like ligase; the UniProt entry
  A0A3Q7GIB5 is a different (RING-domain, 699 aa) model of the locus.
- **Histone H2A** Solyc01g099410 is in UniProt (P25469, LeH2A-1). The review said it was
  not. Its best Arabidopsis hit is H2A.5, so replication-dependent S-phase expression is
  not established (row kept at `low`).
- **SlPIN3** Solyc04g007690 is DE in hypocotyl *epidermis* (0.43/0.20) and only weakly in hook
  endodermis-like (0.35/0.27); SlPIN4 has pct.2 0.30-0.56. Both were dropped as endodermis
  markers.
- **SlREO** Solyc01g090610: Jones et al. 2008 call it a root-specific cortex promoter, but it
  is in the Kajala 2021 exodermis (EXO) list and in Song's unassigned snRNA cluster iv:21, which also has GPAT4 and KCS2a.
  Kept at `low` with the conflict in `basis`.
- Dropped as non-specific or unsupported: MDP25 (Solyc10g005100), "EXPA18" (Solyc12g089380,
  ITAG EXPA8), HKT1;1 (Solyc07g014690, rice citation only), "AAP1" (Solyc04g077050,
  ITAG AAP6; pct.2 0.3-0.4 in Song).

## Gaps

No validated marker (no `function` row) for: Guard, Trichome, Glandular_Trichome,
Collenchyma, Cortex, Pericycle, Pith, Procambium, Phloem_Companion, Phloem_Parenchyma,
Mesophyll (contamination check) and S_Phase. Epidermis has only ML1. Endodermis rests on
MYB36 (one study) and a root-validated CASP1 whose hypocotyl expression is unshown.
For these types use the Arabidopsis tables through homology (SUC2, SWEET11/12, KAT1/FAMA,
ATHB8, PCNA/H3.1, SCR). Step 4 targets: tomato SCR/SHR/SGR (shoot endodermis), SlSUC2/SlSUT1
(companion cells), WOX4/PXY (procambium), glandular trichome genes (e.g. terpene synthases
of type VI trichomes), and a hypocotyl cortex gene.

## Recommended label reference

None of the published labels can be imported: Huang 2026 is cluster-only, with no per-cell
table. If the data are re-processed from CNP0007766, use only hypocotyl "endodermis-like"
(clusters 8, 14) and "xylem" (7, 11, 17) as provisional labels. Relabel hypocotyl
"procambium" (15) as Sieve_Element/Phloem, hook "phloem" (9, 11) as Dividing_cells, and hook
"procambium" (8) as S_Phase. Annotate the rest de novo from `markers_draft.tsv` plus the
Arabidopsis tables. Song 2023 (callus) is the better source of tomato vascular signatures
and of an independent epidermis/cuticle signature.

## Overlap with the skill's marker tables

There is no tomato table in `references/markers/`. The only tomato mention is in
`arabidopsis_leaf.tsv` (GL1, noted as absent in tomato). Through homology, these rows
duplicate Arabidopsis rows: ATML1 (Epidermis), SEOR1 family (Sieve_Element), XCP1/XCP2, VND
clade (VND7 in the table; the tomato gene is VND1/2-like), DOF5.6 (Phloem, root),
CASP1-3 and MYB36 (Endodermis, root) and the cell-cycle states. New to the skill:
the tomato SEOa/SEOb, PP2-A9-like and HMA phloem genes, GPAT4/KCS2a for the cuticle-producing
shoot epidermis, CESA4/CESA8 secondary-wall CESAs, UXS6 and CAD. The `tissue` value
`hypocotyl` is new; `map_markers.py --tissue` accepts any string.

## Could not access or verify

- CNGB CNP0007766 file list (JavaScript page); GitHub ctan2020/Tomato-hook-SC (404); so no
  per-cell labels, processed object or per-cluster DE.
- Huang 2026 Fig 1B/D dotplots and Supplemental Figures.pdf were not rendered, so dotplot-only
  claims (ML1, CASPs, IRX1/5, XCP, SWEET, VND2) are unverified.
- Li et al. 2018 (tomato CASP1 reporter) and Jones et al. 2008 (SlREO) were not read; they are
  cited through Huang 2026 and the Canto-Pastor review.
- BLAST checks are best hits against Arabidopsis Swiss-Prot (16,421 reviewed proteins), not a
  full phylogeny. CASP1-3 and DOF5.6 have near-tied tomato paralogs.
