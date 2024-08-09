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
parser.add_argument('--debug', action='store_true',
                    help='end scene you want to end')
parser.add_argument('--org_gs', action='store_true',
                    help='no prune and no reg loss')
parser.add_argument('--above', action='store_true',
                    help='use above views')
parser.add_argument('--demo', action='store_true',
                    help='run demo')

args = parser.parse_args()

raw_data_dir='/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1'
if args.above:
    blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render/' # blender_render
else:
    blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/blender_render/' # blender_render
object_cat_path = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/filelists/'
# task0: create all object and id list

# obj_total_path=[]
# object_id_list = []
# print("object_cat_path", len(os.listdir(object_cat_path)), os.listdir(object_cat_path))
# for object_id_file in os.listdir(object_cat_path):
#     cat_id = object_id_file.split('.')[0]
#     with open(os.path.join(object_cat_path, object_id_file), 'r') as f:
#         object_list = f.readlines()
#     object_list = [obj.strip() for obj in object_list]
#     for object_id in object_list:
#         obj_total_path.append(os.path.join(blender_renders_path, cat_id, object_id))
#         object_id_list.append(object_id)

# print("object_id_list example", object_id_list[:10] )
# obj_total_path = sorted(obj_total_path)

with open('shapnetv1_output.json', 'r') as f:
    shapenet_v1_dict = json.load(f)

obj_total_path = []
object_id_list_missing = []
for cat_id in shapenet_v1_dict.keys():
    for id_num, obj_id in enumerate(shapenet_v1_dict[cat_id]):
        if args.org_gs:
            if id_num % 1000 == 0:
                obj_total_path.append(os.path.join(blender_renders_path, cat_id, obj_id))
        else:
            obj_total_path.append(os.path.join(blender_renders_path, cat_id, obj_id))
        

        # if obj_id not in object_id_list:
        #     object_id_list_missing.append(obj_id)
        
if not args.org_gs:
    if  args.end_idx > len(obj_total_path) or args.end_idx == -1:
        args.end_idx = len(obj_total_path)

print("total length of obj_total_path", len(obj_total_path))
sub_objects_list = obj_total_path[args.start_idx:args.end_idx]
print("sub_scenes_list", len(sub_objects_list))

# first check render finish situation
# for scene_i in tqdm.tqdm(sub_objects_list):
#     if not os.path.exists(os.path.join(scene_i.replace('/render',''), 'model.obj')):
#         print(f"scene {scene_i} does not have model, skip")
problematic_scenes = []
error_scenes = {}
finsh_scenes = []

if args.demo:
    seen_category = []

for scene_i in tqdm.tqdm(sub_objects_list):
    cat_id = scene_i.split('/')[-2]
    if args.demo:
        if cat_id in seen_category:
            continue
        seen_category.append(cat_id)
        
    start_t = time.time()
    # in first time we run without active sampling
    prune_output_dir = os.path.join(scene_i ,'light_gs_demo2')
    if args.org_gs:
        prune_output_dir = prune_output_dir.replace('blender_render', 'blender_render_org_gs')#'/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/blender_render_org_gs/' 
    os.makedirs(prune_output_dir,exist_ok=True)
    port=6032+int(args.start_idx) // 100

    prune_percent = 0.6 # start value
    print(f"######## processing {scene_i} ###############", prune_output_dir)
    # check if results exist or not
    if os.path.exists(os.path.join(prune_output_dir, 'point_cloud' ,'iteration_30000', 'point_cloud.ply')):
        finsh_scenes.append(scene_i)
        pass #print(f"scene {scene_i} already exist, skip")
    elif not os.path.exists(os.path.join(scene_i, 'image.zip')):
        print(f"scene {scene_i} does not finish render, skip")
        problematic_scenes.append(scene_i)
    else:
        if not args.debug:
            try:
                if args.org_gs:
                    os.system(f"python train_densify_prune.py -s {scene_i} -m {prune_output_dir} --eval --port {port} --prune_iterations 40000 --scale_reg=False") 
                else:
                    os.system(f"python train_densify_prune.py -s {scene_i} -m {prune_output_dir} --eval --port {port} --prune_percent {prune_percent} --prune_decay 0.6") 
            except Exception as error:
                error_scenes[scene_i] = error
                print(f"scene {scene_i} has error {error}")

# np.savetxt(f'./{args.start_idx}_{args.end_idx}_problematic_scenes.txt', problematic_scenes, fmt='%s')
# np.savetxt(f'./{args.start_idx}_{args.end_idx}_finished_scenes.txt', finsh_scenes, fmt='%s')


# with open(f'./{args.start_idx}_{args.end_idx}_error_scenes.json', 'w') as f:
# 	json.dump(error_scenes, f, indent=4)

    # # get some log from metrics.csv
    # load_metric = np.loadtxt(os.path.join(prune_output_dir, 'metric.csv'), delimiter=',', skiprows=1)
    # # get gaussian numbers and psnr
    # print("load_metric", load_metric)
    


    