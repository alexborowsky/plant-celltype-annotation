#!/bin/bash
# Generic Slurm wrapper for the plant-celltype-annotation scripts.
# Usage (override resources on the command line):
#   sbatch -p bigmem --mem=256G --time=4:00:00 -o logs/ct_%j.out \
#       run_step.sbatch python /path/to/cluster_evidence.py --h5ad ... --output ...
# Set CONDA_ENV / CONDA_SH to change the environment.
#SBATCH --job-name=ct_annot
#SBATCH --partition=normal
#SBATCH --time=4:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --output=ct_annot_%j.out

set -euo pipefail
CONDA_SH="${CONDA_SH:-$HOME/miniconda3/etc/profile.d/conda.sh}"
CONDA_ENV="${CONDA_ENV:-scanpy}"
source "$CONDA_SH"
conda activate "$CONDA_ENV"
export MPLCONFIGDIR="${SCRATCH:-/tmp}/.mplconfig"
export NUMBA_CACHE_DIR="${SCRATCH:-/tmp}/.numba_cache"

echo "[$(date)] $*"
"$@"
echo "[$(date)] done"
