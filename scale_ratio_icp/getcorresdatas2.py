import numpy as np
from corresponding import corresponding



def get_corres_datas2(input1, input2, oridata1, oridata2):

    if input1.shape[0] >= input2.shape[0]:
        # Find corresponding points
        result, ndists = corresponding(input2, input1)
        corresdata1 = []
        corresdata2 = []
        oricorresdata1 = []
        oricorresdata2 = []
        dist = 0

        for i in range(result.shape[1]):
            if ndists[1, i] > 0.6 * ndists[0, i]:
                corresdata2.append(input2[result[0, i], :])
                oricorresdata2.append(oridata2[result[0, i], :])
                corresdata1.append(input1[i, :])
                oricorresdata1.append(oridata1[i, :])
                dist += ndists[0, i]

    else:
        # Switch roles of input1 and input2
        result, ndists = corresponding(input1, input2)
        corresdata1 = []
        corresdata2 = []
        oricorresdata1 = []
        oricorresdata2 = []
        dist = 0

        for i in range(result.shape[1]):
            if ndists[1, i] > 0.6 * ndists[0, i]:
                corresdata1.append(input1[result[0, i], :])
                oricorresdata1.append(oridata1[result[0, i], :])
                corresdata2.append(input2[i, :])
                oricorresdata2.append(oridata2[i, :])
                dist += ndists[0, i]

    # Convert lists to numpy arrays
    corresdata1 = np.array(corresdata1)
    corresdata2 = np.array(corresdata2)
    oricorresdata1 = np.array(oricorresdata1)
    oricorresdata2 = np.array(oricorresdata2)

    return corresdata1, corresdata2, oricorresdata1, oricorresdata2, dist