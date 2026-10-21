# Plant-specific pitfalls when annotating clusters

## Homology traps
- **A best hit is not an ortholog.** Large families (ABCG, LTP, SWEET, NAC,
  MYB, cysteine proteases) scatter best hits across paralogs. For example,
  the Nb gene curated as "CER5" best-hits ABCG15, not CER5/ABCG12. Report
  the actual hit, and prefer RBH or OrthoFinder orthogroups where possible.
- **Polyploids and recent WGDs** (N. benthamiana, wheat, *Brassica*, maize)
  can have 2–4 copies per Arabidopsis gene, often with divergent expression.
  Examine every copy, and don't average away a subfunctionalized one.
- **Low identity (<40%)** means family-level homology only. Treat markers
  like this as `low` confidence unless the user has validated them.
- **SULTR2 sulfate transporters mark vascular bundles, not one vascular
  type.** SULTR2 genes are reliably enriched in vascular-associated cells
  in every species examined. But which cell type each copy marks is not
  conserved. In Arabidopsis leaf, SULTR2;2 is bundle sheath and SULTR2;1 is
  xylem parenchyma. In the rice leaf atlas, the SULTR2;1 orthologue is bundle
  sheath. In a *N. benthamiana* leaf test, the dominant SULTR2 co-orthologue
  best-hit SULTR2;1 but was expressed in bundle sheath, which led to a
  bundle-sheath → xylem-parenchyma miscall. Treat a SULTR2 hit as
  "vascular bundle (BS / XP / phloem parenchyma)". Decide the specific type
  from other evidence:
  - SCR/SCL23 (bundle sheath, often sparse in nuclei);
  - photosynthesis genes (C3 bundle sheath is photosynthetic, XP is not);
  - HKT1, xylem loaders, or NPF/AAP transporters (XP);
  - cluster share against expected abundance.

  The Arabidopsis SULTR2;1/2;2 rows are tagged `requires=Brassicaceae`, so
  they don't drive type calls elsewhere. `map_markers.py` also warns when
  members of one gene family are listed for different cell types. The same
  logic applies to any family split between neighbouring cell types
  (SWEET, AAP, PHT, NPF).
- **Lineage-specific genes** (for example, Solanaceae acylsugar genes in
  glandular trichomes) have no meaningful Arabidopsis marker. Use curated
  species markers or literature from a close relative.

## Ambient RNA and dominant cell types
- In green tissue, mesophyll transcripts (RBCS, CAB/LHCB, PSB*) leak into
  every droplet. A mesophyll score based on presence is meaningless. Use
  z-scored cluster means and fraction-expressing *relative* to other
  clusters.
- A cluster whose only signal is "a bit less photosynthesis" is often
  low-quality or an unlabeled rare type diluted by ambient RNA. Look at DE
  for a positive signal before labeling it.
- Chloroplast- and mitochondria-encoded fractions (`pct_organellar`,
  `pct_chloroplast`, `pct_mt`) differ by cell type (mesophyll is high,
  epidermis and vasculature are low). High organellar % by itself does not
  mean a cell is dying in plant leaves. Compare against the dataset and
  within a lineage.

- **Nuclei data carry ambient RNA too.** In snRNA-seq of leaves,
  photosynthesis transcripts were detected in 50–90% of all nuclei in our
  test data, so mesophyll can end up defined only as "photosynthesis-high,
  nothing else". Low reads-in-cells (<30%) in the pipeline report is a
  warning sign; consider ambient correction (SoupX, CellBender) before
  annotating.

## Doublets
- Doublet clusters look like a cell type with **high counts** (≳1.3× the
  median) and **two unrelated programs** (mesophyll + epidermis, bundle
  sheath + phloem). In the sorghum PIPseq test they were 10% of nuclei.
- Scrublet's automatic threshold called 0.1% doublets there and missed them;
  the clusters' median doublet scores (0.10–0.19 vs 0.02–0.04) were the
  useful signal. Compare per-cluster medians rather than trusting the
  per-cell call.
- Label them `Doublet_like` (or exclude them with an `Unknown` row) rather
  than forcing a type; they stay out of the cell-type pages of the report.

