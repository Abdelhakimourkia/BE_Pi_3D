import numpy as np

def corresponding(input1, input2):

    result = []
    ndists = []

    for i in range(input2.shape[0]):
        minnum = float('inf')
        subminnum = float('inf')
        minind = -1
        subminind = -1

        for j in range(input1.shape[0]):
            tmpnum = np.linalg.norm(input1[j, :] - input2[i, :])
            
            if tmpnum < minnum:
                minnum = tmpnum
                minind = j
            elif minnum <= tmpnum < subminnum:
                subminnum = tmpnum
                subminind = j

        result.append([minind, subminind])
        ndists.append([minnum, subminnum])

    result = np.array(result).T  # Transpose to match (2, n)
    ndists = np.array(ndists).T  # Transpose to match (2, n)

    return result, ndists