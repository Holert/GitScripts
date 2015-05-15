""" Calculates HMM hit abundances in metagenomic datasets by reading sequence coverage from contig files """

# File created on 07 Mar 2015.

# author__ = "Johannes Holert"

# usage: python calcProtAbund_fromCoverageinMetagen.py 	<hmms.filtered.clean.txt> 	<sequencecoveragefile>
# 				0										1							2

import sys
filein = open(sys.argv[1], 'r')
filecoverage = open(sys.argv[2], 'r')
outy = sys.argv[1]
output = outy + '.abundancy.txt'
fileout = open(output, 'w')

# create empty dictionaries

read_dict = {}
coverage_dict = {}
result_dict = {}

# read lines in input file, split lines by Tab


for line in filecoverage:
    if line.startswith('ID'): # skips header line in results files
        continue
    else:
	    line2 = line.split('\t')
	    contig_ID = line2[0] # contigID
	    contig_coverage = float(line2[1]) # coverage
	    coverage_dict[contig_ID] = contig_coverage # create dictionary key = contig_ID
    
for line in filein:
    line1 = line.split('\t')
    query = line1[1] # HMM
    subject = line1[0] # protein ID
    protein = subject.rsplit('_', 1) # split protein ID by underscore delimiter, results in list
    contig = protein[0] # get first entry in list = contig ID
    coverage = coverage_dict.get(contig) # look up contig in coverage dict and get value
    current_result = result_dict.get(query, 0) # set initial coverage value in dict for HMM to 0
    update_result = current_result + coverage # add coverage values to each other
    result_dict[query] = update_result # write new coverage value to dict with HMMs as key

print result_dict

for key, value in result_dict.iteritems():
	fileout.write("%s\t%f\t\output\n" %(key, value[0]))

fileout.close()
filein.close()


""" pseudocode

dataset1 Protein_ID, HMM, Evalue, Coverage
dataset2 contig_ID AvCoverage

read files
split files
	dataset 1: line.split('\t')
	key = HMM [2]
	values = [1, 3, 4]
	create dictionary read_HMM
	
	--> need to split protein ID: delete last _# --> contig ID for lookup in covereage file
	
	dataset 2: line.split('\t')
	key = contig [1]
	value = averagecoverage [2]
	create dictionary read_coverage

for key get value 1 (proteinID)
	look up value in dict read coverage and get value 1 (coverage)
	write value 1 from coverage dit to read dictionary

write out file

"""
