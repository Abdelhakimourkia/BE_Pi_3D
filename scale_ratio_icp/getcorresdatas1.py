import numpy as np
from corresponding import corresponding



def get_corres_datas1(input1, input2, oridata1, oridata2):

    # Call the corresponding function
    result, ndists = corresponding(input1, input2)

    corresdata1 = []
    corresdata2 = []
    oricorresdata1 = []
    oricorresdata2 = []
    dist = 0

    threshold = (np.max(ndists[0, :]) - np.min(ndists[0, :])) * 0.88

    for i in range(result.shape[1]):
        corresdata1.append(input1[result[0, i], :])
        corresdata2.append(input2[i, :])
        oricorresdata1.append(oridata1[result[0, i], :])
        oricorresdata2.append(oridata2[i, :])
        dist += ndists[0, i]

    # Convert lists to numpy arrays
    corresdata1 = np.array(corresdata1)
    corresdata2 = np.array(corresdata2)
    oricorresdata1 = np.array(oricorresdata1)
    oricorresdata2 = np.array(oricorresdata2)

    return corresdata1, corresdata2, oricorresdata1, oricorresdata2, dist