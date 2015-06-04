""" Calculates protein abundances in metagenomic datasets by reading sequence coverage from original sequence files """

# File created on 07 Mar 2015.

# author__ = "Johannes Holert"

# usage: python calcProtAbund_fromCoverageinMetagen.py 	<gi.lineages.txt> 	<sequencecoveragefile>
# 				0										1							2

import sys
import re


filein = open(sys.argv[1], 'r')
filecoverage = open(sys.argv[2], 'r')
shortname = re.sub('.txt$','', sys.argv[1], re.I)
output = shortname + ".coverage.txt"
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

print coverage_dict
    
for line in filein:
    line1 = line.split('\t')
    protein_ID = line1[1] # protein ID
    protein = protein_ID.rsplit('_', 1) # split protein ID by underscore delimiter, results in list
    print line1
    print protein
    contig = protein[0] # get first entry in list = contig ID
    print contig
    coverage = coverage_dict.get(contig) # look up contig in coverage dict and get value
    print coverage
    fileout.write("%s\t%s\t%s\t%s\t%s\t%s" %(line1[0], line1[1], line1[2], coverage, line1[3], line1[4]))
    
fileout.close()
filein.close()