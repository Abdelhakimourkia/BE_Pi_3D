import numpy as np
from set_boundary import set_boundary
from getcorresdatas2 import get_corres_datas2




def find_dt(dataset1, dataset2, dt):
    """
    Calculate the updated delta t (dt) based on two datasets.

    Args:
        dataset1 (numpy.ndarray): Dataset 1 with columns [w, cwd].
        dataset2 (numpy.ndarray): Dataset 2 with columns [w, cwd].
        dt (float): Initial delta t value.

    Returns:
        dtnew (float): Updated delta t. Returns -1 if no valid data is found.
        dist (float): Distance between corresponding datasets.
    """
    # Adjust dataset2 with the current dt
    dataset2prim = dataset2.copy()
    dataset2prim[:, 0] *= dt

    # Find boundary datasets
    newdata1, newdata2, oridata1, oridata2 = set_boundary(dataset1, dataset2, dataset2prim)

    # Check for valid data size
    if newdata1.shape[0] <= 1 or newdata2.shape[0] <= 1:
        return -1, None

    # Find corresponding datasets
    corresdata1, corresdata2, oricorresdata1, oricorresdata2, dist = get_corres_datas2(newdata1, newdata2, oridata1, oridata2)

    # Compute the numerator and denominator for the updated dt
    dtnew_d = 0
    dtnew_n = 0
    for i in range(oricorresdata1.shape[0]):
        dtnew_d += oricorresdata1[i, 0] * oricorresdata2[i, 0]
        dtnew_n += oricorresdata2[i, 0] ** 2

    # Calculate the updated dt
    dtnew = dtnew_d / dtnew_n if dtnew_n != 0 else -1

    return dtnew, dist