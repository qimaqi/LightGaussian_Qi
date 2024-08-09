#!/bin/bash
#SBATCH --job-name=zip_data
#!/bin/bash

#SBATCH --ntasks=8
#SBATCH --nodes=2
#SBATCH --gpus-per-node=1

module load gcc/9.3.0
module load eth_proxy
module load cuda/11.8.0
source /cluster/work/cvl/qimaqi/miniconda3/etc/profile.d/conda.sh 
conda activate lightgaussian



python zip_data.py
