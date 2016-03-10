""" Rename a file by reading its original filename, looking the filename up in a list of new filenames and renaming it accordingly"""

# File created on 14 Dec 2015.

# author__ = "Johannes Holert"

# usage: python Rename_files_from_list 	file.fna	<txt_containing new filenames
# the list of new filenames has to contain the original filename 	
# 				0						1			2				

import sys
import re
import os

filein = open(sys.argv[1], 'r')
#listin = open(sys.argv[2], 'r')

# shortname = re.sub('.assembled.fna$','', sys.argv[1], re.I)

with open(sys.argv[2]) as f:
    content = f.readlines()
matching = [s for s in content if shortname in s]

for filename in os.listdir("."):
    os.rename(filename, matching[0])

"""print shortname

print content
matching = [s for s in content if shortname in s]
print matching

os.rename(filein, "matching")"""

filein.close()

"""
output = shortname + ".proteins.txt"
# output = file + ".proteins.txt"
fileout = open(output, 'w')

# create list

file_dict = defaultdict(list)

# read lines in input file, split lines by comma

for line in filein:
    if line.startswith('Filename'): # skips header line in results files
        continue
    else:
	    line1 = line.split(',')
	    filename = line1[0] # filename
	    proteinID = line1[1] # protein ID
	    # print proteinID
	    file_dict[filename].append(proteinID) # feed keys and values to dictionary
# print file_dict

for key in file_dict:
	file = key + ".faa" # for .gz use ".faa.gz"
	filein_1 = open(file, 'r') #  gzip.open
	# print filein_1
	for seq_record in SeqIO.parse(filein_1, format = "fasta"):
		# print seq_record
		line2 = seq_record.description
		line3 = re.sub(r'\s', '', line2).split('#')
		if line3[0] in file_dict[key]:
			# print line3[0]
			partial_info = line3[4]
			partial = partial_info.split(';')
			completeness = partial[1]
			fileout.write("%s\t%s\t%s\t%s\n" %(key, line3[0], completeness, seq_record.seq))
		else:
			continue

fileout.close()
filein.close()
filein_1.close()


"""
