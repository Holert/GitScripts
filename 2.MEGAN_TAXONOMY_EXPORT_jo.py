#!/usr/bin/python
import sys, os, re, getopt, glob, numpy as np, os.path
import timeit

start = timeit.default_timer()

Usage = """
Usage:  ./MEGAN_TAXONOMY_EXPORT.py -I LIST.tsv -O ~/MEGAN_OUTPUT/

SOFTWARE/FILE DEPENDENCY:
	- MEGAN v5.5.3

COMMAND DEPENDENCY:

	-I	Directory containing your ".rma" files

	OR

	-I	Specify a ".tsv" in which you specify the various locations of your ".rma":

		Column 1: Sample Name
		Column 2: Location of ".rma"

	-O	Specify Output Directory

Usage:  ./MEGAN_TAXONOMY_EXPORT.py -I LIST.tsv -O ~/MEGAN_OUTPUT/ 

or 
	./MEGAN_TAXONOMY_EXPORT.py -I ~/Metagenomes/RMA/ -O ~/MEGAN_OUTPUT/
"""

if len(sys.argv)<2:
        print Usage
        sys.exit()

# Store input and output file names
INPUT=''
OUTPUT=''

# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"O:I:")

###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-I':
        INPUT= a
    if o == '-O':
        OUTPUT= a

## CREATE OUTPUT
if os.path.exists('./' + OUTPUT):
	print "\nOutput Folder Exists - Caution: Files May Be Re-Written"
else:
	os.mkdir(OUTPUT)

## IMPORT DIR NAMES into DICTIONARY

if os.path.isfile(INPUT):
	FILE_DICT={}

	with open(INPUT) as f:
       		next(f)

        	for line in f:
	        	line = line.strip("\r\n")
              		line = line.split("\t")

			FILE_DICT[line[0]] = line[1]

		print "Using "+INPUT+" file."


else:

	FILE_DICT = {}
	for file in glob.glob(INPUT+"/*.rma"):
		if INPUT != ".":
			name = re.sub(INPUT,"",file)
			name = re.sub("./","",name)
			name = re.sub(".rma","",name)

		else:
			name = re.sub("./","",file)
			name = re.sub(".rma","",name)

		FILE_DICT[name] = file

	print "Using "+INPUT+" directory for input files."
	
## Write Command File
output = open(OUTPUT+"/"+"command.txt", "w")

for key, value in FILE_DICT.iteritems():

	ID = key
	RMA = value
		
	output.write(' '.join([
		"open file=\'"+RMA+"\';",
	]))

	output.write(' '.join([
		"export what=paths",
		" file=\'"+OUTPUT+"/"+ID+".taxonomy.export.txt\';",
	]))

output.close()
	
## Run Command File
os.system("xvfb-run --auto-servernum --server-num=1 MEGAN -g -L /home/holert/scripts/metagenomics/MEGAN5-academic-license.txt -E -c "+OUTPUT+"/command.txt")
