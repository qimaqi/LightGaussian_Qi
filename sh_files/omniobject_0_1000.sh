#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_0_2000_%j.out
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:1

module load eth_proxy
# module load gcc/8.2.0
# module load python_gpu/3.11.2
module load stack/2024-06
module load python_cuda/3.11.6
module load cuda/12.1.1 

export MKL_THREADING_LAYER=INTEL
export MKL_SERVICE_FORCE_INTEL=1

source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian

python omniobject_prune_schusch.py --start_idx=283 --end_idx=1000
