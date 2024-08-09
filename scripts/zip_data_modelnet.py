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

with open('../modelnet_all_dict.json', 'r') as f:
    modelnet_dict = json.load(f)
print("modelnet_dict.keys()", modelnet_dict.keys())
# choose keys by given number
gaussian_count_dict = {}
gaussian_count = 0
for cat_id in modelnet_dict.keys():
	for task in modelnet_dict[cat_id]:
		gaussian_count += len(modelnet_dict[cat_id][task])
		gaussian_count_dict[cat_id] = gaussian_count
	# gaussian_count += len(shapenet_v1_dict[cat_id])
	# gaussian_count_dict[cat_id] = gaussian_count

# ['airplane', 'bathtub', 'bed', 'bench', 'bookshelf', 'bottle', 'bowl', 'car', 'chair', 'cone', 'cup', 'curtain', 'desk', 'door', 'dresser', 'flower_pot', 'glass_box', 'guitar', 'keyboard', 'lamp', 'laptop', 'mantel', 'monitor', 'night_stand', 'person', 'piano', 'plant', 'radio', 'range_hood', 'sink', 'sofa', 'stairs', 'stool', 'table', 'tent', 'toilet', 'tv_stand', 'vase', 'wardrobe', 'xbox']
# gaussian_count_dict {'airplane': 726, 'bathtub': 882, 'bed': 1497, 'bench': 1690, 'bookshelf': 2362, 'bottle': 2797, 'bowl': 2881, 'car': 3178, 'chair': 4167, 'cone': 4354, 'cup': 4453, 'curtain': 4611, 'desk': 4897, 'door': 5026, 'dresser': 5312, 'flower_pot': 5481, 'glass_box': 5752, 'guitar': 6007, 'keyboard': 6172, 'lamp': 6316, 'laptop': 6485, 'mantel': 6869, 'monitor': 7434, 'night_stand': 7720, 'person': 7828, 'piano': 8159, 'plant': 8499, 'radio': 8623, 'range_hood': 8838, 'sink': 8986, 'sofa': 9766, 'stairs': 9910, 'stool': 10020, 'table': 10512, 'tent': 10695, 'toilet': 11139, 'tv_stand': 11506, 'vase': 12081, 'wardrobe': 12188, 'xbox': 12311}

print("gaussian_count_dict", gaussian_count_dict)

# 03001627
cat_id_list = ['dresser', 'flower_pot', 'glass_box', 'guitar', 'keyboard', 'lamp', 'laptop', 'mantel', 'monitor', 'night_stand', 'person']
# [ 'piano', 'plant', 'radio', 'range_hood', 'sink', 'sofa', 'stairs', 'stool', 'table', 'tent', 'toilet', 'tv_stand', 'vase', 'wardrobe', 'xbox']
gaussian_count = 0
blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/ModelNet40/blender_render/'

target_outpur_dir = '/cluster/work/cvl/qimaqi/ws_dataset/modelnet_output/to_download/'
for cat_id in cat_id_list:
	for task in ['train', 'test']:
		for obj_id in modelnet_dict[cat_id][task]:
			obj_id = obj_id.split('.')[0]
			obj_folder = os.path.join(blender_renders_path, cat_id, task, obj_id)
			print("obj_folder", obj_folder)
			if os.path.exists(os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply')):
				target_obj_folder = os.path.join(target_outpur_dir, cat_id, task, obj_id)
				if not os.path.exists(target_obj_folder):
					os.makedirs(target_obj_folder)
				shutil.copy(os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply'), target_obj_folder)
				gaussian_count+=1
			else:
				print("Non exist", os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply'))
	# add zip data function
	zip_data_path = os.path.join(target_outpur_dir, cat_id)
	zip_data_name = cat_id # + '.zip'
	# zip_cmd = 'zip -r ' + zip_data_name + ' ' + zip_data_path
	# os.system(zip_cmd)
	target_folder = zip_data_path
	destination_zip_path = os.path.join(target_outpur_dir, zip_data_name)
	shutil.make_archive(destination_zip_path, 'zip', target_folder)

	# remove folder
	shutil.rmtree(zip_data_path)

print("gaussian_count", gaussian_count)


			

