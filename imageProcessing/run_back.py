import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import*
from config import*
from modifydat import*

file_name = "imageInput/"+"Document 16_5.jpg"

img = cv2.imread(file_name)
img = cv2.resize(img,(width,height),interpolation=cv2.INTER_AREA)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(gray, minThreshBackRec,maxThreshBackRec,cv2.THRESH_BINARY_INV)
ret2,thresh2 = cv2.threshold(gray, minThreshBackCir,maxThreshBackCir,cv2.THRESH_BINARY_INV)
kernel = np.ones((1,1),np.uint8)
kernel2 = np.ones((2,2),np.uint8)

#blur = cv2.GaussianBlur(thresh2,(3,3),0)
thresh2 = cv2.morphologyEx(thresh2, cv2.MORPH_OPEN, kernel)
thresh2 = cv2.erode(thresh2,kernel,iterations = 5)
erosion = cv2.erode(thresh2,kernel2,iterations = 5)


img1,contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
img2,contours2, hierarchy2 = cv2.findContours(thresh2.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
img3,contours3, hierarchy3 = cv2.findContours(erosion, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

rec_list = list() #reference
cir_list = list()

imgcont = img1.copy()
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, .035 * cv2.arcLength(cnt, True), True)
    #print(len(approx))
    if len(approx)==4:
        area = cv2.contourArea(cnt)
        perim = cv2.arcLength(cnt,True)
        #print(area)
        if 50000 <= area <= 60000:
            M = cv2.moments(cnt) 
            cx = round(M["m10"] / M["m00"],3)
            cy = round(M["m01"] / M["m00"],3)
            tempApprox = [list(e[0]) for e in approx]
            
            indM,Min = 0,10000000
            indM_2,Min_2 = 0,""
            for j,e in enumerate(tempApprox):
                if e[1] == Min:indM_2,Min_2 = j,Min 
                if e[1] < Min:
                    indM_2,Min_2 = indM,Min 
                    indM,Min = j,e[1]
                if Min < e[1] < Min_2 : indM_2,Min_2 = j,e[1]
            #print(tempApprox)
            #print(indM,Min,indM_2,Min_2)
            approx[indM][0][1] +=50 
            approx[indM_2][0][1] +=50 
            
            rec_list.append([cx,cy,approx])
            cv2.drawContours(imgcont,[approx],0,(100,255,0),5)
            #cv2.drawContours(erosion,[approx],0,(100,255,0),5)
cir_list_temp = [[] for e in range(10)]
rec_list = sort_coor(rec_list)
recBound = [e[2] for e in rec_list ]
for cnt in contours2:
    approx = cv2.approxPolyDP(cnt, .035 * cv2.arcLength(cnt, True), True)
    if 5<=len(approx):
        area = cv2.contourArea(cnt)
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        circleArea = radius * radius * np.pi
       # print("(cx,cy) = {:.3f},{:.3f} area = {:.3f} CirArea = {:.3f}".format(cx,cy,area,circleArea))
        if 240 <=circleArea <= 400 :
           # print(circleArea)
            cx,cy,radius = int(cx),int(cy),int(radius)
            for j,e in enumerate(recBound):
                dist = cv2.pointPolygonTest(e,(cx,cy),True)
                if dist >= 0 :
                    cir_list_temp[j].append([cx,cy,area,radius])
                    cv2.circle(thresh2, (cx, cy),radius, (100, 255, 0), 2)
            cir_list.append([cx,cy,area,radius])
            #cv2.circle(thresh2, (cx, cy),radius, (100, 255, 0), 2)
#print([len(e) for e in cir_list_temp])


cir_list = sort_coor(cir_list)

Anscir_list = [[] for e in range(10)]
#print(len(cir_list))
for cnt in contours3:
    approx = cv2.approxPolyDP(cnt, .035 * cv2.arcLength(cnt, True), True)
    if 5<=len(approx):
        area = cv2.contourArea(cnt)
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        circleArea = radius * radius * np.pi
        #print("(cx,cy) = {:.3f},{:.3f} area = {:.3f} CirArea = {:.3f}".format(cx,cy,area,circleArea))
        if 100 <=circleArea <= 200 :
            #print(circleArea)
            cx,cy,radius = int(cx),int(cy),int(radius)
            
            for j,e in enumerate(recBound):
                dist = cv2.pointPolygonTest(e,(cx,cy),True)
                if dist >= 0:
                    Anscir_list[j].append([cx,cy,area,radius])
                    #cv2.circle(erosion, (cx, cy),radius, (100, 255, 0), 2)
                    break
for j in range(10): 
    cir_list_temp[j] = sort_coor(cir_list_temp[j])
    for i,e in enumerate(cir_list_temp[j]):
        if i+1 < len(cir_list_temp[j]):
            X,Y,R = e[:2]+[e[3]]
            CX,CY = cir_list_temp[j][i+1][:2]
            if (X-CX)**2+(Y-CY)**2 <= R**2:
                cir_list_temp[j].pop(i+1)
    Anscir_list[j] = sort_coor(Anscir_list[j])
#print([len(e) for e in cir_list_temp])
ans_list = list(Anscir_list)
ind = [0]*10
studentAnsWrite = [["-"]*6 for e in range(10)] 
#print(cir_list_temp[0])
for i in range(10):
    for cir in cir_list_temp[i]:
        cx, cy,radius = cir[:2]+[cir[3]]
        dist = cv2.pointPolygonTest(recBound[i],(cx,cy),True)
        if dist >= 0:
            #cv2.circle(thresh2,(cx, cy),radius, (100, 255, 0), -1)
            #print(cx,cy,radius,i,ind[i])
            if len(ans_list[i])!=0: x,y = ans_list[i][0][:2]
            else:continue       
            if (cx-x)**2+(cy-y)**2<= radius**2:
                #cv2.circle(thresh2, (cx, cy),radius, (50, 50, 0), 2)
                #print(ind[i],ind[i]//6,ind[i]%6)
                if studentAnsWrite[i][ind[i]%6] == '-':
                    studentAnsWrite[i][ind[i]%6] = str(ind[i]//6)
                else: 
                    studentAnsWrite[i][ind[i]%6] ='X'
                    print("Bug : double choose at")
                ans_list[i] = ans_list[i][1:]
            ind[i]+=1
            #break
ans = ["".join(studentAnsWrite[e][:4]+["."]+studentAnsWrite[e][4:]) for e in range(10)]
#realAns = "".join(ans)
print(ans)
plt.figure(1)
plt.imshow(imgcont)

plt.figure(2)
plt.imshow(thresh2)

#plt.figure(3)
#plt.imshow(erosion)
plt.show()