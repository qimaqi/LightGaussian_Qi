import os
import sys
import time
import argparse
import trimesh 
from plyfile import PlyData, PlyElement
import shutil
import json 
import glob 


gaussian_count = 0
unfinish = 0
blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/ModelNet40/blender_render'
obj_total_path = []
object_id_list_missing = []
for cat_id in os.listdir(blender_renders_path):
	for task in os.listdir(os.path.join(blender_renders_path, cat_id)):
		for obj_id in os.listdir(os.path.join(blender_renders_path, cat_id, task)):
			obj_folder = os.path.join(blender_renders_path, cat_id, task, obj_id)
			if os.path.exists(os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply')):
				gaussian_count+=1	
				# delete the events file
				tensorboard_file = glob.glob(os.path.join(obj_folder,'light_gs','events.out.*'))
				# if len(tensorboard_file) > 0:
				# 	# print("tensorboard_file", tensorboard_file)
				# 	for i in range(len(tensorboard_file)):
				# 		os.remove(tensorboard_file[i])
			else:
				unfinish += 1


print("gaussian_count", gaussian_count)
print("unfinish", unfinish)
			

