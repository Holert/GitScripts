# script for renaming MyCC result forlders with filename


for i in 20*; do mv "$i" `awk '-F[/\ ]' 'FNR == 2 {print substr($6, 1, length($6)-6)}' $i/log 2>/dev/null`; done