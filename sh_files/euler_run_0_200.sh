#!/bin/bash
#SBATCH --job-name=nerfstudio_0_200


# openxlab dataset info --dataset-repo OpenXDLab/OmniObject3D-New

JOB_START_TIME=$(date)
echo "SLURM_JOB_ID:    ${SLURM_JOB_ID}" 
echo "Running on node: $(hostname)"
echo "Starting on:     ${JOB_START_TIME}" 

# module load gcc/8.2.0
# module load python_gpu/3.8.5
# module load open3d/0.9.0
# export PYTHONPATH=$HOME/.local/lib/python3.8/site-packages:$PYTHONPATH
# pip install tensorboard==2.4.1
# pip install Pillow==9.5.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
module load gcc/9.3.0
module load cuda/11.8.0
module load eth_proxy
# module load python/3.11.2

conda activate nerfstudio_env

start_idx=0
end_idx=200

python nerfstudio_nerf_train_euler.py --start_idx=$start_idx --end_idx=$end_idx

# sbatch --output=sbatch_log/0_200_fine_model.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=rtx_4090:1 euler_run_0_200.sh
# 61689825

# sbatch --output=sbatch_log/0_200_fine_model.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=rtx_4090:1 euler_run_0_200.sh
# 61919992

# sbatch --output=sbatch_log/0_200_fine_model.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=rtx_4090:1 euler_run_0_200.sh
# 62311497