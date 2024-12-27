#!/bin/bash


module load eth_proxy
module load stack/2024-06
module load python_cuda/3.11.6
# export PYTHONPATH=$HOME/.local/lib64/python3.11/site-packages:$PYTHONPATH
#  export PYTHONPATH=$HOME/.local/lib64/python3.11/site-packages:$PYTHONPATH
start_idx=0
end_idx=53000
# 000

python3 render_batch.py --start_idx=$start_idx --end_idx=$end_idx
# sbatch --output=./joblogs/s_0_2000_%j.log  --ntasks=16 --mem-per-cpu=4g --time=2-0 --gpus=rtx_4090:1 shapenet_render_euler_0_2000.sh    

# 2033469