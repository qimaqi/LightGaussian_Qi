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

with open('../shapnet_part.json', 'r') as f:
    shapenet_part_dict = json.load(f)
print("shapnet_part.keys()", shapenet_part_dict.keys())
# choose keys by given number
gaussian_count_dict = {}
gaussian_count = 0
for cat_id in shapenet_part_dict.keys():
	gaussian_count += len(shapenet_part_dict[cat_id])
	gaussian_count_dict[cat_id] = gaussian_count

print("gaussian_count_dict", gaussian_count_dict)


gaussian_count = 0
blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render/'
# cat_id = '03211117'  ['02933112', '03761084', '04468005', '04401088', '03636649']
# ['04530566','04090263', '02958343', '02747177', '03593526', '03691459', '03513137', '04074963', '02828884', '03790512', '02946921', '04460130', '03928116', '02801938', '02808440', '04256520', '02992529', '03337140', '04330267']
# ['03467517', '03759954', '02773838', '02880940', '03261776', '03938244', '03207941', '02843684', '03991062', '03046257', '03948459', '04554684', '04004475', '02942699', '04099429', '02818832', '03797390', '04225987', '03085013', '02954340', '03710193']
cat_id_list = ['02958343']
# ['02691156', '03211117', '02933112', '03761084', '04468005', '04401088', '03636649', '03001627']
target_outpur_dir = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/part_output/'
for cat_id in cat_id_list:
	for obj_id in tqdm(shapenet_v1_dict[cat_id]):
		obj_folder = os.path.join(blender_renders_path, cat_id, obj_id)
		# print("obj_folder", obj_folder)
		if os.path.exists(os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply')):
			target_obj_folder = os.path.join(target_outpur_dir, cat_id, obj_id)
			if not os.path.exists(target_obj_folder):
				os.makedirs(target_obj_folder)
			shutil.copy(os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply'), target_obj_folder)
			gaussian_count+=1
		else:
			print("Non exist", os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply'))
	# add zip data function
	zip_data_path = os.path.join(target_outpur_dir, cat_id)
	zip_data_name = zip_data_path + '.zip'
	zip_cmd = 'zip -r ' + zip_data_name + ' ' + zip_data_path
	os.system(zip_cmd)
	# remove folder
	shutil.rmtree(zip_data_path)

print("gaussian_count", gaussian_count)


			

