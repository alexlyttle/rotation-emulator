#!/bin/bash
#SBATCH --job-name preprocess_tracks
#SBATCH --time 5:0:0
#SBATCH --qos bbdefault
#SBATCH --ntasks 8
#SBATCH --nodes 1
#SBATCH --account daviesgr-cartography
#SBATCH --mail-type BEGIN,TIME_LIMIT_90

set -e

module purge; module load bluebear
module load SciPy-bundle/2020.03-foss-2020a-Python-3.8.2
module load h5py/2.10.0-foss-2020a-Python-3.8.2
module load matplotlib/3.2.1-foss-2020a-Python-3.8.2

python preprocess_tracks.py
