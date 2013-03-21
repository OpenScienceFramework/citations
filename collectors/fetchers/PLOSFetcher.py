from . import *

class PLOSFetcher(Fetcher):
  '''Fetcher class designed to fetch data from PLOS

  '''
  
  def fetch_target(self, doi=None, pmid=None):
    '''Fetch and return a target document
       args: 
         doi: doi of target document
         pmid: pmid of target document
       returns:
         html version of target docment 
    '''
    
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
