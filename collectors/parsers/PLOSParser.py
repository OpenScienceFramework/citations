from . import *

class PLOSParser(Parser):
  '''Parser designed to interact with PLOS

  '''
  
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
