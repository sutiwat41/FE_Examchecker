from reg import *
from config import*
from academic import Key
from detectAns import*
import os

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

for img in os.listdir(imgDir):
    file_path = imgDir+"/"+img
    if "front" in img:
        print(frontDetect(file_path,False))
    elif "back" in img:
        print(backDetect(file_path,False))