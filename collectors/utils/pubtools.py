# Imports

import re
import copy
import inspect
import requests

from BeautifulSoup import BeautifulSoup as BS

# Set up Entrez
from Bio import Entrez
Entrez.email = 'jm.carp@gmail.com'

pubmed_base_url = 'http://www.ncbi.nlm.nih.gov/pubmed'

def pmid_to_document(pmid):
    
    xml = efetch_pmid(pmid)
    doc = PubMedXML(xml).parse()
    return doc

def efetch_pmid(pmid):
    '''Query PubMed API by PMID; return XML.
      
      Args:
          pmid (int/str) : PubMed ID
      Returns:
          PubMed XML
  
    '''
    
    return Entrez.efetch(
        db='pubmed',
        retmode='xml',
        id=pmid
    ).read()

class NotOneResultException(Exception):
    pass

class PubMedSearcher(object):
    
    DEFAULT_PARAMS = {
        'db' : 'pubmed',
        'rettype' : 'xml',
        'retmax' : 999999,
    }

    def search(self, term, extra_params={}):
        params = copy.deepcopy(self.DEFAULT_PARAMS)
        params.update(extra_params)
        search = Entrez.read(
            Entrez.esearch(term=term, **params)
        )
        return search['IdList']

    def search_one(self, term, extra_params={}):
        extra_params_copy = copy.deepcopy(extra_params)
        extra_params_copy['retmax'] = 2
        ids = self.search(term, extra_params_copy)
        if len(ids) == 1:
            return ids[0]
        raise NotOneResultException('Got %d results' % (len(ids)))

def pmid_to_publisher(pmid):
    '''Get publisher link from PubMed.

    Args:
        pmid (int / str) : PubMed ID
    Returns:
        pub_link : Link to document on publisher site

    '''
    
    # Get PubMed URL
    pm_url = '%s/%s' % (pubmed_base_url, pmid)
    
    # Get PubMed HTML
    req = requests.get(pm_url)
    html = req.text

    # Find full text link
    html_parse = BS(html)
    pub_link = html_parse.find(
        'a',
        title=re.compile('^full text', re.I)
    )

    # Return link href
    try:
        return pub_link['href']
    except:
        return ''

class MultiFunParser(object):
  
    def parse(self):
        
        # Initialize information
        info = {}
    
        # Get _get* methods
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        methods = [m for m in methods if m[0].startswith('_get')]
    
        # Apply methods
        for method in methods:
            key = re.sub('_get_', '', method[0])
            key = key.replace('_', '-')
            value = method[1]()
            info[key] = value
    
        # Done
        return info

class PubMedXML(MultiFunParser):
    '''Extract meta-data from PubMed XML
    
    '''

    def __init__(self, xml):
        self.xml = xml
        self.xml_parse = BS(xml)

    def _get_abstract(self):
        abstract = self.xml_parse.find(re.compile('abstracttext', re.I))
        if abstract:
            return unicode(abstract.string)

    def _get_title(self):
        title = self.xml_parse.find(re.compile('article-?title'))
        if title:
            return ''.join(title.findAll(text=True))

    def _get_journal_title(self):
        journal = self.xml_parse.find('journal')
        if journal:
            title = journal.find('title')
            if title:
                return unicode(title.string)

    def _get_keywords(self):
        keywords = self.xml_parse.findAll('kwd')
        return [unicode(keyword.string) for kewword in keywords]
    
    def _get_date(self):
        pubdate = self.xml_parse.find('pubdate')
        if pubdate:
            year = pubdate.find('year')
            return unicode(year.string)

    def _get_author(self):
        authors_xml = self.xml_parse.findAll('author')
        if authors_xml:
            authors = []
            for author_xml in authors_xml:
                author = {}
                last = author_xml.find('lastname')
                if last:
                    author['family'] = unicode(last.string)
                frst = author_xml.find('forename')
                if frst:
                    author['given'] = unicode(frst.string)
                if author:
                    authors.append(author)
            return authors

    def _get_pages(self):
        pages_xml = self.xml_parse.find('medlinepgn')
        if pages_xml:
            pages = {}
            pages_split = pages_xml.string.split('-')
            ndigit_first = len(pages_split[0])
            pages['first'] = pages_split[0]
            if len(pages_split) > 1:
                ndigit_last = len(pages_split[1])
                pages['last'] = pages_split[0][:ndigit_first-ndigit_last] + pages_split[1]
            return pages
