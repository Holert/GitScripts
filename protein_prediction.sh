#for i in `ls *fasta;do echo $i;prodigal -a $i.faa -i $i -m -o $i.txt -p meta -q;done
parallel --gnu -j10 'prodigal -a {.}.faa -i {} -m -o /dev/null -p meta -q' ::: *fasta
