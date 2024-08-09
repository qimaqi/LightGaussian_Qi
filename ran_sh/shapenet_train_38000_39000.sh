#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_38000_39000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian


start_idx=38000
end_idx=39000

python shapenet_train_schusch.py --start_idx=$start_idx --end_idx=$end_idx
# sbatch --output=sbatch_log/38000_39000_gs_%j.out  --ntasks=12 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 shapenet_train_38000_39000.sh
# 63281039 bus error
# 63324203