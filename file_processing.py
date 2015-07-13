###############################################################
######### Ramey Elsarrag: File Parsing for Clustering #########
###############################################################

########################### Imports ###########################
import sys, argparse, re
###############################################################

########################## Variables ##########################
parser = argparse.ArgumentParser(description="""Isolate clustering data from csv""")
parser.add_argument('queries', metavar="QUERY FILE", type=str, nargs='+',
                    help='File for data extraction')
parser.add_argument('deliminator', metavar="LINE DELMINATOR", type=str,
                    help="Optional deliminator for start line")
args = vars(parser.parse_args())

for i in args['queries']:
	#Check for valid delimnator
	deliminator = args['deliminator']
	if(len(deliminator) > 0):
		delim = deliminator
		print ("The delminator is: " + delim)
	else:
		delim = ''
		print ("The delminator is: No delminator was selected")
	
	#Check for valid csv file(s):
	if(len(i) > 0 and i.endswith('.dat') and not i.startswith('temp_')):
		currFile = i
		print("The current file is: " + i)
	else:
		print("File " + i + " is invalid. Skipping.")
		continue

	#Generate name of temp output file
	outputFileName = ("temp_" + re.split('\.', currFile)[0]
                      + '_output.dat')
  	
###############################################################

######################### File Parsing ########################
	inFile = open(currFile, 'r+')	
	outFile = open(outputFileName, 'w+')
	flag = False	
	for l in inFile:
		if l.startswith(delim):
			flag = True
		elif flag == True:
			outFile.write(l)		
		else:
			continue
	inFile.close()
	outFile.close()
	print("Parsing " + currFile + " complete. Output written to " + outputFileName)
raise SystemExit
###############################################################
