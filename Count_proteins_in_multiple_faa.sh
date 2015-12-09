# shell script to count number of proteins in multiple fasta files and export filenames and proteinnumbers

for i in *.faa
do echo $i >> proteinnumbers.txt
grep ">" $i | wc -l >> proteinnumbers.txt
done