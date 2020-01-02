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
