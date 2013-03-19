# Set up BioPython
from Bio import Entrez
Entrez.email = 'jm.carp@gmail.com'

class Lister(object):
  
  def_params = {
    'db' : 'pubmed',
    'rettype' : 'xml',
    'retmax' : 9999999,
  }

  def get_article_list(self):
    raise NotImplementedError

class PublisherLister(Lister):
  
  journals = []

  def get_article_list(self):
   
    term = ' OR '.join(['("%s"[journal])' % journal for journal in self.journals])
    search = Entrez.read(
      Entrez.esearch(term=term, **self.def_params)
    )
    return search['IdList']

class PLOSLister(PublisherLister):
  
  # TODO: update this
  journals = ['plos one', 'plos biology']

class FrontiersLister(PublisherLister):

  # TODO: update this
  journals = ['frontiers in neuroscience', 'frontiers in psychology']

class TermLister(Lister):

  term = ''

  def get_article_list(self):

    search = Entrez.read(
      Entrez.esearch(term=self.term, **self.def_params)
    )
    return search['IdList']

class OAILister(TermLister):

  term = 'open access[filter]'

  def_params = {
    'db' : 'pmc',
    'rettype' : 'xml',
    'retmax' : 9999999,
  }

