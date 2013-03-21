from . import *

class OAIFetcher(Fetcher):
  '''Fetcher class designed to fetch data from OAI

  '''

  # TODO: store history of requests in db
  
  # Print format for datetime objects
  date_fmt = '%Y-%m-%d'

  def fetch_batch(self, date_from=None, date_until=None):
    '''Fetch and return a batch of documents.

       args:
         date_from : datetime - start date of batch request
         date_until : datetime - stop date of batch request
       returns:
         docs : a generator of raw documents in xml

    '''
    
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

    # Fetch XML from OAI
    xml = self.query(**params)
    
    # Parse XML
    xml_parse = BS(xml)
    
    # Extend records to docs
    yield xml_parse.findAll('record')
    
    # Get resumption token
    token = xml_parse.find(re.compile('resumptiontoken', re.I))
    
    # Loop until no token
    while token:
      params['resumptionToken'] = token.text
      xml = self.query(**params)
      xml_parse = BS(xml)
      token = xml_parse.find(re.compile('resumptiontoken', re.I))
      yield xml_parse.findAll('record')
    
  def query(self, **kwargs):
    '''Retrieve articles from PMC-OAI in XML format

    Args:
      kwargs (dict): Parameters accepted by PMC-OAI
    Returns:
      Raw XML from PMC OAI
    '''
    
    # Delete extra parameters -- resumptionToken specific requirement
    if 'resumptionToken' in kwargs:
      for extra_param in ['from', 'until', 'metadataPrefix']:
        if extra_param in kwargs:
          del kwargs[extra_param]

    # Build URL for request
    url_params = '&'.join(['%s=%s' % (key, val) for key, val in kwargs.iteritems()])
    url = '%s?%s' % (oai_base_url, url_params)

    # Get and return XML from OAI
    req = requests.get(url)
    return req.text
