#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_0_1000_%j.out


module load eth_proxy
module load stack/2024-04
module load cuda/11.8.0

source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian_new

JOB_START_TIME=$(date)
echo "SLURM_JOB_ID:    ${SLURM_JOB_ID}" 
echo "Running on node: $(hostname)"
echo "Starting on:     ${JOB_START_TIME}" 


cd ..
# sbatch --output=sbatch_log/shape_all_gs_%j.out  --ntasks=12 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 shapenet_train_missing_all.sh
# python train_densify_prune.py -s /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic/lego -m /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic_output/lego --eval --port 6032 --prune_percent 0.6 --prune_decay 0.6

python train_densify_prune.py -s /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic/chair -m /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic_output/chair --eval --port 6032 --prune_percent 0.6 --prune_decay 0.6

python train_densify_prune.py -s /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic/drums -m /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic_output/drums --eval --port 6032 --prune_percent 0.6 --prune_decay 0.6

python train_densify_prune.py -s /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic/ficus -m /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic_output/ficus --eval --port 6032 --prune_percent 0.6 --prune_decay 0.6

python train_densify_prune.py -s /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic/hotdog -m /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic_output/hotdog --eval --port 6032 --prune_percent 0.6 --prune_decay 0.6


python train_densify_prune.py -s /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic/materials -m /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic_output/materials --eval --port 6032 --prune_percent 0.6 --prune_decay 0.6


python train_densify_prune.py -s /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic/mic -m /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic_output/mic --eval --port 6032 --prune_percent 0.6 --prune_decay 0.6

python train_densify_prune.py -s /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic/ship -m /cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/dataset/nerf_synthetic_output/ship --eval --port 6032 --prune_percent 0.6 --prune_decay 0.6