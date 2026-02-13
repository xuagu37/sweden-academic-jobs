#!/bin/bash

set -e  # Exit on error

module load Miniforge3
mamba activate sweden-academic-jobs

python -m swedjobs
bash scripts/deploy_pages.sh 

