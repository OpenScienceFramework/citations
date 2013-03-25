#from utils import 

import re
import requests
import urllib
import urlparse
from BeautifulSoup import BeautifulSoup as BS

import pubtools

# Taken from http://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
doi_ptn = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b')
ncbi_ptn = re.compile(r'pubmed', re.I)

def get_dois(txt):
    
    return doi_ptn.findall(txt)

def doi_to_pmid(doi):
    
    try:
        return pubtools.PubMedSearcher().search_one(doi)
    except:
        pass

def scrape_plos_findcited(findcited_url):
    
    req = requests.get(findcited_url)
    html = req.text
    html_parsed = BS(html)

    links = html_parsed(
        'a',
        onclick=re.compile('ambrafindarticle', re.I)
    )
    
    pmid = None

    for link in links:
        
        # Get HREF
        try:
            href = link['href']
        except:
            continue
        
        # Check for DOI
        dois = get_dois(href)
        if dois:
            pmid = doi_to_pmid(dois[0])
            if pmid:
                break
        
        # Check for PubMed info
        if ncbi_ptn.search(href):
            
            parsed_url = urlparse.urlparse(href)
            if not hasattr(parsed_url, 'query'):
                continue
            parsed_query = urlparse.parse_qs(parsed_url.query)
            if 'term' not in parsed_query:
                continue
            term = parsed_query['term']
            if type(term) == list:
                term = term[0]
            term_unquote = urllib.unquote_plus(term)
            print term_unquote
            try:
                pmid = pubtools.PubMedSearcher().search_one(term_unquote)
                break
            except Exception as e:
                print e.message
                continue

    if pmid:

        pubmed_xml = pubtools.efetch_pmid(pmid)
        art_info = pubtools.PubMedXML(pubmed_xml).parse()

        return art_info
