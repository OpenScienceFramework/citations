# script for grabbing PMID's from Pubmed's open access articles in .nxml format
import glob
from lxml import etree

# grab every article in every journal directory
# @todo: modularize the path
articles = glob.glob('/path/to/journals/*/*.nxml')
# for every article found, write pmids to pmid_list.txt
# @todo: modularize the outputfile's name
with open('pmid_list.txt', 'w') as pmid_list:
    for article in articles:
        with open(article, 'r') as f:
            tree = etree.parse(f)
            pmids = tree.xpath("//*/pub-id[@pub-id-type='pmid']/text()")
            pmid_list.write('\n'.join(pmids))