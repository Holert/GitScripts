""" Retrieves protein information from Prodigal results based on protein ID and filename 
required proteins have to be in .csv file with filenames in column 1 and protein ID in column 2
prodigal results in *.faa"""

# File created on 23 Oct 2015.

# author__ = "Johannes Holert"

# usage: python Protein_info_from_prodigalresults.py 	<csv_file_containing_HMMhits> 	
# 				0										1							

import sys
import re
# import gzip
import Bio
from Bio import SeqIO
from collections import defaultdict

filein = open(sys.argv[1], 'r')
shortname = re.sub('.csv$','', sys.argv[1], re.I)
output = shortname + ".proteins.txt"
# output = file + ".proteins.txt"
fileout = open(output, 'w')

# create dictionary

file_dict = defaultdict(list)

# read lines in input file, split lines by comma

for line in filein:
    if line.startswith('Filename'): # skips header line in results files
        continue
    else:
	    line1 = line.split(',')
	    filename = line1[0] # filename
	    proteinID = line1[1].rstrip() # protein ID
	    # print proteinID
	    file_dict[filename].append(proteinID) # feed keys and values to dictionary
# print file_dict

for key in file_dict:
	file = key + ".faa" # for .gz use ".faa.gz"
	filein_1 = open(file, 'r') #  gzip.open
	print "Extracting file %s" %file
	for seq_record in SeqIO.parse(filein_1, format = "fasta"):
		# print seq_record
		line2 = seq_record.description
		# print line2
		line3 = re.sub(r'\s', '', line2).split('#')
		# print line3[0]
		if line3[0] in file_dict[key]:
			print "I found protein %s" %line3[0]
			partial_info = line3[4]
			partial = partial_info.split(';')
			completeness = partial[1]
			start = line3[1]
			end = line3[2]
			orientation = line3[3]
			# fileout.write("%s\t%s\t%s\t%s\t%s\n" %(key, line3[0], start, end, orientation))
			fileout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(key, line3[0], completeness, seq_record.seq, start, end, orientation))
		else:
			continue

fileout.close()
filein.close()
filein_1.close()

"""    
to do:
add better description
make work for gz zipped and plain fasta files
"""
