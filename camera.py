import numpy as np
import cv2 
from camera_calibrator import find_corners


class Camera :
    def __init__(self ,CHECKERBOARD):  

        self.threedpoints = [] 
        self.twodpoints = [] 
        self.k
        self.dist
        self._CHECKERBOARD = CHECKERBOARD
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) 
        self.__create_obj_points__()

    def __create_obj_points__(self) :
        self.objectp3d = np.zeros((self.CHECKERBOARD[0] 
					* self.CHECKERBOARD[1], 
					3), np.float32) 
        self.objectp3d[ :, :2] = np.mgrid[0:self.CHECKERBOARD[0], 
                                    0:self.CHECKERBOARD[1]].T.reshape(-1, 2) 


    def process_img(self, image, draw = False) :
        self.img_shape = image.shape[::-1]

        
        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        ret, corners = cv2.findChessboardCorners( 
                        grayColor, self.CHECKERBOARD, None)
        
        if ret == True: 
            
            self.threedpoints.append(self.objectp3d) 

            corners2 = cv2.cornerSubPix( 
                grayColor, corners, (11, 11), (-1, -1), self.criteria) 

            self.twodpoints.append(corners2) 
            if draw :
                cv2.drawChessboardCorners(image, 
                                        self.CHECKERBOARD, 
                                        corners2, ret) 
                cv2.imshow('img', image) 
                cv2.waitKey(0)


    def calibrate_camera(self) :
        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera( self.threedpoints, 
                                                                self.twodpoints, 
                                                                self.img_shape, 
                                                                None, None) 
        self.k = matrix
        self.dist = distortion


    def find_extrinsic(self,image) :
        threedpoints = [] 
        twodpoints = [] 
        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        corners = find_corners(grayColor)
        if corners :
            twodpoints.append(corners) 
            threedpoints.append(self.objectp3d) 
            ret, _, _, r_vecs, t_vecs = cv2.calibrateCamera( threedpoints, twodpoints, grayColor.shape[::-1],cameraMatrix=self.K, distCoeffs=self.dist ) 
            return  r_vecs, t_vecs
        return None
             
           

		        


    
