#!/bin/bash
# End-to-end smoke test of the skill's scripts on a small synthetic rice-root dataset.
# Exercises: map_markers (--no-blast, trait filter, core + characterized tables),
# published-label import (CSV, barcode-mismatch warning, then fixed barcodes),
# cluster_evidence (published key as cluster + meta key), apply_annotations
# (adopted published rows before cluster rows), annotation_report, and an
# accuracy check against the known truth.
#
# Usage (on a compute node; about 2-4 min, < 4 GB RAM):
#   bash tests/smoke_test.sh [OUTDIR]
# Needs scanpy >= 1.8 with leidenalg (set CONDA_SH / CONDA_ENV to activate a conda env).
set -euo pipefail
SKILL=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:-${SCRATCH:-/tmp}/plant_celltype_smoketest}
S=$SKILL/scripts
M=$SKILL/references/markers
mkdir -p "$OUT"; cd "$OUT"
if ! python -c "import scanpy, leidenalg" 2>/dev/null && [ -n "${CONDA_SH:-}" ] && [ -f "$CONDA_SH" ]; then
  source "$CONDA_SH" && conda activate "${CONDA_ENV:-scanpy}"
fi
step() { echo; echo "=== $*"; }

step "1. synthetic data"
python "$SKILL/tests/make_synthetic.py" --skill "$SKILL" --out "$OUT"

step "2. map markers (same species, core + characterized rice tables)"
python "$S/map_markers.py" --no-blast --target-traits Oryza \
    --reference "$M/rice_root.tsv" "$M/characterized/rice.tsv" --out-markers markers_rice.tsv | tail -5

step "3a. import published labels as published: expect a low-match warning (barcode suffix)"
python -c "
import sys; sys.path.insert(0, '$S')
import scanpy as sc
from apply_annotations import import_labels
a = sc.read_h5ad('synthetic.h5ad')
import_labels(a, 'published_labels.csv:published_label:pub')
" > import_raw.log 2>&1 || true   # zero overlap exits non-zero by design
cat import_raw.log
grep -q "WARN low match" import_raw.log && echo "PASS: low-match warning raised"

step "3b. fix barcodes (strip '-1') as Step 1 instructs"
python -c "
import pandas as pd
t = pd.read_csv('published_labels.csv', index_col=0)
t.index = t.index.str.replace(r'-1$', '', regex=True)
t.to_csv('published_labels_fixed.csv')
"

step "4. cluster evidence with the published key"
python "$S/cluster_evidence.py" --h5ad synthetic.h5ad --output evidence \
    --markers markers_rice.tsv \
    --import-labels published_labels_fixed.csv:published_label:published_celltype \
    --cluster-keys published_celltype leiden_res0.3 leiden_res0.8 \
    --meta-keys sample published_celltype | tail -5
ls evidence/cluster_evidence_published_celltype.md evidence/marker_scores_leiden_res0.8.tsv evidence/cluster_hierarchy.tsv

step "5. annotation table: adopt published Trichoblast/Endodermis/Xylem, call the rest from clusters"
python - <<'EOF'
# Stand-in for the agent's Step 7 reasoning: cluster rows get the majority true type of the
# cells not already covered by adopted published labels.
import scanpy as sc, pandas as pd
a = sc.read_h5ad('synthetic.h5ad')
pub = pd.read_csv('published_labels_fixed.csv', index_col=0)['published_label']
a.obs['pub'] = pub.reindex(a.obs_names).values
adopt = ['Trichoblast', 'Endodermis', 'Xylem']
rest = a.obs[~a.obs['pub'].isin(adopt)]
rows = [('published_celltype', t, t, f'Adopted (synthetic publication); markers enriched') for t in adopt]
for cl, sub in rest.groupby('leiden_res0.8'):
    if len(sub) >= 10:
        rows.append(('0.8', cl, sub['truth'].value_counts().idxmax(), 'cluster call (stand-in for Step 7)'))
pd.DataFrame(rows, columns=['Resolution', 'Cluster', 'CellType', 'Evidence']).to_csv('CellTypeAnnotations.txt', sep='\t', index=False)
print(len(rows), 'annotation rows')
EOF

