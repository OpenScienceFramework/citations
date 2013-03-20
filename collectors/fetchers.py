''' 
Retrieves either raw target document data or a batch of raw document
data from a speciifed source.

Parameters:
  fetch_target()
    document id : Some way of identifying a document from a speciifed 
    source
  fetch_batch()
    constraints : Some set of constraints for the size, time, delay, or
    other relavent factors for a batch request.
Returns:
  raw_doc_data : The raw data for a target document or batch of
    target documents
'''
import re
import requests
from BeautifulSoup import BeautifulSoup as BS

doi_base_url = 'http://dx.doi.org'
oai_base_url = 'http://www.pubmedcentral.gov/oai/oai.cgi'

# Abstract fetcher class
class Fetcher(object):
  
  # Fetches and returns raw document data for a specific document
  def fetch_target(self):
    raise NotImplementedError

  # Fetches and returns raw document data for a batch of documents
  def fetch_batch(self):
    raise NotImplementedError

# Fetcher class designed to fetch data from PLOS
class PLOSFetcher(Fetcher):
  
  '''Fetch and return a target document
     params: 
       doi: doi of target document
       pmid: pmid of target document
     returns:
       html version of target docment 
  '''
  def fetch_target(self, doi=None, pmid=None):
    
    # Get DOI if missing
    if pmid and not doi:

      xml = efetch_pmid(pmid)
      xml_parse = BS(xml)
      doi = pubxml.find('articleid', idtype='doi')
    
    # Build publisher link
    pub_link = '%s/%s' % (doi_base_url, doi)
    
    # Get HTML text
    req = requests.get(publink)
    return req.text

# Fetcher class designed to fetch data from OAI
class OAIFetcher(Fetcher):

  # TODO: store history of requests in db
  
  # Print format for datetime objects
  date_fmt = '%Y-%m-%d'

  '''Fetch and return a batch of documents
     params:
       date_from : datetime - start date of batch request
       date_until : datetime - stop date of batch request
     returns:
       docs : a list of raw documents in xml
  '''
  def fetch_batch(self, date_from=None, date_until=None):
    
    # Default query parameters
    params = {
      'verb' : 'ListRecords',
      'metadataPrefix' : 'pmc',
    }
    
    # Get start date
    if date_from:
      params['from'] = date_from.strftime(self.date_fmt)
    
    # Get stop date
    if date_until:
      params['until'] = date_until.strftime(self.date_fmt)
    
    # Initialize documents
    docs = []

    # Fetch XML
    xml = self.query(**params)
    
    # Parse XML
    xml_parse = BS(xml)
    
    # Extend records to docs
    yield xml_parse.findAll('record')
    #docs.extend(xml_parse.findAll('record'))
    
    # Get resumption token
    token = xml_parse.find(re.compile('resumptiontoken', re.I))
    
    # Loop until no token
    while token:
      params['resumptionToken'] = token.text
      xml = self.query(**params)
      xml_parse = BS(xml)
      yield xml_parse.findAll('record')
      #docs.extend(xml_parse.findAll('record'))
      token = xml_parse.find(re.compile('resumptiontoken', re.I))
    
    ## Done
    #return docs

  '''Gets documents from PMC OAI in XML
     params : params
     returns : 
  '''
  def query(self, **kwargs):
    '''Get articles from PMC OAI in XML format.
    '''
    
    print 'Querying OAI with params %s...' % (kwargs)
    
    # Delete extra parameters
    if 'resumptionToken' in kwargs:
      for extra_param in ['from', 'until', 'metadataPrefix']:
        if extra_param in kwargs:
          del kwargs[extra_param]

    # Build URL
    url_params = '&'.join(['%s=%s' % (key, val) for key, val in kwargs.iteritems()])
    url = '%s?%s' % (oai_base_url, url_params)

    # Get XML from OAI
    req = requests.get(url)
    return req.text
