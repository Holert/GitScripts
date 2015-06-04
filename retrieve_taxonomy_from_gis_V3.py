
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
shortname = re.sub('.fasta.blastp.gi$','', sys.argv[1], re.I)
shortname2 = re.sub('.combined_unique.fa.contigs_signHMMs','', shortname, re.I)

# Create a dictionary with the names of the sequences requested
# requestedsequences = []
gi_dict = {}
for line in filelist:
   line = line.strip('\n')
   line = line.strip('\r')
   line = line.split('\t')
   protein_ID = line[0]
   gi = line[1]
   gi_dict[protein_ID] = gi
   requestedsequences = gi_dict.values()

print requestedsequences
print "%d Sequence(s) requested" % len(requestedsequences)
print ''

count = int(len(requestedsequences))
#out_handle = open(out_file, "a")
batch_size = 1000
for start in range(0, count, batch_size):
    end = min(count, start + count)
    #batch = gi_list[start:end]
    print "Going to download record %i to %i using epost+efetch" %(start + 1, end)
    #post_results = Entrez.read(Entrez.epost("nuccore", id=",".join(batch)))
    post_results = Entrez.read(Entrez.epost("protein", id=",".join(requestedsequences)))
    webenv = post_results["WebEnv"]
    query_key = post_results["QueryKey"]
    #fetch_handle = Entrez.efetch(db="nuccore", rettype="fasta",retmode="text", webenv=webenv, query_key=query_key)
    fetch_handle = Entrez.efetch(db="protein", rettype="gb",retmode="text", webenv=webenv, query_key=query_key)
    #data = fetch_handle.read()
    records = SeqIO.parse(fetch_handle,"genbank")

# create dict containing taxonomy, organism and filename as values for gi number keys
taxonomy_dict = {}
for record in records:
    taxonomy_dict[record.annotations['gi']] = [record.annotations['taxonomy'], record.annotations['organism'], shortname2]
    # print taxonomy_dict
    
# combine all results and write out to tab delim file
for key, values in gi_dict.iteritems():
    protein_taxonomy = taxonomy_dict.get(values)
    protein_taxonomy.append(key)
    protein_taxonomy.append(values)
    fileout.write ('%s\t%s\t%s\t%s\t%s\n' %(protein_taxonomy[2], protein_taxonomy[3], protein_taxonomy[4], protein_taxonomy[0], protein_taxonomy[1]))
print "Done"
fileout.close()



#request = Entrez.epost(db='protein', id = ",".join(requestedsequences), rettype="gb", retmode="text")
#result = Entrez.read(request)

#handle = Entrez.efetch(db="protein", id=requestedsequences, rettype="gb", retmode="text")
#records = SeqIO.parse(handle,"genbank")
##print records