step "6. apply annotations"
python "$S/apply_annotations.py" --h5ad synthetic.h5ad --annotations CellTypeAnnotations.txt \
    --markers markers_rice.tsv \
    --import-labels published_labels_fixed.csv:published_label:published_celltype \
    --plots-dir annotation_qc --meta-keys sample --out-h5ad annotated.h5ad | tail -5

step "7. evidence report"
python "$S/annotation_report.py" --h5ad annotated.h5ad --annotations CellTypeAnnotations.txt \
    --markers markers_rice.tsv --output annotation_qc/annotation_report.pdf | tail -3
ls -la annotation_qc/annotation_report.pdf

step "7b. gene checks, published gene sets, report with extra genes"
mkdir -p checks
python "$S/check_genes.py" --h5ad annotated.h5ad --cluster-key leiden_res0.8 --genes OsCSLD1,OsRHL1 NOPE \
    --marker-tables markers_rice.tsv --out checks/genes.tsv | tail -4
awk -F'\t' 'NR>1{print $3"\t"$1}' markers_rice.tsv | sed '1i set_name\tgene_id' > sets.tsv
python "$S/score_gene_sets.py" --h5ad annotated.h5ad --cluster-key leiden_res0.8 --sets sets.tsv --out checks/sets | tail -3
python "$S/annotation_report.py" --h5ad annotated.h5ad --annotations CellTypeAnnotations.txt \
    --markers markers_rice.tsv --extra-genes Xylem=OsCSLD1 --output annotation_qc/report_extra.pdf | tail -2

step "7d. State column: state-only row, apply, state pages in the report"
python - <<'EOF'
import scanpy as sc, pandas as pd
a = sc.read_h5ad('synthetic.h5ad')
t = pd.read_csv('CellTypeAnnotations.txt', sep='\t', dtype=str)
t.insert(3, 'State', '')
t.insert(4, 'Confidence', 'medium')
cl = a.obs['leiden_res0.8'].astype(str).value_counts().index[0]
t.loc[len(t)] = ['0.8', cl, '-', 'Heat_Stress', '', f'state-only test row; {a.var_names[0]} cited']
t.to_csv('CellTypeAnnotations_state.txt', sep='\t', index=False)
EOF
python "$S/apply_annotations.py" --h5ad synthetic.h5ad --annotations CellTypeAnnotations_state.txt \
    --import-labels published_labels_fixed.csv:published_label:published_celltype \
    --out-h5ad annotated_state.h5ad > apply_state.log
python "$S/annotation_report.py" --h5ad annotated_state.h5ad --annotations CellTypeAnnotations_state.txt \
    --markers markers_rice.tsv --output annotation_qc/report_state.pdf > report_state.log
if grep -q "state page: Heat_Stress (.*1 cited)" report_state.log; then echo "PASS: state page with cited gene"
else echo "FAIL: no state page"; tail -5 report_state.log; exit 1; fi
python - <<'EOF'
import pandas as pd
c = pd.read_csv('annotation_qc/report_state_confidence.tsv', sep='\t', index_col=0)
print(c[['cells', 'overall', 'analyst', 'markers']].to_string())
assert set(c['analyst']) <= {'medium', 'none'} and c['overall'].isin(['high', 'medium', 'low', 'unresolved']).all()
assert (c['overall'] != 'high').all(), 'overall confidence above the analyst level'
print('PASS: overall confidence')
import scanpy as sc
o = sc.read_h5ad('annotated_state.h5ad').obs
assert 'cell_type_source' in o and (o.loc[o['cell_type'] != 'Unknown', 'cell_type_source'] != 'none').all()
print('PASS: per-cell annotation row recorded')
EOF

