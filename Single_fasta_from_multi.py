""" Retrieves protein information from Prodigal results based on protein ID and filename 
required proteins have to be in .csv file with filenames in column 1 and protein ID in column 2
prodigal results in *.faa"""

# File created on 23 Oct 2015.

# author__ = "Johannes Holert"

# usage: python Single_fasta_from_multi.py 	<multifastafile> 	
# 				0										1							

import sys
import re
# import gzip
import Bio
from Bio import SeqIO
from collections import defaultdict


file_dict = defaultdict(list)


filein = open(sys.argv[1], 'r')

for line in filein:
    line1 = line.split('_C_')
    filename = line1[0] # filename
    contig = line1[1].rstrip() # contig ID
    print(filename)
    file_dict[filename].append(contig)
    
for key in file_dict:
	file = key + ".fasta" # for .gz use ".faa.gz"
	filein_1 = open(file, 'r') #  gzip.open
	print("Extracting file %s" %file) 
	for record in SeqIO.parse(filein_1, format = "fasta"):
		# print seq_record
		line2 = record.id
		# print(line2)
		#line3 = re.sub(r'\s', '', line2).split('_')
		# line3 = line2.rsplit('_', 1)
		# print(line3[0])
		# if line3[0] in file_dict[key]:
		if line2 in file_dict[key]:
			print("I found contig %s" %line2)
			output_handle = key + "_" + line2
			SeqIO.write(record, output_handle + ".fasta", "fasta")
    
filein.close()