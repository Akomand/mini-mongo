import sys
import random
import fileinput
import csv
import operator


# GLOBAL VARIABLES
num_records = 500
record_size = 106
middle = 0

global f
global cf
global of

counter = 0
mergeCounter = 0
first = ''


# MAIN PROGRAM TO RUN
def main():
	global counter
	global f
	isOpen = False

	# PROMPT FOR DATABASE OPERATION
	while True:
		choice = int(input('''
		(1) CREATE
		(2) OPEN
		(3) CLOSE
		(4) DISPLAY
		(5) UPDATE
		(6) ADD
		(7) DELETE
		(8) CREATE REPORT
		(9) EXIT
		Enter an option (1 - 9): '''))

		# CREATE 
		if choice == 1:
			file = input('File name (eg. Fortune_500_HQ): ')
			createDatabase(file)
			print('DATABASE HAS BEEN CREATED')
			sys.exit(0)

		# OPEN
		if choice == 2:
			if not isOpen:
				openDatabase()
				print('DATABASE OPENED')
				isOpen = True
			else:
				print('CLOSE CURRENT DATABASE TO OPEN ANOTHER')

		# CLOSE
		if choice == 3:
			if isOpen:
				closeDatabase()
				print('DATABASE CLOSED')
				isOpen = False

		# DISPLAY
		if choice == 4:
			if isOpen:
				f = open('Fortune_500_HQ.data', 'r')
				displayRecord(f)
				f.close()
			else:
				print('DATABASE NOT OPEN!')

		# UPDATE
		if choice == 5:
			if isOpen:
				f = open('Fortune_500_HQ.data', 'r')
				updateRecord(f)
				print('RECORD UPDATED!')
				f.close()
			else:
				print('DATABASE NOT OPEN!')

		# ADD
		if choice == 6:
			if isOpen:
				f = open('Fortune_500_HQ.data', 'r')
				addRecord(f)
				print('RECORD ADDED!')
				f.close()
			else:
				print('DATABASE NOT OPEN!')

		# DELETE
		if choice == 7:
			if isOpen:
				f = open('Fortune_500_HQ.data', 'r')
				deleteRecord(f)
				print('RECORD DELETED!')
				f.close()
			else:
				print('DATABASE NOT OPEN!')

		# REPORT
		if choice == 8:
			if isOpen:
				f = open('Fortune_500_HQ.data', 'r')
				createReport(f)
				f.close()
			else:
				print('DATABASE NOT OPEN!')

		# EXIT
		if choice == 9:
			sys.exit(0)

		if counter > 4:
			mergeBack(f)
			counter = 0



# CREATE DATABASE
def createDatabase(file):
    global first
    with open('Fortune_500_HQ.csv', 'r') as csv_file:
        with open('Fortune_500_HQ.config', 'w') as config_file:
            first = csv_file.readline()
            config_file.write(str(num_records) + '\n')
            config_file.write(first.replace(',', ' '))
        with open('Fortune_500_HQ.data', 'w') as data_file:
            spamreader = csv.reader(csv_file, delimiter=',')
            for row in spamreader:
                line = "{: <10} {: <40} {: <20} {: <10} {: <10} {: <10}\n".format(*row)
                data_file.write(line)
        with open('Fortune_500_HQ.overflow', 'w') as overflow_file:
            overflow_file.close()
        data_file.close()
    csv_file.close()


# OPEN DATABASE
def openDatabase():
	global f
	global cf
	global of

	prompt = input('Enter a Database (eg. Fortune_500_HQ): ')	# PROMPT USER FOR DATABASE NAME

	f = open(prompt + '.data', 'r+')		# OPEN DATA FILE
	cf = open(prompt + '.config', 'r')		# OPEN CONFIG FILE
	of = open(prompt + '.overflow', 'r')	# OPEN OVERFLOW FILE
	return True


# CLOSE DATABASE
def closeDatabase():
	f.close()		# CLOSE DATA FILE
	cf.close()		# CLOSE CONFIG FILE
	of.close()		# CLOSE OVERFLOW FILE


