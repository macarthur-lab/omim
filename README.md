# omim

Repository for OMIM data.

parse_omim.py downloads data from OMIM API via HTTP request, writes to a tsv file. Script uses a hard-coded API key which has some expiration date. New keys can be requested from the OMIM website here https://omim.org/api/.

Also, parse_omim cherry-picks a few fields to include in the output file. These fields come from the schema described here https://omim.org/help/api, specifically the "Entry Data" section.

example usage:

e.g python parse_omim.py --hgnc gene_symbol_thesaurus.txt --use --output omim_table.txt

gene_symbol_thesaurus is a file which maps gene aliases to the corresponding HGNC symbol. 

If the --use option is activated, then only entries with a gene AND associated phenotype AND where the gene can be matched to an HGNC-approved symbol will be included.

