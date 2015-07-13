###############################################################
################# Ramey Elsarrag: Clustering ##################
###############################################################

########################### Imports ###########################
import sys, subprocess, argparse, re
###############################################################

########################## Variables ##########################
parser = argparse.ArgumentParser(description="""Perform Clustering using R""")
parser.add_argument('-q', metavar="QUERY FILE", type=str, nargs='+',
                    help='File for clustering analysis, must be a csv file saved as a .dat file. The file_processing script can be used to isolate the appropriate section of the file for clustering.')
parser.add_argument('-c', metavar="CLUSTERING ALGORITHM", type=str,
                    help="Method for clustering analysis, if method is not present in methods.inf then it must be added, along with the appropriate R Script.")
parser.add_argument('-m', metavar="METHOD ARGUMENTS", nargs='+', 
					help='Arguments for clustering analysis. Must match those needed in methods.inf, which match the arguments needed by the R script.')

args = vars(parser.parse_args())
for i in args['q']:
	#Retrieve methods
	method = args['c']
	methods_file = open('methods.inf', 'r+')
	flag = False
	c = 0
	algorithm = ""
	methods_data = {}
	for l in methods_file:
		if l.strip() == "START":
			flag = True
		elif l.strip() == "END":
			flag = False
			algorithm = ""
			c = 0
		elif flag == True and c == 0:
			methods_data[l.strip()] = []
			algorithm = l.strip()			
			c+=1
		elif flag == True and c == 1:
			methods_data[algorithm].append(l.strip())
			c+=1
		elif flag == True and c > 1:
			methods_data[algorithm].append(l.strip())
			c+=1
		else:
			continue
	methods_file.close()
	
	#Check for valid Method
	if(len(method) < 1 or (method not in methods_data.keys())):
		print(method)
		print("Invalid Method")
		raise SystemExit
	else:
		method = method
		print ("The Clustering Algorithm is: " + method)
		
	#Check for valid csv file(s):
	if(len(i) > 0 and i.endswith('.dat')):
		currFile = i
		print("The current file is: " + i)
	else:
		print("File " + i + " is invalid. Skipping.")
		continue  	
###############################################################

########################## Clustering #########################
	#Generate appropriate command
	command = methods_data[method][0]
	cmd_args = args['m']
	for c in cmd_args:
		command = re.sub(r'\[\[.*?\]\]', c.strip(), command, count=1)	
	file_argument = ".R " + currFile.strip() + ""
	command = re.sub(r'\/*?\.R', file_argument, command) 
	#Starts new R process with appropriate command
	try:
		subprocess.Popen(command, shell=True).wait()
	except Exception:
		print('Error Executing command: ' + command + '. Skipping.')
		continue
	print("Clustering has been completed on: " + currFile.strip())
###############################################################
