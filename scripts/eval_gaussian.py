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

def compute_jsd_2d(p, q):
    p = np.stack(p, axis=0)
    p = np.sum(p, axis=0)
    p = p / (np.sum(p) + 1e-9)
	
    q = np.stack(q, axis=0)
    q = np.sum(q, axis=0)
    q = q / (np.sum(q) + 1e-9)

    from scipy.spatial.distance import jensenshannon
    return jensenshannon(p.flatten(), q.flatten())

def kernel_parallel_unpacked(x, samples2, kernel):
  d = 0
  for s2 in samples2:
    d += kernel(x, s2)
  return d


def kernel_parallel_worker(t):
  return kernel_parallel_unpacked(*t)

def disc(samples1, samples2, kernel, is_parallel=True, *args, **kwargs):
  ''' Discrepancy between 2 samples '''
  d = 0

  if not is_parallel:
    for s1 in samples1:
      for s2 in samples2:
        d += kernel(s1, s2, *args, **kwargs)
  else:
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #   for dist in executor.map(kernel_parallel_worker, [
    #       (s1, samples2, partial(kernel, *args, **kwargs)) for s1 in samples1
    #   ]):
    #     d += dist

    with concurrent.futures.ThreadPoolExecutor() as executor:
      for dist in executor.map(kernel_parallel_worker, [
          (s1, samples2, partial(kernel, *args, **kwargs)) for s1 in samples1
      ]):
        d += dist

  d /= len(samples1) * len(samples2)
  return d

def compute_mmd(samples1, samples2, kernel, is_hist=True, *args, **kwargs):
  ''' MMD between two samples '''
  # normalize histograms into pmf  
  if is_hist:
    samples1 = [s1 / (np.sum(s1)+1e-9) for s1 in samples1]
    samples2 = [s2 / (np.sum(s2)+1e-9) for s2 in samples2]
	
  #print('===============================')
  #print('s1: ', disc(samples1, samples1, kernel, *args, **kwargs))
  #print('--------------------------')
  #print('s2: ', disc(samples2, samples2, kernel, *args, **kwargs))
  #print('--------------------------')
#   print('cross: ', disc(samples1, samples2, kernel, *args, **kwargs))
#   print('===============================')
  return disc(samples1, samples1, kernel, *args, **kwargs) + \
          disc(samples2, samples2, kernel, *args, **kwargs) - \
          2 * disc(samples1, samples2, kernel, *args, **kwargs)

def gaussian(x, y, sigma=0.5):  
  support_size = max(len(x), len(y))
  # convert histogram values x and y to float, and make them equal len
  x = x.astype(np.float)
  y = y.astype(np.float)
  if len(x) < len(y):
    x = np.hstack((x, [0.0] * (support_size - len(x))))
  elif len(y) < len(x):
    y = np.hstack((y, [0.0] * (support_size - len(y))))

  #import matplotlib.pyplot as plt
  #plt.subplot(1, 2, 1)
  #plt.imshow(x)
  #plt.subplot(1, 2, 2)
  #plt.imshow(y)
  #plt.show()

  #TODO: Calculate empirical sigma by fitting dist to gaussian 
  dist = np.linalg.norm(x - y, 2)
  return np.exp(-dist * dist / (2 * sigma * sigma))

# add some 3D evalution
def point_cloud_to_histogram(field_size, bins, point_cloud):
  
    square_size = field_size / bins

    halfway_offset = 0
    if(bins % 2 == 0):
        halfway_offset = (bins / 2) * square_size
    else:
        print('ERROR')
    # print("halfway_offset", halfway_offset, "field_size", field_size)
    histogram = np.histogramdd(point_cloud, bins=bins) # , range=([-halfway_offset, halfway_offset], [-halfway_offset, halfway_offset])

    return histogram[0]


