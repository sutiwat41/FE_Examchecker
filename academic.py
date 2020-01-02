from reqlib import* 
from config import*
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
            name = self.data[col].values[1]
            if name not in self.Examiner: 
                self.Examiner[name] = [col] 
            else: self.Examiner[name].append(col)

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

def grading(keyDict,ansDict):
    #return score for each question + sum score
    #return score for each part + sum score
    scoreDict = dict()
    scoreSumDict = dict()
    scoreSum = 0
    for id in ansDict.keys():
        outlist = [0]*70
        partsc  = [0]*6 
        for i in range(70):
            if keyDict[i+1].values[0] == "free":
                if i < 60: outlist[i] = 4
                else: outlist[i] = 6 
            elif str(ansDict[id][i]).strip() == "ไม่ตอบ"  or str(ansDict[id][i]).strip() in 'xXcCz-': 
                outlist[i] = 0
            elif float(ansDict[id][i]) == float(keyDict[i+1].values[0]):
                if i < 60: outlist[i] = 4
                else: outlist[i] = 6 
                
    for i,p in enumerate(QuesPart):
        for e in p:
            partsc[i] = sum(outlist[e[0]-1:e[1]])

    scoreSum = sum(outlist)
    scoreDict[id] = outlist+[scoreSum] 
    scoreSumDict[id] = partsc+[scoreSum]

    return scoreDict,scoreSumDict