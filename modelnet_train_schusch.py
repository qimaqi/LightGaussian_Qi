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
import zipfile
from tensorboard.backend.event_processing import event_accumulator
from io import BytesIO

parser = argparse.ArgumentParser()
parser.add_argument('--start_idx', type=int, default=0, 
                help='start scene you want to train.')
parser.add_argument('--end_idx', type=int, default=2,
                    help='end scene you want to end')
parser.add_argument('--debug', action='store_true',
                    help='end scene you want to end')


args = parser.parse_args()


raw_data_dir='/cluster/work/cvl/qimaqi/ws_dataset/ModelNet40/'
blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/ModelNet40/blender_render/'

with open('modelnet_all_dict.json', 'r') as f:
    shapenet_v1_dict = json.load(f)

obj_total_path = []
object_id_list_missing = []


for cat_id in shapenet_v1_dict.keys():
    for split_i in shapenet_v1_dict[cat_id]:
        for obj_id in shapenet_v1_dict[cat_id][split_i]:
            obj_name = obj_id.split('.')[0]
            obj_total_path.append(os.path.join(blender_renders_path, cat_id, split_i, obj_name))


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
finished_scenes = []
error_scenes = {}

for scene_i in tqdm.tqdm(sub_objects_list):
    start_t = time.time()
    # in first time we run without active sampling
    prune_output_dir = os.path.join(scene_i ,'light_gs')
    os.makedirs(prune_output_dir,exist_ok=True)
    port=6048+int(args.start_idx) // 50

    prune_percent = 0.6 # start value
    # print(f"######## processing {scene_i} ###############", prune_output_dir)
    # check if results exist or not
    if os.path.exists(os.path.join(prune_output_dir, 'point_cloud' ,'iteration_30000', 'point_cloud.ply')):
        
        # check image zip all white or not
        try:
            with zipfile.ZipFile(os.path.join(scene_i, 'image.zip'), 'r') as zip_ref:
                zip_contents = zip_ref.namelist()
                image_data = zip_ref.read(zip_contents[0])
                image_file = BytesIO(image_data)
                image = Image.open(image_file)
                image_np = np.array(image)
                image_np_sum = np.sum(image_np)
                # if image_np_sum == 0:   
                #     print("image_np_sum", image_np_sum)
                #     print("===================================")
                # # else:
                # #     if not args.debug:
                # #         try:
                # #             os.system(f"python train_densify_prune.py -s {scene_i} -m {prune_output_dir} --eval --port {port} --prune_percent {prune_percent} --prune_decay 0.6") 
                # #         except Exception as error:
                # #             print(f"scene {scene_i} has error {error}")
                # else:
                #     # print(f"scene {scene_i} already exist, skip")
                finished_scenes.append(scene_i)
        except Exception as error:
            print(f"scene {scene_i} has error {error}")
            error_scenes[scene_i] = error
                

    elif not os.path.exists(os.path.join(scene_i, 'image.zip')):
        print(f"scene {scene_i} does not finish render, skip")
        problematic_scenes.append(scene_i)
    else:
        if not args.debug:
            try:
                os.system(f"python train_densify_prune.py -s {scene_i} -m {prune_output_dir} --eval --port {port} --prune_percent {prune_percent} --prune_decay 0.6") 
            except Exception as error:
                print(f"scene {scene_i} has error {error}")   
                error_scenes[scene_i] = error
    # # get some log from metrics.csv
    # load_metric = np.loadtxt(os.path.join(prune_output_dir, 'metric.csv'), delimiter=',', skiprows=1)
    # # get gaussian numbers and psnr
    # print("load_metric", load_metric)
    

np.savetxt(f'./modelnet_{args.start_idx}_{args.end_idx}_problematic_scenes.txt', problematic_scenes, fmt='%s')
np.savetxt(f'./modelnet_{args.start_idx}_{args.end_idx}_finished_scenes.txt', finished_scenes, fmt='%s')
with open(f'./modelnet_{args.start_idx}_{args.end_idx}_error_scenes.json', 'w') as f:
    json.dump(error_scenes, f, indent=4)
    

# '0409026', '4090263', '02958343', '02747177', '03593526', '03691459', '03513137', '04074963', '02828884', '03790512', '02946921', '04460130', '03928116', '02801938', '02808440', '04256520', '02992529', '03337140', '04330267'
# module load eth_proxy
# module load stack/2024-06
# module load python_cuda/3.11.6        
# python3 render_batch_modelnet.py --start_idx=1000 --end_idx=2000  --debug=False


# sbatch --output=sbatch_log/0000_1000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 modelnet_train_0_1000.sh
# 63486854

# sbatch --output=sbatch_log/1000_2000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 modelnet_1000_2000.sh
# 63486855


# sbatch --output=sbatch_log/2000_3000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 modelnet_2000_3000.sh 63486858

# sbatch --output=sbatch_log/2000_3000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 modelnet_2000_3000.sh 63486858

# sbatch --output=sbatch_log/3000_4000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 modelnet_3000_4000.sh 63486859

# sbatch --output=sbatch_log/4000_5000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 modelnet_4000_5000.sh 63486860


# sbatch --output=sbatch_log/5000_6000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 modelnet_5000_6000.sh 63486861


# sbatch --output=sbatch_log/6000_7000_gs_%j.out  --ntasks=8 --mem-per-cpu=4g   --time=4-0 --gpus=titan_rtx:1 modelnet_6000_7000.sh 63486861