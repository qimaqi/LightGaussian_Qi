#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_9000_10000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian


start_idx=9000
end_idx=10000

python shapenet_train_schusch.py --start_idx=$start_idx --end_idx=$end_idx # --debug
# sbatch --output=sbatch_log/9000_10000_gs_%j.out  --ntasks=12 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 shapenet_train_9000_10000.sh
# 63513735