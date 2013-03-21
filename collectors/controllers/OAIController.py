from . import *

from ..fetchers import OAIFetcher
from ..parsers import OAIParser

class OAIController(CorpusController):
  '''CorpusController designed for the OAI database
  
  '''

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
    #fetcher = fetchers.OAIFetcher.OAIFetcher()
    fetcher = OAIFetcher.OAIFetcher()
    doc_batches = fetcher.fetch_batch(date_from, date_until, **kwargs)

    # Initialize parser
    parser = OAIParser.OAIParser()
    #parser = parsers.OAIParser()

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
