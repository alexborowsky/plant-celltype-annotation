<!-- Collated from the survey review of cotton_anther (survey collation, last synced 2026-10-20). Relative paths below refer to the maintainers' resources folder. -->

# Cotton anther: collated cell-type marker resources

Collated 2026-10-20 from the Part A review in `Li2024/` (see `Li2024/README.md`). This was a desk collation only: the data were not reanalysed.

Files in this folder:
- `expected_cell_types.tsv`: the cell types expected from the anatomy of a stage-7 (tetrad) *Gossypium hirsutum* anther. I wrote it from anatomy, not from the published labels. `function_markers` counts the `function` rows in `markers_draft.tsv`.
- `markers_draft.tsv`: 55 rows in the skill marker schema (`ref_species=cotton`, `tissue=anther`). `ref_gene` holds HAU TM-1 v1.1 IDs (`Ghir_A01G000010` style), the IDs used in the paper. The best Arabidopsis hit (AGI) is given in `basis`. `alt_id` is empty, because no second cotton ID system (UTX/JGI `Gohir.`, NAU `GH_`) could be mapped (see Could not verify). The paper's AGI is a homolog, not the same gene, so it does not go in `alt_id`.

## Datasets

| Dataset | Citation | Platform | Cells | Label access | Quality |
|---|---|---|---|---|---|
| Li2024 | Li Y, Ma H, Wu Y ... Zhang X, Min L. Single-Cell Transcriptome Atlas and Regulatory Dynamics in Developing Cotton Anthers. *Adv Sci* 11(3):e2304017 (2024). doi:10.1002/advs.202304017; PMC10797427. Data: BioProject PRJNA1010459, SRR25782594-98 (raw reads only, 38-71 GB each) | FACS-sorted nuclei, 10x 3' v3 snRNA-seq, plus 10x Multiome; line H05; stage-7 anthers; normal (NT) vs high temperature (HT) | NT atlas 17,732 nuclei (1 library, 18 clusters); NT multiome 6,892; HT 9,740 (2 reps) + 6,166 multiome | Cluster level only (Fig 1C, Table S2). No per-cell labels, no processed object, no code. HT labels were transferred from NT | Medium. ISH for every wall layer; tapetum excellent. Single NT library; the vascular and connective calls are weak; two clusters are stress states |

Other searches (2026-10-20, Europe PMC REST: cotton/Gossypium + anther + single-cell/single-nucleus/scRNA-seq/snRNA-seq, 210 hits screened by title): I found no other cotton anther single-cell dataset. Related but not used: the GhAL5 heat-tolerance study (Adv Sci 2026, doi:10.1002/advs.202507766) is bulk 3D-genome/RNA, not single-cell; the alfalfa anther atlas (Plant Biotechnol J 2025, doi:10.1111/pbi.70276) is a different family. Cotton gland single-cell studies of other organs could confirm the Pigment_Gland rows, but I did not review them here.

## Per-cell-type verdict matrix

There is only one dataset, so the matrix has one column. "Not reported" means the type is not annotated in that dataset.

| Expected type | Li2024 |
|---|---|
| Epidermis | Adopt (cl1); Revise cl8 (epidermal genes mixed with the endothecium AOC4/JA set) |
| Endothecium | Adopt (cl3, PRX71 ISH); Revise cl6 (SWEET10/ACL5/NAC062) and cl11 (flavonoid signature) |
| Middle_Layer | Adopt (cl4, PRX40 ISH) |
| Tapetum | Adopt (cl2, 5, 7, 10 as states of one type; cl10 = pollen-wall state, ISH + cotton knockouts) |
| Meiocyte | Revise: cl12 is an S-phase histone signature (HTA3/H2AX ISH); cl13 is G2/M (probably meiosis II) |
| Microspore | Adopt with caveat (cl14; MS5 in 28% of cells; small for a tetrad-rich stage) |
| Connective | Revise (cl0, "tentative", 4 specific genes) |
| Stomium_Septum | Not reported |
| Pigment_Gland | Not reported as such; cl9 ("vascular") is probably gossypol-gland secretory cells (inferred) |
| Xylem | Not reported as such; cl16 ("vascular", ~51 cells) has a secondary-wall signature but also suberin/lipid genes |
| Procambium / Phloem_Companion | Not reported; cl17 "phloem" is Rejected (ABA/senescence state; PP2-A1 broad) |
| Vascular (generic) | Revise cl15 (NAC083 ISH, starvation/ABA state) |
| Sieve_Element | Not expected (nuclei) |
| Filament | Not reported |
| Dividing_cells / S_Phase | Present as cl13 / cl12, labeled meiotic cells |

