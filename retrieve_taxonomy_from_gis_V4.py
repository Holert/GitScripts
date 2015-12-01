
import sys
import re
from Bio import SeqIO
from Bio import Entrez
Entrez.email = "holert@mail.ubc.ca"


# Inputs
filelist = open(sys.argv[1], 'r')

# Output
out1 = sys.argv[1] + '.lineages.txt'
fileout = open(out1, 'w')

# Create a list with the names of the sequences requested
requestedsequences = []
for line in filelist:
   line = line.strip('\n')
   line = line.strip('\r')
   requestedsequences.append(line)
# print requestedsequences
print "%d Sequence(s) requested" % len(requestedsequences)
print ''
    # print "Going to download record %i to %i using epost+efetch" %(start + 1, end)
post_results = Entrez.read(Entrez.epost("protein", id=",".join(requestedsequences)))
webenv = post_results["WebEnv"]
query_key = post_results["QueryKey"]
fetch_handle = Entrez.efetch(db="protein", rettype="gb",retmode="text", webenv=webenv, query_key=query_key)
records = SeqIO.parse(fetch_handle,"genbank")
for record in records:
    fileout.write ('%s\t%s\t%s\t%s\n' %(record.annotations['gi'], record.id, record.annotations['taxonomy'], record.annotations['organism']))
print "Done"
fileout.close()
