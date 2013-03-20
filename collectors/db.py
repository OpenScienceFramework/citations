
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

class IncompleteDocumentException(Exception):
  pass

class DB(object):
  
  # Fields that all documents must have
  required_fields = ['author', 'title', 'date']

  def __init__(self):
    
    # Set up database
    coll = MongoClient()
    self.citations = coll.citations
    self.documents = self.citations.documents
    self.batches = self.citations.batches
  
  def last_date_range(self, source):
    
    return self.batches.find({'source' : source})\
    .sort('from', DESCENDING)\
    .limit(1)

  def add_date_range(self, source, date_from, date_until):
    
    self.batches.insert({
      'source' : source,
      'from' : date_from,
      'until' : date_until,
    })
   
  def add_or_update(self, document):
    '''Add document to database or update existing document(s).

    '''
    
    # Raise exception if fields missing
    if not all([field in document['data'] for field in self.required_fields]):
      raise IncompleteDocumentException
    
    # Build query
    query = {
      'data.title' : document['data']['title'],
      'data.author.0.family-name' : document['data']['author'][0]['family-name'],
      'data.date' : document['data']['date'],
    }
    
    # Run query
    results = self.documents.find(query)
    
    # Check results for conflicts
    all_conflicts = True
    for result in results:
      union_keys = set(result['data'].keys()) & set(document['data'].keys())
      if any([result['data'][key] != document['data'][key] for key in union_keys]):
        # Conflict: Add conflict? to existing result
        found_conflict = True
        document['flags']['conflict?'] = True
        db.documents.update(
          {'_id' : result['_id']},
          {'$set' : {
            'flags.conflict?' : True,
          }},
        )
      else:
        # No conflict: Update existing result
        db.documents.update(
          {'_id' : result['_id']},
          {
            '$set' : {'data' : document['data']},
            '$pushAll' : {'sources' : document['sources']},
          }
        )
        all_conflicts = False

    # Insert document if no matches or all conflicts
    if results is None or all_conflicts:
      db.documents.insert(document)
