<!-- Collated from the survey review of peanut_fruit (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Peanut fruit (peg and early pod): collated cell-type marker resources

Group `peanut_fruit` for the plant-celltype-annotation skill. Collated 2026-10-20.

Inputs:
- the one review in `survey/merged_reviews.json` (Cui 2024, folder `Cui2024/`)
- a check of a second, unreviewed peg atlas found during collation (Jin 2025 preprint, folder `Jin2025_preprint_unreviewed/`), used only to compare gene IDs

No data were re-analysed.

## Files

| File | Content |
|---|---|
| `expected_cell_types.tsv` | Cell types expected from peg and young-pod anatomy, with marker coverage (skill format) |
| `markers_draft.tsv` | 29 rows in the skill schema plus `alt_id`. `ref_gene` is the Tifrunner gnm2 ID; `alt_id` is the NCBI RefSeq gene (`LOC…`), filled only for a unique 100%-identity match |
| `id_crosswalk_gnm2_to_refseq.tsv` | BLASTP of each marker's gnm2 primary protein against the RefSeq Tifrunner gnm2 proteome (GCF_003086295.3), top 3 loci per gene |
| `Cui2024/` | The review: README, evaluation.tsv, markers.tsv, supplements, LegumeMine ID checks |
| `Jin2025_preprint_unreviewed/` | Research Square page, SupplementaryTables.xlsx (2.6 MB), SupplementaryFigures.docx (1.6 MB) |

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Cui2024 (reviewed) | Cui Y … Liu X (2024) *Plant Commun* 5:100979, doi:10.1016/j.xplc.2024.100979; PRJNA1068272 | 10x Multiome (snRNA + snATAC), nuclei; Tifrunner gnm2 IDs | 49,896 nuclei; 3 stages (aerial peg, 2–3 d in soil, 4–7 d pod), 2 reps each; 21 clusters, 10 labels | `cluster_only`: the cluster→type map is in the Fig 2A legend; per-cell barcodes have no label column; portal http://8.140.245.74:6677/ not checked | low (review); medium-low in the folder README |
| Jin2025 (not reviewed) | Jin W … Liu H (2025) Research Square preprint, doi:10.21203/rs.3.rs-5752647/v1; GSA CRA014828 | snRNA-seq (FANS nuclei); NCBI RefSeq `LOC` IDs (written `ncbi_112…`) | 50,903 nuclei; aerial (20 clusters) and subterranean (22 clusters) pegs; 9 types | none found: the supplementary tables are QC, pseudotime gene modules, bulk DEGs and probes, with no cluster DE or labels | not graded: preprint, markers borrowed from "Liu et al. 2022"; in situ (Supp Fig S5) is low-resolution |

Seen but not examined:
- Sun et al. 2026 *Plant Physiol* (doi:10.1093/plphys/kiag710): snRNA-seq of peanut seeds (seed coat, cotyledon, embryonic axis). This is a separate seed group, but it is the obvious source for seed-coat and embryo markers.
- PeanutOmics (doi:10.1016/j.xplc.2025.101622): an atlas portal that may host processed objects.

## Verdict matrix (published label → canonical, per dataset)

Cui verdicts come from the review, with the corrections below. Jin labels are listed as published; they were not evaluated.

| Canonical type | Cui2024 | Jin2025 (preprint) |
|---|---|---|
| Epidermis | **c9 Adopt-level** inside "cuticular layer" (Revise): PDF1, ABCG11, ABCG32, CER3 | "epidermis and exodermis" (aerial c4, 6, 7; c11, 17 at the tip): not evaluated |
| Exodermis (suberized outer layer) | c18 "periderm" Revise: GPAT5, CYP86A1, MYB93, KCS1; appears only after soil entry | merged into "epidermis and exodermis" |
| Cortex / pericarp parenchyma | "stele" c0, 1, 6 Revise (a peg has no stele); c12 heat-shock and c13 SAUR states | "cortex" c1; "peg cortex of stem homology" c0; "basic tissue" c3, 13, 14 |
| Inner_Pericarp | c17 "unknown" → hypothesis (AGL5 in situ, SEP3-like, SHP-like) | the same MADS genes mark "ovule" c2, 5, 9: **conflict** |
| Xylem (+ fibres) | c16 Revise→Xylem: CESA7 in situ, CESA4, CTL2, UXT1, MYB103 | "xylem" c16 (uncharacterized markers) |
| Procambium | c10 (in "xylem") → Procambium: ACL5, ATHB-8, WAT1 | "phloem and cambium" c19 |
| Phloem | c7, 15 Revise, unconfirmed (cited APL, PME32, ABCC13 are not in the DE tables) | in "phloem and cambium" c19 |
| Endodermis (starch sheath) | c8 "vascular system" → REVIEW hypothesis (IDD14, SGR6, PIN, NPY5) | not called |
| Dividing_cells (state) | c5 "meristem" Reject as type → G2/M | not called |
| S_Phase (state) | c4 "embryo" Reject as type → S phase of young-seed cells (DEK-like in situ in the seed core) | not called |
| Endosperm | **c20 "unknown": corrected from "artifact" to an endosperm/central-cell hypothesis** (AGL80-like log2FC 12.7) | not called |
| Ovule / Seed_Coat / Embryo | not resolved | "ovule" c2, 5, 9, from 2 MADS markers only |
| Anthocyanin_Accumulating (state) | c14 "tip tissue" Revise → pigmentation state | not called |
| Unresolved | c2 (saponin CYP93E1/β-amyrin), c3 (defence PR-10/chitinase), c11, c19 (NAC021) | — |

## Cross-study markers (by gene ID)

There are three shared gene IDs. Gnm2 IDs were matched to Jin's NCBI LOC IDs by BLASTP against the RefSeq gnm2 proteome, at 100% identity. None qualifies for the one-level confidence raise, so no row was raised:

| gnm2 | LOC | Cui2024 | Jin2025 | Why it is not agreement |
|---|---|---|---|---|
| ES1ZP9 (AGL5, SHP-like) | LOC112795288 (100%, homeolog 96.7%) | c17; in situ in the inner shell wall (Fig 5G) | "ovule" marker | Different cell types; Jin took the marker from Liu 2022 and shows no specificity data |
| GAA875 (SEP3-like; DE name MADS4) | LOC112734872 (an identical protein is also encoded by LOC112792608) | c17 top DEG (7.2) | "ovule" marker | Different cell types; the ID mapping is ambiguous |
| V88TU5 (NAC021/022) | LOC112703413 (100%, homeolog 97.8%) | c19 (4.7); in situ in the outer pericarp layers + integuments | in situ in aerial and subterranean pegs | Neither study pins it to one type |

n_cross_study = 0. The c17 MADS genes are found in both atlases, so they mark something real. Whether that is ovule or inner pericarp needs a better in situ.

## Gaps (expected types with no validated peanut marker)

- Guard, Trichome
- Phloem_Parenchyma, Phloem_Companion, and Phloem in general
- Sclerenchyma (shares CESA4/7 with xylem)
- Endodermis/starch sheath: only REVIEW rows
- Cortex/pericarp parenchyma: no specific marker
- Placenta, Seed_Coat, Nucellus, Embryo
- Endosperm: one REVIEW row

The only `function` row is CESA7 (Xylem). Use the Arabidopsis leaf tables through homology for epidermis, guard, phloem and procambium. Do not use the Arabidopsis root endodermis rows (CASPs): they describe root Casparian-strip endodermis, not a starch sheath.

## Recommended label reference

Cui 2024 is the only usable reference: it has cluster DE tables with stable gnm2 IDs and several in situ images. Use it at cluster level only:
- Adopt c9 (Epidermis), c16 (Xylem) and c18 (suberized outer layer → Exodermis).
- Treat c5 and c4 as cell-cycle states.
- Treat everything else as a hypothesis.

Jin 2025 has no published labels or cluster DE tables and uses a different ID system, so it is not a label reference.

## Conflicts and corrections to the review

1. **c20 is not obviously an artifact.** Its top genes include a type I MADS AGL80-like gene (D8U91S; best Arabidopsis hits AGL80 47% and PHE1 40%; log2FC 12.7, near zero elsewhere), defensin-like and TAPETUM DETERMINANT1-like small secreted proteins, and DIR1-like LTP. That fits a central-cell/endosperm (female gametophyte) cluster in fertilized ovules. Revise from "Reject" to an endosperm hypothesis.
2. **KCS1 (AYAJ7Z) is not specific to c18.** I rendered Cui Supp Fig 5 (mmc1.pdf p. 11) with poppler on a compute node. The in situ labels a subepidermal pericarp band and the ovule integuments. NAC021 shows a similar pattern (outer pericarp + integuments), and DEK-like labels the young-seed core (consistent with the S_Phase/young-seed reading of c4).
3. **Symbol checks against RefSeq:**
   - FCRD5F, the paper's "PIN3", is named PIN4-like by RefSeq.
   - 3JX01Z is MYB86 in the DE table and MYB103 in Supp Table 3. BLAST best full-length hit: AT1G63910 MYB103.
   - 7U2XF6 ("AGL1"; DE table "MADS1") is an SHP/AG-clade gene.
   - GAA875 ("MADS4") is SEP3-like, not B-sister.
   - ISGY16 ("APL") is named IPN2-like by RefSeq and is absent from the DE tables, so it was **not** included.
4. **Other paper problems already in the review:**
   - The PHOT1 in situ probe ID `1Q8FUJ` does not exist.
   - YAB5 in situ (W7IKXG) and YAB5 qPCR (20NM7L) use different IDs. Neither ID is in the DE tables, so YAB5 was excluded.
   - CYP87A3 (TTT4AK) is not in the cluster DE tables: excluded.
   - The text puts AGL5 in c0, but the DE table puts it in c17.
5. **Cell-type naming:**
   - "Periderm" → `Exodermis`: a suberized subepidermal layer; no phellogen is shown.
   - "Stele" → `Cortex`/pericarp parenchyma.
   - "Meristem" → `Dividing_cells` (state); "Embryo" → `S_Phase` (state).
   - "Tip tissue" → `Anthocyanin_Accumulating` (state).
   - New names not in the skill tables: `Inner_Pericarp`, `Endosperm`, `Anthocyanin_Accumulating`.
6. **Grading is stricter than in the review.** The review graded PDF1, ABCG11, GPAT5, CYP86A1, ACL5, ATHB-8 and KCS1 as `function`. Here they are `characterized_enriched`/`low`, because the only peanut evidence is cluster enrichment (see literature_search.md, Grading).

## ID notes

- `ref_gene` uses the Cui DE-table form `arahy.Tifrunner.gnm2.ann1.XXXXXX`.
  - LegumeMine and the PeanutBase protein FASTA use `arahy.Tifrunner.gnm2.ann1.Arahy.XXXXXX(.1)`.
  - Many count matrices use `arahy.XXXXXX`.
  - Match on the 6-character suffix.
- `alt_id` = RefSeq `LOC` gene. It is left empty when identity is below 100%, when two loci tie (histone H3, GAA875), or when there is no hit. Use it with `map_markers.py --id-column alt_id` for data on NCBI annotation (e.g. Jin 2025).
- Tifrunner is allotetraploid. Every marker has an A/B homeolog at 94–99% protein identity, which will share reads. Expect markers to work at the homeolog-pair level.
- UniProt does not index the gnm2 IDs. The checks used the Cui tables, LegumeMine (from the review), and BLAST against the PeanutBase gnm2 primary proteome and the RefSeq GCF_003086295.3 proteome.

## Overlap with existing skill tables

There is no peanut or legume table in `references/markers/`. By homology, the draft overlaps the Arabidopsis tables only for:
- PDF1 (Epidermis)
- ATHB-8 (Procambium)
- CESA7/IRX3 (Xylem; also sorghum_leaf CESA7)
- ABCG11/WBC11 (Epidermis; sorghum_leaf)

The phloem markers APL/SUC2/SWEETs would come from the Arabidopsis tables only.

## Could not verify

- Cui per-cluster cell counts (not tabulated); per-replicate composition; the web portal (raw-IP host, not accessed); CNCB PRJCA026274.
- Jin 2025:
  - The figure-level specificity of its markers (main Fig 1B is not in the downloaded supplement).
  - Its three xylem markers: no RefSeq protein link, so not mapped.
  - Its epidermis markers (ABP19b germin-like): best gnm2 hits only about 40% identity, so not mapped.
  - The source "Liu et al. 2022".
- Whether c17 is ovule tissue or inner pericarp, and whether c8 is a starch sheath. Both need in situ with the c17/c8 top genes.
- Sun 2026 (seed snRNA): not reviewed.
