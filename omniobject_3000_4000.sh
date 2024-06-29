#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_1000_2000_%j.out
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:1

export MKL_THREADING_LAYER=INTEL
export MKL_SERVICE_FORCE_INTEL=1

source /scratch_net/schusch/qimaqi/miniconda3/etc/profile.d/conda.sh
source /scratch_net/schusch/qimaqi/miniconda3/bin/activate
conda activate lightgaussian
python omniobject_prune_schusch.py --start_idx=3000 --end_idx=4000
# 823771