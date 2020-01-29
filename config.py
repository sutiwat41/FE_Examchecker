#directory config
reqFileDir = "require file"  #All document : register,key
imgDir ="imageInput"         #image of Answer
outputDir = "output file"
#------- Condition config -------#
checkZero = False   # True for detect Zero before Answer
fullScore = 300
#-------  Question section config -------#
partDep = [0]*7
partDepHead = ["กลศาสตร์","ไฟฟ้า","คลื่น","ความถนัดทางวิศวกรรม","สมบัติสาร","เคมี","คณิตศาสตร์"]
partDep[0] = "1-9,21,61-62"   #กลศาสตร์
partDep[1] = "10-16,63-64"  #ไฟฟ้า
partDep[2] = "17-20"  #คลื่น 
partDep[3] = "19-20,51-60"  #ความถนัดทางวิศวกรรม
partDep[4] = "22-28,65-67"  #สมบัติสาร
partDep[5] = "29-36"  #เคมี
partDep[6] = "37-48,69-70"  #คณิตศาสตร์
numPart = len(partDep)
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
min_threshold = 200 #210 
max_threshold = 210 #255

minThreshBackRec = 215  #215
maxThreshBackRec = 250  #250

minThreshBackCir = 140 #140
maxThreshBackCir = 160  #160

rec_LB = 190
rec_UB = 600
