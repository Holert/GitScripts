#!/bin/bash
# A simple script for the batch creation of blast databases from a directory with fasta files.
# These shell scripts have to be executed from subject_proteomes directory 
# renames output files and moves them to subdirectory
# usage  bash runBackBlast_Chol1.sh *.faa

timestamp=$(date +"%T")

for faa;
do
	echo Running Back-BLAST on $faa
	python -u BackBLAST.py /home/franziska/ReciprocalBLAST/query_proteins/Chol1/Chol1_steroiddegradation_proteins.fasta /home/franziska/ReciprocalBLAST/query_proteomes/Chol1/NZ_AMSL00000000.fasta $faa 2>&1 | tee -a "BackLog$timestamp.txt"
	date +"%T" >> "BackLog$timestamp.txt" 
done
mkdir Chol1
rename s/^/Chol1_/ *.csv
mv *.csv Chol1/
echo All files BLASTed.

for faa;
do
	echo Running Back-BLAST on $faa
	python -u BackBLAST.py /home/franziska/ReciprocalBLAST/query_proteins/Comamonas/CNB2_steroiddegradation_proteins.fasta /home/franziska/ReciprocalBLAST/query_proteomes/Comamonas/CNB2CompleteGenome.fasta $faa 2>&1 | tee -a "BackLog$timestamp.txt"
	date +"%T" >> "BackLog$timestamp.txt" 
done
mkdir CNB2
rename s/^/CNB2_/ *.csv
mv *.csv CNB2/
echo All files BLASTed.

for faa;
do
	echo Running Back-BLAST on $faa
	python -u BackBLAST.py /home/franziska/ReciprocalBLAST/query_proteins/Mtb/Mtb_steroiddegradation_proteins.fasta /home/franziska/ReciprocalBLAST/query_proteomes/Mtb/Mtb_H37Rv.fasta $faa 2>&1 | tee -a "BackLog$timestamp.txt"
	date +"%T" >> "BackLog$timestamp.txt" 
done
mkdir Mtb
rename s/^/Mtb_/ *.csv
mv *.csv Mtb/
echo All files BLASTed.

for faa;
do
	echo Running Back-BLAST on $faa
	python -u BackBLAST.py /home/franziska/ReciprocalBLAST/query_proteins/RHA1/RHA1_steroiddegradation_proteins.fasta /home/franziska/ReciprocalBLAST/query_proteomes/RHA1/RHA1CompleteGenome.fasta $faa 2>&1 | tee -a "BackLog$timestamp.txt"
	date +"%T" >> "BackLog$timestamp.txt" 
done
mkdir RHA1
rename s/^/RHA1_/ *.csv
mv *.csv RHA1/
echo All files BLASTed.
exit 0


