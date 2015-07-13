###############################################################
############# Ramey Elsarrag: Clustering Pipeline #############
###############################################################

########################### Imports ###########################
import sys, subprocess, argparse, os, re, time
###############################################################

########################## Variables ##########################
parser = argparse.ArgumentParser(description="""Perform Clustering using R""")
parser.add_argument('--q', metavar="QUERY FILE", type=str, nargs='+',
                    help='File for clustering analysis, must be a csv file saved as a .dat file. The file_processing script can be used to isolate the appropriate section of the file for clustering.')
parser.add_argument('--d', metavar="DIRECTORY(S)", type=str, nargs='+',
                    help='Directry to perform clustering analysis. Analysis will be attempted on all files satisfying criteria; i.e: non-empty files ending with .dat. User is responsible for removing files that satisfy criteia and are NOT to be analyzed. Files is subdirectories will NOT be analyzed.')
parser.add_argument('--del', metavar="LINE DELMINATOR", type=str,
                    help="Optional deliminator for start line")
parser.add_argument('--dc', metavar="DIRECTORY(S)", type=str, nargs='+',
                    help='Direcotries to be cleaned after execution. All files begginning with "temp_" will be removed. Files is subdirectories satisfying removal criterial will NOT be removed.')
parser.add_argument('-c', metavar="CLUSTERING ALGORITHM", type=str,
                    help="Method for clustering analysis, if method is not present in methods.inf then it must be added, along with the appropriate R Script.")
parser.add_argument('-cm', metavar="METHOD ARGUMENTS", nargs='+', 
					help='Arguments for clustering analysis. Must match those needed in methods.inf, which match the arguments needed by the R script.')
parser.add_argument('-v', metavar="VALIDATION ALGORITHM", type=str,
                    help="The method used to validate the clustering analysis. Must be present in validation.inf, if not it needs to be added, along with the appropriate R script.")
parser.add_argument('-vm', metavar="METHOD ARGUMENTS", nargs='+', 
					help='Arguments for validation analysis. Must match those needed in validation.inf, which match the arguments needed by the R script.')

args = vars(parser.parse_args())

if not (args['q'] or args['d']):
    parser.error('No query files provided, add --q or --d')
###############################################################

########################## Pipeline ###########################
#File Processing
print "Processing Files..."
deliminator = args['del']
if(len(deliminator) > 0):
	delim = deliminator
else:
	delim = ''

if not args['q'] == None:
	for i in args['q']:
		if i.endswith('.dat') and not i.startswith('temp'):
			subprocess.Popen("python file_processing.py " + i + " " + deliminator, shell=True).wait()
if not args['d'] == None:
	for i in args['d']:
		files = [f for f in os.listdir(i) if os.path.isfile(f)]
		for f in files:
			if f.endswith('.dat') and not f.startswith('temp'):
				subprocess.Popen("python file_processing.py " + f + " " + deliminator, shell=True).wait()
print "File Processing Complete."

#Clustering
print "Clustering..."
files_raw = [f for f in os.listdir('.') if os.path.isfile(f)]
clustering_files = []
for i in files_raw:
	if i.startswith('temp_'):
		clustering_files.append(i)
for i in clustering_files:
	clustering_args = " "
	for c in args['cm']:
		clustering_args += c
		clustering_args += " "		
	subprocess.Popen('python clustering.py -q ' + i + " -c " + args['c'] + " -m " + clustering_args, shell=True).wait()
print "Clustering Complete."

#Validation:
print "Validating Clusters..."
files_raw = [f for f in os.listdir('.') if os.path.isfile(f)]
validation_files = []
for i in files_raw:
        if i.endswith('.clu'):
                print(i)
		validation_files.append(i)
validation_args = " "
for i in args['vm']:
	validation_args += i
	validation_args += " "
for i in clustering_files:
        subprocess.Popen('python validation.py -q ' + i + " -v " + args['v'] + " -m " + validation_args, shell=True).wait()
print "Validation Complete."

#Cleanup
print "Removing Temporary Files..."
temp_files = [f for f in os.listdir('.') if os.path.isfile(f)]
for i in temp_files:
	if i.startswith('temp_'):
		os.remove(i)
print "Temporary Files Removed."
###############################################################
