#directory config
reqFileDir = "require file"  #All document : register,key
imgDir ="imageInput"         #image of Answer

#-------  Question section config -------#
partDep = [0]*6
partDepHead = ["กลศาสตร์","ไฟฟ้า","คลื่น และ ความถนัดทางวิศวกรรม","สมบัติสาร","เคมี","คณิตศาสตร์"]
partDep[0] = "1-10,61-62"   #กลศาสตร์
partDep[1] = "11-18,63-64"  #ไฟฟ้า
partDep[2] = "19-20,51-60"  #คลื่น และ ความถนัดทางวิศวกรรม
partDep[3] = "21-29,65-66"  #สมบัติสาร
partDep[4] = "30-39,67-68"  #เคมี
partDep[5] = "40-50,69-70"  #คณิตศาสตร์

QuesPart = []
for e in partDep:
    tempLis = []
    for p in e.split(","):
        tempLis.append([int(q)  for q in p.split("-")])
    QuesPart.append(tempLis)

#-------  Image Processing config -------#
#Image Resize

width = 1067
height = 1535

#config_threshold
#decrease threshold for add darkness 
#increase threshold for add brightness
min_threshold = 235 #210 
max_threshold = 255 #255

minThreshBackRec = 215
maxThreshBackRec = 250

minThreshBackCir = 140
maxThreshBackCir = 160

rec_LB = 190
rec_UB = 600
