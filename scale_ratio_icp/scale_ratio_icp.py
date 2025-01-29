import numpy as np
from find_dt import find_dt
from calcostfunction import calcostfunction2
from tqdm import tqdm



def scale_ratio_icp(file1, file2, iter_num):
    """
    Perform Scale Ratio Iterative Closest Point (ICP) algorithm.

    Args:
        file1 (str): Path to the first dataset file.
        file2 (str): Path to the second dataset file.
        iter_num (int): Number of iterations to perform.

    Returns:
        None
    """
    print("Calculation begin!")
    
    # Load datasets
    cdw1 = np.loadtxt(file1)
    cdw2 = np.loadtxt(file2)
    
    # Remove rows with near-constant values
    cdw1 = cdw1[np.sum(np.abs(cdw1[:, 1:] - 1), axis=1) >= 1e-1]
    cdw2 = cdw2[np.sum(np.abs(cdw2[:, 1:] - 1), axis=1) >= 1e-1]

    # Initialize delta t
    init_t = []
    if cdw1[0, 0] / cdw2[0, 0] >= 1:
        for i in np.arange(1, 10.1, 0.1):  # i is delta t
            costresult = calcostfunction2(cdw1, cdw2, i, 1)
            init_t.append([i, costresult])
    else:
        for i in np.arange(0, 1.01, 0.01):  # i is delta t
            costresult = calcostfunction2(cdw1, cdw2, i, 1)
            init_t.append([i, costresult])

    init_t = np.array(init_t)

    # Find the minimum value of initial delta t
    value, ind = np.min(init_t[:, 1]), np.argmin(init_t[:, 1])
    initt = init_t[ind, 0]
    init_value = init_t[ind, 1]

    # Scale Ratio ICP iteration
    iteration = iter_num
    eps = 1e-3
    dtnewicp = 1
    final_ratio = initt

    for i in tqdm(range(1, iteration + 1)):
        dtnewicp, dist = find_dt(cdw1, cdw2, final_ratio)
        final_ratio = dtnewicp

        if abs(dtnewicp + 1) < 1e-10:
            print("New dt is -1, system exit!")
            return

        print(f"Iter {i}\tInitial t is: {initt:.3f}.")
        print(f"\tNew delta t is: {dtnewicp:.3f}.")

    print(f"Final Ratio t is: {final_ratio:.3f}")
    print("Calculation finish!")
    return final_ratio, initt