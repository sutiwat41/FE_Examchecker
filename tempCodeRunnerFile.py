tempAnsDict = ansexcel
tempAnsDict=tempAnsDict.set_index('รหัสประจำตัวสอบ')
idTemp = list(tempAnsDict.index)
tempAnsDict = tempAnsDict.to_numpy()

for v,id in enumerate(idTemp):
    AnsDict[id] = list(tempAnsDict[v][ind_1+1:])