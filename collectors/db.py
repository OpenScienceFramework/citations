'''
Controller for handling add requests and queries to/from
MongoDB.

Database:
citations.documents -- MongoDB collection storing document objects
citations.batches -- MongoDB collection storing batch date information from various source Fetcher()s
'''
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

# @TODO: Implement this exception
# Excepetion thrown when an attempt to add an article
# missing required information
class IncompleteDocumentException(Exception):
  pass

# Controller class for handiling DB transactions
class DB(object):
  
  # Fields that all documents objects must have to be added
  required_fields = ['author', 'title', 'date']

  def __init__(self):
    
    # Set up database
    coll = MongoClient()
    self.citations = coll.citations
    self.documents = self.citations.documents
    self.batches = self.citations.batches
  
  # returns the last datetime a source was probed for document data
  def last_date_range(self, source):
    
    return self.batches.find({'source': source})\
        .sort('from', DESCENDING)\
        .limit(1)

  # adds or updates the datetime a source was probed for document data
  def add_date_range(self, source, date_from, date_until):
    
    self.batches.insert({
      'source': source,
      'from': date_from,
      'until': date_until,
    })
   
  '''
     Adds or updates a document to the database
     Params : 
       document - document to be added/updated
  '''
  def add_or_update(self, document):

    # @todo: Is it possible for a document to be corrupted between extraction and reinsertion?
    #if document.document.hasMinData():
    #    raise IncompleteDocumentException

    # Build query to check if document exists in the database
    query = {
      'data.title' : document['data']['title'],
      'data.author.0.family' : document['data']['author'][0]['family'],
      'data.date' : document['data']['date'],
    }
    
    # Run query 
    results = self.documents.find(query)
    
    # Check results (documents found in the db) for conflicts with 
    # the document to be added/updated
    all_conflicts = True
    for result in results:
      union_keys = set(result['data'].keys()) & set(document['data'].keys())
      if any([result['data'][key] != document['data'][key] for key in union_keys]):
        # if a conflict is found: Add conflict? to existing result
        found_conflict = True
        document['flags']['conflict?'] = True
        self.db.documents.update(
          {'_id' : result['_id']},
          {'$set' : {
            'flags.conflict?' : True,
          }},
        )
      else:
        # else: Update existing result
        self.db.documents.update(
          {'_id' : result['_id']},
          {
            '$set' : {'data' : document['data']},
            '$pushAll' : {'sources' : document['sources']},
          }
        )
        all_conflicts = False

    # if there is no conflict and the document does not already exist
    # in the database, add it
    if results is None or all_conflicts:
      self.db.documents.insert(document)