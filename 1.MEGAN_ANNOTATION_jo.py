#!/usr/bin/python
import sys, os, re, getopt, glob, numpy as np
import timeit

start = timeit.default_timer()

Usage = """
Usage:  ./MEGAN_ANNOTATION.py -L LIST.tsv -U "blast.out" -T Y -O ~/MEGAN_OUTPUT/ -P Y

SOFTWARE/FILE DEPENDENCY:
	- MEGAN v5.10.1
	- gi_taxid-March2015X.bin

COMMAND DEPENDENCY:
	-I	Directory containing your ".blast.out" files and ".fa" files <optional>
	-U	Unique file extention identifier ".blast.out" or ".blast.min.out"

OPITONAL ARGUMENTS:
	-T <Y>	Specify if your format is Tabular

	-O	Specify Output Directory

	-P <Y>	Specify Protein Database

	-L	LIST-MODE, where you can specify files in various locations with a List file (.tsv format) containing:

		Column 1: Sample Name
		Column 2: Location of Blast Output
		Column 3: Location of FASTA File (optional)

Usage:  ./MEGAN_ANNOTATION.py -L LIST.tsv -U "blast.out" -O ~/MEGAN_OUTPUT/ -P Y
	(to process a list of multiple files in specific locations in regular blast format using the protein GI number database)
or 
	./MEGAN_ANNOTATION.py -I ~/Metagenomes/BLAST_OUTPUT/ -U "blast.out" -T Y -O ~/MEGAN_OUTPUT/
	(to process all "blast.out" files (fmt 7) in the directory "~/Metagenomes/BLAST_OUTPUT/" using the nucleotide database of GI numbers)
"""

if len(sys.argv)<2:
        print Usage
        sys.exit()

# Store input and output file names
INPUT=''
LIST=''
FORMAT=''
OUTPUT=''
DATABASE=''
IDENTIFIER=''

# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"L:T:O:P:I:U:")

###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-I':
        INPUT= a
    if o == '-L':
        LIST= a
    if o == '-T':
        FORMAT= a
    if o == '-O':
        OUTPUT= a
    if o == '-P':
        DATABASE= a
    if o == '-U':
        IDENTIFIER= a

## CREATE OUTPUT
if os.path.exists('./' + OUTPUT):
	print "\nOutput Folder Exists - Caution: Files May Be Re-Written"
else:
	os.mkdir(OUTPUT)

## IMPORT DIR NAMES into DICTIONARY
try:
	LIST
	if len(LIST)>0:
		FILE_DICT={}
		FASTA_Present={}

		with open(LIST) as f:
       			next(f)

	        	for line in f:
       		        	line = line.strip("\r\n")
        	       		line = line.split("\t")

				try:
					line[2]
		                	FILE_DICT[line[0]] = [line[1],line[2]]
					FASTA_Present[line[0]] = "PRESENT"
				except:
					FILE_DICT[line[0]] = line[1]
					FASTA_Present[line[0]] = "ABSENT"
except:
	pass

try:
	FILE_DICT
	SOURCE = "DICT"	
	print "Using "+LIST+" for input"

except NameError:
	SOURCE = "GLOB"	
	print "Using "+INPUT+" directory for input files"

if SOURCE == "GLOB":
	FILE_DICT = {}
	FASTA_Present = {}
	NAME = []

	for file in glob.glob(INPUT+"/*."+IDENTIFIER):
		name = re.sub("."+IDENTIFIER,"",file)
		name = re.sub(".fa|.compiled|.subset","",name)
		name = re.sub("./","",name)

		if INPUT != ".":
			name = re.sub(INPUT,"",name)
			name = re.sub("./","",name)


		FILE_DICT[name] = file
	
	for file in glob.glob(INPUT+"/*.fa"):
		name = re.sub(".fa|.compiled|.subset","",file)
		name = re.sub("./","",name)

		if INPUT != ".":
			name = re.sub(INPUT,"",name)
			name = re.sub("./","",name)

		if name in FILE_DICT:
			FILE_DICT[name] = [FILE_DICT[name],file]
			FASTA_Present[name] = "PRESENT"
		else:
			FASTA_Present[name] = "ABSENT"

