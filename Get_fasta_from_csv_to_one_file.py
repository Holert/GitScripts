""" Gets AA sequence from csv or tsv files and stores it in fasta format"""

# File created on 27 Oct 2015.

# author__ = "Johannes Holert"

# usage: python Get_fasta_from_csv_to_one_file.py 	<proteins.csv> 
# 				0										1

import sys
import re


filein = open(sys.argv[1], 'r')
out1 = sys.argv[1] + '.faa'
fileout = open(out1, 'w')

# read lines in input file, split lines by comma

for line in filein:
    if line.startswith('Filename'): # skips header line in results files
        continue
    else:
	    line2 = line.split('\t')
	    Filename = line2[0] 
	    proteinID = line2[1] 
	    seq = line2[3]
	    fileout.write(">%s_%s\n%s" %(Filename, proteinID, seq))


fileout.close()
filein.close()
