"""Smoke test: check apply_annotations' cycling carve-out warnings and short-row warning on a tiny object."""
import os, subprocess, sys
import numpy as np, pandas as pd, anndata as ad
T = sys.argv[1] if len(sys.argv) > 1 else '/tmp/carve'
os.makedirs(T, exist_ok=True)
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts')
n = 2000
rng = np.random.default_rng(0)
# 0 mesophyll, 1 tissue-wide S phase (25%), 2 MSE S phase, 3 S phase that the authors filtered as QC
cl = np.array(['0'] * 1100 + ['1'] * 500 + ['2'] * 300 + ['3'] * 100)
a = ad.AnnData(X=rng.poisson(1, (n, 5)).astype(np.float32),
               obs=pd.DataFrame({'leiden_res0.5': cl, 'sample': 's1'}, index=[f'c{i}' for i in range(n)]))
a.write_h5ad(f'{T}/x.h5ad')
pub = pd.Series(np.select([cl == '2', cl == '1', cl == '3'], ['MSE', 'Cell Cycle: G1-S', 'QC'], 'Mesophyll'),
                index=a.obs_names)
pub.to_frame('label').to_csv(f'{T}/pub.tsv', sep='\t')
open(f'{T}/ann.txt', 'w').write(
    'Resolution\tCluster\tCellType\tState\tConfidence\tEvidence\n'
    '0.5\t0\tMesophyll\t\thigh\tphotosynthesis\n'
    '0.5\t1\tMesophyll\tS_Phase\tlow\tmajority mesophyll\n'
    '0.5\t3\tUnknown\tS_Phase\t\tauthors filtered these\n'
    '0.5\t2\tUnknown\tS_Phase\n')   # short row (no Confidence/Evidence)
r = subprocess.run([sys.executable, f'{S}/apply_annotations.py', '--h5ad', f'{T}/x.h5ad', '--annotations',
                    f'{T}/ann.txt', '--no-write', '--import-labels', f'{T}/pub.tsv:label:published'],
                   capture_output=True, text=True)
out = r.stdout + r.stderr
print(out[-3000:])
ok = [('typed big cycling', '(25% of all)' in out),
      ('no note on phase/QC labels', '"Cell Cycle: G1-S"' not in out and '"QC"' not in out),
      ('unknown carve-out note', '"MSE"' in out and 'carve-out applies' in out),
      ('short row', 'columns but the header has' in out)]
for k, v in ok:
    print(k, 'PASS' if v else 'FAIL')
sys.exit(0 if all(v for _, v in ok) and r.returncode == 0 else 1)
