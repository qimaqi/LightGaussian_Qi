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

with open('../shapnetv1_output.json', 'r') as f:
    shapenet_v1_dict = json.load(f)
print("shapenet_v1_dict.keys()", shapenet_v1_dict.keys())
# choose keys by given number
gaussian_count_dict = {}
gaussian_count = 0
for cat_id in shapenet_v1_dict.keys():
	gaussian_count += len(shapenet_v1_dict[cat_id])
	gaussian_count_dict[cat_id] = gaussian_count

print("gaussian_count_dict", gaussian_count_dict)

# 03001627
# gaussian_count_dict {'02691156': 4045, '03211117': 5138, '02933112': 6709, '03761084': 6861, '04468005': 7250, '04401088': 8339, '03636649': 10657, '03001627': 17435, '02871439': 17887, '02924116': 18826, '04379243': 27259, '02876657': 27757, '03624134': 28181, '03325088': 28925, '03642806': 29385, '04530566': 31324, '04090263': 33697, '02958343': 37211, '02747177': 37553, '03593526': 38149, '03691459': 39746, '03513137': 39908, '04074963': 39974, '02828884': 41787, '03790512': 42124, '02946921': 42232, '04460130': 42365, '03928116': 42604, '02801938': 42717, '02808440': 43573, '04256520': 46746, '02992529': 47577, '03337140': 47875, '04330267': 48093, '03467517': 48890, '03759954': 48957, '02773838': 49040, '02880940': 49226, '03261776': 49299, '03938244': 49395, '03207941': 49488, '02843684': 49561, '03991062': 50163, '03046257': 50814, '03948459': 51121, '04554684': 51290, '04004475': 51456, '02942699': 51569, '04099429': 51654, '02818832': 51887, '03797390': 52101, '04225987': 52253, '03085013': 52318, '02954340': 52374, '03710193': 52468}

# dict_keys(['02691156', '03211117', '02933112', '03761084', '04468005', '04401088', '03636649', '03001627', '02871439', '02924116', '04379243', '02876657', '03624134', '03325088', '03642806', '04530566', '04090263', '02958343', '02747177', '03593526', '03691459', '03513137', '04074963', '02828884', '03790512', '02946921', '04460130', '03928116', '02801938', '02808440', '04256520', '02992529', '03337140', '04330267', '03467517', '03759954', '02773838', '02880940', '03261776', '03938244', '03207941', '02843684', '03991062', '03046257', '03948459', '04554684', '04004475', '02942699', '04099429', '02818832', '03797390', '04225987', '03085013', '02954340', '03710193'])
gaussian_count = 0
blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render/'
# cat_id = '03211117'  ['02933112', '03761084', '04468005', '04401088', '03636649']
# ['04530566','04090263', '02958343', '02747177', '03593526', '03691459', '03513137', '04074963', '02828884', '03790512', '02946921', '04460130', '03928116', '02801938', '02808440', '04256520', '02992529', '03337140', '04330267']
# ['03467517', '03759954', '02773838', '02880940', '03261776', '03938244', '03207941', '02843684', '03991062', '03046257', '03948459', '04554684', '04004475', '02942699', '04099429', '02818832', '03797390', '04225987', '03085013', '02954340', '03710193']
cat_id_list = ['02808440','02828884']
# ['02691156', '03211117', '02933112', '03761084', '04468005', '04401088', '03636649', '03001627']
target_outpur_dir = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render_output/bak/'
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


			

