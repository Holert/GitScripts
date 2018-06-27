# script for extracting and naming GC-MS results


for i in *.D; do mv "$i/results.csv" "$i.csv"; done
rm -r *.D