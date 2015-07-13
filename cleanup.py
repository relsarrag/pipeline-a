###############################################################
################### Ramey Elsarrag: Cleanup ###################
###############################################################

########################### Imports ###########################
import sys, os, argparse
###############################################################

########################## Variables ##########################	
parser = argparse.ArgumentParser(description="""Remove temporary files generated during pipeline execution""")
parser.add_argument('-d', metavar="DIRECTORY", type=str, nargs='+',
                    help='Directories to be cleaned, all files beginning with "temp_" will be removed.')

args = vars(parser.parse_args())
###############################################################

############################ Cleanup ##########################
for i in args['d']:
	#Remove files starting with 'temp_'
	files = [f for f in os.listdir(i) if os.path.isfile(f)]
	for f in files:
		if f.startswith('temp_'):
			print("Removing: " + f)
			os.remove(f)
###############################################################
