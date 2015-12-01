#!/usr/bin/python
import sys, os, re, getopt, glob, numpy as np
import timeit

start = timeit.default_timer()

FILE_LIST = []

output = open("CAZy.Full.Taxonomy.tsv","w")
output.write("CAZY_CLASS\tCAZY_FAMILY\tSUBFAMILY\tKINGDOM\tDOMAIN\tPHYLUM\tORDER\tFAMILY\tGENUS\tSPECIES\tACCESSION\n")

# Check if number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#MAKE FUNCTION TO IDENTIFY WHETHER DOMAIN, PHYLUM, CLASS, ORDER, FAMILY, GENUS or SPECIES
def taxonomic_rank(name):

	PROKARYOTES = ["Archaea","Bacteria"]

	test = name.split()

	if name in PROKARYOTES:
		return "PROKARYOTES"

	elif name == "Eukaryota":
		return "EUKARYOTES"
		
	elif name == "Fungi":
		return "FUNGI"

	elif name[len(name)-4:len(name)] == "ales":
		return "ORDER" 

	#FAMILY NAMES ARE INCONSISTENT
	elif name[len(name)-5:len(name)] == "aceae":
		return "FAMILY" 

	#MOSTLY EUKARYOTE FAMILY NAMES
	elif name[len(name)-4:len(name)] == "idae":
		return "FAMILY" 

#	elif np.size(test) == 2:
#		if re.search("phylum",name):
#			pass
#		else:
#			return "GENUS"

# READ IN TAXONOMY FILES
for file in glob.glob("*.taxonomy.txt"):
	FILE_LIST.append(file)

for file in FILE_LIST:
	
	NAME = file.split(".")
	NAME = NAME[0]

	if NAME[0:2] == "CB":
		CAZY_CLASS = NAME[0:3]

	else:
		CAZY_CLASS = NAME[0:2]


	if NAME.find("_") != -1:
		CAZY_FAMILY = NAME.split("_") 	
		CAZY_FAMILY = CAZY_FAMILY[0]
		SUBFAMILY = NAME

	else:
		CAZY_FAMILY = NAME	
		SUBFAMILY = "NA"

	# PROCESS EACH TAXONOMIC STRING 
	for line in open(file):
		KINGDOM = ""
		DOMAIN = ""
		PHYLUM = ""
		ORDER = ""
		FAMILY = ""
		GENUS = ""
		SPECIES = ""

		line = line.strip()
		full_line = line
		line = line.split(";")
		
		
		ACCESSION = line[0]

		# EXCLUDE UNASSIGNED READS
		if line[2] == " Not assigned" or  line[4] == " unclassified sequences":
			KINGDOM = "Unclassified"
			DOMAIN = "Unclassified"
			PHYLUM = "Unclassified"
			ORDER = "Unclassified"
			FAMILY = "Unclassified"
			GENUS = "Unclassified"
			SPECIES = "Unclassified"

		elif line[4] == " Viruses":

			GENUS = line[len(line)-3]
			GENUS = GENUS.split()

			SPECIES = GENUS[1]
			GENUS = GENUS[0]

			KINGDOM = "Virus"
			DOMAIN = "Virus"
			PHYLUM = "Unclassified"
			ORDER = "Unclassified"
			FAMILY = "Unclassified"

		elif full_line.find(" artificial sequences") != -1:
			KINGDOM = "Unclassified"
			DOMAIN = "Unclassified"
			PHYLUM = "Unclassified"
			ORDER = "Unclassified"
			FAMILY = "Unclassified"
			GENUS = "Unclassified"
			SPECIES = "Unclassified"

		else:
			# GO THROUGH TAXONOMIC RANK STARTING AT KINGOM
			line = line[6:len(line)]	

			# GO THROUGH EACH RANK
			for item in line:
				item = item.strip()

				# SKIP BOOTSTRAP VALUES
				if is_number(item):
					pass

				#Make sure value is not empty	
				elif not item:
					pass

				#PROCESS EACH RANK
				else:
					RANK = taxonomic_rank(item)
				
				# Bypass all unassigned items
				if not RANK:
					pass

				else:
					if is_number(item):
						pass

					elif RANK == "PROKARYOTES":
						KINGDOM = item
						DOMAIN = item
						PHYLUM = line[2]
						PHYLUM = PHYLUM.strip()

					elif RANK == "EUKARYOTES":
						KINGDOM = item
						DOMAIN = line[2]
						DOMAIN = DOMAIN.strip()
						PHYLUM = line[4]
						PHYLUM = PHYLUM.strip()

					elif RANK == "FUNGI":
						DOMAIN = item
						DOMAIN = DOMAIN.strip()

					elif RANK == "DOMAIN":
						DOMAIN = item
						DOMAIN = DOMAIN.strip()

					elif RANK == "CLASS":
						CLASS = item
						CLASS = CLASS.strip()

					elif RANK == "ORDER":
						ORDER = item
						ORDER = ORDER.strip()

					elif RANK == "FAMILY":
						FAMILY = item
						FAMILY = FAMILY.strip()
	
