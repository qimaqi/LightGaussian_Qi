#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_40000_41000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian


start_idx=1000
end_idx=2000

python modelnet_train_schusch.py --start_idx=$start_idx --end_idx=$end_idx 
# sbatch --output=sbatch_log/m_0000_1000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=2-0 --gpus=titan_rtx:1 modelnet_train_0_1000.sh
# 
