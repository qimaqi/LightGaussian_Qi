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

gaussian_raw_save_path = '/usr/bmicnas02/data-biwi-01/ct_video_mae/omniobject3d/output_raw/'
blender_renders_path = '/usr/bmicnas02/data-biwi-01/ct_video_mae/blender_renders/'

scenes_list = sorted(os.listdir(gaussian_raw_save_path))

if  args.end_idx > len(scenes_list) or args.end_idx == -1:
    args.end_idx = len(scenes_list)

print("total length of scenes_list", len(scenes_list))
# scenes_list = scenes_list[::-1]

sub_scenes_list = scenes_list[args.start_idx:args.end_idx]
print("sub_scenes_list", sub_scenes_list)


for scene_i in tqdm.tqdm(sub_scenes_list):
    start_t = time.time()
    # in first time we run without active sampling
    scene_class = scene_i.split('_')[:-1]
    scene_class = '_'.join(scene_class)
    scene_tgt_path = os.path.join(blender_renders_path, scene_class, scene_i, 'render')
    point_cloud_path = os.path.join(gaussian_raw_save_path, scene_i ,'point_cloud', 'iteration_20000' , 'point_cloud.ply')
    prune_output_dir = os.path.join(gaussian_raw_save_path, scene_i ,'lightning_output')
    os.makedirs(prune_output_dir,exist_ok=True)

    # print(f"######## untar {scene_i} to {scene_tgt_path} ###############")
    # os.system(f'tar -xzvf /usr/bmicnas02/data-biwi-01/qimaqi_data/blender_renders/{scene_class}.tar.gz  --directory=/usr/bmicnas02/data-biwi-01/qimaqi_data/blender_renders/{scene_class}/ --strip-components=1 ./{scene_i}')
    port=6047

    prune_percent = 0.6 # start value
    print(f"######## processing {scene_i} ###############", scene_tgt_path, prune_output_dir)

    os.system(f"python train_densify_prune.py -s {scene_tgt_path} -m {prune_output_dir} --eval --port {port} --prune_percent {prune_percent} --prune_decay 0.6") # --prune_iterations 20000

    # data_dir = os.path.join(scene_tgt_path, 'render')
    # with open(os.path.join(data_dir, 'transforms.json'), 'r') as fp:
    #     meta = json.load(fp)

    # train_json = copy.deepcopy(meta)
    # test_json = copy.deepcopy(meta)

    # train_json['frames'] = train_json['frames'][:-4]
    # test_json['frames'] = test_json['frames'][-4:]

    # for frame in train_json['frames']:
    #     frame['file_path'] = os.path.join('images', frame['file_path'])
    # for frame in test_json['frames']:
    #     frame['file_path'] = os.path.join('images', frame['file_path'])

    # with open(os.path.join(data_dir,'transforms_train.json'), 'w') as f:
    #     json.dump(train_json, f, indent=4) 

    # with open(os.path.join(data_dir,'transforms_test.json'), 'w') as f:
    #     json.dump(test_json, f, indent=4) 

    # with open(os.path.join(data_dir,'transforms_val.json'), 'w') as f:
    #     json.dump(test_json, f, indent=4) 

    # # # clean some files
    # shutil.rmtree(os.path.join(data_dir, 'depths'))
    # shutil.rmtree(os.path.join(data_dir, 'normals'))

    # # split transsform

    # # prepare config files
    # print()
    # print(f"######## processing {scene_i} ###############")
    # print()
    # os.system(f'python main.py fit --data.path {scene_tgt_path}/render/ -n {scene_i} --max_steps 20_000 --output {output_dir} --trainer.enable_progress_bar=False --trainer.check_val_every_n_epoch=100')
    # print(f"######## finish {scene_i} cost ###############", time.time()-start_t)
    # # shutil.rmtree(os.path.join('.', 'sbatch_log', 'debug.log'))
