# quast analysis of *.fna metagenome sequences

for i in *.fasta; do python /home/data/metagenome_collection/quast-3.0/metaquast.py --no-plots --no-html --no-snps --max-ref-number 0 --min-contig 10 --threads 10 $i;rm quast_results/*/quast_corrected_input/*;done