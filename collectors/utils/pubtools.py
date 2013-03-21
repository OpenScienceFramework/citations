# Set up Entrez
from Bio import Entrez
Entrez.email = 'jm.carp@gmail.com'

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

  def _get_article_title(self):
    title = self.xml_parse.find(re.compile('article-title'))
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

  def _get_authors(self):
    authors_xml = self.xml_parse.findAll('author')
    if authors_xml:
      authors = []
      for author_xml in authors_xml:
        author = {}
        last = author_xml.find('lastname')
        if last:
          author['family-name'] = unicode(last.string)
        frst = author_xml.find('forename')
        if frst:
          author['given-name'] = unicode(frst.string)
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
