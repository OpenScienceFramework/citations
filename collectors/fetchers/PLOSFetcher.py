# Imports

from . import *

class PLOSFetcher(Fetcher):
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
        pub_link = pubtools.pmid_to_publisher(pmid)
        
        # Get HTML text
        req = requests.get(pub_link)
        return req.text
