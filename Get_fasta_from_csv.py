""" Gets AA sequence from csv or tsv files and stores it in fasta format"""

# File created on 27 Oct 2015.

# author__ = "Johannes Holert"

# usage: python Get_fasta_from_csv.py 	<proteins.txt> 
# 				0										1

import sys
import re


filein = open(sys.argv[1], 'r')

# read lines in input file, split lines by Tab

for line in filein:
    if line.startswith('Filename'): # skips header line in results files
        continue
    else:
	    line2 = line.split('\t')
	    Filename = line2[0] # contigID
	    proteinID = line2[1] # coverage
	    seq = line2[3] # create dictionary key = contig_ID
	    output = proteinID + ".fasta"
	    fileout = open(output, 'w')
	    fileout.write(">%s_%s\n%s" %(Filename, proteinID, seq))

fileout.close()
filein.close()
