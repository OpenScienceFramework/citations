'''
Represents the interface between user and location, addition, 
and querying of documents to and from the database.
'''

# Imports 
import sys 
import datetime

from .. import database
from .. import Document
from ..utils import pubtools

from functools import wraps

def log_query(func):
    @wraps(func)
    def logged_func(self, *args, **kwargs):
        start_time = datetime.datetime.now()
        ids = func(self, *args, **kwargs)
        #TODO: Verify that ids are valid ids
        stop_time = datetime.datetime.now()
        query = {
            'name' : func.__name__,
            'klass' : self.__class__.__name__,
            'args' : args,
            'kwargs' : kwargs,
            'time' : {
                'start_time' : start_time,
                'stop_time' : stop_time,
            },
            'ids' : ids,
        }
        #TODO: Rename DB file / class
        self.database.insert_query(query)
    return logged_func

class CorpusController(object):

    # Abstract class variables

    @property
    def lister(self):
        raise NotImplementedError('Subclasses must implement lister')

    @property
    def fetcher(self):
        raise NotImplementedError('Subclasses must implement fetcher')

    @property
    def parser(self):
        raise NotImplementedError('Subclasses must implement parser')
    
    # Abstract methods

    def batch(self):
        raise NotImplementedError('Subclass must define batch()')

    def target(self):
        raise NotImplementedError('Subclass must define target()')
    
    def __init__(self, _database=None):
        if _database is None:
            _database = database.Database()
        self.database = _database

class PublisherCorpusController(CorpusController):
    
    @log_query
    def batch(self, max_count=50, overwrite=False):
        '''Process many articles from a publisher.

        '''
        
        # Get list of documents
        fetch_ids = self.lister().list_documents()

        # Remove finished IDs
        if not overwrite:
            db_ids = self.database.documents.find(
                {'properties.pmid' : {'$exists' : True}}, 
                {'properties.pmid' : 1}
            ) 
            db_ids = [id['properties']['pmid'] for id in db_ids]
            fetch_ids = list(set(fetch_ids) - set(db_ids))
        
        # Limit batch to max_count documents
        if max_count:
            fetch_ids = fetch_ids[:max_count]
        
        # Initialize all IDs
        all_ids = []

        # Loop over articles
        for id in fetch_ids:
            
            # Process document
            ref_ids, doc_id = self._process_one(id)
            all_ids.extend(ref_ids + [doc_id])
        
        # Return all IDs
        return all_ids
    
    @log_query
    def target(self, id, overwrite=False):
        '''Process one article from a publisher.

        '''
        
        #TODO: check overwrite
        
        # Process document
        ref_ids, doc_id = self._process_one(id)
        return ref_ids + [doc_id]
    
    def _process_one(self, id):
        '''Process one reference, specified by PubMed ID. Get list of articles
        using the lister class, download full text using the fetcher class,
        and extract and parse references using the parser class.

        This method is not normally called directly, but should be called by
        methods decorated with the @log_query decorator, such as batch()
        and target().

        '''

        print 'Working on article %s...' % (id)

        # Get document text
        print 'Getting document text...'
        text = self.fetcher().fetch_target(id)
        
        # Parse document
        print 'Parsing document...'
        ref_ids = []
        refs = self.parser().parse_document(text)
        for ref in refs:
            if not ref['ref']:
                print 'Incomplete reference. Skipping...'
                continue
            print 'Adding reference to database...'
            doc = Document.Document({
                'properties' : ref['ref'],
                'raw' : ref['raw'],
                'references' : [],
                'source' : ['pubmed'],
                'flags' : {}
            })
            ref_id = self.database.add_or_update(doc)
            ref_ids.append(ref_id)
        
        # Add head document to database
        print 'Adding head document to database...'
        properties = pubtools.pmid_to_document(id)
        properties['pmid'] = id
        doc = Document.Document({
            'properties' : properties,
            'raw' : text,
            'references' : ref_ids,
            'source' : ['pubmed'],
            'flags' : {},
        })
        doc_id = self.database.add_or_update(doc)

        return ref_ids, doc_id