# GET RECORD
def getRecord(f, recordNum):
	#f = open('Fortune_500_HQ.data', 'r')
	record = "record"
	global num_records
	global record_size
	
	if recordNum >= 0 and recordNum <= num_records:
		f.seek(0,0)
		f.seek(record_size * recordNum) #offset from the beginning of the file
		record = f.readline()
	#f.close()
	return record


# FIND RECORD: BINARY SEARCH BY PRIMARY KEY (COMPANY/BUSINESS NAME)
def binarySearch(f, name):
	global middle
	#f = open('Fortune_500_HQ.data', 'r')
	global num_records,record_size
	low=0
	high=num_records-1
	record = "We only have 9 records, requested record NOT_FOUND"
	Found = False

	while not Found and high >= low:
		middle = (low+high) // 2
		#middle = low + (high-low) // 2
		record = getRecord(f, middle)
		middleidnum = record[11:41].strip().replace('_', ' ') # This was -_- 
		if middleidnum == name:
			Found = True
		if middleidnum < name:
			low = middle+1
		if middleidnum > name: 
			high = middle-1
	
	if(Found == True):
		return record
	else:
		return 'COULD NOT FIND RECORD.'
	#f.close()



# DISPLAY RECORD
def displayRecord(f):
	name = input("Enter the name of a company: ")		# PROMPT FOR RECORD TO DISPLAY
	record = binarySearch(f, name)						# FIND RECORD 

	# PRINT OUT RECORD TO CONSOLE
	print("{: <10} {: <40} {: <20} {: <10} {: <10} {: <10}".format('RANK', 'NAME', 'CITY', 'STATE', 'ZIP', 'EMPLOYEES'))
	print(record)




# UPDATE RECORD
def updateRecord(f):
	global middle
	#f = open('Fortune_500_HQ.data', 'r')
	name = input("NAME: ")			        # PROMPT FOR RECORD TO BE UPDATED
	record = binarySearch(f, name)			# FIND RECORD
	if record == 'COULD NOT FIND RECORD.':
		print('Record doesn\'t exist!')
		sys.exit(0)
	f.seek(0,0)
	recordList = record.split()				# PUT RECORD INTO A LIST WITH EACH ENTRY AS A FIELD

	# STORE EACH FIELD VALUE INTO VARIABLES
	rank = recordList[0]
	company = recordList[1]
	city = recordList[2]
	state = recordList[3]
	zipC = recordList[4]
	employees = recordList[5]

	# PROMPT FOR FIELD TO UPDATE
	field = input('Field (RANK, CITY, STATE, ZIP, EMPLOYEES): ')


	# BASED ON FIELD INPUTTED, UPDATE VARIABLES
	if field == 'RANK':
		rank = input('ENTER A RANK: ')
	elif field == 'CITY':
		city = input('ENTER A CITY: ')
	elif field == 'STATE':
		state = input('ENTER STATE: ')
	elif field == 'ZIP':
		zipC = input('ENTER ZIP: ')
	elif field == 'EMPLOYEES':
		employees = input('ENTER EMPLOYEES: ')
	else:
		print('Field doesn\'t exist!')
		sys.exit(0)

	# FORMAT THE NEW RECORD
	rec = "{: <10} {: <40} {: <20} {: <10} {: <10} {: <10}\n".format(rank, company, city, state, zipC, employees)
		
	# USE PYTHON'S INPLACE FEATURE TO REPLACE THE RECORD WITH THE NEW RECORD
	with open('Fortune_500_HQ.data', 'r+') as f:
		f.seek(record_size * middle)
		f.write(rec)



