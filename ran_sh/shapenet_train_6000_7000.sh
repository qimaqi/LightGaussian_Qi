#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_6000_7000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian


start_idx=6000
end_idx=7000

python shapenet_train_schusch.py --start_idx=$start_idx --end_idx=$end_idx
# sbatch --output=sbatch_log/6000_7000_gs_%j.out  --ntasks=12 --mem-per-cpu=4g   --time=1-0 --gpus=titan_rtx:1 shapenet_train_6000_7000.sh
# 63270568 fail
# 63429286