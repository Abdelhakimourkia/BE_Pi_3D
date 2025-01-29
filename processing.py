import open3d as o3d
import copy
import numpy as np
from sklearn.neighbors import NearestNeighbors


def subdiv_pointcloud(point_cloud, subdiv):
    bounding_box = point_cloud.get_oriented_bounding_box()
    extent = np.max(bounding_box.get_max_bound() - bounding_box.get_min_bound())
    voxel_size = extent/subdiv
    return voxel_size



def pick_points(pcd):
    print("")
    print(
        "1) Please pick at least three correspondences using [shift + left click]"
    )
    print("   Press [shift + right click] to undo point picking")
    print("2) After picking points, press 'Q' to close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  
    vis.destroy_window()
    print("")
    return vis.get_picked_points()





def edit_geometry(geometry):
    #geometry.compute_vertex_normals()
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(geometry)
    vis.run()  
    vis.destroy_window()
    edited = vis.get_cropped_geometry()
    l, ind = edited.remove_statistical_outlier(nb_neighbors=20,
                                                    std_ratio=1.0)
    inlier_cloud = edited.select_by_index(ind)
    return inlier_cloud



def read_point_cloud(file_path) :
    source= o3d.io.read_point_cloud(file_path)
    l, ind = source.remove_statistical_outlier(nb_neighbors=30,
                                                        std_ratio=1.0)
    return source.select_by_index(ind)


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])


def preprocess_point_cloud(pcd, voxel_size):
    
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2

    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5

    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


def prepare_dataset(source,target,voxel_size):
    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh



def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5

    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    
    return result



def execute_fast_global_registration(source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.5

    result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
    return result


def refine_registration(source, target, result, voxel_size):
    distance_threshold = voxel_size * 0.4
    result = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, result.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    return result
