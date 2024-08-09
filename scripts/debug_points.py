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


path = '/cluster/work/cvl/qimaqi/ws_dataset/shapenet/ShapeNetCore.v1/render/03636649/273314626729b1e973222d877df1ecac/point_cloud.obj'
mesh = trimesh.load(path)
num_points = 5000
points, face_index = trimesh.sample.sample_surface(mesh, num_points)
face_normals = mesh.face_normals
# Retrieve the normals for the sampled points based on face index
sampled_normals = face_normals[face_index]
mesh.visual = mesh.visual.to_color()
vertex_colors = mesh.visual.vertex_colors[:, :3]  # Ignore the alpha channel
sampled_colors = np.zeros((num_points, 3))

for i in range(num_points):
    # Get the indices of the vertices of the face
    face_vertices = mesh.faces[face_index[i]]
    # Get the vertex coordinates and their corresponding colors
    vertices = mesh.vertices[face_vertices]
    colors = vertex_colors[face_vertices]

    # Compute barycentric coordinates
    v0 = vertices[1] - vertices[0]
    v1 = vertices[2] - vertices[0]
    v2 = points[i] - vertices[0]
    d00 = np.dot(v0, v0)
    d01 = np.dot(v0, v1)
    d11 = np.dot(v1, v1)
    d20 = np.dot(v2, v0)
    d21 = np.dot(v2, v1)
    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    # Interpolate color using barycentric coordinates
    sampled_colors[i] = u * colors[0] + v * colors[1] + w * colors[2]
positions = points
colors = sampled_colors
normals = sampled_normals
positions = np.array(positions)
colors = np.array(colors)
print("colors", colors.min(), colors.max())
normals = np.array(normals)

# save to ply with trimesh
ply_filename = './debug_points.ply'
trimesh.points.PointCloud(vertices=positions, colors=colors, normals=normals).export(ply_filename)
