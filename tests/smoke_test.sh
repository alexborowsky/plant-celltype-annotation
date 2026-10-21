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
