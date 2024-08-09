#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_0_1000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian

JOB_START_TIME=$(date)
echo "SLURM_JOB_ID:    ${SLURM_JOB_ID}" 
echo "Running on node: $(hostname)"
echo "Starting on:     ${JOB_START_TIME}" 


start_idx=10000
end_idx=20000

python shapenet_train_schusch.py --start_idx=$start_idx --end_idx=$end_idx
# sbatch --output=sbatch_log/10000_20000_gs_%j.out  --ntasks=12 --mem-per-cpu=4g   --time=2-0 --gpus=titan_rtx:1 shapenet_train_missing_10000_20000.sh
