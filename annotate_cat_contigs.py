#! /usr/bin/python

import re
import sys
import os
from optparse import OptionParser


usage = '''
Usage:
./annotate_CAT_taxonomy.py -m <CAT contig taxonomy> -s <contig size>

Creates a table with taxonomic annotations summed according to the contig length
'''

parser = OptionParser(usage)
parser.add_option("-m", "--cat", dest="cat_fp",
    help='cat contig taxonomy [REQUIRED]')
parser.add_option("-s", "--size", dest="size_fp", help='contig size [REQUIRED]')


def main(argv):
    (opts, args) = parser.parse_args()

    # Initialize files
    cat_fp = opts.cat_fp
    size_fp = opts.size_fp

    basename_source = re.sub('.m8.contigclassification.tab$', '', cat_fp, re.I)
    output_fp = basename_source + ".annotated_taxonomy.txt"

    fileout = open(output_fp, 'w')
    cat_result = open(cat_fp, 'r')
    sizes = open(size_fp, 'r')

    # Create dictionary of contig size
    dict_contig_sizes = {}

    for line in sizes:
        line = line.rstrip('\n').rstrip('\r')
        line = line.split('\t')
        dict_contig_sizes[line[0]] = float(line[1])
    genome_size = sum(dict_contig_sizes.values())
    sizes.close()

    weighed_dict_kingdom = {}
    weighed_dict_phylum = {}
    weighed_dict_class = {}
    weighed_dict_order = {}
    weighed_dict_family = {}
    weighed_dict_genus = {}
    weighed_dict_species = {}
    
    # Read cat record, add contig size
    for line2 in cat_result:
            line2 = line2.strip('\n')
            line3 = line2.split('\t')
            kingdom = line3[1]
            phylum = line3[2]
            clas = line3[3]
            order = line3[4]
            family = line3[5]
            genus = line3[6]
            species = line3[7]
            
            
            contig_size = float(dict_contig_sizes.get(line3[0]))
            
            count_kingdom = weighed_dict_kingdom.get(kingdom, 0)
            new_count_kingdom = count_kingdom + contig_size/genome_size
            weighed_dict_kingdom[kingdom] = new_count_kingdom
            
            count_phylum = weighed_dict_phylum.get(phylum, 0)
            new_count_phylum = count_phylum + contig_size/genome_size
            weighed_dict_phylum[phylum] = new_count_phylum
            
            count_class = weighed_dict_class.get(clas, 0)
            new_count_class = count_class + contig_size/genome_size
            weighed_dict_class[clas] = new_count_class
            
            count_order = weighed_dict_order.get(order, 0)
            new_count_order = count_order + contig_size/genome_size
            weighed_dict_order[order] = new_count_order
            
            count_family = weighed_dict_family.get(family, 0)
            new_count_family = count_family + contig_size/genome_size
            weighed_dict_family[family] = new_count_family
            
            count_genus = weighed_dict_genus.get(genus, 0)
            new_count_genus = count_genus + contig_size/genome_size
            weighed_dict_genus[genus] = new_count_genus
            
            count_species = weighed_dict_species.get(species, 0)
            new_count_species = count_species + contig_size/genome_size
            weighed_dict_species[species] = new_count_species
    cat_result.close()

    KINGDOM = max(weighed_dict_kingdom, key=weighed_dict_kingdom.get), max(weighed_dict_kingdom.values())
    PHYLUM = max(weighed_dict_phylum, key=weighed_dict_phylum.get), max(weighed_dict_phylum.values())
    CLASS = max(weighed_dict_class, key=weighed_dict_class.get), max(weighed_dict_class.values())
    ORDER = max(weighed_dict_order, key=weighed_dict_order.get), max(weighed_dict_order.values())
    FAMILY = max(weighed_dict_family, key=weighed_dict_family.get), max(weighed_dict_family.values())
    GENUS = max(weighed_dict_genus, key=weighed_dict_genus.get), max(weighed_dict_genus.values())
    SPECIES = max(weighed_dict_species, key=weighed_dict_species.get), max(weighed_dict_species.values())
    
    fileout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(basename_source, KINGDOM[0], KINGDOM[1], PHYLUM[0], PHYLUM[1], CLASS[0], CLASS[1], ORDER[0], ORDER[1], FAMILY[0], FAMILY[1], GENUS[0], GENUS[1], SPECIES[0], SPECIES[1]))
    fileout.close()

# the main function
main(sys.argv[1:])