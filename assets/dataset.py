#column sequence : operator, flightNo, source, depttime, dest, arrivaltime, days, stop 
import csv

data = []
source = ''
i = 0
with open('dataset_excel/csv/Vistara_ss16.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')	
	for line in reader:
		
		count = len(line)
		# print line
		if not line[3]:
			col = line[0].split(" ")
			source = col[1]
			
		else:
			row = []
			row.insert(0,line[3])
			row.insert(2,line[4])
			row.insert(3,line[7])
			row.insert(4,line[0])
			row.insert(5,line[8])
			row.insert(6,line[6])
			row.insert(7,line[9])
			row.insert(2,source)
			data.insert(i,row)
		
		
		

		

with open('dataset_excel/csv/output.csv', 'a') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar=" ", quoting=csv.QUOTE_MINIMAL)

	writer.writerow(["operator", "flightNo", "source", "depttime", "dest", "arrivaltime", "days", "stop"])

	for line in data:
		colStr = ""
		for col in line:	
			colStr = colStr + '"'+ col + '"' + ","
		colStr = colStr[:-1]	
		colStr = colStr
		# print colStr
		writer.writerow([colStr])
	# print data