## Cross-study markers

None. With a single dataset, no marker qualifies for the cross-study confidence increase, and no confidence value in `markers_draft.tsv` was raised. The strongest cotton-specific evidence is within Li 2024 itself: GhCYP703A2 (Ghir_D12G012350) and GhQRT3 (Ghir_D02G025140) have tapetal ISH plus cotton knockout phenotypes, so they are `function`/`high` on single-study evidence. GhAMS (Ghir_D12G003620) is `high` because of ISH plus the defining tapetal function of AMS, although it is detected in 66% of non-tapetal nuclei and is specific only by level.

## Grading notes

- `function` rows are characterized Arabidopsis anther genes whose function defines the cell type (tapetal sporopollenin and regulatory genes, MS5/TDM1, HDG2/FDH, CESA4/IRX7, cell-cycle genes) and that are enriched in the matching cluster in Table S2. Without cotton ISH or a mutant, the maximum is `medium`.
- `characterized_enriched` + `medium` = cotton ISH in Li 2024 (KCS11, PRX71, PRX40, HTA3) or strong single-cluster specificity of a characterized gene (QRT1, A6). `low` = enrichment only, broad background, or an ISH whose specificity the review doubted (CAX3, NAC083, TPS21-like).
- 26 rows come from the review (the 25 in the merged review JSON plus GhGSO1 Ghir_A12G005100 from `Li2024/markers_curated.tsv`). 29 rows were added at collation from Table S2, mostly the second homeolog (A/D) of a reviewed marker, plus PDF1, FDH, LAP5, CYP704B1, A6, CESA4, IRX7 and the cell-cycle state genes. Each is marked "Added at collation" in `basis`. Homeologs of ISH genes are graded one level below the probed gene: the probe may detect both, but this was not shown.
- New cell-type names, not yet in any skill table: `Middle_Layer`, `Microspore` (tetrad-stage; the Arabidopsis inflorescence draft uses `Pollen` for later stages), `Connective`, `Pigment_Gland`, `Stomium_Septum`. `Tapetum`, `Endothecium`, `Meiocyte` match `arabidopsis_inflorescence/markers_draft.tsv`.
- `requires=Gossypium` on the three Pigment_Gland rows. This is a new trait tag. If the table enters the skill, add `Gossypium → eudicot` (or a tribe tag, Gossypieae, since Thespesia and Kokia also have gossypol glands) to `IMPLIES` in `map_markers.py`.
- `tissue=anther` is new as well (the skill README lists leaf/root/any; the Arabidopsis inflorescence draft uses `flower`).

## Gaps (no validated `function` marker)

Endothecium, Middle_Layer, Meiocyte, Connective, Stomium_Septum, Pigment_Gland, Procambium, Phloem_Companion, Filament, and generic Vascular. Of these, Endothecium, Middle_Layer and Meiocyte have cotton ISH markers, but only at `characterized_enriched`. No meiosis-specific gene (DMC1, ZYP1, SPO11-1, MSH5) is meiocyte-specific in Table S2, and ASY1 (Ghir_D02G015470, Ghir_A03G014130) is enriched in the tapetal clusters, not in cl12/13. Phloem markers (SUC2, APL, SWEET11) are absent from all clusters' DE lists.

## Recommended label reference

Li 2024 is the only reference. Use it at cluster level only, through marker transfer, because no per-cell labels exist; the NT atlas (one library) is the cleaner set, and the HT labels should not be reused (forced transfer). Adopt Epidermis (cl1), Endothecium (cl3), Middle_Layer (cl4), Tapetum (cl2/5/7/10, one type with substates) and Microspore (cl14). Treat cl12/cl13 as S_Phase/Dividing_cells states inside the meiocyte lineage, cl9 as a Pigment_Gland hypothesis, cl16 as unresolved secondary-wall cells, cl0 as unconfirmed Connective, and Reject cl17 (stress/senescence). For phloem, procambium and stomium, use the Arabidopsis tables via homology.

