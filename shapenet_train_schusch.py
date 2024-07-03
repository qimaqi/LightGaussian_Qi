import os 
import numpy as np 
import shutil
import yaml
import argparse
import glob 
import copy
import tqdm
import PIL.Image as Image
import io
import json
import time

from tensorboard.backend.event_processing import event_accumulator


parser = argparse.ArgumentParser()
parser.add_argument('--start_idx', type=int, default=0, 
                help='start scene you want to train.')
parser.add_argument('--end_idx', type=int, default=2,
                    help='end scene you want to end')

args = parser.parse_args()

blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render/'
object_cat_path = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/filelists/'
# task0: create all object and id list

obj_total_path=[]
for object_id_file in os.listdir(object_cat_path):
    object_id = object_id_file.split('.')[0]
    with open(os.path.join(object_cat_path, object_id_file), 'r') as f:
        object_list = f.readlines()
    object_list = [obj.strip() for obj in object_list]
    for object_i in object_list:
        obj_total_path.append(os.path.join(blender_renders_path, object_id, object_i))

    
obj_total_path = sorted(obj_total_path)

if  args.end_idx > len(obj_total_path) or args.end_idx == -1:
    args.end_idx = len(obj_total_path)

print("total length of obj_total_path", len(scenes_list))
sub_scenes_list = scenes_list[args.start_idx:args.end_idx]
print("sub_scenes_list", sub_scenes_list)


for scene_i in tqdm.tqdm(obj_total_path):
    start_t = time.time()
    # in first time we run without active sampling
    prune_output_dir = os.path.join(gaussian_raw_save_path, scene_i ,'light_gs')
    os.makedirs(prune_output_dir,exist_ok=True)
    # print(f"######## untar {scene_i} to {scene_tgt_path} ###############")
    # os.system(f'tar -xzvf /usr/bmicnas02/data-biwi-01/qimaqi_data/blender_renders/{scene_class}.tar.gz  --directory=/usr/bmicnas02/data-biwi-01/qimaqi_data/blender_renders/{scene_class}/ --strip-components=1 ./{scene_i}')
    port=6047

    prune_percent = 0.6 # start value
    print(f"######## processing {scene_i} ###############", scene_tgt_path, prune_output_dir)

    os.system(f"python train_densify_prune.py -s {scene_i} -m {prune_output_dir} --eval --port {port} --prune_percent {prune_percent} --prune_decay 0.6") 
    
    # get some log
    