import numpy as np

def set_boundary(dataset1, dataset2, dataset3):

    oridata1 = dataset1.copy()
    oridata2 = dataset2.copy()

    newdata1 = dataset1.copy()
    newdata2 = dataset3.copy()

    
    v = []
    for i in range(newdata1.shape[0] - 1, 0, -1):
        if (newdata1[i, 0] - newdata2[-1, 0] > 1e-10 and
                newdata1[i - 1, 0] - newdata2[-1, 0] >= 1e-10):
            v.append(i)
    newdata1 = np.delete(newdata1, v, axis=0)
    oridata1 = np.delete(oridata1, v, axis=0)

    # Process newdata2
    v = []
    for i in range(newdata2.shape[0] - 1, 0, -1):
        if (newdata2[i, 0] - newdata1[-1, 0] > 1e-10 and
                newdata2[i - 1, 0] - newdata1[-1, 0] >= 1e-10):
            v.append(i)
    newdata2 = np.delete(newdata2, v, axis=0)
    oridata2 = np.delete(oridata2, v, axis=0)

    # Remove elements from newdata2 at the start
    v = []
    for i in range(newdata2.shape[0] - 1):
        if (newdata2[i, 0] - newdata1[0, 0] < -1e-10 and newdata2[i + 1, 0] - newdata1[0, 0] <= -1e-10):
            v.append(i)
            
    newdata2 = np.delete(newdata2, v, axis=0)
    oridata2 = np.delete(oridata2, v, axis=0)

    # Remove elements from newdata1 at the start
    v = []
    for i in range(newdata1.shape[0] - 1):
        if (newdata1[i, 0] - newdata2[0, 0] < -1e-10 and
                newdata1[i + 1, 0] - newdata2[0, 0] <= -1e-10):
            v.append(i)
    newdata1 = np.delete(newdata1, v, axis=0)
    oridata1 = np.delete(oridata1, v, axis=0)

    # Check ratio and adjust datasets if necessary
    if newdata1.shape[0] / dataset1.shape[0] <= 0.5:
        oridata1 = dataset1.copy()
        oridata2 = dataset2 * 100

        return_dataset1 = dataset1 * 1000
        return_dataset2 = dataset3
        return return_dataset1, return_dataset2, oridata1, oridata2

    return newdata1, newdata2, oridata1, oridata2