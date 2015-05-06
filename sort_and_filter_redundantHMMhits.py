# Script for finding redundant HMM hits (proteins with more than one hit from the same HMM) in metagenomic datasets in filtered results datasets from HMM_search_and_parse_and_extract.py (Erick)


# usage: python sort_and_filter_redundantHMMhits.py <hmms.filtered.txt>
# 				0									1

import sys

filein = open(sys.argv[1], 'r')
outy = sys.argv[1]
output = outy + '.clean.txt'
fileout = open(output, 'w')

# create empty dictionary

read_dictionary = {}

# read lines in input file, split lines by Tab, extract protein ID, HMM and e-value

for line in filein:
    line1 = line.split('\t')
    query = line1[0] # protein ID
    subject = line1[1] # HMM
    evalue = line1[2] # e-value
    current_result = read_dictionary.get(query, [ 'none', 10])	# get e-value for protein ID
    if evalue < current_result[1]: # compare e-values
      	new_result =[subject, evalue]         
        read_dictionary[query] = new_result		# update entry in dictionary
    else:
        continue
        
        
#write dictionary

for key, value in read_dictionary.iteritems():
   fileout.write("%s\t%s\t%s\n" %(key, value[0], value[1]))

fileout.close()
filein.close()
