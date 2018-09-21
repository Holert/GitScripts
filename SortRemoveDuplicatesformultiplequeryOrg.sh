#!/bin/bash
# A simple script that removes multiple hits from BackBlast results if multiple best hits to different query organisms are present and only keeps the hit with the highest identity score. 
# USAGE: bash SortRemoveDuplicatesfrommultiplequeryOrg.sh *.csv

for csv;
do
	echo Removing duplicate hits from on $csv
	sort -k 3,3r -t , $csv | sort -u -k 2,2 -t , > "$csv.out"
done
echo Done.
exit 0

