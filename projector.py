
import numpy as np
import cv2 as cv
from camera_calibrator import find_corners

class Projector :
    def __init__(self , projector_image):
        self.threedpoints = []
        self.twodpoints = []
        self.projector_image = cv.cvtColor(projector_image, cv.COLOR_BGR2GRAY) 
        self.k =None
        
    def calculate_obj_pts(self,projeted_img ,rvec,tvec,K) :
        grayColor = cv.cvtColor(projeted_img, cv.COLOR_BGR2GRAY) 
        corners = find_corners(grayColor)
        if corners :
            corners = corners.reshape(-1,2)
            corners = np.hstack((corners , np.ones(corners.shape[0],1))).reshape(3,-1)
            H = self.__compute_homography__(K,rvec,tvec)
            transformed_h = np.dot(np.linalg.inv(H), corners).T  
            transformed = transformed_h[:,:2] / transformed_h[:, 2:]  
            object_point = np.hstack((transformed, np.zeros((transformed.shape[0],1))))
            self.threedpoints.append(object_point)

    def calcule_img_pts(self) :
        corners = find_corners(self.projector_image)
        if corners :
            self.twodpoints.append(corners)


    def calibrate_projector(self) :
        _, matrix, _, _, _ = cv.calibrateCamera(self.threedpoints, 
                                                self.twodpoints, 
                                                self.projector_image.shape[::-1],
                                                None,
                                                None) 
        self.K = matrix

    

    def __compute_homograph__(self,K, rvec, tvec):
        R, _ = cv.Rodrigues(rvec)
        t = tvec.reshape(-1, 1)
        R_partial = R[:, :2]  
        Rt = np.hstack((R_partial, t))  
        H = np.dot(K, Rt)
        return H






















