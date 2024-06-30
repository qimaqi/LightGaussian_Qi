#!/bin/bash
#SBATCH --job-name=prune_gs
#SBATCH --output=sbatch_log/prune_gs_0_2000_%j.out
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:1

export MKL_THREADING_LAYER=INTEL
export MKL_SERVICE_FORCE_INTEL=1

source /scratch_net/schusch/qimaqi/miniconda3/etc/profile.d/conda.sh
source /scratch_net/schusch/qimaqi/miniconda3/bin/activate
conda activate lightgaussian
# python omniobject_train_schusch.py --start_idx=0 --end_idx=2

 python train_densify_prune.py -s /usr/bmicnas02/data-biwi-01/qimaqi_data/qimaqi/LightGaussian_Qi/datasets/b089abdb33c39321afd477f714c68df9 -m /usr/bmicnas02/data-biwi-01/qimaqi_data/qimaqi/LightGaussian_Qi/datasets/b089abdb33c39321afd477f714c68df9/prune/ --eval --port 6047  --prune_percent 0.6 --prune_decay 0.6
