import os
import sys
import time
import argparse
import trimesh 
from plyfile import PlyData, PlyElement
import shutil
import json 
import glob 

with open('../shapnetv1_output.json', 'r') as f:
    shapenet_v1_dict = json.load(f)

gaussian_count = 0
blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/blender_render/'
obj_total_path = []
object_id_list_missing = []
for cat_id in shapenet_v1_dict.keys():
	for obj_id in shapenet_v1_dict[cat_id]:
		obj_folder = os.path.join(blender_renders_path, cat_id, obj_id)
		# print("obj_folder", obj_folder)
		if os.path.exists(os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply')):
			cat_folder = os.path.join('/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapenet_gs_demo_data/', cat_id)
			# os.makedirs(cat_folder,exist_ok=True)
			gaussian_count+=1
			# delete the events file
			tensorboard_file = glob.glob(os.path.join(obj_folder,'light_gs','events.out.*'))
			if len(tensorboard_file) > 0:
				# print("tensorboard_file", tensorboard_file)
				for i in range(len(tensorboard_file)):
					os.remove(tensorboard_file[i])
				# os.remove(tensorboard_file[0])
		# else:
		# 	print("non gaussian find", obj_folder)

print("gaussian_count", gaussian_count)


			

