from scale_ratio_icp import scale_ratio_icp
import open3d as o3d 
import numpy as np
file1 = "/Users/abdelhakimourkia/Desktop/Aourkia/BE_PI3D/scale_ratio_icp/data/pointoneseg.ply.cdw"
file2 ="/Users/abdelhakimourkia/Desktop/Aourkia/BE_PI3D/scale_ratio_icp/data/pointtwoseg.ply.cdw"
import matplotlib.pyplot as plt
"""
model1 = o3d.io.read_point_cloud("data/dense.ply")    
model2 =  o3d.io.read_point_cloud("data/exemple1.ply") 



o3d.visualization.draw_geometries([model1, model2])

t = scale_ratio_icp(file1, file2, 400)
#print(t)
model2.scale(t, center= model2.get_center())
o3d.visualization.draw_geometries([model1, model2])"""

mat1 = np.loadtxt(file1)
mat2 = np.loadtxt(file2)
dims1 =       np.arange(1,mat1.shape[1])       
dims2 = mat2.shape[1] -1

plt.figure()
