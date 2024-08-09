import json
import numpy as np
from camera_pose_visualizer import CameraPoseVisualizer
import matplotlib.pyplot as plt
import os 

if __name__ == '__main__':
    org_cam_poses_c2w = []
    visualizer = CameraPoseVisualizer([-1, 1], [-1, 1], [-1, 1])
    transform_path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/blender_render/02691156/10155655850468db78d106ce0a280f87/transforms_train.json'
    # '/cluster/work/cvl/qimaqi/3dv_gaussian/ShapenetRender_more_variation/transforms_train.json'
    with open(transform_path) as json_file:
        contents = json.load(json_file)

        fovx = contents["camera_angle_x"]

        frames = contents["frames"]
  
 
        for idx, frame in enumerate(frames):
     
            # NeRF 'transform_matrix' is a camera-to-world transform
            c2w = np.array(frame["transform_matrix"])
            # change from OpenGL/Blender camera axes (Y up, Z back) to COLMAP (Y down, Z forward)
            c2w[:3, 1:3] *= -1
            org_cam_poses_c2w.append(c2w)
                    

    K = np.array([[500.0, 0, 640, 0],[0, 500.0, 360, 0], [0,0,1, 0],[0,0, 0,1]])
    img_size = np.array([400,400]) # W, H

    org_cam_poses_c2w = np.array(org_cam_poses_c2w)
    for index, frame_i in enumerate(org_cam_poses_c2w):
        visualizer.extrinsic2pyramid(frame_i, plt.cm.rainbow(index / len(org_cam_poses_c2w)), 0.2)

    visualizer.show()

    # import matplotlib.pyplot as plt
    # plt.plot(org_cam_poses_c2w[:,0,-1], org_cam_poses_c2w[:,1,-1])
    # plt.show()
