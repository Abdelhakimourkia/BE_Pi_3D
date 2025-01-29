
import open3d as o3d
import copy
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import distance_matrix


def estimate_scale_using_ransac(source ,target, scale_source,scale_target) :
    source_down = source.voxel_down_sample(scale_source)
    target_down =  target.voxel_down_sample(scale_target)
    o3d.visualization.draw_geometries([source_down, target_down])
    source_fpfh = compute_descriptors(source_down,scale_source)
    target_fpfh = compute_descriptors(target_down, scale_target)
    ransac_result = ransac_matching(source_down, target_down,scale_source, scale_target)
    print(ransac_result.transformation)
    print(ransac_result.correspondence_set)
    correspondences = np.asarray(ransac_result.correspondence_set)
    source_points = np.asarray(source_down.points)[correspondences[:, 0]]
    target_points = np.asarray(target_down.points)[correspondences[:, 1]]
    source_distances = calcule_mean_distance(source_points)
    target_distances = calcule_mean_distance(target_points)

    return  target_distances / source_distances




def ransac_matching(source_cloud, target_cloud, scale_source, scale_target):
    source_fpfh = compute_descriptors(source_cloud, scale_source)
    target_fpfh = compute_descriptors(target_cloud, scale_target)
    distance_threshold_ransac = scale_target * 2
    result_ransac = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_cloud, target_cloud, source_fpfh, target_fpfh, True,
        distance_threshold_ransac,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        5, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold_ransac)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(400000, 0.999))
    return result_ransac


def compute_descriptors(point_cloud, scale):
    radius_normal = scale * 2
    point_cloud.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    radius_feature = scale * 5
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        point_cloud,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return fpfh


def calcule_mean_distance(key_points_source) :
    means = []
    for x in key_points_source :
        mean = np.mean(np.linalg.norm (x - key_points_source))
        means.append(mean)
    
    mean =  np.mean(np.array(means))
    return mean