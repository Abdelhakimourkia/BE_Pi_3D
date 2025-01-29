from app import ConfigurationWindow 
import open3d as o3d
import numpy as np
import copy
from processing import *
import tkinter as tk
from tkinter import messagebox
import subprocess
from scale.classical_rescale import *
from scale.fpfh_rescale import *
from scale.mesh_resolution_rescale import *
from scale.ransac_rescale import *
import sys
import os
from utils import *
sys.path.append('/Users/abdelhakimourkia/Desktop/Aourkia/BE_PI3D/scale_ratio_icp')
from scale_ratio_icp.scale_ratio_icp import scale_ratio_icp
voxel_size = 0.08
import shutil

def main() :
    root = tk.Tk()
 
    app = ConfigurationWindow(root )
    root.mainloop()
    source = o3d.io.read_point_cloud(app.source_model_path)
    source = edit_geometry(source)
    target = o3d.io.read_point_cloud(app.target_model_path)
    target = edit_geometry(target)
    o3d.visualization.draw_geometries([source, target])

    methode  = app.scale.get()
    if methode == "manuel":
        print("ok")
        messagebox.showinfo(title="Information" , message="""1) Please pick at least three correspondences using [shift + left click] \n
                                                            2) Press [shift + right click] to undo point picking \n
                                                            3) After picking points, press 'Q' to close the window""")
        
        print("Select corresponding points in the source model.")
        picked_points_source = pick_points(source)

        print("Select corresponding points in the target model.")
        picked_points_target = pick_points(target)

        if len(picked_points_source) != len(picked_points_target):
            messagebox.showerror("error" , message="The number of selected points must be the same for source and target.")
            raise ValueError("The number of selected points must be the same for source and target.")
        
        key_points_source = np.asarray(source.points)[picked_points_source,:]
        key_points_target = np.asarray(target.points)[picked_points_target,:]

        dist_source = calcule_mean_distance(key_points_source)
        dist_target = calcule_mean_distance(key_points_target)
        scale_factor = dist_target / dist_source
        print(f"Computed scale factor: {scale_factor}")
    else :

        scale_source = subdiv_pointcloud(source, 100)
        scale_target = subdiv_pointcloud(target , 100)

        if methode == "mesh resolution" :
            scale_factor ,_,_=  estimate_scale_using_mesh_resolution(source ,target, scale_source,scale_target)
        elif methode == "ransac matching" :
            scale_factor = estimate_scale_using_ransac(source ,target, scale_source,scale_target)
        elif methode == "scale ratio icp" :
                dir_path = "./output"

                
                os.makedirs(dir_path, exist_ok=True)
                source_file =  save_ply_model_for_processing(source ,app.source_model_path ,dir_path,scale_source)
                target_file =  save_ply_model_for_processing(target ,app.target_model_path ,dir_path,scale_target)
                 
                   # source_file = build_path(app.source_model_path , dir_path)
                    #arget_file =  build_path(app.target_model_path , dir_path)

                cpp_executable = "/Users/abdelhakimourkia/Desktop/Aourkia/BE_PI3D/ScaleRatioICP/ContributionRateGeneration/build/scalesextract" 
                cpp_args = [source_file, target_file , '12'] 
                progress_bar_duration = 10  
                run_cpp_program_with_args(cpp_executable, cpp_args, progress_bar_duration)
                scale_factor,_= scale_ratio_icp(target_file +".cdw", source_file+".cdw", 100) 
                shutil.rmtree(dir_path)

    print(f"Computed scale factor: {scale_factor}")
    # Scale the source to match the target
    source.scale(scale_factor, center=source.get_center())
    o3d.visualization.draw_geometries([source, target])
    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(source , target,voxel_size)
    result = execute_global_registration(source_down, target_down, source_fpfh,
                                        target_fpfh, voxel_size)

    result = refine_registration(source, target, result, voxel_size)

    draw_registration_result(source, target,result.transformation)

            

if __name__ == "__main__":
    main()