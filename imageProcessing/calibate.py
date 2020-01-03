import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import*
from config import*
from modifydat import*

file_name = "research/"+"calibate__12.jpg"

img = cv2.imread(file_name)

img = cv2.resize(img,(width,height),interpolation=cv2.INTER_AREA)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray ,min_threshold,max_threshold,cv2.THRESH_BINARY_INV)
kernel = np.ones((2,2),np.uint8)
thresh1 = thresh
#thresh1 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
erosion = cv2.erode(thresh1,kernel,iterations = 3)


img1,contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
img2,contours2, hierarchy2 = cv2.findContours(erosion.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

rec_list = list() #reference
cir_list = list()

imgcont = img1.copy()
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, .035 * cv2.arcLength(cnt, True), True)
    #print(len(approx),end=" ")
    if len(approx)==4:
        area = cv2.contourArea(cnt)
        perim = cv2.arcLength(cnt,True)
        if rec_LB <= area <= rec_UB and perim/area<=1:
            M = cv2.moments(cnt) 
            cx = round(M["m10"] / M["m00"],3)
            cy = round(M["m01"] / M["m00"],3)

            rec_list.append([cx,cy])
            cv2.drawContours(imgcont,[cnt],0,(100,255,0),-1)
        
    elif 5<=len(approx):
        area = cv2.contourArea(cnt)
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        circleArea = radius * radius * np.pi
        #print("(cx,cy) = {:.3f},{:.3f} area = {:.3f} CirArea = {:.3f}".format(cx,cy,area,circleArea))
        if 300 <=circleArea <= 800 :
  
            cx,cy,radius = int(cx),int(cy),int(radius)
            cir_list.append([cx,cy,area,radius])
            #print(total,area,radius)
            cv2.circle(imgcont, (cx, cy),radius, (50, 100, 0), 2)
            #cv2.drawContours(imgcont, [cnt], 0, (50,100,0), -1)

plt.figure(1)
plt.imshow(imgcont)

#plt.figure(2)
#plt.imshow(erosion)

plt.figure(3)
plt.imshow(thresh)
plt.show()