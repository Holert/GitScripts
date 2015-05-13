""" This program extracts peak area values from csv result-files created in GC-MS analysis with Agilent 5973 GC/MS system for quantification of cholesterol """

# File created on 13 Mar 2015.

# author__ = "Johannes Holert"

# usage: python GCMS_CholesterolQuantification.py 	<resultfile.csv> 
# 				0										1

import sys
import csv
filein = open(sys.argv[1], 'r')
outy = sys.argv[1]
output = outy + 'quantitation.csv' # substitute parts of input name
fileout = open(output, 'w')

# read lines in input file, split lines by Tab, extract protein ID, HMM and e-value

reader = csv.reader(filein)
for row in reader:
    if len(row) < 3:
        continue
    else:
        area = row[8]
        if area == "Area":
            continue
        else:
            ret_time = float(row[2])
            area = float(area)
            if (ret_time < 17) and (ret_time > 16):
                fileout.write ("%s\t%s\tStandard\n" %(ret_time, area))
            elif (ret_time < 19.7) and (ret_time > 19.0):
                fileout.write ("%s\t%s\tCholesterol\n" %(ret_time, area))
            else:
               continue

filein.close()
fileout.close()
    
    