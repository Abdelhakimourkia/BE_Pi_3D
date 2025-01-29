# Import required modules 
import cv2 
import numpy as np 
import os 
import glob 



CHECKERBOARD = (7, 7) 
criteria = (cv2.TERM_CRITERIA_EPS +
			cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) 
objectp3d = np.zeros((CHECKERBOARD[0] 
					* CHECKERBOARD[1], 
					3), np.float32) 
objectp3d[ :, :2] = np.mgrid[0:CHECKERBOARD[0], 
							0:CHECKERBOARD[1]].T.reshape(-1, 2) 



def find_corners(gray_img):
	ret, corners = cv2.findChessboardCorners( 
				gray_img, CHECKERBOARD, None)
	if ret == True: 
		corners2 = cv2.cornerSubPix( 
			gray_img, corners, (11, 11), (-1, -1), criteria) 
		return corners2
	return None



	



def calibrate_camera() :
	
	threedpoints = [] 
	
	twodpoints = [] 
	prev_img_shape = None

	images = glob.glob('images/*.jpg') 
	print("nb image" , len(images))
	for filename in images: 
		
		image = cv2.imread(filename) 
		grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
		ret, corners = cv2.findChessboardCorners( 
						grayColor, CHECKERBOARD, None)
		
		if ret == True: 
			
			threedpoints.append(objectp3d) 

			corners2 = cv2.cornerSubPix( 
				grayColor, corners, (11, 11), (-1, -1), criteria) 

			twodpoints.append(corners2) 
			cv2.drawChessboardCorners(image, 
									CHECKERBOARD, 
									corners2, ret) 

		cv2.imshow('img', image) 
		cv2.waitKey(0) 

	cv2.destroyAllWindows() 

	ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera( 
		threedpoints, twodpoints, grayColor.shape[::-1], None, None) 
	
	file_path = os.path.join(os.getcwd() , "calibration.npz")
	np.savez(file_path ,
		  K = matrix, 
		  dist = distortion
		  )
	return matrix ,distortion, r_vecs, t_vecs





def main() :
	matrix ,distortion, r_vecs, t_vecs = calibrate_camera()
	# Displaying required output 
	print(" Camera matrix:") 
	print(matrix) 

	print("\n Distortion coefficient:") 
	print(distortion) 

	print("\n Rotation Vectors:") 
	print(r_vecs )

	print("\n Translation Vectors:") 
	print(t_vecs) 

if __name__ == '__main__' :
	main()


