# omim

Repository for OMIM data.

parse_omim.py downloads data from the OMIM API via HTTP request and writes it to a tsv file. The script uses a hard-coded API key which has some expiration date. New keys can be requested from the OMIM website here https://omim.org/api/.

The script cherry-picks a few fields to include in the output file. These fields come from the schema described here https://omim.org/help/api, specifically the "Entry Data" section.

### e.g. python src/parse_omim.py --hgnc data/gene_symbol_thesaurus.txt --use --output data/use_omim_table.txt

gene_symbol_thesaurus.txt is a file which maps gene aliases to their corresponding HGNC symbol. Aliases will map to at most one HGNC symbol; however, multiple aliases can map to the same HGNC symbol. 

This can get complicated so the schema we've adopted is to have three columns which describe how the gene names are processed: genes, hgnc_synonyms, and hgnc_genes. 

"genes" is a pipe-delimited field containing all the gene names listed in the OMIM database for a given entry. 

"hgnc_synonyms" is another pipe-delimited field where the sub-fields contain the HGNC synonyms of the aliases listed in the "genes" field. If no synonym is present, the value will be NA. 

And finally, "hgnc_genes" is a comma-delimited field containing all non-NA entries in the "hgnc_synonyms" field. This will probably be the column you will want to use.

### gene name schema

| genes                 | hgnc_synonyms  | hgnc_genes |
|-----------------------|----------------|------------|
| CMM\|MLM\|DNS           | CMM\|CDKN2A\|CMM | CMM,CDKN2A |
| SCAR4\|SCASI           | SCASI\|SCASI    | SCASI      |
| B3GALT6\|SEMDJL1\|EDSP2 | B3GALT6\|NA\|NA  | B3GALT6    |

If the --use option is activated, then only entries with a gene AND associated phenotype AND where the gene can be matched to an HGNC-approved symbol will be included.

