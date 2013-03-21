'''
Represents the interface between user and location, addition, 
and querying of documents to and from the database.
'''
import sys
import datetime

#from listers import *
#from fetchers import *
#from parsers import *
import listers
import fetchers
import parsers

import db

class CorpusController(object):

  def __init__(self, db=None):
    if db is None:
      db = db.DB()
    self.db = db
  
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
      refs = parser(doc).parse_head_ref()
      # send stuff to db...

# CorpusController designed for the OAI database
class OAIController(CorpusController):
  
  # Default start date for batch retrieval
  DATE_FROM = datetime.date(2010, 1, 1)

  # Default time window for batch retrieval
  DATE_INCR = datetime.timedelta(days=1)

  def batch(self, date_from=None, date_incr=DATE_INCR, **kwargs):
    '''Retrieve, parse, and push a batch of documents.

    Args:
      date_from (datetime.date): Start date
      date_incr (datetime.timedelta): Time window
      kwargs: Optional OAI parameters

    '''
    
    #TODO: save kwargs to query metadata

    # Get start date
    if not date_from:
      date_from = self.db.last_date_range('oai')[0]['until'] + \
        datetime.timedelta(days=1)

    # Get end date
    if date_incr:
      date_until = date_from + date_incr
    else:
      date_until = None

    # Fetch batch of articles
    fetcher = fetchers.OAIFetcher()
    doc_batches = fetcher.fetch_batch(date_from, date_until, **kwargs)
    
    # Initialize parser
    parser = parsers.OAIParser()

    # Loop over batches of articles
    for doc_batch in doc_batches:

      # Loop over articles in batch
      for doc in doc_batch:

        # Parse document
        parsed_docs = parser.parse_document(doc)

        # Send parsed articles to DB
        for doc in parsed_docs:
          self.db.add_or_update(doc)
    
    # Update date range
    self.db.add_date_range('oai', date_from, date_until)

# CorpusController designed for the Plos database 
class PLOSController(CorpusController):
    pass #@TODO: implement
