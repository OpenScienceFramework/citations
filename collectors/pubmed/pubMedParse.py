# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:35:54 2013

@author: David Stack
"""

from lxml import etree
from Bio import Entrez
Entrez.email = ''

def main():
    dataPath = 'C:/Users/David/Dropbox/Conferences/PyCon 2013/sprints/data/pmid_list.txt'
    
    # read pmids from dataPath
    with open(dataPath) as f:
        pmidsIn = f.read()
        
    # convert raw string to list
    pmidsIn = pmidsIn.split('\n')
    
    # get all references contained within all pmidsIn articles
    print 'Getting Pub Med Ids...'
    pmids = get_info_from_oai(pmidsIn, sort=True)
    
    # print
    for p in pmids:
        print p
    
    print 'pmids len:', len(pmids)
    
def get_info_from_oai(pmidsIn, sort=False, debug=False):
    '''
    Gets information (pmids, etc.) from the PubMed Central OAI service
    (PMC-OAI) using Biopython's Entrez.efetch method. Searches for all
    articles from provided pmidsIn.
    
    See https://www.ncbi.nlm.nih.gov/pmc/tools/oai/
    
    Parameters
    ----------
    pmidsIn : string/int or list of strings
        one or more PubMed IDs
    sort : bool
        (optional) sort output pmid list or not
    debug : bool
        (optional) print more info for debugging
        
    Returns
    -------
    List of pmids.
    '''
    # convert pmidsIn to csv string if pmidsIn is a list
    if type(pmidsIn) == type([]):
        ','.join(pmidsIn)
    
    # read xml from pubMed database
    # if the len of pmidsIn more than 1, then the xml returned is a 
    # PubmedArticleSet of PubmedArticles. It is still all one xml doc
    xml = Entrez.efetch(db='PubMed', retmode='xml', id=pmidsIn).read()
    
    # save as element tree
    tree = etree.fromstring(xml)
    if debug: print etree.tostring(tree, pretty_print=True)
    
    # get pmids
    pmidsOut = tree.xpath("//CommentsCorrections[@RefType='Cites']/PMID/text()")
    
    # TODO: get other info from xml files (author, title, year, etc.)
    
    # convert to integers
    pmidsOut = map(int, pmidsOut)
    
    # sort
    if sort:
        pmidsOut.sort()
    
    return pmidsOut
    
# Run main() if module is run as a program
if __name__ == '__main__':
    main()
