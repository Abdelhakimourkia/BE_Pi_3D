import numpy as np
from set_boundary import set_boundary
from getcorresdatas1 import get_corres_datas1


def calcostfunction2(dataset1, dataset2, dt, state):
    """
    Calculate the cost function.

    Args:
        dataset1 (ndarray): Dataset 1, shape (m, d), where `m` is the number of rows and `d` is the number of dimensions.
        dataset2 (ndarray): Dataset 2, shape (n, d), where `n` is the number of rows and `d` is the number of dimensions.
        dt (float): Delta t scaling factor.
        state (int): State parameter (used for optional scaling).

    Returns:
        float: Calculated cost function value.
    """
    # Apply delta t to the first column of dataset2
    dataset2prim = dataset2.copy()
    dataset2prim[:, 0] *= dt

    # Find boundary data
    newdata1, newdata2, oridata1, oridata2 = set_boundary(dataset1, dataset2, dataset2prim)

    # If datasets are too small, return a large cost
    if newdata1.shape[0] <= 1 or newdata2.shape[0] <= 1:
        return 1e+10

    # Find corresponded datasets
    corresdata1, corresdata2, oricorresdata1, oricorresdata2, dist = get_corres_datas1(newdata1, newdata2, oridata1, oridata2)

    # Return the distance as the cost
    return dist

    # Optional detailed calculation (commented out in MATLAB code)
    # Uncomment and implement if needed:
    # sumresult = 0
    # for i in range(len(oricorresdata1)):
    #     for j in range(1, corresdata1.shape[1]):  # Exclude the first column
    #         sumresult += (
    #             (oricorresdata2[i, j] - oricorresdata1[i, j]) ** 2
    #             + (state * oricorresdata2[i, 0] - state * oricorresdata1[i, 0]) ** 2
    #         )
    # return sumresult