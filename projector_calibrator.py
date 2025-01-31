
import numpy as np
import cv2 as cv
from camera_calibrator import find_corners
from camera import Camera

class Projector :
    def __init__(self , projector_image):
        self.threedpoints = []
        self.twodpoints = []
        self.projector_image = cv.cvtColor(projector_image, cv.COLOR_BGR2GRAY) 
        self.k =None
        
    def calculate_obj_pts(self,projeted_img ,rvec,tvec,K) :
        grayColor = cv.cvtColor(projeted_img, cv.COLOR_BGR2GRAY) 
        corners = find_corners(grayColor,(9,9))
        # remove the last three corners
        corners = corners[:-3]
        cv.drawChessboardCorners(projeted_img, 
									(9,9), 
									corners, None) 
        cv.imshow('img', projeted_img)
        cv.waitKey(0) 
        if len(corners) > 0 :
            corners = corners.reshape(-1,2)
            corners = np.hstack((corners , np.ones((corners.shape[0],1)))).reshape(3,-1)
            H = self.__compute_homograph__(K,rvec,tvec)
            transformed_h = np.dot(np.linalg.inv(H), corners).T  
            transformed = transformed_h[:,:2] / transformed_h[:, 2:]  
            object_point = np.hstack((transformed, np.zeros((transformed.shape[0],1)))).astype(np.float32)
            self.threedpoints.append(object_point)

    def calcule_img_pts(self) :
        corners = find_corners(self.projector_image,(9,9))
        # remove the last three corners
        corners = corners[:-3]
        cv.drawChessboardCorners(self.projector_image,
                                    (9,9), 
                                    corners, None)
        cv.imshow('img', self.projector_image)
        cv.waitKey(0) 
        if len(corners) > 0 :
            self.twodpoints.append(corners.reshape(-1, 2))


    def calibrate_projector(self) :
        for i, (obj_pts, img_pts) in enumerate(zip(self.threedpoints, self.twodpoints)):
            print(f"Image {i}: 3D points shape: {obj_pts.shape}, 2D points shape: {img_pts.shape}")
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
    
def main() :
    cam = Camera((7,7))
    # open calibration.npz to load dist K and dist
    cam.k = np.load("calibration.npz")["K"]
    cam.dist = np.load("calibration.npz")["dist"]
    R, t = cam.find_extrinsic(cv.imread("images/damier.jpg"))
    R,t = R[0],t[0]

    proj = Projector(cv.imread("images/projector.jpg"))
    proj.calculate_obj_pts(cv.imread("images/projected.jpg"),R,t,cam.k)
    proj.calcule_img_pts()
    proj.calibrate_projector()
    print(proj.K)

main()