## States that masquerade as types
| Signal | Likely state | Handling |
|---|---|---|
| Replication histones (H3.1, H4, H2A), PCNA, MCMs | S phase | Label `S_Phase` or assign underlying type from other markers; note choice |
| CYCB, CDKB, KNOLLE, kinesins | G2/M `Dividing_cells` | same |
| SAG12, cysteine proteases, autophagy | Senescing | state |
| PR1/PR2/PR3/PR5, WRKYs, JA/SA genes | Defense/response | Check treatment composition; often a mesophyll substate |
| LHY/CCA1/TOC1/PRRs | Circadian phase | Don't use as type markers; harvest-time confound |
| HSPs, wound/ethylene genes, ERFs | Protoplasting / dissociation stress | Common in protoplast scRNA and weaker in snRNA; not a type |

## Composition and batch
- A cluster in which >80% of cells come from one sample, or a treatment
  enrichment of more than 2×, is usually batch, a treatment response, or
  transgene-driven. Check it before assigning a type.
- If a real cell type is missing from one replicate, suspect dissociation
  bias, and mention it.

## Transgenes and reporters
- Promoter-reporters (for example, a bundle-sheath promoter driving
  NLS-3xVenus) are among the best validation signals. They should be
  excluded from HVG/PCA so they don't drive clustering, and then used
  post hoc.
- Agro-delivered constructs are expressed only in transformed cells from
  treated samples. Their absence in mock is expected and does not argue
  against the cell-type call.

## Lineage- and tissue-specific differences
- **C4 grasses (sorghum, maize, *Setaria*):** Kranz anatomy inverts the
  photosynthesis markers. RBCS, NADP-ME, and RCA mark *bundle sheath*,
  while PEPC (PPC), PPDK, NADP-MDH, and CA mark *mesophyll*. Don't use
  Arabidopsis mesophyll markers for grass mesophyll without checking.
- **Monocot leaves** have no jigsaw pavement cells. They do have bulliform
  cells, subsidiary cells (the stomatal complex), silica/cork cells, and
  distinct long versus short epidermal cells.
- **Solanaceae** leaves have glandular trichomes (head cells vs
  stalk/base cells) that are transcriptionally very distinct.
- **Roots:** the tip has a strong developmental gradient
  (meristem → elongation → differentiation). Clusters may represent
  zones, not types, and pseudotime is often more appropriate.
- **Nuclei (snRNA)** under-represent enucleate or small-nucleus cells
  (sieve elements, mature xylem vessels). **Protoplasts** under-represent
  cells with thick or lignified walls (xylem, fibers, some epidermis).
- **Bryophytes (liverworts, mosses, hornworts)** have no xylem, phloem,
  roots or flowers, and their gametophytes have no stomata (moss and
  hornwort sporophytes do).
  Vascular, root, hydathode, periderm and flower rows carry
  `excludes=bryophyte`, so give
  `--target-traits liverwort` (or `moss`/`hornwort`). Expect water-conducting
  hydroids/leptoids only in some mosses, plus rhizoids, oil-body cells
  (liverworts), and gemma cups or underleaves depending on the plant's body
  form. Leafy liverworts (e.g. *Calypogeia*) have leaves and underleaves
  but no air chambers; thalloid ones (*Marchantia*) have air pores and
  photosynthetic filaments.

## Resolution choice
- Rare types (guard, xylem, companion cells, trichome) often appear only at
  resolution ≥ 0.8–1.5. Put those rows first in the annotation table.
- Abundant types split at high resolution into state/gradient
  sub-clusters. Label them at low resolution (≤ 0.5).
- If a coarse cluster contains two biologically distinct types that no
  resolution cleanly separates, subcluster it using the Harmony embedding
  restricted to those cells.

## Scanpy gotchas
- Some older h5ad files lose `adata.uns['log1p']['base']` on round-trip. Set
  it to `None` before calling `rank_genes_groups`. The scripts do this.
- Use log-normalized values (`.raw` or a log layer) for scoring and plots,
  never the scaled `X`.
