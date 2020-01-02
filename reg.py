from reqlib import*
class Reg:
    #Data from reg
    def __init__(self,file):
        self.filename = file #.xlsx file only
        #self.head = ['รหัสประจำตัวสอบ','คำนำหน้า','ชื่อ','นามสกุล','ห้อง','เลขที่นั่งสอบ','โรงเรียน']
        self.head = []
        self.regData = dict() 
        self.absent = []


    def grantData(self):
        #grant all Data from file
        rawData = pd.read_excel(self.filename)
        self.head = rawData.columns.values
        
        #create regData -> key : student id 
        #                 item : Reg Data 
        for col in rawData.values:
            self.regData[col[0]] = list(col[1:])