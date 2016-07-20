"""
Code courtesy of Eric Minkiel
"""

import argparse
from collections import defaultdict
import gzip

def parse_hgnc(hgnc_path, mode='id'):
    '''
    Parse the HGNC database to get current gene symbol for all 19,000 genes with protein products
    Suggested input:
        wget ftp://ftp.ebi.ac.uk/pub/databases/genenames/locus_types/gene_with_protein_product.txt.gz
        gunzip gene_with_protein_product.txt.gz
    Note for some reason the file from EBI seems to be unreadable by zcat but can still be gunzipped.
    Behavior depends on mode.
    If mode = 'id', returns a dictonary mapping HGNC ids (e.g. "HGNC:5") to all HGNC info, including approved gene symbol (e.g. "A1BG")
    If mode = 'update', returns a dictionary mapping any previous symbols or synonyms (e.g. "ACF") to current approved HGNC symbol (e.g. "AC1F")
    '''
    
    if hgnc_path.endswith('gz') or hgnc_path.endswith('.gzip'):
        hgnc_file = gzip.open(hgnc_path)
    else:
        hgnc_file = open(hgnc_path)

    hgnc = {}
    header = hgnc_file.readline()
    colnames = header.strip().split('\t')
    for line in hgnc_file.readlines():
        cols = line.split('\t')
        if mode == 'id':
            print cols
            hgnc_id = cols[colnames.index('HGNC ID')]
            hgnc[hgnc_id] = dict(zip(colnames,line.split('\t')))
        if mode == 'update':
            all_possible_names_and_symbols = map(str.strip,cols[colnames.index('Previous Symbols')].split(',') + 
                cols[colnames.index('Approved Symbol')].split(',') + 
                cols[colnames.index('Synonyms')].split(','))
            for symbol in all_possible_names_and_symbols:
                if symbol != '': # skip blanks
                    hgnc[symbol] = cols[colnames.index('Approved Symbol')]
    return hgnc


def main(args):
    d1 = parse_hgnc(args.hgnc, mode='update')
    d2 = defaultdict(list)
    for symbol in d1:
        approved = d1[symbol]
        d2[approved].append(symbol)

    with open(args.out, 'w') as o:
        o.write('approved\tsynonyms\n')
        for approved in d2:
            synonyms = ','.join(d2[approved])
            o.write('%s\t%s\n' % (approved, synonyms))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='hgnc', help='gene_with_protein_product.txt.gz file')
    parser.add_argument('-o', dest='out', help='gene_symbol_thesaurus.txt file')
    args = parser.parse_args()

    main(args)





