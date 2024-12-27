#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_0_1000_%j.out


# module load gcc/9.3.0
# module load eth_proxy
# module load cuda/11.8.0
module load eth_proxy
module load stack/2024-04
module load cuda/11.8.0

source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian_new

JOB_START_TIME=$(date)
echo "SLURM_JOB_ID:    ${SLURM_JOB_ID}" 
echo "Running on node: $(hostname)"
echo "Starting on:     ${JOB_START_TIME}" 


# start_idx=0
# end_idx=20000
# start_idx=20000
# end_idx=40000
start_idx=0
end_idx=2

#  srun --ntasks=8 --mem-per-cpu=4G --gpus=1  --time=240 --pty bash -i
python shapenet_train_schusch.py --start_idx=$start_idx --end_idx=$end_idx --above #--demo
# python shapenet_train_schusch_missing.py --start_idx=$start_idx --end_idx=$end_idx --above --demo

# sbatch --output=sbatch_log/0_1000_gs_%j.out  --ntasks=12 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 shapenet_train_0_1000.sh
# 63509472