## Conflicts and corrections to the review

- **PRX40.** The cotton ISH puts PRX40 (Ghir_A02G005650) in the middle layer, but Arabidopsis PRX9/PRX40 are tapetal. Kept as Middle_Layer from the cotton ISH, with the conflict in `basis`: do not transfer this call to other species by homology.
- **HTA3 (H2AX).** Kept under Meiocyte at `medium` (locule ISH), but cl12's whole signature is replication histones. The two HTB1 rows place the same cluster under S_Phase. Expect cl12 to carry both labels' markers; call it by the absence of somatic wall markers.
- **SGO2** (Ghir_D05G010700, AT5G04320) is cl13-specific; it is placed under Meiocyte, while CYCB1;2/CDKB2;2 from the same cluster are under Dividing_cells.
- **TPS21-like (cl9)** is graded `low` here, not `medium` as in the review, because the cell type (Pigment_Gland) is inferred and conflicts with the paper's Vascular label. The paralogs were not checked against the cotton cadinene synthase (CDN1) family.
- **CAX3** has two hits: the ISH probe Ghir_A09G017370 is cl0-specific but weak (0.28/0.06), while Ghir_D09G016810 is more highly enriched in cl0 (0.47/0.18) but not specific. Only the probe gene is in the table.
- **NAC083** naming: Table S2 maps several genes to AT5G13180 (Ghir_A04G010910 cl15, Ghir_A05G034790 cl6/8, Ghir_Scaffold1571G000010 cl14). Only the ISH probe Ghir_D04G015160 is used. It is specific in both cl15 and cl16.
- **cl16 Xylem rows.** CESA4/IRX7 are secondary-wall genes, but at stage 7 the endothecium has not yet thickened, so xylem is the likelier identity. The cluster's top genes are FAR1/FAR5/GPAT6/NIP5;1 (pct ~1.0), which fits neither cleanly. Confidence `low`.
- Review entry "GhCYP703A2-A" (Ghir_A12G012140) was `characterized_enriched`; here it is `function`/`medium`, since CYP703A2 is a defining tapetal sporopollenin gene and the homeolog is more strongly enriched than the probed D copy.
- All 25 review IDs were re-confirmed in Table S2 (s010.xlsx), and the 11 ISH IDs in Table S8 (s007.xlsx). Every row's Ghir ID was checked by script to have the stated AGI best hit in Table S2.

## Overlap with existing skill tables

There is no cotton table and no anther/flower table in `references/markers/`. By Arabidopsis best hit, only the epidermal and cell-cycle rows overlap: PDF1 (AT2G42840) and FDH (AT2G26250) are in `arabidopsis_leaf.tsv` (Epidermis); `arabidopsis_leaf.tsv` has CYCB1;1 (AT4G37490) and H3.1/PCNA for the states, which are different loci from the CYCB1;2 and HTB1 used here. The tapetal, meiocyte and endothecium genes overlap with the not-yet-merged `datasets/arabidopsis_inflorescence/markers_draft.tsv` (AMS, CYP703A2, CYP704B1, ACOS5, LAP5, ABCG26, MS2, A6, MS1; ASY1/DMC1 for Meiocyte; MYB26 for Endothecium).

## Could not verify

- **Database ID check.** UniProt has no HAU `Ghir_` locus names (0 hits for Ghir_D12G003620), Ensembl Plants has only *G. raimondii*, and CottonFGD gene pages are behind a Cloudflare challenge, which I did not try to bypass. IDs rest on the paper's own tables (S2, S8). For UTX (`Gohir.`) or NAU IDs, use CottonFGD/CottonGen conversion tables in a browser, or BLAST.
- Full-resolution ISH images (only low-res JPGs from the Europe PMC bundle), so ISH specificity was not judged independently.
- Per-cluster cell counts (graphical only, Fig 1C/5B).
- Arabidopsis function citations in `source` (Sorensen 2003, Morant 2007, etc.) are given by author/year as in the other drafts; DOIs were not looked up.
- No processed matrix or per-cell labels are public ("available on request"); the SRA reads (38-71 GB per run) were not downloaded.
