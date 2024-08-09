import os
import sys
import time
import argparse
import trimesh 
from plyfile import PlyData, PlyElement
import shutil
import json 
import glob 
from tqdm import tqdm 


demo_data_list = os.path.join('/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render/*/*/light_gs_demo/')

demo_data_list = glob.glob(demo_data_list)

print("demo_data_list", demo_data_list)
target_path = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/demo_gs'
for i in demo_data_list:
    cat_id = i.split('/')[-4]
    src_dir = i 
    dst_dir = os.path.join(target_path, cat_id)
    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
    