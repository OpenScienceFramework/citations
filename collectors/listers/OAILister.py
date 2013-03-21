from . import *

class OAILister(TermLister):

  term = 'open access[filter]'

  def_params = { 
    'db' : 'pmc',
    'rettype' : 'xml',
    'retmax' : 9999999,
  }
