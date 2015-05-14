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

reader = csv.reader(filein) # read lines in input file
for row in reader:
    if len(row) < 3: 
        continue # identify header rows by length and skip these rows
    else:
        area = row[8] # read out peak areas
        if area == "Area": # skip string Area
            continue
        else:
            ret_time = float(row[2]) # read out retention times and convert into flowting numbers
            area = float(area) # convert areas into flowting numbers
            if (ret_time < 17) and (ret_time > 16): # set time frame for detection of 5alpha-cholestane standard peak
                fileout.write ("%s,%s,Standard\n" %(ret_time, area)) # write retention time and peak area for internal standard
            elif (ret_time < 19.7) and (ret_time > 19.0): # set time frame for detection of cholesterol peak
                fileout.write ("%s,%s,Cholesterol\n" %(ret_time, area)) # write retention time and peak area for cholesterol
            else:
               continue

filein.close()
fileout.close()
    
    