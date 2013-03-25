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

# Imports
import re
import requests
from BeautifulSoup import BeautifulSoup as BS

from ..utils import pubtools

# Parameters
timeout = 15

# URLs
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
