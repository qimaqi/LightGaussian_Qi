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

 python train_densify_prune.py -s /usr/bmicnas02/data-biwi-01/qimaqi_data/qimaqi/LightGaussian_Qi/datasets/b089abdb33c39321afd477f714c68df9 -m /usr/bmicnas02/data-biwi-01/qimaqi_data/qimaqi/LightGaussian_Qi/datasets/b089abdb33c39321afd477f714c68df9/prune_tune0/ --eval --port 6047  --prune_percent 0.6 --prune_decay 0.6 --checkpoint_iterations=30000 --save_iterations=30000 #--prune_type=important_score

#  python train_densify_prune.py -s /usr/bmicnas02/data-biwi-01/qimaqi_data/qimaqi/LightGaussian_Qi/datasets/b089abdb33c39321afd477f714c68df9 -m /usr/bmicnas02/data-biwi-01/qimaqi_data/qimaqi/LightGaussian_Qi/datasets/b089abdb33c39321afd477f714c68df9/prune_tune1/ --eval --port 6047  --prune_percent 0.6 --prune_decay 0.6 --checkpoint_iterations=30000 --save_iterations=30000 #--prune_type=v_important_score

#  python train_densify_prune.py -s /usr/bmicnas02/data-biwi-01/qimaqi_data/qimaqi/LightGaussian_Qi/datasets/b089abdb33c39321afd477f714c68df9 -m /usr/bmicnas02/data-biwi-01/qimaqi_data/qimaqi/LightGaussian_Qi/datasets/b089abdb33c39321afd477f714c68df9/prune_tune2/ --eval --port 6047  --prune_percent 0.6 --prune_decay 0.6 --checkpoint_iterations=30000 --save_iterations=30000 #--prune_type=max_v_important_score


# if args.prune_type == "important_score":
#     gaussians.prune_gaussians(
#         (args.prune_decay**i) * args.prune_percent, imp_list
#     )
# elif args.prune_type == "v_important_score":
#     # normalize scale
#     v_list = calculate_v_imp_score(gaussians, imp_list, args.v_pow)
#     gaussians.prune_gaussians(
#         (args.prune_decay**i) * args.prune_percent, v_list
#     )
# elif args.prune_type == "max_v_important_score":