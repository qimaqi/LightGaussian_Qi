#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_15000_16000_%j.out


module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian


start_idx="[11000 14000 17000 20400 44000 45000 46000 48000 49000]"
end_idx="[11500 15500 17500 20500 44400 45400 46400 48400 49400]"

# # python shapenet_train_schusch_list.py --start_idx=$start_idx --end_idx=$end_idx
# python modelnet_train_schusch.py --start_idx="[11000, 15000, 17000, 20400,44000, 45000, 46000, 48000, 49000]" --end_idx="[11500, 15500, 17500, 20500, 44400, 45400, 46400, 48400, 49400]"
     
python train_densify_prune.py -s /cluster/work/cvl/qimaqi/ws_dataset/ModelNet40/render/airplane/train/airplane_0527/ -m /cluster/work/cvl/qimaqi/ws_dataset/ModelNet40/render/airplane/train/airplane_0527/light_gs/ --eval --port 6044 --prune_percent 0.6  --prune_decay 0.6