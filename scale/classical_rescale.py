
import open3d as o3d
import copy
import numpy as np


def rescale(source , target) :
    # Calculer les boîtes englobantes
    bbox1 = target.get_axis_aligned_bounding_box()
    bbox2 = source.get_axis_aligned_bounding_box()
   
    max_extent1 = max(bbox1.get_extent())  # Taille maximale du modèle 1
    max_extent2 = max(bbox2.get_extent())  # Taille maximale du modèle 2
    scale_factor = max_extent1 / max_extent2

    source.scale(scale_factor, center=bbox2.get_center())

    return source , target

def normalize(source , target) :
    
    bbox1 = source.get_axis_aligned_bounding_box()
    bbox2 = target.get_axis_aligned_bounding_box()

    scale1 = max(bbox1.get_extent())
    scale2 = max(bbox2.get_extent())

    source.scale(1.0 / scale1, center=bbox1.get_center())
    target.scale(1.0 / scale2, center=bbox2.get_center())
    return source , target