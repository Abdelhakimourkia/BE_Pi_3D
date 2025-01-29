import cv2 as cv
import os 
cap = cv.VideoCapture(0) 
import glob


images = glob.glob('images/*.jpg') 

if images :
    for img in images :
        os.remove(img)



ind = 1
while True :
    suc,img =  cap.read()
    
    cv.imshow("calibrate_img" , img)
    key = cv.waitKey(1)
    if key == ord("q") :
        break
    if key == ord("a") :
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        file = os.path.join("images",f"image_{ind}.jpg")
        cv.imwrite(filename=file , img= gray)
        print("saved")
        ind +=1