## Write Validation of FASTAs Used
inputvalidation = open(OUTPUT+"/"+"Validation of fasta inputs.txt","w")

for key, value in FASTA_Present.iteritems():
	inputvalidation.write(key+"\t"+value+"\n")

inputvalidation.close()

## Write Command File
if len(OUTPUT) > 0:
	output = open(OUTPUT+"/"+"command.txt", "w")
else:
	output = open(INPUT+"/"+"command.txt", "w")
	OUTPUT = INPUT	

if len(DATABASE)>0:
	output.write("load taxGIFile='/home/holert/db/gi_taxid-March2015X.bin';\n")
else:
	output.write("load taxGIFile='/home/holert/db/gi_taxid-March2015X.bin';\n")

for key, value in FILE_DICT.iteritems():

	if np.size(value) > 1:
		BLAST = value[0]
		FASTA = value[1]
		
	else:
		BLAST = value
		FASTA = "NA"

	if FASTA == "NA":
		print "No Fasta Files will be Associated with your MEGAN .rma Files\n"
		if len(FORMAT)>0:
			output.write(' '.join([
				"import",	
				"blastFile="+BLAST,
				"meganFile="+OUTPUT+"/"+key+".rma",
				"maxMatches=10",
				"minScore=50.0",
				"maxExpected=0.01",
				"topPercent=10.0",
				"minSupport=50",
				"minComplexity=0.0",
				"useMinimalCoverageHeuristic=false",
				"useSeed=false",
				"useCOG=false",
				"useKegg=false",
				"paired=false",
				"useIdentityFilter=false",
				"textStoragePolicy=Embed",
				"blastFormat=BlastTAB",
				"mapping='Taxonomy:BUILT_IN=true,Taxonomy:GI_MAP=true';\n"
			]))

		else:
			output.write(' '.join([
				"import",	
				"blastFile="+BLAST,
				"meganFile="+OUTPUT+"/"+key+".rma\n"
				"maxMatches=10",
				"minScore=50.0",
				"maxExpected=0.01",
				"topPercent=10.0",
				"minSupport=50",
				"minComplexity=0.0",
				"useMinimalCoverageHeuristic=false",
				"useSeed=false",
				"useCOG=false",
				"useKegg=false",
				"paired=false",
				"useIdentityFilter=false",
				"textStoragePolicy=Embed",
				"mapping='Taxonomy:BUILT_IN=true,Taxonomy:GI_MAP=true';\n"
			]))
	else:
		print "Fasta Files will be Associated with your MEGAN .rma Files\n"
		if len(FORMAT)>0:
			output.write(' '.join([
				"import",	
				"blastFile="+BLAST,
				"fastaFile="+FASTA,
				"meganFile="+OUTPUT+"/"+key+".rma",
				"maxMatches=10",
				"minScore=50.0",
				"maxExpected=0.01",
				"topPercent=10.0",
				"minSupport=50",
				"minComplexity=0.0",
				"useMinimalCoverageHeuristic=false",
				"useSeed=false",
				"useCOG=false",
				"useKegg=false",
				"paired=false",
				"useIdentityFilter=false",
				"textStoragePolicy=Embed",
				"blastFormat=BlastTAB",
				"mapping='Taxonomy:BUILT_IN=true,Taxonomy:GI_MAP=true';\n"
			]))

		else:
			output.write(' '.join([
				"import",	
				"blastFile="+BLAST,
				"fastaFile="+FASTA,
				"meganFile="+OUTPUT+"/"+key+".rma\n"
				"maxMatches=10",
				"minScore=50.0",
				"maxExpected=0.01",
				"topPercent=10.0",
				"minSupport=50",
				"minComplexity=0.0",
				"useMinimalCoverageHeuristic=false",
				"useSeed=false",
				"useCOG=false",
				"useKegg=false",
				"paired=false",
				"useIdentityFilter=false",
				"textStoragePolicy=Embed",
				"mapping='Taxonomy:BUILT_IN=true,Taxonomy:GI_MAP=true';\n"
			]))

output.close()
	
## Run Command File
os.system("xvfb-run --auto-servernum --server-num=1 MEGAN -g -L /home/holert/scripts/metagenomics/MEGAN5-academic-license.txt -E -c "+OUTPUT+"/command.txt")