#					elif RANK == "GENUS":
#						if item:
#							item = item.split()
#							GENUS = item[0]
#							SPECIES = item[1]
#							SPECIES = SPECIES[:1].upper() + SPECIES[1:]

#							GENUS = GENUS.strip()
#							SPECIES = SPECIES.strip()

#							if GENUS == "[Clostridium]":
#								GENUS = "Clostridium"
								

					if PHYLUM == "Actinobacteria <phylum>":
						PHYLUM = "Actinobacteria"

			if line:
				GENUS = line[len(line)-3]
				GENUS = GENUS.split()

				if np.size(GENUS) > 1:
					SPECIES = GENUS[1]
					GENUS = GENUS[0]
					SPECIES = SPECIES[:1].upper() + SPECIES[1:]

				else:
					GENUS = GENUS[0]

			GENUS = GENUS.strip()
			SPECIES = SPECIES.strip()

			if GENUS == "[Clostridium]":
				GENUS = "Clostridium"


			# IMPROVE CAPTURE OF FUNGI
			if DOMAIN == "Fungi":

				if full_line.find(" environ") != -1:
					pass

				else:
					if line:
						TESTER = line[6]

						if TESTER.find("incertae") != -1:
							PHYLUM = line[10]

						else:
							PHYLUM = line[8]

			# CATCH THE OUTSTANDING TAXA WHICH ARE ONLY CLASSIFED AT THE DOMAIN LEVEL
			if GENUS == "uncultured":
				PHYLUM = "Unclassified"
				CLASS = "Unclassified"
				ORDER = "Unclassified"
				FAMILY = "Unclassified"

			# CATCH THE SUPER IRREGULAR RANKING IN EUKARYA
			if KINGDOM == "Eukaryota":
				if not ORDER:
					ORDER = line[len(line)-7]

			if not KINGDOM:
				KINGDOM = "Classification Missing"
			if not DOMAIN:
				DOMAIN = "Classification Missing"
			if not PHYLUM:
				PHYLUM = "Classification Missing"
			if not FAMILY:
				FAMILY = "Classification Missing"
			if not GENUS:
				GENUS = "Classification Missing"
			if not SPECIES:
				SPECIES = "Classification Missing"


#		print "KINGDOM: "+KINGDOM
#		print "DOMAIN: "+DOMAIN
#		print "PHYLUM: "+PHYLUM
#		print "ORDER: "+ORDER 
#		print "FAMILY: "+FAMILY 
#		print "GENUS: "+GENUS 
#		print "SPECIES: "+SPECIES
#		print "--"

		output.write(CAZY_CLASS+"\t"+CAZY_FAMILY+"\t"+SUBFAMILY+"\t"+KINGDOM+"\t"+DOMAIN+"\t"+PHYLUM+"\t"+ORDER+"\t"+FAMILY+"\t"+GENUS+"\t"+SPECIES+"\t"+ACCESSION+"\n")

stop = timeit.default_timer()

print "This operation took " + str(stop - start) + " seconds."
