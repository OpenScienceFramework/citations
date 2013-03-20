'''
Parses, constructs, and returns document objects. Interacts with corresponding source CorpusController.

Parameters:
   html/xml/... : Raw document data to be parsed
Returns:
   Document : Document object constructed
'''
from BeautifulSoup import BeautifulSoup as BS

# Abstract parsing class
class Parser(object):
  
  # Extrapolates document fields and returns a document object
  def parse(self):
    raise NotImplementedError
  
  # Extracts and returns set of documents to be parsed
  def extract(self):
    raise NotImplementedError

# Parser designed to intereact with PLOS
class PLOSParser(Parser):
  
  # Extapolate document fields and return the corresponding document object
  def parse(self, html):
    
    # Parse HTML
    html_parse = BS(html)

    # Get reference container
    ref_container = html_parse.find('ol', {'class' : 'references'})
    if not ref_container:
      return

    # Get references
    refs = ref_container.findAll('li')
    refs = [{'text' : ''.join(ref.findAll(text=True))} for ref in refs]

    return refs
  
  # Extract reference fields and return list of references to be parsed
  def extract(self):
    
    pass
