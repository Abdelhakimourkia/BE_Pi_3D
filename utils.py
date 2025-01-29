
import subprocess
import time
from tqdm import tqdm
import os
import open3d as o3d

def run_cpp_program_with_args(executable, args, progress_bar_duration):

    command = [executable] + args

    # Start the C++ executable with arguments
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

   
    with tqdm(total=progress_bar_duration, desc="Processing", unit="s") as pbar:
        elapsed_time = 0
        while process.poll() is None:  
            time.sleep(1)  
            elapsed_time += 1
            pbar.update(1)  

           
            if elapsed_time > progress_bar_duration:
                pbar.total = elapsed_time + 1
                pbar.refresh()

       
        pbar.n = pbar.total
        pbar.close()

    
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        print("\nProgram completed successfully.")
        print("Output:\n", stdout)
    else:
        print("\nProgram encountered an error.")
        print("Error:\n", stderr)


def save_ply_model_for_processing(pcd,pcd_path,output_dir,voxel_size) :
    pcd_down = pcd.voxel_down_sample(voxel_size)
    result_file =  build_path(pcd_path, output_dir)
    radius_normal = voxel_size * 2
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    o3d.io.write_point_cloud(result_file , pcd_down)
    return result_file

def build_path(pcd_path,output_dir) :
    pcd_file_name , extention =   os.path.basename(pcd_path).split(".")
    result_file =  os.path.join(output_dir ,pcd_file_name+"_processed." + extention)
    return result_file
    






