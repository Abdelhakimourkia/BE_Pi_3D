import numpy as np
from tqdm import tqdm
from sklearn.decomposition import PCA
from scipy.spatial import distance_matrix

def compute_spin_image(point, normal, points, bin_size, image_width):
    vecs = point - points
    betas = np.sum(normal * vecs,axis=1)
    dist = np.linalg.norm(vecs , axis=1)

    alphas = np.sqrt(dist**2 - betas**2)
    valid_indices = np.where( (np.abs(betas) <= image_width)  & (alphas <= image_width) )[0]
    alphas = alphas[valid_indices]
    betas = betas[valid_indices]

    num_bins = int( image_width / bin_size)  
    spin_image = np.zeros((num_bins, num_bins))
    
    alpha_bins = np.floor((alphas) / bin_size).astype(int)
    beta_bins = np.floor((-betas + (image_width/2)) / bin_size).astype(int)
    
    for i , j in zip(beta_bins, alpha_bins):
        if 0 <= i < num_bins and 0 <= j < num_bins:
            spin_image[i, j] += 1

    return spin_image


def point_cloud_spin_images(points , normals,bin_size,image_width) :
    print("#######################################################################")
    print(" calculting spin_image feature descriptor for a point cloud:  ")
    num_bins = int(2 * image_width / bin_size)  
    spin_image_matrix = np.empty((points.shape[0],num_bins**2))
    for i, (pt, normal) in tqdm(enumerate(zip(points, normals)), total=points.shape[0]):
        spin_image = compute_spin_image(pt, normal, points, bin_size, image_width)
        spin_image_matrix[i, :] = spin_image.flatten()  
    print("spin Image : " , spin_image_matrix.shape)
    return spin_image_matrix


def pca_and_contribution_rate(spin_image_matrix) :
    pca = PCA()
    pca.fit(spin_image_matrix)
    eigenvalues = np.expand_dims(pca.explained_variance_,1)
    cumulative_rates = np.cumsum(eigenvalues) / np.sum(eigenvalues)
    # pca.components_  (m*m , m*m)  pour un w on a   0<= d <= m*m -1 d represent les lignes
    # cumulative_rates (m*m,1)  pour chaque  0<= d <= m*m -1  d represent les colonnes et donc on a pour chaque d c_d_w 
    # pour un w fixe
    return pca.components_  , cumulative_rates 

def c_wi(points , normals ,bin_size ,w) :
    # cumulative_rates (m*m,1)  pour chaque  0<= d <= m*m -1  d represent les colonnes et donc on a pour chaque d c_d_w 
    # pour un w fixe
    spin_image_matrix = point_cloud_spin_images(points , normals,bin_size,w)
    _ , c_w =pca_and_contribution_rate(spin_image_matrix)
    return c_w #(m*m,1) 

def curves_c_w (points , normals ,bin_size,w_range) :
    # dim de sortie est (m*m , len(w_range)) c_a_d d en ligne et i en colonne
    return np.stack([c_wi(points , normals ,bin_size ,w)  for w in w_range], axis= 1)

def initialize_scale_ratio(points1,points2 , normals1,normals2 ,bin_size, wmesh1, wmesh2, steps=100):
    tm1 = wmesh1
    tm2 = wmesh2
    w_range1 = np.linspace(tm1, 1000 * tm1, steps)
    w_range2 = np.linspace(tm2, 1000 * tm2, steps)
    print(len(w_range1))
    t_candidates = np.linspace(0.01, 100 * tm2 / tm1, steps)
    #(d , i)
    print("#######################################################################")
    print("processig of a point cloud : 1")
    curves1 =  curves_c_w (points1 , normals1 ,bin_size,w_range1)
    print("#######################################################################")
    print("processig of a point cloud : 2")
    curves2 =  curves_c_w (points2 , normals2 ,bin_size,w_range2)
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
        vec1 = np.stack([curves1[d, :], w_aligned], axis=-1)
        vec2 = np.stack([curves2[d, :], w_range2], axis=-1)
        dist = distance_matrix(vec1, vec2)
        correspondences_matrix[d, :] = np.argmin(dist, axis=1)
    return correspondences_matrix





def update_scale_ratio(correspondences_matrix, curves1, curves2, w_range1, w_range2):
    num_dims = curves1.shape[0]
    numerator = 0
    denominator = 0
    for d in range(num_dims):
        for i in range(w_range1.shape[0]):
            idx = correspondences_matrix[d, i]
            numerator += w_range1[i] * w_range2[idx]
            denominator += w_range1[i] ** 2
    t_new = numerator / denominator
    return t_new


def minimize_scale_ratio(points1, points2, normals1, normals2, bin_size, wmesh1, wmesh2, steps=100, tol=1e-6, max_iter=100):
    # Initialisation
    t, curves1, curves2, w_range1, w_range2 = initialize_scale_ratio(points1, points2, normals1, normals2, bin_size, wmesh1, wmesh2, steps)
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
    







