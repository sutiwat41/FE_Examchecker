import pandas as pd 
raw_file = "reg.xlsx"
data_table = pd.read_excel(raw_file, index_col=0)
"""
for row in data_table.values:
	print(row)
	#if key == "รหัสประจำตัว":	print(data_table[key])
"""
headt = data_table.keys().values
for key in data_table.keys():
	
	if key == "รหัสประจำตัวสอบ":
		idlis = list()
		for cell in data_table[key]:
			datlen = len(str(cell))
			print(datlen,9-datlen)
			idlis.append("0"*(9-datlen)+str(cell) )
		data_table[key] = list(idlis) 
		idnew = list()
		for i in idlis:
			x = ""
			for j in i :
				x+=j+" "*2
			idnew.append(x)
		data_table["idnew"] = idnew


	elif str(key) in "0123456789" :
		tmplis = list()
		for i in idlis:

			y = ".  "
			for j in i:
				if j == str(key):	y += "●"#chr(152)
				else: y+=" "
			y+= " ."
			print(i,y)
			tmplis.append(y)
		data_table[key] = tmplis
with pd.ExcelWriter(raw_file,mode = "a") as writer:
	data_table.to_excel(writer)#,sheet_name='updated')
print("Complete")
#print(data_table)
