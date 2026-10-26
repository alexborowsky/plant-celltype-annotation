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
