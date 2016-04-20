import csv

i = 0
with open('flight_dataset.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	row = ''
	for line in reader:
		if i == 0:
			# print line
			i = i + 1
		else:
			row += "('"+line[0] + "','" + line[1]+"','"+line[2] + "','" + line[3] + "','" + line[5] + "','" + line[4] + "','" +  line[6] + "','" +  line[7] + "'," + line[8] + "),\n"
			i + i + 1

# row = row[:-1]
# print row
row = '\n\n\nINSERT INTO flights (operator, operatorcode, flightno, source, destination, departuretime, arrivaltime, days, stop) values ' + row + ';'

with open("ir_project_database.sql", "a") as myfile:
    myfile.write(row)