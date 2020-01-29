import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import*
from config import*
from modifydat import*

def frontDetect(fileName,display):
    #fileName (image) | display -> image :True, False
    #return  id , Ans 1 - 60

    rec_list = list() #reference
    cir_list = list()
    Anscir_list = list()

    #---------- read image ----------#
    img = cv2.imread(fileName)
    img = cv2.resize(img,(width,height),interpolation=cv2.INTER_AREA)

    #---------- set up image ----------#
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret,thresh1 = cv2.threshold(gray ,min_threshold ,max_threshold ,cv2.THRESH_BINARY_INV)
    kernel = np.ones((2,2),np.uint8)

    erosion = cv2.erode(thresh1,kernel,iterations = 3)

    #---------- find contour ----------#
    img1,contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    img2,contours2, hierarchy2 = cv2.findContours(erosion.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    imgid = img1.copy()
    imgcont = img1.copy()
    startX,startY  = 0,0
    #---------- find contour : rectangle and circle ----------#
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, .035 * cv2.arcLength(cnt, True), True)
        if len(approx)==4:
            area = cv2.contourArea(cnt)
            perim = cv2.arcLength(cnt,True)
            x,y,w,h = cv2.boundingRect(approx)
            if rec_LB <= area <= rec_UB and perim/area<=1:
                M = cv2.moments(cnt) 
                cx = round(M["m10"] / M["m00"],3)
                cy = round(M["m01"] / M["m00"],3)

                rec_list.append([cx,cy])#,area,perim])
                cv2.drawContours(imgcont,[cnt],0,(100,255,0),-1)
            elif 70000<area<110000 and w < h :  
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
                cv2.circle(imgcont, (cx, cy),radius, (50, 100, 0), 2)

    #---------- find contour : chosen circle ----------#
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

    #---------- find contour : find id circle ----------#
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
                #cv2.circle(imgid, (cx-startX, cy-startY),radius, (50, 100, 0), 2)
                #cv2.circle(imgcont, (cx, cy+34),radius, (50, 100, 0), 2)

    
    #---------- Sort Coordinate : top-left ----------#
    rec_list = sort_coor(rec_list)
    cir_list = sort_coor(cir_list)
    Anscir_list = sort_coor(Anscir_list)
    cir_id_list = sort_coor(cir_id_list)

    
    #---------- Set Boundry : For read ID ----------#
    coor_trans = [ [[-80,20]],[[-345,20]],[[-345,340]],[[-80,340]]]
    coor = np.array(coor_trans)+np.array([[rec_list[0]]]*4,dtype = int)


    #---------- Set Boundry : For read Answer of Question ----------#
    coor_order = [2,5,3,6,1,4]
    coor_trans_q= [[[-10,10]],[[-160,10]],[[-160,330]],[[-10,330]]]
    coor_q = list()
    for j,e in enumerate(coor_order):
        coor_q.append(np.array(coor_trans_q)+np.array([[rec_list[e]]]*4,dtype = int))
        #cv2.drawContours(imgcont, [coor_q[j]], 0, (160,255,0), 5)

    
    id_list = list()
    ans_list = [[] for e in range(6)]
    studentAns = ['-']*60
    id = ['*']*9
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

                    if studentAns[i*10+ind[i]//5] == '-':
                        studentAns[i*10+ind[i]//5] = str(ind[i]%5+1)
                    else: 
                        studentAns[i*10+ind[i]//5] ='X'

                    #dequeue
                    ans_list[i] = ans_list[i][1:]
                ind[i]+=1
    #print(id,studentAns)
    #print(id)
    
    id = "".join(id)
    return {"id":id,"ans":studentAns}


def backDetect(fileName,display):
    img = cv2.imread(fileName)
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
            if 80 <=circleArea <= 250 :
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

    #---------- Detect circle number  ----------#
    for e in cir_list_temp:
        if len(e) != 60:
            return "Bug : Circle less than 60 for Part2"

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
                        #print("Bug : double choose at",i)
                    ans_list[i] = ans_list[i][1:]
                ind[i]+=1
                #break
    ans = ["".join(studentAnsWrite[e][:4]+["."]+studentAnsWrite[e][4:]) for e in range(10)]
    return ans