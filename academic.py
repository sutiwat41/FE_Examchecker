from reqlib import* 
from config import*
from tqdm import tqdm
class Key:
    #key of exam
    def __init__(self,file):
        self.filename = file #.xlsx
        self.data = dict()
        self.Examiner = dict()
        self.val = dict()

    def grantData(self):
        # grant all key
        # creat Examiner : collect No. question 
        self.data = pd.read_excel(self.filename) 
        
        for col in self.data.columns:
            self.val[col] = self.data[col].values[0]
            """name = self.data[col].values[1]
            if name not in self.Examiner: 
                self.Examiner[name] = [col] 
            else: self.Examiner[name].append(col)"""

class Answer:
    #Answer of exam
    def __init__(self,file):
        self.filename = file #.xlsx
        self.ansDict = dict()

    def grantData(self):
        # grant all answer
        # creat Examiner : collect No. question 
        ansDf = pd.read_excel(self.filename)
        ans_col = ansDf.columns.values
        ind = list(ans_col).index('รหัสประจำตัวสอบ')
        ind_1 = list(ans_col).index('ข้อที่ 1')
        for i in ansDf.get_values():
	        self.ansDict[i[ind]] = list(i[ind_1:ind_1+70]) 

        return self.ansDict  

def grading(keyDict,ansDict,progressBar):
    #return score for each question + sum score
    #return score for each part + sum score
    scoreDict = dict()
    scorePartDict = dict()
    scoreSum = 0
    if progressBar: runDict = tqdm(ansDict.keys())
    else: runDict = ansDict.keys()
    for id in runDict:
        #print(id)
        nonBug =True
        outlist = [0]*70
        partsc  = [0]*numPart 
        for i in range(70):
            #print(ansDict[id][i],i)
            if i>=60:
                if checkZero:
                    if type(ansDict[id][i]) == "str" and "-" in ansDict[id][i] : 
                        ansDict[id][i] = "-"
                else:
                    if type(ansDict[id][i]) == "str":
                        ansDict[id][i] = ansDict[id][i].replace("-","0")
            if keyDict[i+1].values[0] == "free":
                if i < 60: outlist[i] = 4
                else: outlist[i] = 6 
            elif "ไม่" in str(ansDict[id][i]).strip() or str(ansDict[id][i]).strip() == "ไม่ตอบ"  or str(ansDict[id][i]).strip() in 'xXcCz-' or 'x' in str(ansDict[id][i]).lower(): 
                outlist[i] = 0
            elif '*' in str(ansDict[id][i]):
                nonBug = False
                break
            elif float(ansDict[id][i]) == float(keyDict[i+1].values[0]):
                if i < 60: outlist[i] = 4
                else: outlist[i] = 6 

        if nonBug:         
            for i,p in enumerate(QuesPart):
                for e in p:
                    if len(e) == 1 : partsc[i] += outlist[e[0]-1]
                    else: partsc[i] += sum(outlist[e[0]-1:e[1]])
            scoreSum = sum(outlist)
        else:
            scoreSum = "Bug"
            for i,p in enumerate(QuesPart):partsc[i] = "*"
        
        scoreDict[id] = outlist+[scoreSum] 
        scorePartDict[id] = partsc+[scoreSum,round(scoreSum/fullScore*100,2)]
        

    return scoreDict,scorePartDict