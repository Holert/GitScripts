# Script for finding redundant HMM hits (proteins with more than one hit from the same HMM) in metagenomic datasets in filtered results from HMM_search_and_parse_and_extract.py (Erick Cardenas)

# File created on 07 Mar 2015.

# author__ = "Johannes Holert"

# usage: python sort_and_filter_redundantHMMhits.py <hmms.filtered.txt>
# 				0									1

import sys
import re

filein = open(sys.argv[1], 'r')
shortname = re.sub('.txt$','', sys.argv[1], re.I)
output = shortname + ".clean.txt"
fileout = open(output, 'w')


# create empty dictionary

read_dictionary = {}

# read lines in input file, split lines by Tab, extract protein ID, HMM and e-value

for line in filein:
    line1 = line.split('\t')
    #print (line1)
    query = line1[0] # protein ID
    subject = line1[1] # HMM
    evalue = float(line1[2]) # e-value
    coverage = float(line1[7]) # coverage
    current_result = read_dictionary.get(query, ['none', 10, 'none'])	# set e-value
    if evalue < float(current_result[1]): # compare e-values
    	new_result = [subject, evalue, coverage]
    	read_dictionary[query] = new_result # update entry in dictionary
    else:
    	continue
        
        
# write dictionary

for key, value in read_dictionary.iteritems():
	fileout.write("%s\t%s\t%s\t%s\t%s\n" %(shortname, key, value[0], value[1], value[2]))

fileout.close()
filein.close()

""" 
to do: 
"""
