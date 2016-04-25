#!/usr/bin/env python

"""
Created by: Jojo Holert

Description:   A program that extracts single nucleotide files from a genbank file containing mulitple nucleotides (plasmids, chromosomes, etc.)

Requirements: - This script requires the Biopython module: http://biopython.org/wiki/Download

Usage: Extract_nucl_fromGenbank.py <genbankfile.gbff>
                                    1
"""

# Imports & Setup:
import os
import csv
import sys
from Bio import SeqIO
import re
import gzip
#----------------------------------


#out1 = sys.argv[1] + '.faa'
#fileout = open(out1, 'w')

handle = gzip.open(sys.argv[1], "rU")
 
for record in SeqIO.parse(handle, "gb"):
    output_handle = record.id
    SeqIO.write(record, output_handle + '.gbff', "gb")
    
handle.close()