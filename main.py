from reg import *
from config import*
from academic import *
from detectAns import*
from tqdm import tqdm
import os

#------ set up file ------#

reg_file = reqFileDir+ "/reg.xlsx"
key_file = reqFileDir+ "/key.xlsx"
ans_xlsx_file = outputDir+"/readFile_3321.xlsx"

#------ grant reg data ------#
regDa = Reg(reg_file)

#-------  grant key -------#
keydf = Key(key_file)
keydf.grantData()


#------- grant answer -------#

bugFile = set()
TmpAnsDict = dict()
print("Reading Front...")
for img in tqdm(os.listdir(imgDir+"/front")):
    file_path = imgDir+"/front/"+img
    classID = img[img.find("-")+1:]
    try:
        ans = frontDetect(file_path,False)
        TmpAnsDict[classID] = [ans["id"]]+ans["ans"]        
    except:
        print("Bug : Front(Crash)",classID) 
        bugFile.add(classID)
"""
print("Reading Back...")
for img in tqdm(os.listdir(imgDir+"/back")):
    file_path = imgDir+"/back/"+img
    classID = img[img.find("-")+1:]
    if classID in bugFile or classID not in TmpAnsDict: continue
    try:
        ans = backDetect(file_path,False)
        if "Bug" in ans:
            TmpAnsDict[classID] += ['*']*10    
        else  :TmpAnsDict[classID] += ans
    except :
        TmpAnsDict[classID] += [0]*10
        bugFile.add(classID)
        print("Bug : Back(Crash)",classID)
        """
#------- Merge front back -------#
AnsDict = dict()
AnsList = list()
for e in TmpAnsDict:
    AnsList.append([e]+TmpAnsDict[e])
    AnsDict[TmpAnsDict[e][0]] = TmpAnsDict[e][1:]
    
#print(AnsDict)
print(bugFile,len(bugFile))
#------- to excel file : Ans to excel -------#
AnsToExcel = pd.DataFrame(AnsList,columns = ["file name","id"] + [e+1 for e in range(60)])
print(AnsToExcel)
lastDat = pd.DataFrame.from_dict(AnsToExcel)
with pd.ExcelWriter(ans_xlsx_file,mode = "w") as writer:
	lastDat.to_excel(writer,sheet_name='input')
#------- Check Answer  -------#
"""
totalScore,totalScoreSum = grading(keydf.data,AnsDict,False)
print(totalScore)
print(totalScoreSum)"""
#------- to excel file -------#