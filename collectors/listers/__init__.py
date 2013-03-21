# Set up BioPython
from Bio import Entrez
Entrez.email = 'jm.carp@gmail.com'

class Lister(object):
  
  def_params = { 
    'db' : 'pubmed',
    'rettype' : 'xml',
    'retmax' : 9999999,
  }

  def list_documents(self):
    raise NotImplementedError

class TermLister(Lister):

  term = ''

  def list_documents(self):

    search = Entrez.read(
      Entrez.esearch(term=self.term, **self.def_params)
    )   
    return search['IdList']

class MultiJournalLister(TermLister):
  
  journals = []
  term = ' OR '.join(['("%s"[journal])' % journal for journal in journals])
