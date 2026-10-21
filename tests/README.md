# Tests

`smoke_test.sh` runs the whole script chain (map markers, cluster evidence,
subcluster, apply, report) on a synthetic dataset built by `make_synthetic.py`,
in about a minute on a compute node, and checks the labels against the truth.
Run it after changing any script:

```bash
CONDA_SH=~/miniconda3/etc/profile.d/conda.sh CONDA_ENV=scanpy bash tests/smoke_test.sh
```

The skill is also being tested by giving an agent a real dataset and only the
skill, with no memory of other projects, and comparing its annotation with a
reference annotation. Those datasets are not public yet.