step "7e. type_under_state: a state subset keeps its type on the genes the state leaves alone"
python - <<'EOF'
import numpy as np, scanpy as sc
a = sc.read_h5ad('synthetic.h5ad')
a.obs['total_counts'] = np.asarray(np.expm1(a.X).sum(1)).ravel()
t = a.obs['truth'].astype(str)
top = t.value_counts().index[:2]
rng = np.random.default_rng(0)
g = np.array(['other'] * a.n_obs, dtype=object)
idx = np.flatnonzero(t == top[0])
q = rng.choice(idx, len(idx) // 3, replace=False)
g[idx] = 'A'
g[q] = 'Q'
g[t == top[1]] = 'B'
a.obs['grp'] = g
a.write_h5ad('tus_input.h5ad')
EOF
python "$S/type_under_state.py" --h5ad tus_input.h5ad --query Q=grp:Q --candidate A=grp:A --candidate B=grp:B \
    --n-genes 30 --min-cells 20 --out checks/tus > tus.log
python - <<'EOF'
import pandas as pd
s = pd.read_csv('checks/tus_scores.tsv', sep='\t')
m = s.loc[s['group'] == 'Q', 'median'].iloc[0]
print(f'query median {m} (A = 1, B = 0)')
assert m > 0.6, 'type_under_state did not place a subset of type A near A'
print('PASS: type_under_state')
EOF

step "7f. Within column: a row restricted to cells inside a coarse cluster"
python - <<'EOF'
import scanpy as sc, pandas as pd
a = sc.read_h5ad('synthetic.h5ad')
fine = a.obs['leiden_res0.8'].astype(str)
coarse = a.obs['leiden_res0.3'].astype(str)
# a fine cluster and the coarse cluster holding most of it
fc = fine.value_counts().index[0]
cc = coarse[fine == fc].value_counts().index[0]
pd.DataFrame([['0.8', fc, 'TestType', 'high', f'0.3:{cc}', 'restricted row']],
             columns=['Resolution', 'Cluster', 'CellType', 'Confidence', 'Within', 'Evidence']).to_csv(
    'CellTypeAnnotations_within.txt', sep='\t', index=False)
open('within_expect.txt', 'w').write(str(int(((fine == fc) & (coarse == cc)).sum())))
EOF
python "$S/apply_annotations.py" --h5ad synthetic.h5ad --annotations CellTypeAnnotations_within.txt \
    --out-h5ad annotated_within.h5ad > apply_within.log
python - <<'EOF'
import scanpy as sc
o = sc.read_h5ad('annotated_within.h5ad').obs
n, want = int((o['cell_type'] == 'TestType').sum()), int(open('within_expect.txt').read())
assert n == want, f'Within: {n} labelled, expected {want}'
assert o.loc[o['cell_type'] == 'TestType', 'cell_type_source'].str.contains('@').all()
print(f'PASS: Within restricts the row ({n:,} cells)')
EOF

step "7g. depth-matched O/E and --assay atac (cluster_evidence, check_genes)"
python - <<'EOF'
# Gene activity-like data: detection of every gene rises with depth; cluster D is 4x deeper.
# g_depth has no cluster preference (raw in-vs-out favours D, O/E should not); g_true marks B;
# cluster C carries organellar (ChrC_) loci as its top genes.
import numpy as np, pandas as pd, anndata as ad, scanpy as sc
rng = np.random.default_rng(1)
cl = np.repeat(['A', 'B', 'C', 'D'], 300)
depth = rng.lognormal(7, 0.4, len(cl)) * np.where(cl == 'D', 4, 1)
genes = ['g_depth', 'g_true'] + [f'ChrC_g{i}' for i in range(12)] + [f'g{i}' for i in range(300)]
p = np.tile(1 - np.exp(-depth / 6000), (len(genes), 1)).T  # Poisson detection: rises with depth
p[:, 1] = np.where(cl == 'B', 0.7, 0.03)
p[cl == 'C', 2:14] = 0.9
X = (rng.random(p.shape) < p).astype(np.float32)
a = ad.AnnData(X=X, obs=pd.DataFrame({'clu': cl, 'total_counts': depth, 'sample': 's1'},
                                     index=[f'n{i}' for i in range(len(cl))]), var=pd.DataFrame(index=genes))
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
a.obs['clu'] = a.obs['clu'].astype('category')
a.write_h5ad('depth_test.h5ad')
pd.DataFrame({'gene_id': ['g_depth', 'g_true', 'NOT_A_GENE'], 'symbol': ['DEP', 'TRUE', 'MISSING'],
              'cell_type': ['TypeD', 'TypeB', 'TypeB'], 'evidence': ['function'] * 3}).to_csv(
    'depth_markers.tsv', sep='\t', index=False)
pd.DataFrame({'barcode': a.obs_names, 'lab': 'L' + a.obs['clu'].astype(str)}).to_csv(
    'depth_labels.tsv', sep='\t', index=False)
EOF
mkdir -p checks
python "$S/check_genes.py" --h5ad depth_test.h5ad --cluster-key clu --genes g_depth g_true \
    --depth-key total_counts --out checks/depth.tsv > depth_check.log
python - <<'EOF'
import pandas as pd
t = pd.read_csv('checks/depth.tsv', sep='\t', dtype={'cluster': str})
d = t[t.gene_id == 'g_depth'].set_index('cluster')
raw = d.at['D', 'frac'] / d.drop('D')['frac'].mean()
print(f"g_depth in D: frac {d.at['D', 'frac']:.2f}, raw in/out x{raw:.1f}, O/E x{d.at['D', 'oe']:.2f}")
assert raw > 1.5 and d.at['D', 'oe'] < 1.3, 'depth-matched O/E did not remove the depth effect'
pk = t[(t.gene_id == 'g_true') & t.is_peak]
assert pk['cluster'].iloc[0] == 'B' and pk['oe'].iloc[0] > 3, 'true marker lost its peak'
print('PASS: check_genes --depth-key')
EOF
python "$S/cluster_evidence.py" --h5ad depth_test.h5ad --output evidence_atac --assay atac \
    --markers depth_markers.tsv --cluster-keys clu --skip-plots \
    --stress-genes "$SKILL/references/stress/protoplasting_induced_Shahan2022.txt" > evidence_atac.log
grep -q "unmeasurable here, not absent" evidence_atac.log && echo "PASS: missing marker reported as unmeasurable"
grep -q "stress list is ignored" evidence_atac.log && echo "PASS: stress list off for atac"
python - <<'EOF'
import re
md = open('evidence_atac/cluster_evidence_clu.md').read()
assert 'Assay: ATAC' in md and 'Depth-matched' in md
sec = {m.group(1): m.group(2) for m in re.finditer(r'## clu cluster (\w+):(.*?)(?=\n## |\Z)', md, re.S)}
assert 'organellar_DNA' in sec['C'] and 'organellar_DNA' not in sec['A'], 'organellar flag'
assert 'possible doublets' not in md
top_b = re.search(r'Marker scores\*\*: (\w+) oe', sec['B']).group(1)
print('top type by O/E in B:', top_b)
assert top_b == 'TypeB'
open('evidence_atac/marker_scores_oe_clu.tsv').read()
print('PASS: cluster_evidence --assay atac (organellar flag, O/E ranking, doublet/stress off)')
EOF
python - <<EOF
import sys, pandas as pd; sys.path.insert(0, '$S')
from cluster_evidence import dotplot_pages
mk = pd.DataFrame({'gene_id': [f'G{i}' for i in range(2708)], 'cell_type': [f'T{i % 60}' for i in range(2708)],
                   'evidence': 'expression'})
pages, dropped = dotplot_pages(mk, 120, 8, 6)
n = sum(len(g) for pg in pages for g in pg.values())
assert len(pages) <= 6 and all(sum(map(len, pg.values())) <= 120 for pg in pages) and n + dropped == 2708
print(f'PASS: dotplot pages for 2,708 markers: {len(pages)} pages, {n} genes shown')
EOF

step "7h. check_genes: import labels, symbol messages, same-symbol genes, no-table exit"
printf 'query_gene\tref_gene\thit_rank\tpident\tref_symbol\tref_description\trbh\ng_true\tAT1G00001\t1\t80\tTRUEA\t\tyes\ng_depth\tAT1G00002\t3\t40\tLOWR\t\t\ng1\tAT1G00003\t1\t70\tSAMEA\t\tyes\ng2\tAT1G00004\t1\t70\tSAMEB\t\tyes\n' > tiny_map.tsv
printf 'gene_id\tsymbol\tdescription\taliases\nAT1G00001\tTRUEA\tx\tAliasOne\nAT1G00002\tLOWR\tx\t\nAT1G00003\tSAMEA\tx\tSHARED\nAT1G00004\tSAMEB\tx\tSHARED\n' > tiny_ref.tsv
python "$S/check_genes.py" --h5ad depth_test.h5ad --cluster-key published \
    --import-labels depth_labels.tsv:lab:published --genes aliasone LOWR SHARED \
    --gene-map tiny_map.tsv --ref-annotation tiny_ref.tsv > genes_msgs.log
grep -q "| aliasone | g_true" genes_msgs.log && echo "PASS: alias, case-insensitive"
grep -q "LOWR\*\*: resolved to AT1G00002.*rank <= 2 (best: g_depth at rank 3" genes_msgs.log && echo "PASS: rank message"
grep -q "SHARED: names 2 different reference genes" genes_msgs.log && grep -q "SHARED \[AT1G00003\]" genes_msgs.log \
    && echo "PASS: same symbol, different genes kept apart"
grep -q "## published (4 clusters)" genes_msgs.log && echo "PASS: --import-labels as cluster key"
set +e
python "$S/check_genes.py" --h5ad depth_test.h5ad --cluster-key clu --genes g_true SOMESYMBOL > genes_notab.log 2>&1
rc=$?
set -e
if [ $rc -eq 2 ] && grep -q "need a table to resolve" genes_notab.log; then echo "PASS: unresolved symbol without tables exits 2"
else echo "FAIL: exit $rc"; tail -3 genes_notab.log; exit 1; fi

step "7i ATAC. gene activity (peaks and fragments) and subcluster --lsi on synthetic snATAC"
python "$SKILL/tests/make_synthetic_atac.py" --out atac
python "$S/gene_activity.py" --h5ad atac/atac.h5ad --gff atac/genes.gff3 --out atac/ga_peaks.h5ad > atac/ga_peaks.log
python "$S/gene_activity.py" --h5ad atac/atac.h5ad --gff atac/genes.gff3 --out atac/ga_frag.h5ad \
    --fragments atac/frag/s1_fragments.tsv.gz atac/frag/s2_fragments.tsv.gz > atac/ga_frag.log
python "$S/subcluster.py" --h5ad atac/atac.h5ad --cluster-key leiden_res0.5 --clusters 0 1 --lsi \
    --batch-key sample --n-pcs 8 --resolutions 0.3 --output-h5ad atac/sub_lsi.h5ad > atac/sub_lsi.log
python - <<'EOF'
import numpy as np, pandas as pd, scanpy as sc
e = pd.read_csv('atac/expect.tsv', sep='\t').set_index('gene')['type']
p, f = sc.read_h5ad('atac/ga_peaks.h5ad'), sc.read_h5ad('atac/ga_frag.h5ad')
assert 'G00' in p.var_names, 'gene: prefix not stripped'
m = p.var['measurable']
assert m['G_MINUS_UP'] and not m['G_MINUS_DN'] and not m['G_NOPEAK'], 'strand-aware window or measurable flag wrong'
t = p.obs['truth'].astype(str).values
for g, ty in e[e.isin(['A', 'B', 'C'])].items():
    x = np.asarray(p[:, g].X.todense()).ravel()
    assert x[t == ty].mean() > 2 * x[t != ty].mean(), f'{g} not enriched in {ty}'
r = [np.corrcoef(np.asarray(p[:, g].X.todense()).ravel(), np.asarray(f[:, g].X.todense()).ravel())[0, 1]
     for g in e.index[:30]]
assert np.median(r) > 0.6, f'peaks vs fragments gene activity disagree (median r {np.median(r):.2f})'
assert p.obsm['X_lsi'].shape[0] == p.n_obs and 'leiden_res0.5' in p.obs
s = sc.read_h5ad('atac/sub_lsi.h5ad')
assert 'X_lsi_sub' in s.obsm and s.uns['subcluster_source']['lsi']
print(f'PASS: gene activity ({m.sum()}/{len(m)} measurable; peaks vs fragments median r {np.median(r):.2f}); '
      f'subcluster --lsi ({s.obs["leiden_sub_0.3"].nunique()} subclusters)')
EOF

step "7l evidence ranking, NUMT, symbols"
python - <<'EOF'
# Cluster B: four coherent markers of TypeMulti (70% vs 10%) and one strong gene of TypeSingle (90% vs 2%).
# Cluster C: top genes are Arabidopsis chr2 NUMT loci (nuclear IDs). obs frip_x is an extra QC column.
import numpy as np, pandas as pd, anndata as ad, scanpy as sc
rng = np.random.default_rng(2)
cl = np.repeat(['A', 'B', 'C'], 300)
numt = ['AT2G07633', 'AT2G07671', 'AT2G07687', 'AT2G07689', 'AT2G07695', 'AT2G07698', 'AT2G07707', 'AT2G07718',
        'AT2G07727', 'AT2G07739', 'AT2G07741', 'AT2G07751']
genes = ['m1', 'm2', 'm3', 'm4', 's1'] + numt + [f'g{i}' for i in range(200)]
p = np.full((len(cl), len(genes)), 0.1)
p[:, 4] = 0.02
p[cl == 'B', 0:4] = 0.7
p[cl == 'B', 4] = 0.9
p[cl == 'C', 5:17] = 0.95
X = (rng.random(p.shape) < p).astype(np.float32)
a = ad.AnnData(X=X, obs=pd.DataFrame({'clu': cl, 'total_counts': X.sum(1) * 50 + 1000, 'sample': 's1',
                                      'frip_x': np.where(cl == 'C', 0.2, 0.6)},
                                     index=[f'r{i}' for i in range(len(cl))]), var=pd.DataFrame(index=genes))
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
a.obs['clu'] = a.obs['clu'].astype('category')
a.write_h5ad('rank_test.h5ad')
pd.DataFrame({'gene_id': ['m1', 'm2', 'm3', 'm4', 's1'], 'symbol': ['M1', 'M2', 'M3', 'M4', 'S1'],
              'cell_type': ['TypeMulti'] * 4 + ['TypeSingle'], 'evidence': ['expression'] * 5}).to_csv(
    'rank_markers.tsv', sep='\t', index=False)
half = a.obs_names[cl == 'B']
pd.DataFrame({'barcode': half, 'sub': np.where(np.arange(len(half)) % 2, 'b1', 'b2')}).to_csv(
    'rank_sub.tsv', sep='\t', index=False)
pd.DataFrame({'barcode': a.obs_names, 'lab': 'L' + a.obs['clu'].astype(str)}).to_csv(
    'rank_labels.tsv', sep='\t', index=False)
EOF
python "$S/cluster_evidence.py" --h5ad rank_test.h5ad --output evidence_rank --assay atac --depth-key total_counts \
    --markers rank_markers.tsv --cluster-keys clu pubA pubB --skip-plots --qc-keys frip_x \
    --import-labels rank_labels.tsv:lab:pubA rank_labels.tsv:lab:pubB > evidence_rank.log
grep -q "imported lab from rank_labels.tsv as pubB" evidence_rank.log && echo "PASS: --import-labels takes several values"
python - <<'EOF'
import re, pandas as pd
md = open('evidence_rank/cluster_evidence_clu.md').read()
sec = {m.group(1): m.group(2) for m in re.finditer(r'## clu cluster (\w+):(.*?)(?=\n## |\Z)', md, re.S)}
top_b = re.search(r'Marker scores\*\*: (\w+) oe', sec['B']).group(1)
sc_ = pd.read_csv('evidence_rank/marker_score_details_clu.tsv', sep='\t', dtype={'cluster': str})
b = sc_[sc_.cluster == 'B'].set_index('cell_type')
print(f"B: TypeSingle oe {b.at['TypeSingle', 'score_oe']:.2f} (rank {b.at['TypeSingle', 'rank_score_oe']:.2f}), "
      f"TypeMulti oe {b.at['TypeMulti', 'score_oe']:.2f} (rank {b.at['TypeMulti', 'rank_score_oe']:.2f}); top {top_b}")
assert b.at['TypeSingle', 'score_oe'] > b.at['TypeMulti', 'score_oe'], 'test setup: single gene should have higher mean'
assert top_b == 'TypeMulti', 'one-gene type still outranks the multi-gene type'
assert 'organellar_DNA' in sec['C'] and 'organellar_DNA' not in sec['A'], 'NUMT loci not flagged'
assert 'frip_x' in sec['A'], '--qc-keys column not shown'
print('PASS: set-size ranking, NUMT organellar flag, --qc-keys')
EOF
python - <<EOF
import sys, re, numpy as np, pandas as pd; sys.path.insert(0, '$S')
from cluster_evidence import organelle_mask, ORGANELLE_DESC
import anndata as ad
a = ad.AnnData(np.zeros((2, 3), np.float32), var=pd.DataFrame(index=['x1', 'x2', 'x3']))
ann = pd.DataFrame({'symbol': ['', '', 'RBCS'], 'description': ['Ycf1 protein', 'cytochrome c oxidase subunit II',
                    'Rubisco small subunit']}, index=['x1', 'x2', 'x3'])
m = organelle_mask(['x1', 'x2', 'x3'], a, None, re.compile(r'^ATCG'), ann=ann, numt=set())
assert list(m) == [True, True, False], m
print('PASS: organellar-product descriptions')
EOF
printf 'gene_id\tsymbol\tdescription\taliases\nAT1G00011\tPEAR1/DOF2.4\tx\t\nAT1G00012\tKNOLLE (SYP111)\tx\t\nAT1G00013\tATHB-15\tx\tCNA\nAT1G00014\tCYCB1;1\tx\t\n' > sym_ref.tsv
printf 'query_gene\tref_gene\thit_rank\tpident\tref_symbol\tref_description\trbh\nm1\tAT1G00011\t1\t80\t\t\tyes\nm2\tAT1G00012\t1\t80\t\t\tyes\nm3\tAT1G00013\t1\t80\t\t\tyes\nm4\tAT1G00014\t1\t80\t\t\tyes\n' > sym_map.tsv
python "$S/check_genes.py" --h5ad rank_test.h5ad --cluster-key clu --genes PEAR1 DOF2.4 SYP111 HB15 'CYCB1;1' \
    --gene-map sym_map.tsv --ref-annotation sym_ref.tsv > sym.log
for q in "PEAR1 | m1" "DOF2.4 | m1" "SYP111 | m2" "HB15 | m3" "CYCB1;1 | m4"; do
  grep -q "| $q" sym.log || { echo "FAIL symbol $q"; grep -n "PEAR1\|SYP111\|HB15\|CYCB" sym.log | head; exit 1; }
done
echo "PASS: A/B, A (B), hyphen/prefix-normalised and ';' symbols"
python "$S/check_genes.py" --h5ad rank_test.h5ad --cluster-key sub --import-labels rank_sub.tsv:sub \
    --genes m1 --depth-key total_counts --out checks/sub.tsv > sub.log
python - <<'EOF'
import pandas as pd
t = pd.read_csv('checks/sub.tsv', sep='\t', dtype={'cluster': str})
e = t[t.gene_id == 'm1'].set_index('cluster')
print(f"subset key: m1 in b1 frac {e.at['b1', 'frac']:.2f}, exp {e.at['b1', 'frac_exp']:.2f}, O/E {e.at['b1', 'oe']:.1f}")
assert e.at['b1', 'frac_exp'] < 0.4, 'expectation not taken from all other cells'
print('PASS: subset key uses all other cells for the expectation')
EOF

step "7j. cycling carve-out warnings and short-row warning (apply_annotations)"
python "$SKILL/tests/test_apply_cycling.py" "$OUT/carve" > "$OUT/carve.log" 2>&1 || { tail -40 "$OUT/carve.log"; echo "FAIL 7j"; exit 1; }
grep -E "PASS|FAIL" "$OUT/carve.log"

step "7k report depth mode: annotation_report.py --assay atac judges markers by depth-matched O/E"
python - <<'PYEOF'
# depth_test.h5ad (step 7g): cluster D is 4x deeper; g_depth (marker DEP for TypeD) has no real preference,
# g_true (TRUE for TypeB) marks B. Raw in-vs-out credits DEP in TypeD; depth-matched O/E must not.
import numpy as np, pandas as pd, scanpy as sc
a = sc.read_h5ad('depth_test.h5ad')
a.obsm['X_umap'] = np.random.default_rng(0).normal(size=(a.n_obs, 2)) + \
    np.c_[a.obs['clu'].cat.codes.to_numpy() * 4, np.zeros(a.n_obs)]
a.obs['ct'] = a.obs['clu'].map({'A': 'TypeA', 'B': 'TypeB', 'C': 'TypeC', 'D': 'TypeD'}).astype('category')
a.write_h5ad('depth_report.h5ad')
pd.DataFrame({'Resolution': ['ct'] * 4, 'Cluster': ['TypeA', 'TypeB', 'TypeC', 'TypeD'],
              'CellType': ['TypeA', 'TypeB', 'TypeC', 'TypeD'], 'Confidence': ['medium'] * 4,
              'Evidence': ['test'] * 4}).to_csv('depth_ann.txt', sep='\t', index=False)
PYEOF
python "$S/annotation_report.py" --h5ad depth_report.h5ad --key ct --annotations depth_ann.txt \
    --markers depth_markers.tsv --output annotation_qc/report_depth_raw.pdf > report_depth_raw.log 2>&1 \
    || { tail -20 report_depth_raw.log; echo "FAIL 7k (raw)"; exit 1; }
python "$S/annotation_report.py" --h5ad depth_report.h5ad --key ct --annotations depth_ann.txt \
    --markers depth_markers.tsv --assay atac --extra-genes TypeB=g_true TypeD=g_depth \
    --output annotation_qc/report_depth.pdf > report_depth.log 2>&1 || { tail -20 report_depth.log; echo "FAIL 7k"; exit 1; }
grep -q "depth-matched O/E on 'total_counts'" report_depth.log || { tail -20 report_depth.log; echo "FAIL 7k: no depth mode"; exit 1; }
python - <<'PYEOF'
import pandas as pd
raw = pd.read_csv('annotation_qc/report_depth_raw_confidence.tsv', sep='\t', index_col=0)
dep = pd.read_csv('annotation_qc/report_depth_confidence.tsv', sep='\t', index_col=0)
print(dep.to_string())
why = lambda t, ct: ' '.join(str(x) for x in t.loc[ct].values)
assert 'DEP' in why(raw, 'TypeD'), 'raw mode should credit the depth-driven marker DEP'
assert 'DEP' not in why(dep, 'TypeD'), 'depth mode still credits the depth-driven marker DEP'
assert 'TRUE' in why(dep, 'TypeB'), 'depth mode lost the true marker TRUE'
print('PASS: report depth mode (DEP not credited in the deep TypeD; TRUE kept for TypeB)')
PYEOF

step "7c. lineage tags on the shipped marker tables"
python "$SKILL/tests/test_lineage_tags.py" | tail -2

step "8. accuracy vs truth"
python - <<'EOF'
import scanpy as sc
a = sc.read_h5ad('annotated.h5ad')
acc = (a.obs['cell_type'].astype(str) == a.obs['truth'].astype(str)).mean()
unk = (a.obs['cell_type'].astype(str) == 'Unknown').mean()
print(f'accuracy {acc:.3f}  unknown {unk:.3f}')
assert acc >= 0.9, 'accuracy below 0.9'
print('PASS: smoke test complete')
EOF