# DELETE RECORD
def deleteRecord(f):
	#f = open('Fortune_500_HQ.data', 'r')
	name = str(input("NAME: "))				# PROMPT FOR RECORD TO BE DELETED
	record = binarySearch(f, name)			# FIND RECORD

	# FILL IN THE VALUES AS -1 AND N/A
	rank = '-1'
	company = 'N/A'
	city = 'N/A'
	state = 'N/A'
	zipC = 'N/A'
	employees = 'N/A'

	# FORMAT THE RECORD WITH THE VALUES ABOVE
	rec = "{: <10} {: <40} {: <20} {: <10} {: <10} {: <10}\n".format(rank, company, city, state, zipC, employees)

	# USE PYTHON'S INPLACE FEATURE TO REPLACE RECORD WITH THE NEW RECORD WITH VALUES INDICATING DELETION
	with open('Fortune_500_HQ.data', 'r+') as f:
		f.seek(record_size * middle)
		f.write(rec)

	

# ADD RECORD
def addRecord(f):
	#f = open('Fortune_500_HQ.data', 'r')
	global num_records
	global counter

	# SET UP A (GLOBAL) COUNTER VARIABLE IN ORDER TO COUNT THE NUMBER OF RECORDS ADDED INTO OVERFLOW
	counter = counter + 1
	

	with open('Fortune_500_HQ.overflow', 'a') as of:

		# PROMPT FOR FIELD VALUES THAT ARE TO BE CREATED INTO A RECORD
		rank = input('RANK: ')			
		company = str(input('NAME: '))
		city = str(input('CITY: '))
		state = input('STATE: ')
		zipC = input('ZIP: ')
		employees = input('EMPLOYEES: ')

		# FORMAT THE RECORD 
		line = "{: <10} {: <40} {: <20} {: <10} {: <10} {: <10}\n".format(rank, company.replace(' ', '_'), city.replace(' ', '_'), state, zipC, employees)

		# ONLY ADD TO OVERFLOW FILE IF RECORD IS NOT FOUND IN DATA FILE
		if binarySearch(f, company) == 'COULD NOT FIND RECORD.':
			of.write(line)
		of.close()
	


# MERGE OVERFLOW RECORDS BACK INTO DATA FILE AND PERFORM REMOVAL OF DELETED RECORDS
def mergeBack(f):
	#f = open('Fortune_500_HQ.data', 'r')
	global counter
	global num_records
	global first
	flag = True

	with open('Fortune_500_HQ.overflow', 'r') as inFile:
		lineList = [line.rstrip('\n').split() for line in inFile]	# READ OVERFLOW RECORDS INTO A LIST
		lineList = bubbleSort(lineList)
		# print(lineList)
		
		# ITERATE OVER EACH OVERFLOW RECORD
		for e in lineList:
			flag = True
			for line in fileinput.input('Fortune_500_HQ.data',inplace=1):
				if flag:		# FLAG TO MERGE RECORD AND CONTINUE WITH REST OF RECORDS
					if line.split()[1] > e[1]:		# COMPARE PRIMARY KEY OF THE LINE VS. OVERFLOW RECORD
						flag = False
						print ("{: <10} {: <40} {: <20} {: <10} {: <10} {: <10}".format(e[0], e[1], e[2], e[3], e[4], e[5]))
						num_records = num_records + 1
				if line.split()[0] == '-1':
					num_records -= 1
				elif line.split()[0] != '-1':			# IF THE 'RANK' FIELD IS '-1', IT MEANS RECORD HAS BEEN DELETED
					print (line[:-1])	# PROCEED TO WRITE EVERY LINE EXCEPT THE ONE THAT IS DELETED (INDICATED BY '-1')
		wf = open('Fortune_500_HQ.overflow', 'w')
		wf.close()

		with open('Fortune_500_HQ.config', 'w') as config:
			config.write(str(num_records) + '\n')
			config.write(first.replace(',', ' '))
		


# BUBBLE SORT USED TO SORT OVERFLOW RECORDS
def bubbleSort(arr):
    n = len(arr)
 
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][1] > arr[j+1][1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]			
    return arr



# CREATE A REPORT OF THE FIRST 10 RECORDS
def createReport(f):
	#f = open('Fortune_500_HQ.data', 'r')
	top = [next(f) for x in range(10)]		# GET LINES 0-9 IN THE DATA FILE
	print(''.join(top))					# PRINT THE LINES OUT
	#f.close()



# RUN
main()