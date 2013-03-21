# Imports

import re
from BeautifulSoup import BeautifulSoup as BS

from .. import Document 

class Parser(object):
  '''Abstract parsing class

  '''
  
  # Extrapolates document fields and returns a document object
  def parse(self):
    raise NotImplementedError
  
  # Extracts and returns set of documents to be parsed
  def extract(self):
    raise NotImplementedError
