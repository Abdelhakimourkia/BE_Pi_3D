import open3d as o3d
import copy
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import distance_matrix



def estimate_scale_using_mesh_resolution(source , target,scale_source,scale_target) :
    source_down = source.voxel_down_sample(scale_source)
    target_down =  target.voxel_down_sample(scale_target)
    source_points = np.asarray(source_down.points)
    target_points = np.asarray(target_down.points)
    source_distances = compute_mesh_resolution(source_points)
    target_distances = compute_mesh_resolution(target_points)
    return  target_distances / source_distances , source_distances,target_distances


def compute_mesh_resolution(points):
    dists = distance_matrix(points, points)
    return np.median(dists[dists > 0])