import os
import sys
import time
import argparse
import trimesh 
from plyfile import PlyData, PlyElement
import shutil
import json 
import glob 
import numpy as np 
import concurrent.futures
from functools import partial
from matplotlib import pyplot as plt
import random 
from tqdm import tqdm

# dict_0 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_0_10000.json'
# dict_1 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_10000_20000.json'
# dict_2 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_20000_30000.json'
# dict_3 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_30000_40000.json'
# dict_40 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_40000_46000.json'
# dict_41 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_46000_50000.json'
# dict_5 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_50000_52468.json'



# # load json 0 1 2 3 4
# with open(dict_0, 'r') as f:
# 	shapenet_v1_dict_0 = json.load(f)

# new_dict = {}
# for cat_id in shapenet_v1_dict_0.keys():
# 	for obj_i in shapenet_v1_dict_0[cat_id]:
# 		object_id = obj_i['obj_id']
# 		new_id = str(cat_id) + '-' + str(object_id)
# 		# remove obj_id
# 		obj_i.pop('obj_id')
# 		new_dict[new_id] = obj_i


# with open(dict_1, 'r') as f:
# 	shapenet_v1_dict_1 = json.load(f)

# for cat_id in shapenet_v1_dict_1.keys():
# 	for obj_i in shapenet_v1_dict_1[cat_id]:
# 		object_id = obj_i['obj_id']
# 		new_id = str(cat_id) + '-' + str(object_id)
# 		# remove obj_id
# 		obj_i.pop('obj_id')
# 		new_dict[new_id] = obj_i


# with open(dict_2, 'r') as f:
# 	shapenet_v1_dict_2 = json.load(f)

# for cat_id in shapenet_v1_dict_2.keys():
# 	for obj_i in shapenet_v1_dict_2[cat_id]:
# 		object_id = obj_i['obj_id']
# 		new_id = str(cat_id) + '-' + str(object_id)
# 		# remove obj_id
# 		obj_i.pop('obj_id')
# 		new_dict[new_id] = obj_i


# with open(dict_3, 'r') as f:
# 	shapenet_v1_dict_3 = json.load(f)

# for cat_id in shapenet_v1_dict_3.keys():
# 	for obj_i in shapenet_v1_dict_3[cat_id]:
# 		object_id = obj_i['obj_id']
# 		new_id = str(cat_id) + '-' + str(object_id)
# 		# remove obj_id
# 		obj_i.pop('obj_id')
# 		new_dict[new_id] = obj_i



# with open(dict_40, 'r') as f:
# 	shapenet_v1_dict_40 = json.load(f)

# for cat_id in shapenet_v1_dict_40.keys():
# 	for obj_i in shapenet_v1_dict_40[cat_id]:
# 		object_id = obj_i['obj_id']
# 		new_id = str(cat_id) + '-' + str(object_id)
# 		# remove obj_id
# 		obj_i.pop('obj_id')
# 		new_dict[new_id] = obj_i


# with open(dict_41, 'r') as f:
# 	shapenet_v1_dict_41 = json.load(f)

# for cat_id in shapenet_v1_dict_41.keys():
# 	for obj_i in shapenet_v1_dict_41[cat_id]:
# 		object_id = obj_i['obj_id']
# 		new_id = str(cat_id) + '-' + str(object_id)
# 		# remove obj_id
# 		obj_i.pop('obj_id')
# 		new_dict[new_id] = obj_i

# with open(dict_5, 'r') as f:
# 	shapenet_v1_dict_5 = json.load(f)

# for cat_id in shapenet_v1_dict_5.keys():
# 	for obj_i in shapenet_v1_dict_5[cat_id]:
# 		object_id = obj_i['obj_id']
# 		new_id = str(cat_id) + '-' + str(object_id)
# 		# remove obj_id
# 		obj_i.pop('obj_id')
# 		new_dict[new_id] = obj_i

# # combine with one dict

# print("shapenet_v1_dict", len(new_dict))

# # save
# with open('shapnetv1_gaussian_all.json', 'w') as f:
# 	json.dump(new_dict, f, indent=4)


# shapnetv1_gaussian_all
# dict_0 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_0_10000.json' 9960
# dict_1 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_10000_20000.json' 10000
# dict_2 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_20000_30000.json' 9999
# dict_3 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_30000_40000.json' 9999
# dict_4 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_40000_50000.json' 7850
# dict_5 = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/shapnetv1_gaussian_50000_52468.json' 2467

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--summerize_file', type=str, default='/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/scripts/modelnet_gaussian_0_12311.json', 
					help='place_saving_dict')
	args = parser.parse_args()

	# example dict
	# shapenet_gaussian_example_dict = {}
	# shapenet_gaussian_example_dict['name'] = "ShapeNetCore.v1 Gaussian"
	# shapenet_gaussian_example_dict['description'] = "Training Gaussian Splatting on ShapeNet PointCLoud Dataset"
	# # shapenet_gaussian_example_dict['reference'] = "TODO"
	# shapenet_gaussian_example_dict['license'] = "TODO"
	# # shapenet_gaussian_example_dict['release'] = "TODO"
	# # shapenet_gaussian_example_dict['labels'] = "TODO"
	# shapenet_gaussian_example_dict['numTraining'] = "TODO"
	# shapenet_gaussian_example_dict['numTest'] = "TODO"
	# shapenet_gaussian_example_dict['file_ending'] = ".ply"

	with open(args.summerize_file, 'r') as f:
		modelnet_dict = json.load(f)


	mmt_results = []
	psnr_results = []
	gaussin_num  =[]
	jsd_results = []
	new_dict = {}
	count = 0
	for cat_i in modelnet_dict:
		for task in modelnet_dict[cat_i]:
			for obj_i in modelnet_dict[cat_i][task]:
				try:
					mmt_results.append(float(obj_i['mmd_xz']))
					mmt_results.append(float(obj_i['mmd_xy']))
					mmt_results.append(float(obj_i['mmd_yz']))
					psnr_results.append(float(obj_i['psnr']))
					gaussin_num.append(float(obj_i['gaussian_nums']))
					jsd_results.append(float(obj_i['jsd_xz']))
					jsd_results.append(float(obj_i['jsd_xy']))
					jsd_results.append(float(obj_i['jsd_yz']))
					count+=1
				except:
					print("error", obj_i)
				


	# with open('shapnetv1_gaussian_all_rename.json', 'w') as f:
	# 	json.dump(new_dict, f, indent=4)

	print("mmt_results", np.mean(mmt_results))
	print("psnr", np.mean(psnr_results))
	print("gaussian_nums", np.mean(gaussin_num))
	print("valid object", count)
	print("jsd", np.mean(jsd_results))

	# recreate json

