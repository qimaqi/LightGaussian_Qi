#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_15000_16000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian




# python shapenet_train_schusch_list.py --start_idx=$start_idx --end_idx=$end_idx
python shapenet_train_schusch_list.py --start_idx="[0, 8000, 13000, 19000, 42000]" --end_idx="[7000, 11000, 14000, 20000, 43000]"
# sbatch --output=sbatch_log/missing_short02_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 shapenet_train_missing_short_02.sh
# 63425352