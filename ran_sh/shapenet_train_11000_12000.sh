#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_11000_12000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian


start_idx=11000
end_idx=12000

python shapenet_train_schusch.py --start_idx=$start_idx --end_idx=$end_idx
# sbatch --output=sbatch_log/11000_12000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=rtx_2080_ti:1 shapenet_train_11000_12000.sh
# 63271095