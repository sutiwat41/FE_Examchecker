from reg import *
from config import*
from academic import Key

#------ set up file ------#

reg_file = reqFileDir+ "/reg.xlsx"
key_file = reqFileDir+ "/key.xlsx"
ans_xlsx_file = ""

#------ grant reg data ------#
regDa = Reg(reg_file)

#-------  grant key -------#
keydf = Key(key_file)
keydf.grantData()


#------- grant answer -------#
"""
ansdict = dict()
ansexcel = pd.read_excel(ans_xlsx_file)
ans_col = ansexcel.columns.values

ind = list(ans_col).index('รหัสประจำตัวสอบ')
ind_1 = list(ans_col).index('ข้อที่ 1')
for i in ansexcel.get_values(): ansdict[i[ind]] = list(i[ind_1:ind_1+70]) """