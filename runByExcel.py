from reg import *
from config import*
from academic import *
from detectAns import*



#------ set up file ------#

reg_file = reqFileDir+ "/reg_2020FEST.xlsx"
key_file = reqFileDir+ "/key_2020FEST.xlsx"
ans_xlsx_file = reqFileDir+"/answerfile.xlsx"
score_xlsx_file = outputDir+"/scoreFEST2020.xlsx"

#------ grant reg data ------#
regDa = Reg(reg_file)
regDa.grantData()

#-------  grant key -------#
keydf = Key(key_file)
keydf.grantData()

#------- grant answer -------#
AnsDict = dict()
ansexcel = pd.read_excel(ans_xlsx_file)
ans_col = ansexcel.columns.values
ind = list(ans_col).index('รหัสประจำตัวสอบ')
ind_1 = list(ans_col).index('ข้อที่ 1')
for i in ansexcel.get_values():
	AnsDict[i[ind]] = list(i[ind_1:ind_1+70])

#------- grading -------#
print("Grading :")
totalScore,totalScorePart = grading(keydf.data,AnsDict,True)
print("Grading Complete")

#------- Merge Data with Reg -------#
print("Merge Data with Reg :")

for id in tqdm(totalScore):
    if  id not in regDa.regData.keys():print(id)
    else:
        totalScore[id] = regDa.regData[id]+totalScore[id]
        totalScorePart[id] = regDa.regData[id]+totalScorePart[id]
print("Merge Complete")
#------- set up for Excel : Set up head -------#
showdict = dict()
showforreg = dict()

reghead = regDa.head
scorehead = [str(i) for i in range(1,71)] +['sum']
outhead = list(reghead)+ scorehead
outhead_forreg = list(reghead)+partDepHead+['sum','เปอร์เซ็นต์']

#------- set up for Excel : Convert dict to List -------#
tempLisSum = list()
tempLisPart = list()
for id in totalScore:
    tempLisSum.append([id]+totalScore[id])
    tempLisPart.append([id]+totalScorePart[id])



tempLisSum = np.array(tempLisSum)
tempLisPart = np.array(tempLisPart)


for i,col in enumerate(outhead): 
    #print(i,col)
    #print(tempLisSum[::,i])
    showdict[col] = tempLisSum[::,i]
for i,col in enumerate(outhead_forreg): showforreg[col] = tempLisPart[::,i]


lastreg = pd.DataFrame(showdict,columns=outhead_forreg )

last = pd.DataFrame.from_dict(showdict)
lastreg = pd.DataFrame.from_dict(showforreg)

#------- to Excel -------#
with pd.ExcelWriter(score_xlsx_file ,mode = "w") as writer:
	last.to_excel(writer,sheet_name='foracad')
	lastreg.to_excel(writer,sheet_name='forreg')
print("Complete")