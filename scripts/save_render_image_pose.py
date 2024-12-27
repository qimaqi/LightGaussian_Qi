import os 
import json 
from glob import glob
import zipfile
from tqdm import tqdm
import shutil 

render_save_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/render/'
render_tgt_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/render_blender_format/'
# go through all the cat id
move_file = True 
if move_file:
    for cat_id in tqdm(os.listdir(render_save_path)):
        if os.path.isdir(os.path.join(render_save_path, cat_id)):
            # go through all the model id
            for model_id in os.listdir( os.path.join(render_save_path, cat_id)):
                if os.path.isdir(os.path.join(render_save_path, cat_id, model_id)):
                    # go through all the render image
                    image_save_path = os.path.join(render_save_path, cat_id, model_id, 'image.zip')
                    train_split_json = os.path.join(render_save_path, cat_id, model_id, 'transforms_train.json')
                    test_split_json = os.path.join(render_save_path, cat_id, model_id, 'transforms_test.json')
                    val_split_json = os.path.join(render_save_path, cat_id, model_id, 'transforms_val.json')
                    
                    if os.path.exists(image_save_path) and os.path.exists(train_split_json) and os.path.exists(test_split_json) and os.path.exists(val_split_json):
                        # move the image to the corresponding folder
                        # create the folder with cat name
                        new_cat_folder = os.path.join(render_tgt_path, cat_id)
                        if not os.path.exists(new_cat_folder):
                            os.makedirs(new_cat_folder)
                        # create the folder with model name
                        new_model_folder = os.path.join(new_cat_folder, model_id)
                        if not os.path.exists(new_model_folder):
                            os.makedirs(new_model_folder)
                        # move the image to the new folder
                        # print(f"move {image_save_path} to {new_model_folder}")
                        shutil.move(image_save_path, new_model_folder)
                        # move the json file to the new folder
                        shutil.move(train_split_json, new_model_folder)
                        shutil.move(test_split_json, new_model_folder)
                        shutil.move(val_split_json, new_model_folder)
