""" This program extracts peak area values from csv result-files created in GC-MS analysis with Agilent 5973 GC/MS system for quantification of cholestenone """

# File created on 13 Mar 2015.

# author__ = "Johannes Holert"

# usage: python GCMS_CholesterolQuantification.py 	<resultfile.csv> 
# 				0										1

import sys
import csv
import re

filein = open(sys.argv[1], 'r')
shortname = re.sub('.csv$','', sys.argv[1], re.I)
# finds file format removes extension, case insensitive search
output = shortname + ".quant.csv"
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
            if (ret_time < 16.7) and (ret_time > 16.4): # set time frame for detection of 5alpha-cholestane standard peak
                fileout.write ("%s,%s,Standard,%s\n" %(ret_time, area, output)) # write retention time and peak area for internal standard
            elif (ret_time < 21) and (ret_time > 19.3): # set time frame for detection of cholestenone peak
                fileout.write ("%s,%s,Cholestenone\n" %(ret_time, area)) # write retention time and peak area for cholestenone
            else:
               continue

filein.close()
fileout.close()
    
""" To Do:
 
 - check and correct time frames
 - change output file naming
 - rewrite for cholestenone
  """
   
    