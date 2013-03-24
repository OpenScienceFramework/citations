'''
Controller for handling add requests and queries to/from
MongoDB.

Database:
citations.documents -- MongoDB collection storing document objects
citations.batches -- MongoDB collection storing batch date information from various source Fetcher()s
'''

###########
# Imports #
###########

# Set up PyMongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

import Document

class Database(object):
    '''Interface to MongoDB'''
  
    def __init__(self, *args, **kwargs):
        
        # Set up database
        connection = MongoClient(*args, **kwargs)
        database = connection.data
        self.documents = database.documents
        self.queries = database.queries
        self.batches = database.metadata
    
    def insert_query(self, query):
        '''Insert metadata about a query.

        '''
        
        self.queries.insert(query)

    def last_date_range(self, source):
        '''returns the last datetime a source was probed for document data

        '''
        
        return self.batches.find({'source': source})\
            .sort('from', DESCENDING)\
            .limit(1)

    def add_date_range(self, source, date_from, date_until):
        '''adds or updates the datetime a source was probed for document data

        '''
    
        self.batches.insert({
            'source': source,
            'from': date_from,
            'until': date_until,
        })
   
    def add_or_update(self, doc):
        '''Add or update a document to the database. If document conflicts
        with other documents in the database, flag all as conflicted and
        created duplicate records.

        Args:
            doc (Document) : document to be added / updated
        Returns:
            list of database IDs added / updated

        '''
    
        # doc must be a Document instance
        if not isinstance(doc, Document.Document):
            raise TypeError('add_or_update() must take a Document()')

        # Check for document in database
        results = self.documents.find({
            'uid' : doc.getUID(),
        })
    
        # Check results (documents found in the db) for conflicts with 
        # the document to be added/updated
        updated_ids = []
        all_conflicts = True
        for result in results:
      
            # Get keys common to both stored and new documents
            result_keys = set(result['properties'].keys())
            document_keys = set(doc.document['properties'].keys())
            union_keys = result_keys & document_keys

            if any([result['properties'][key] != doc.document['properties'][key] 
                    for key in union_keys]):
                # if a conflict is found: Add conflict? to existing result
                found_conflict = True
                doc.document['flags']['conflict?'] = True
                self.documents.update(
                    {'_id' : result['_id']},
                    {'$set' : {
                        'flags.conflict?' : True,
                    }},
                )
            else:
                # else: Update existing result
                self.documents.update(
                    {'_id' : result['_id']},
                    {
                        '$set' : {'properties' : doc.document['properties']},
                        '$addToSet' : {'source' : {'$each' : doc.document['source']}},
                    }
                )
                updated_doc = self.documents.find_one(
                    {'_id' : result['_id']},
                    {'uid' : 1},
                )
                updated_ids.append(updated_doc['uid'])
                all_conflicts = False

        # if there is no conflict and the document does not already exist
        # in the database, add it
        if results is None or all_conflicts:
            new_doc_id = self.documents.insert(doc.document)
            new_doc = self.documents.find_one(
                {'_id' : new_doc_id},
                {'uid' : 1},
            )
            return [new_doc['uid']]
        return updated_ids
