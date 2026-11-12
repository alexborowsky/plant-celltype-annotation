# snATAC-seq and multiome data

The skill's evidence scripts read expression. For single-nucleus ATAC (chromatin accessibility) data, convert accessibility to a per-gene **gene activity** matrix, then run the same steps on it, with the changes below. Read this file before Step 1 when the data are snATAC or multiome.

## 1. Choose the route by assay

Check what the object holds before anything else: a peak or tile matrix, fragment files, a paired RNA modality, and the published labels (where they come from and at what level).

| Situation | Route |
|---|---|
| **Multiome, with published RNA labels for the same nuclei** (same barcodes) | The RNA labels are per-nucleus evidence from an independent modality. Run Part A on them (check them on gene activity as Step 3b describes), adopt the ones that pass **per nucleus** (`--import-labels`, adopted rows first), put Doublet rows before them, and use ATAC only for nuclei the RNA labels leave out. |
| **Multiome, RNA counts available, no labels** | Annotate the RNA modality with the normal skill. Use ATAC as a second readout only. |
| **ATAC only, published per-nucleus labels** | Part A as usual. Published ATAC labels are themselves inferred from accessibility, so a disagreement is not automatically your error. Say which side the evidence favours. |
| **ATAC only, published labels per cluster** (cluster IDs + a label table) | The labels describe the authors' clusters, not each nucleus. Map them only where your clusters reproduce theirs. Never treat them as per-nucleus evidence, and do not use the published clusters as annotation rows without checking each one. |
| **ATAC only, no labels** | De novo (Part B) on gene activity, with the depth controls and lower confidence below. |

In the multiome route:
- RNA-**Unassigned** (or unknown) nuclei count as not covered: annotate them from ATAC.
- An RNA-labelled nucleus that fails only an ATAC QC criterion (low fragments, organellar-DNA cluster) keeps its RNA
  label; only doublets override it. Put Doublet rows before the adopted rows, other ATAC QC rows after them.
- De novo fallback rows placed after the adopted rows add only the uncovered nuclei and trigger
  `mostly_shadowed`; write "intended fallback" in their Evidence to acknowledge that.

Pooled-organ atlases (several organs in one object) can carry labels from the other organs. Subset to the organ you are annotating first, and drop labels that cannot occur in it.

## 2. Gene activity

```bash
python $S/gene_activity.py --h5ad atac.h5ad --gff genes.gff3.gz --out gene_activity.h5ad \
    [--fragments frag/<sample>_fragments.tsv.gz ...]
```

- **Window:** gene body + 2 kb upstream of the TSS, strand-aware (`--upstream`, `--downstream`).
- **From fragments** (preferred when fragment files exist and the run time is acceptable): counts Tn5 insertions (both fragment ends) per window. This is close to Signac GeneActivity and ArchR gene scores, and every gene gets a value.
- **From peaks** (default; fast): sums the counts of the peaks that overlap each window. A gene with no overlapping peak is **unmeasurable** (`var['measurable'] = False`, listed in `<out>.unmeasurable_genes.txt`). That means "no data", not "off". A marker that is "not in var_names" or unmeasurable in ATAC means no peak there, not a gene ID problem.
- **Gene IDs** must match the protein FASTA used for homology. Some annotations put a version in the GFF3 `ID` (`Sobic.001G000100.v5.1`) and the plain locus in `Name`; the script notes this. Use `--gene-id-attr Name` then.
- **Binary matrices** (published 0/1 ACR matrices) give near-binary gene scores. Detection fractions then carry all the signal.
- **Output:** X = log1p(CP10k), `layers['counts']` = raw. obs, clusters, embeddings and UMAP are copied from the input, so all scripts and `--import-labels` work unchanged.
- **Tandem duplicates** and neighbouring genes share peaks: their scores are correlated by construction. Treat a hit on one copy of a tandem array as one locus, not several.

Run map_markers, cluster_evidence, check_genes, type_under_state, apply_annotations and annotation_report on `gene_activity.h5ad`. Apply the final table to the peak object as well (same obs_names) when the user wants the labels there.

## 3. Depth control is mandatory

Gene activity detection rises with depth, and depth can vary 100–1,000-fold between nuclei. A high-depth cluster "wins" unrelated markers, and a low-depth cluster looks like it has no program.

- Run `cluster_evidence.py` and `check_genes.py` with `--assay atac --depth-key <obs column>` (total fragments, or `n_gene_activity_counts`). They then report depth-matched observed/expected detection (O/E: each nucleus is compared with nuclei of similar depth) instead of raw in-vs-out fractions.
- Read markers by depth-matched O/E (or z), not by raw "% in vs % out". A marker at 40% in vs 25% out in a cluster with twice the median depth may be no enrichment at all.
- `type_under_state.py` already uses a matched-depth reference.
- Report the depth (median fragments, × the dataset median) of every cluster you label, and say when a call rests on a depth difference.

