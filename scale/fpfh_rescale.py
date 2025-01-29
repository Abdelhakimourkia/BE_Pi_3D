import open3d as o3d
import copy
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import distance_matrix


def estimate_scale_using_fpfh(source, target, scale_source, scale_target):

    source_down = source.voxel_down_sample(scale_source)
    target_down =  target.voxel_down_sample(scale_target)
    o3d.visualization.draw_geometries([source_down, target_down])
    source_fpfh = compute_descriptors(source_down,scale_source)
    target_fpfh = compute_descriptors(target_down, scale_target)

    distance_treashhold = 0.5
    source_features = np.asarray(source_fpfh.data).T
    target_features = np.asarray(target_fpfh.data).T

    nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(target_features)
    distances, indices = nbrs.kneighbors(source_features)
    
    distances =  distances[:,0]

    #filtred_indices =  np.where(distances > distance_treashhold)[0]

    #indices = indices[:, 0][filtred_indices]
    
    source_points = np.asarray(source_down.points)#[filtred_indices,:]
    target_points = np.asarray(target_down.points)[indices]
    print("len" , len(source_points))
    source_distances = calcule_mean_distance(source_points)
    target_distances = calcule_mean_distance(target_points)

    scale_factor = target_distances / source_distances

    return scale_factor


def calcule_mean_distance(key_points_source) :
    means = []
    for x in key_points_source :
        mean = np.mean(np.linalg.norm (x - key_points_source))
        means.append(mean)
    
    mean =  np.mean(np.array(means))
    return mean


def compute_descriptors(point_cloud, scale):
    radius_normal = scale * 2
    point_cloud.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    radius_feature = scale * 5
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        point_cloud,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return fpfh