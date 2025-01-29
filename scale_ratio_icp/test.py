from scale_ratio_icp import scale_ratio_icp
import open3d as o3d 

#file1 = "data/dense_processed.ply.cdw"
#file2 ="data/exemple1_processed.ply.cdw"
#model1 = o3d.io.read_point_cloud("data/dense_processed.ply")    
#model2 =  o3d.io.read_point_cloud("data/exemple1_processed.ply") 


file1 = "/Users/abdelhakimourkia/Desktop/Aourkia/BE_PI3D/ScaleRatioICP/ContributionRateGeneration/data/pointoneseg.ply.cdw"
file2 ="/Users/abdelhakimourkia/Desktop/Aourkia/BE_PI3D/ScaleRatioICP/ContributionRateGeneration/data/pointtwoseg.ply.cdw"

model1 = o3d.io.read_point_cloud("data/pointoneseg.ply")    
model2 =  o3d.io.read_point_cloud("data/pointtwoseg.ply") 

o3d.visualization.draw_geometries([model1, model2])

t,_ = scale_ratio_icp(file1, file2, 400)
print(t)
model2.scale(t, center= model2.get_center())
o3d.visualization.draw_geometries([model1, model2])