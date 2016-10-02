# omim

Repository for downloading and converting OMIM data into an easier-to-use tab-delimitted table.

There are 2 main scripts - one based on the OMIM api and one based on the OMIM downloadable files:
```
python src/parse_omim_from_downloads.py -c src/omim_downloads_key.txt

python src/parse_omim_from_api.py -c src/omim_api_key.txt --hgnc data/gene_symbol_thesaurus.txt --use --output use_omim_table.txt
```
Each produces it's own variant of the tsv table. The details below should help decide which is better for your use-case.


parse_omim_from_downloads.py
----------------------------

This script downloads and parses the latest genemap2.txt file which contains OMIM gene/phenotype relatinoships. 
It requires an API key (either on the command line or through a config file). This key can be requested from the OMIM website here https://omim.org/downloads/.

It outputs the 'omim.tsv' which contains one row for each gene/phenotype relationship and has columns:
   mim_number
   approved_symbol
   gene_name
   ensembl_gene_id
   gene_symbols
   comments
   inheritance
   phenotype_mim_number
   phenotype_description
   phenotype_map_method


parse_omim_from_api.py
----------------------

This script downloads data from the OMIM API via HTTP request and writes it to a tsv file. 
It requires an API key (either on the command line or through a config file). This key can be requested from the OMIM website here https://omim.org/api/.

It outputs a table which contains one row for each gene/phenotype relationship, and has columns:
   genes
   hgnc_synonyms
   hgnc_genes
   phenotype
   phenotypeInheritance
   geneMimNumber
   phenotypeMimNumber
   chromosome
   comments

These fields come from the schema described here https://omim.org/help/api, specifically the "Entry Data" section.

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

# to get HGNC data:
wget ftp://ftp.ebi.ac.uk/pub/databases/genenames/locus_types/gene_with_protein_product.txt.gz