def calculate_spatial(sample_obj, sample_gs, cat_id=None, obj_id=None, save=True, all_views=True):
	sample_obj = np.array(sample_obj)
	sample_gs = np.array(sample_gs)
	if all_views:
		mmd_type = ['xy', 'xz', 'yz'] # ['xz']#
	else:
		mmd_type = ['xz']
	filed_size = 2*np.max(np.abs(sample_obj))
	spatial_results = {}
	for i, mmd_t in enumerate(mmd_type):
		if mmd_t == 'xy':
			sample_obj_2D = sample_obj[:,0:2]
			sample_gs_2D = sample_gs[:,0:2]
		elif mmd_t == 'xz':
			sample_obj_2D = sample_obj[:,[0,2]]
			sample_gs_2D = sample_gs[:,[0,2]]
		elif mmd_t == 'yz':
			sample_obj_2D = sample_obj[:,1:3]
			sample_gs_2D = sample_gs[:,1:3]

		# draw 2D scatter plots for debug
		if save:
			plt.scatter(sample_obj_2D[:,0], sample_obj_2D[:,1], c='r', s=1)
			plt.savefig(f'./{cat_id}_{obj_id}_{i}_sample_obj_2D.png')
			plt.close('all')
			plt.scatter(sample_gs_2D[:,0], sample_gs_2D[:,1], c='b', s=1)
			plt.savefig(f'./{cat_id}_{obj_id}_{i}_sample_gs_2D.png')
			plt.close('all')
		
		model_histograms = point_cloud_to_histogram(filed_size,50,sample_obj_2D)
		gs_histograms = point_cloud_to_histogram(filed_size,50,sample_gs_2D)

		jsd_i = compute_jsd_2d(model_histograms, gs_histograms)
		spatial_results['jsd_'+mmd_t] = jsd_i
	
		mmd_i = compute_mmd(model_histograms, gs_histograms, gaussian, is_hist=True)
		spatial_results['mmd_'+mmd_t] = mmd_i
		# print("range x", np.mean((sample_obj[:,0])), np.mean((sample_gs[:,0])))
		# print("range y", np.mean((sample_obj[:,1])), np.mean((sample_gs[:,1])))
		#print("range x", np.max((sample_obj[:,0])), np.max((sample_gs[:,0]) ), np.min((sample_obj[:,0])), np.min((sample_gs[:,0])) )
		#print("range y", np.max((sample_obj[:,1])), np.max((sample_gs[:,1]) ), np.min((sample_obj[:,1])), np.min((sample_gs[:,1])) )
		# print("range z", np.max((sample_obj[:,2])), np.max((sample_gs[:,2]) ), np.min((sample_obj[:,2])), np.min((sample_gs[:,2])) )
	return spatial_results

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--start_idx', type=int, default=0, 
					help='start scene you want to train.')
	parser.add_argument('--end_idx', type=int, default=-1,
						help='end scene you want to end')
	parser.add_argument('--draw', action='store_true',
						help='end scene you want to end')
	parser.add_argument('--all', action='store_true',
						help='end scene you want to end')
	parser.add_argument('--subset', action='store_true',
						help='eval some of them')
	parser.add_argument('--type', type=int, default=0,
						help='eval some of them')
	args = parser.parse_args()


	# example dict
	shapenet_gaussian_example_dict = {}
	shapenet_gaussian_example_dict['name'] = "ShapeNetCore.v1 Gaussian"
	shapenet_gaussian_example_dict['description'] = "Training Gaussian Splatting on ShapeNet PointCLoud Dataset"
	shapenet_gaussian_example_dict['reference'] = "TODO"
	shapenet_gaussian_example_dict['license'] = "TODO"
	shapenet_gaussian_example_dict['release'] = "TODO"
	shapenet_gaussian_example_dict['labels'] = "TODO"
	shapenet_gaussian_example_dict['numTraining'] = "TODO"
	shapenet_gaussian_example_dict['numTest'] = "TODO"
	shapenet_gaussian_example_dict['file_ending'] = ".ply"

	blender_renders_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render/'

	with open('../shapnetv1_output.json', 'r') as f:
		shapenet_v1_dict = json.load(f)

	obj_total_path = []
	for cat_id in shapenet_v1_dict.keys():
		for id_num, obj_id in enumerate(shapenet_v1_dict[cat_id]):
			if args.subset or args.type==2:
				if id_num % 1000 == 0:
					obj_total_path.append(os.path.join(blender_renders_path, cat_id, obj_id))
			else:
				obj_total_path.append(os.path.join(blender_renders_path, cat_id, obj_id))
			

	if args.end_idx > len(obj_total_path) or args.end_idx == -1 :
		args.end_idx = len(obj_total_path) 

	save_name = f'shapnetv1_gaussian_{args.start_idx}_{args.end_idx}.json'
	obj_total_path = obj_total_path[args.start_idx:args.end_idx]

	shapenet_v1_dict_gs = {}



	# '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/blender_render/'
	# blender_render_org_gs
	object_id_list_missing = []
	count = 0

	for obj_path in tqdm(obj_total_path):
		obj_folder = obj_path
		if args.type==1:
			gs_folder = obj_path.replace('render', 'blender_render')
		elif args.type == 2:
			gs_folder = obj_path.replace('render', 'blender_render_org_gs')
		else:
			gs_folder = obj_path
		obj_id = obj_path.split('/')[-1]
		cat_id =  obj_path.split('/')[-2]
		if cat_id not in shapenet_v1_dict_gs.keys():
			shapenet_v1_dict_gs[cat_id] = []
		pointcloud_gs = os.path.join(gs_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply')
		# num_align_gs = os.path.join(obj_folder,'light_gs' ,'point_cloud' ,'iteration_30000', 'point_cloud.ply')

		obj_path = os.path.join(obj_folder, 'point_cloud.obj')
		# if not os.path.exists(obj_path):
		# 	obj_path = os.path.join('/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/blender_render/', cat_id, obj_id,'point_cloud.obj')

		if os.path.exists(pointcloud_gs): #and os.path.exists(num_align_gs):
			metric_file = os.path.join(gs_folder,'light_gs', 'metric.csv')
			# open csv read metric, get last line
			with open(metric_file, 'r') as f:
				metric = f.read()
			metric_list = metric.split('\n')[-2]
			# print("metric_list", metric_list)
			iteration,split_set,l1_loss,psnr,ssim,lpips,file_size,elapsed,gaussian_nums = metric_list.split(',')
			# print("iteration", iteration)
			# print("split_set", split_set)
			# print("l1_loss", l1_loss)
			# print("psnr", psnr)
			# print("ssim", ssim)
			# print("lpips", lpips)
			# print("file_size", file_size)
			# print("elapsed", elapsed)
			# print("gaussian_nums", gaussian_nums)
			obj_i_metric_dict = {"obj_id": obj_id, "iteration": iteration, "l1_loss": l1_loss, "psnr": psnr, "ssim": ssim, "lpips": lpips, "file_size": file_size, "gaussian_nums": gaussian_nums}
			# 3D evalution
			pointcloud_gs = PlyData.read(pointcloud_gs)
			gs_xyz = np.stack(
				(
					np.asarray(pointcloud_gs.elements[0]["x"]),
					np.asarray(pointcloud_gs.elements[0]["y"]),
					np.asarray(pointcloud_gs.elements[0]["z"]),
				),
				axis=1,
			)
			# gs_xyz to object coordinate 
			# x axis unchange, y axis z, z axis -y
			gs_xyz_copy = gs_xyz.copy()
			gs_xyz[:,1] = gs_xyz_copy[:,2]
			gs_xyz[:,2] = -gs_xyz_copy[:,1]
	
			gaussian_num = len(gs_xyz)
			# fix seed generate same number by sampling

			mesh = trimesh.load(obj_path)
			num_points = gaussian_num
			# fix seed to make sure beloow reproduceable
			np.random.seed(0)
			random.seed(0)
			object_xyz, face_index = trimesh.sample.sample_surface(mesh, num_points)
			
			# calculate 3D metric
			# MMD
			spatial_results = calculate_spatial(object_xyz, gs_xyz, cat_id=cat_id, obj_id = obj_id, save = args.draw,  all_views=args.all)

			obj_i_metric_dict.update(spatial_results)
			shapenet_v1_dict_gs[cat_id].append(obj_i_metric_dict)
			# print("shapenet_v1_dict_gs", shapenet_v1_dict_gs)

		count+=1

		if count % 1000 == 0:
			# # save everytime finish one cat
			with open(save_name, 'w') as f:
				json.dump(shapenet_v1_dict_gs, f, indent=4)

	with open(save_name, 'w') as f:
		json.dump(shapenet_v1_dict_gs, f, indent=4)
	# print some results

	mmt_results = []
	psnr_results = []
	gaussin_num  =[]
	for cat_id in shapenet_v1_dict_gs.keys():
		for obj_i in shapenet_v1_dict_gs[cat_id]:
			mmt_results.append(obj_i['mmd_xz'])
			psnr_results.append(float(obj_i['psnr']))
			gaussin_num.append(float(obj_i['gaussian_nums']))

	print("mmt_results", np.mean(mmt_results))
	print("psnr", np.mean(psnr_results))
	print("gaussian_nums", np.mean(gaussin_num))

