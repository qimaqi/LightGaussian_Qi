#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_20000_21000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian


start_idx=51000
end_idx=51300

python shapenet_train_schusch.py --start_idx=$start_idx --end_idx=$end_idx 
# --debug
# sbatch --output=sbatch_log/51000_53000_gs_%j.out  --ntasks=12 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 shapenet_train_51000_51300.sh

# sbatch --output=sbatch_log/51000_51300_gs_%j.out  --ntasks=12 --mem-per-cpu=4g   --time=4-0 --gpus=rtx_2080_ti:1 shapenet_train_51000_51300.sh

# ??