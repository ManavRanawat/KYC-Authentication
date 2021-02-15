import cv2
import os

def prepImg(pth):
    return cv2.resize(pth,(96,96))

def crop_image(pth):
    print("PATH RECVD: ",pth)
    #dr = os.getcwd() 
    # print(dr)
    img = cv2.imread(pth)
    # print(img)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img,1.1,4)
    print(faces)
    (x,y,w,h) = faces[0]    
    ans = prepImg(img[y:y+h,x:x+w])
    png = r'users\face_img1.jpg'
    cv2.imwrite(png,ans)
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return png

#print(crop_image('jash2.jpeg'))