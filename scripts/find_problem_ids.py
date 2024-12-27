import os 
import json 
from glob import glob


shapenet_all_json = '/cluster/work/cvl/qimaqi/3dv_gaussian/LightGaussian_Qi/shapnetv1_output.json'

with open(shapenet_all_json, 'r') as f:
    shapenet_all = json.load(f)


totad_ids = []
cat_ids = []
for cat_id in shapenet_all:
    for model_id in shapenet_all[cat_id]:
        totad_ids.append(model_id)
        cat_ids.append(cat_id)

# get unique ids
totad_ids = totad_ids
print(len(totad_ids))


# get output ids
output_root_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render/'
# valid_gs_ply_path = glob(os.path.join(output_root_path, '*', '*', 'light_gs', 'point_cloud', 'iteration_30000', 'point_cloud.ply'))
valid_gs_ply_pat_list = []

for cat_id in os.listdir(output_root_path):
    if os.path.isdir(os.path.join(output_root_path, cat_id)):
        for model_id in os.listdir( os.path.join(output_root_path, cat_id)):
            if os.path.isdir(os.path.join(output_root_path, cat_id, model_id)):
                valid_gs_ply_path = os.path.join(output_root_path, cat_id, model_id, 'light_gs', 'point_cloud', 'iteration_30000', 'point_cloud.ply')
                if os.path.exists(valid_gs_ply_path):
                    valid_gs_ply_pat_list.append(model_id)
                    # print("model_id", model_id)
                # else:
                #     print(valid_gs_ply_path, model_id)

# valid_id = [os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(p)))) for p in valid_gs_ply_path]

print(len(valid_gs_ply_pat_list))

for i, model_id in enumerate(totad_ids):
    if model_id not in valid_gs_ply_pat_list:
        print("missing", model_id, "cat_id", cat_ids[i])

# find the cat id of missing ids