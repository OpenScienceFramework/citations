'''
Represents the interface between user and location, addition, 
and querying of documents to and from the database.
'''
import sys

from listers import *
from fetchers import *
from parsers import *

class CorpusController(object):

  def __init__(self, db):
    self.db = db
  
  # obtains, constructs, and adds a batch of documents form a source
  def batch(self, source):
    
    pass
  # obtains, constructs, and adds a target document from a source
  def target(self, article):

    pass

  def hybrid(self, source):

    # Get current module
    module = sys.modules[__name__]

    ## Get utility classes
    lister = getattr(module, '%sLister' % (source))
    #fetcher = getattr(module, '%sFetcher' % (source))
    #parser = getattr(module, '%sParser' % (source))

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
      refs = parser(doc).parse()
      # send stuff to db...

class OAIController(CorpusController):
  
  START_DATE = datetime.datetime(2010, 1, 1)

  def batch(self, date_from=None, date_incr=datetime.timedelta(days=1)):
    
    # Get date of last completed batch
    if not date_from:
      date_from = self.START_DATE
    date_until = date_from + date_incr

    # Fetch batch of articles
    fetcher = OAIFetcher()
    doc_batches = fetcher.fetch_batch(date_from, date_until)
    
    # Pass fetched articles to Parser
    parser = OAIParser()
    for doc_batch in doc_batches:
      for doc in doc_batch:
        doc_parsed = parser.parse(article)
        # Send parsed articles in DB
        self.db.add_or_update(doc_parsed)
    
    # Update date range
    self.db.add_date_range('oai', date_from, date_until)
