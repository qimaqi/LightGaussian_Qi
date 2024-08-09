#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_15000_16000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian




# python shapenet_train_schusch_list.py --start_idx=$start_idx --end_idx=$end_idx
python shapenet_train_schusch_list.py --start_idx="[28000, 36000, 50000 ]" --end_idx="[29000, 40000, 52000]"
# sbatch --output=sbatch_log/missing_short03_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 shapenet_train_missing_03.sh
# 63427229