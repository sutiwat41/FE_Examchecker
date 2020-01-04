import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import*
from config import*
from modifydat import*

rec_list = list() #reference
cir_list = list()
Anscir_list = list()

fileName = "imageInput/"+"205-12-bug.jpg"
img = cv2.imread(fileName)
img = cv2.resize(img,(width,height),interpolation=cv2.INTER_AREA)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)

ret,thresh1 = cv2.threshold(gray ,min_threshold ,max_threshold ,cv2.THRESH_BINARY_INV)
kernel = np.ones((2,2),np.uint8)
#thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
erosion = cv2.erode(thresh1,kernel,iterations = 3)


img1,contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
img2,contours2, hierarchy2 = cv2.findContours(erosion.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

imgid = img1.copy()
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
            #print(cnt)
            #print("square , Area = ",area,"(x,y) =",(cx,cy))
            rec_list.append([cx,cy])#,area,perim])
            cv2.drawContours(imgcont,[cnt],0,(100,255,0),-1)
        elif 80000<area<100000: 
            cv2.drawContours(imgcont,[cnt],0,(100,255,0),5)
            tmpX = [ e[0][0] for e in approx]
            tmpY = [ e[0][1] for e in approx]
            startX,startY  = min(tmpX),min(tmpY)
            imgid = imgid[startY+34:max(tmpY),startX:max(tmpX) ]

    elif 5<=len(approx):
        area = cv2.contourArea(cnt)
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        circleArea = radius * radius * np.pi
        if 300 <=circleArea <= 800 :
  
            cx,cy,radius = int(cx),int(cy),int(radius)
            cir_list.append([cx,cy,area,radius])
            #print(total,area,radius)
            cv2.circle(imgcont, (cx, cy),radius, (50, 100, 0), 2)
            #cv2.drawContours(imgcont, [cnt], 0, (50,100,0), -1)

for cnt in contours2:
    approx = cv2.approxPolyDP(cnt, .035 * cv2.arcLength(cnt, True), True)        
    if 5<=len(approx):
        area = cv2.contourArea(cnt)
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        circleArea = radius * radius * np.pi
        #print(circleArea)
        if 200 <=circleArea <= 800 :
            cx,cy,radius = int(cx),int(cy),int(radius)
            cv2.circle(erosion, (cx, cy),radius, (50, 100, 0), 2)
            Anscir_list.append([cx,cy,area,radius])
cir_id_list = []
imgid,contours3, hierarchy3 = cv2.findContours(imgid.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours3:
    approx = cv2.approxPolyDP(cnt, .035 * cv2.arcLength(cnt, True), True)
    if 5<=len(approx):
        area = cv2.contourArea(cnt)
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        circleArea = radius * radius * np.pi
        #print("(cx,cy) = {:.3f},{:.3f} area = {:.3f} CirArea = {:.3f}".format(cx,cy,area,circleArea))
        if 300 <=circleArea <= 800 :
  
            cx,cy,radius = int(cx+startX),int(cy+startY),int(radius)
            cir_id_list.append([cx,cy,area,radius])
            cv2.circle(imgid, (cx-startX, cy-startY),radius, (50, 100, 0), 2)
            cv2.circle(imgcont, (cx, cy+34),radius, (50, 100, 0), 2)


#sort list ->
rec_list = sort_coor(rec_list)
cir_list = sort_coor(cir_list)
cir_id_list = sort_coor(cir_id_list)
Anscir_list = sort_coor(Anscir_list)
#print(rec_list)

#trans for id
coor_trans = [ [[-80,20]],[[-345,20]],[[-345,340]],[[-80,340]]]
coor = np.array(coor_trans)+np.array([[rec_list[0]]]*4,dtype = int)
#cv2.drawContours(imgcont, [coor], 0, (100,255,0), 5)
#cv2.drawContours(erosion, [coor], 0, (100,255,0), 5)


#trans for question 

coor_order = [2,5,3,6,1,4]
coor_trans_q= [[[-10,10]],[[-170,10]],[[-170,340]],[[-10,340]]]
#coor_q = np.array(coor_trans_q)+np.array([[rec_list[2]]]*4,dtype = int)
coor_q = list()
for j,e in enumerate(coor_order):
    coor_q.append(np.array(coor_trans_q)+np.array([[rec_list[e]]]*4,dtype = int))
    cv2.drawContours(imgcont, [coor_q[j]], 0, (160,255,0), 5)

id_list = list()
ans_list = [[] for e in range(6)]
studentAns = ['-']*61
id = [0]*9

for e in Anscir_list:
    if e[0] <= coor[0][0][0] and e[0] >= coor[1][0][0] and e[1] <= coor[2][0][1] and e[1] >= coor[1][0][1]:
        id_list.append(e)
    for i in range(len(coor_order)):    
        check = e[0] <= coor_q[i][0][0][0] and e[0] >= coor_q[i][1][0][0] and e[1] <= coor_q[i][2][0][1] and e[1] >= coor_q[i][1][0][1]
        if check:
            ans_list[i].append(e)


c = 0
ind = [0]*6
for i,e in enumerate(cir_id_list):
    if i+1 < len(cir_id_list):
        X,Y,R = e[:2]+[e[3]]
        CX,CY = cir_id_list[i+1][:2]
        if (X-CX)**2+(Y-CY)**2 <= R**2:
            cir_id_list.pop(i)
for e in cir_id_list:
    if e[0] <= coor[0][0][0] and e[0] >= coor[1][0][0] and e[1] <= coor[2][0][1] and e[1] >= coor[1][0][1]:
        #print(e)
        if len(id_list)!=0:
            x,y = id_list[0][:2]       
        cx, cy,radius = e[:2]+[e[3]]
        if (cx-x)**2+(cy-y)**2<= radius**2:
            cv2.circle(img, (cx, cy),radius, (0, 255, 0), 2)
            id[c%9] = str(c//9)
            id_list = id_list[1:]
        cv2.circle(imgcont, (cx, cy+34),radius, (50, 100, 0), 2)  
        c+=1


for e in cir_list:
    
    for i in range(len(coor_order)):  
        check = e[0] <= coor_q[i][0][0][0] and e[0] >= coor_q[i][1][0][0] and e[1] <= coor_q[i][2][0][1] and e[1] >= coor_q[i][1][0][1]
        if check:
            if len(ans_list[i])!=0:
                x,y = ans_list[i][0][:2]
            else:
                #print(i,ans_list[i])
                continue
      
            cx, cy,radius = e[:2]+[e[3]]
            if (cx-x)**2+(cy-y)**2<= radius**2:
                cv2.circle(img, (cx, cy),radius, (0, 0, 255), 2)

                if studentAns[i*10+ind[i]//5+1] == '-':
                    studentAns[i*10+ind[i]//5+1] = str(ind[i]%5+1)
                else: 
                    studentAns[i*10+ind[i]//5+1] ='X'
                    print("Bug : double choose at",i*10+ind[i]//5+1)
                #dequeue
                ans_list[i] = ans_list[i][1:]
            ind[i]+=1

#print(id)
#id = "".join(id)
print("id :",id)
print(studentAns)

plt.figure(1)
plt.imshow(imgcont)

plt.figure(2)
#plt.imshow(erosion)
plt.imshow(imgid)
plt.figure(3)
plt.imshow(img)
plt.show()  