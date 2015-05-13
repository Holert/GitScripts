""" Calculates protein abundances in metagenomic datasets by reading sequence coverage from original sequence files """

# File created on 07 Mar 2015.

# author__ = "Johannes Holert"

# usage: python calcProtAbund_fromCoverageinMetagen.py 	<hmms.filtered.clean.txt> 	<sequencecoveragefile>
# 				0										1							2

import sys
filein = open(sys.argv[1], 'r')
filecoverage = open(sys.argv[2], 'r')
outy = sys.argv[1]
output = outy + '.abundancy.txt' """ substitute part of name !!! """
fileout = open(output, 'w')

# create empty dictionaries

read_dict = {}
coverage_dict = {}

# read lines in input file, split lines by Tab, extract protein ID, HMM and e-value

for line in filein:
    line1 = line.split('\t')
    query = line1[1] # HMM
    subject = line1[0] # protein ID
    evalue = float(line1[2]) # e-value
    HMMcoverage = float(line1[3]) # coverage of HMMhit
    newdict = [subject, evalue, HMMcoverage]
    read_dict[query] = newdict # create dictionary key = HMM
    
    # split coming from one side and slipt only once
    
    # print read_dict --> works, potential errors due to tab/space misplacement

for line in filecoverage:
	line2 = line.split('\t')
    contig_ID = line2[0] # contigID
    contig_coverage = line2[1] # coverage
    coverage_dict[contig_ID] = contig_coverage # create dictionary key = contig_ID
    
    # print coverage_dict --> works, potential errors due to tab/space misplacement


# retrieve contig coverage value from coverage_dict

# coverage = coverage_dictionary.get(seq_name,0)
    
for query in read_dict:
	
    current_result = read_dictionary.get(query, ['none', 10, 'none'])	# set e-value
    if evalue < float(current_result[1]): # compare e-values
    	new_result = [subject, evalue, coverage]
    	read_dictionary[query] = new_result # update entry in dictionary
    else:
    	continue
        


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
