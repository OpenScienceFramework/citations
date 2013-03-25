# Imports

from . import *
from ..utils.web import requests_get

class FrontiersFetcher(Fetcher):
    '''Fetcher class designed to fetch data from PLOS
    
    '''
  
    def fetch_target(self, pmid):
        '''Fetch and return a target document
           args: 
             doi: doi of target document
             pmid: pmid of target document
           returns:
             html version of target docment 
        '''
        
        # Get publisher link
        pub_link_orig = pubtools.pmid_to_publisher(pmid)
        
        # Redirect to full-text link
        req_orig = requests_get(pub_link_orig, timeout=timeout)
        pub_link = re.sub('abstract', 'full', req_orig.url)
        
        # Get HTML text
        req = requests_get(pub_link, timeout=timeout)
        return req.text
