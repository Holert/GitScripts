# script for extracting and naming GC-MS results


for i in */; do mv "$i/results.csv" "$i.csv"; done