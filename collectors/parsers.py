
from BeautifulSoup import BeautifulSoup as BS

class Parser(object):
  
  def parse(self):
    raise NotImplementedError
  
  def extract(self):
    raise NotImplementedError

class PLOSParser(Parser):
  
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
  
  def extract(self):
    
    pass
