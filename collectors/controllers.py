
import sys


class CorpusController(object):

  def __init__(self, db=db):
    self.db = db
  
  def batch(self, source):
    
    pass

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
  
  def batch(self, date_incr=datetime.timedelta(weeks=2)):
    
    ## Get date of last completed batch
    #date_from = ...
    #date_until = date_from + date_incr

    # Fetch batch of articles
    fetcher = OAIFetcher()
    documents = fetcher.batch(date_from, date_until)

    # Pass fetched articles to Parser
    parser = OAIParser()
    for document in documents:
      doc_parsed = parser.parse(article)

    ## Send parsed articles in DB
    self.db.add_or_update(doc_parsed)
    #self.dbin.add_or_update(doc_parsed)

