import open3d as o3d
import numpy as np
import copy

from sklearn.decomposition import PCA
from scipy.spatial import distance_matrix
from tqdm import tqdm


def compute_descriptors(point_cloud, scale):
    radius_feature = scale * 5
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        point_cloud,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return fpfh


def pca_and_contribution_rate(spin_image_matrix) :
    pca = PCA()
    pca.fit(spin_image_matrix)
    eigenvalues = np.expand_dims(pca.explained_variance_,1)
    cumulative_rates = np.cumsum(eigenvalues) / np.sum(eigenvalues)
    # pca.components_  (m*m , m*m)  pour un w on a   0<= d <= m*m -1 d represent les lignes
    # cumulative_rates (m*m,1)  pour chaque  0<= d <= m*m -1  d represent les colonnes et donc on a pour chaque d c_d_w 
    # pour un w fixe
    return pca.components_  , cumulative_rates 

def c_wi(point_cloud ,w) :
    # cumulative_rates (m*m,1)  pour chaque  0<= d <= m*m -1  d represent les colonnes et donc on a pour chaque d c_d_w 
    # pour un w fixe
    fpfh = compute_descriptors(point_cloud,w).data
    spin_image_matrix = np.asarray(fpfh).T
    _ , c_w = pca_and_contribution_rate(spin_image_matrix)
    print(c_w.shape)
    return c_w #(m*m,1) 


def curves_c_w (point_cloud,w_range) :
    print("#######################################################################")
    print(" calculting curves:  ")
    # dim de sortie est (m*m , len(w_range)) c_a_d d en ligne et i en colonne
    resultat = np.stack([c_wi(point_cloud ,w)  for w in tqdm(w_range, total=len(w_range))], axis= 1)
    print(resultat.shape)

    return resultat

def initialize_scale_ratio(source,target , wmesh1, wmesh2, steps=100):
    tm1 = wmesh1
    tm2 = wmesh2
    w_range1 = np.linspace(tm1, 1000 * tm1, steps)
    w_range2 = np.linspace(tm2, 1000 * tm2, steps)
    
    t_candidates = np.linspace(0.01, 100 * tm2 / tm1, steps)
    #(d , i)
    print("#######################################################################")
    print("processig of a point cloud : 1")
    curves1 =  curves_c_w (source,w_range1)
    print(curves1.shape)
    print("#######################################################################")
    print("processig of a point cloud : 2")
    curves2 =  curves_c_w (target ,w_range2)
    print(curves2.shape)


    min_error = float('inf')
    t_init = None
    print("#######################################################################")
    print(" An exhaustive search is used to find an initial rough estimate of t : ")
    for t in tqdm(t_candidates,total= len(t_candidates) ):
        error = 0
        #pour d fixe 
        diff1 = curves2 -curves1
        diff2 = w_range2 - w_range2
        obj =  (diff1)**2  + (diff2**2)
        error = np.sum(np.sum(obj , axis= 1), axis= 0)
        if error < min_error:
            min_error = error
            t_init = t
    
    return t_init , curves1 , curves2 , w_range1, w_range2


def find_correspondences(curves1, curves2, w_range1, w_range2, t) :
    # Scale w_range1 using the current t
    w_aligned = t * w_range1
    correspondences_matrix = np.empty((curves1.shape[0] ,w_range2.shape[0] ))

    for d in range(curves1.shape[0]):
        vec1 = np.stack([curves1[d, :], w_aligned], axis=1)
        vec2 = np.stack([curves2[d, :], w_range2], axis=1)
        print(vec1.shape)
        dist = distance_matrix(vec1, vec2)
        correspondences_matrix[d, :] = np.argmin(dist, axis=1).astype(int).T
    print(correspondences_matrix.shape)
    return correspondences_matrix





def update_scale_ratio(correspondences_matrix, curves1, curves2, w_range1, w_range2):
    num_dims = curves1.shape[0]
    numerator = 0
    denominator = 0
    print(correspondences_matrix)
    for d in range(num_dims):
        for i in range(w_range1.shape[0]):
            idx = correspondences_matrix[d, i]
            numerator += w_range1[i] * w_range2[idx]
            denominator += w_range1[i] ** 2
    t_new = numerator / denominator
    return t_new


def minimize_scale_ratio(source,target, wmesh1, wmesh2, steps=100, tol=1e-6, max_iter=100):
    # Initialisation
    t, curves1, curves2, w_range1, w_range2 = initialize_scale_ratio(source,target, wmesh1, wmesh2, steps)
    prev_t = 0
    iteration = 0
    
    print("#######################################################################")
    print(" Minimizing scale ratio t using Scale Ratio ICP:")
    
    while abs(t - prev_t) > tol and iteration < max_iter:
        iteration += 1
        # Trouver les correspondances actuelles
        correspondences = find_correspondences(curves1, curves2, w_range1, w_range2, t)
        # Mettre à jour t
        prev_t = t
        t = update_scale_ratio(correspondences, curves1, curves2, w_range1, w_range2)
        
        print(f"Iteration {iteration}: t = {t}, change = {abs(t - prev_t)}")
    
    if iteration == max_iter:
        print("Warning: Maximum iterations reached without convergence.")
    
    print("Final estimated scale ratio:", t)
    return t