
import open3d   as o3d
import os 
import sys
from getopt import getopt
import numpy as np 

def subdiv_pointcloud(point_cloud, subdiv):
    bounding_box = point_cloud.get_oriented_bounding_box()
    extent = np.max(bounding_box.get_max_bound() - bounding_box.get_min_bound())
    voxel_size = extent/subdiv
    return voxel_size


def save_ply_model(filepath ,  d) :
    pcd = o3d.io.read_point_cloud(filepath)
    voxel_size = subdiv_pointcloud(pcd, d)
    pcd_down = pcd.voxel_down_sample(voxel_size)
    radius_normal = voxel_size * 2
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    path = os.path.basename(filepath).split(".")
    result_file ="data/" +path[0]  + "_processed.ply" 
    o3d.io.write_point_cloud(result_file , pcd_down)

def main() :
    opts, args = getopt(sys.argv[1:],'f1:f2:d',['f1=','f2=' ])
    
    for arg in opts : 
        filename = arg[1]
        print (filename)
        save_ply_model(filename , int(args[0]))

if __name__ == "__main__" :
    main()