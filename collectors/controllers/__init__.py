'''
Represents the interface between user and location, addition, 
and querying of documents to and from the database.
'''

# Imports 
import sys 
import datetime

#from listers import *
#from fetchers import *
#from parsers import *
#import listers
#import fetchers
#import parsers

from .. import fetchers

#import db
from .. import db

class CorpusController(object):

  def __init__(self, _db=None):
    if _db is None:
      _db = db.DB()
    self.db = _db
  
  # obtains, constructs, and adds a batch of documents form a source
  def batch(self, source):
    
    pass #TODO

  # obtains, constructs, and adds a target document from a source
  def target(self, article):

    pass #TODO

  def hybrid(self, source):

    # Get current module
    module = sys.modules[__name__]

    ## Get utility classes
    lister = getattr(module, '%sLister' % (source))
    fetcher = getattr(module, '%sFetcher' % (source))
    parser = getattr(module, '%sParser' % (source))

    source_pmids = lister().get_article_list()

    db_pmids = db.citations.documents.find({}, {'pmid' : 1}) 
    db_pmids = [pmid['pmid'] for pmid in db_pmids]
    pmids_to_fetch = list(set(source_pmids) - set(db_pmids))

    print '%s pmids from source...' % (len(source_pmids))
    print '%s pmids from db...' % (len(db_pmids))
    print '%s pmids to parse...' % (len(pmids_to_fetch))

    return

    for pmid in pmids_to_fetch:
      doc = fetcher(pmid).fetch()
      refs = parser(doc).parse_head_ref()
      # send stuff to db...