## 4. QC for ATAC

- **Per-nucleus QC:** TSS enrichment, FRiP (fraction of fragments in peaks), fragment count and organelle fraction (chloroplast/mitochondrial reads) replace genes and counts. Use whatever the source provides. Low-TSS, low-FRiP nuclei are the ATAC version of low-quality cells.
- **Organellar DNA clusters:** a cluster whose top genes are nuclear plastid or mitochondrial insertions (NUPT/NUMT) or organellar-homolog loci is the ATAC equivalent of an ambient-RNA cluster. Label it Low_Quality (or keep a label that a paired RNA modality gives those nuclei), not a cell type.
- **Doublets:**
  - With fragments, use fragment overlap (AMULET-style: nuclei with more than two reads at many loci) if a tool is available.
  - Otherwise, flag depth outliers (≥ 3–5× the median) that show several unrelated lineage programs at once as `Doublet_like`.
  - High depth alone is not a doublet, and Scrublet on gene activity is weak.
- **Turn off RNA-only flags:**
  - the protoplasting/dissociation stress list (nuclei, and not transcripts);
  - the RNA doublet-count flag in `cluster_evidence.py`.

  `--assay atac` does both.
- **Batch:** low-depth samples often form their own clusters even after Harmony. A cluster enriched for low-depth samples that mixes all lineages is a depth artefact. Label its nuclei by another route (paired RNA, subclustering) or leave them Unknown.

## 5. Lower sensitivity, lower confidence

- Many identity genes are invisible in gene activity: small TF genes and channels (stomatal FAMA/SLAC1/KAT1, root-hair RHD6/COBL9, GL2/WER-class TFs). **Absence of a marker is not evidence against a type** in ATAC. Prefer large, highly transcribed function genes (biosynthetic enzymes, transporters, cell-wall genes) as markers.
- The RNA thresholds do not transfer. Replace the 15% function-marker rule with a depth-matched O/E ≥ 1.5 on several genes of the same program.
- **Grade ATAC-only calls one confidence level lower** than the same evidence would earn in RNA (high → medium). Calls adopted from a paired RNA modality keep their RNA grade.
- **Second readouts** (optional, when they would settle a call):
  - **ACR-set specificity:** build a set of regions specific to each confidently labelled group and score every nucleus by the share of its accessible regions in each set relative to the set's share overall. It is depth-independent by construction.
  - **Motif deviation** (chromVAR or similar), if it is already installed: a lineage TF family's motif accessibility (e.g. WOX, DOF, MYB, HD-ZIP IV) can support a call that gene activity cannot.

  Do not install software for this.

## 6. Clusters and subclustering

- Cluster on LSI (TF-IDF + SVD on peaks or tiles; drop the first component when it tracks depth), Harmony-corrected across samples. Do not use a PCA of gene activity for clustering.
- **Subcluster** with `subcluster.py --lsi --batch-key sample` on the **peak object**. It recomputes LSI within the subset. Then import the subclusters onto the gene-activity object; obs_names are shared. Without `--lsi`, it uses `X_lsi_harmony` or `X_lsi` when there is no PCA.
  Small subsets (a few hundred nuclei) often form one cluster at resolutions 0.2–0.5; try 0.8–1.0 before concluding
  the subset is homogeneous (`--resolutions 0.3 0.5 0.8 1.0`).

## 7. States and names

- Cycling nuclei in ATAC are hard to stage. Use `Cycling` for a mixed S + G2/M program, or `S_Phase` / `G2M` when the histone or mitotic genes separate. The Step 8 cycling rule applies unchanged.
- State programs (stress, defense) are usually weaker in accessibility than in RNA. Call a state only on a coherent program, and expect fewer states than in an RNA atlas of the same tissue.

## 8. Reading published objects

- **Seurat/Signac `.rds`:**
  - Export counts, region names, barcodes and metadata with `Matrix::writeMM` from R, rather than converting the whole object.
  - Large objects (several GB) can take an hour to load.
  - Seurat v3 objects need slot access (`obj@assays$peaks@counts`); v5 uses `LayerData`.
- **GEO supplementary files** are sometimes gzipped twice (`.gz` holding a `.gz`). Check with `file` before parsing.
- **Barcodes:** ATAC and GEX barcodes of a multiome differ (different whitelists, sometimes reverse-complemented), and `-1` suffixes come and go. State the mapping you used and the match rate per sample.

In the report, say which route you took (Section 1), how gene activity was computed, which depth control you used, and which calls are ATAC-only (and so graded one level lower).
