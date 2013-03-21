"""
Tests db class functionality
(1) : Documents are identical -- keep original
(2) : Union of documents is identical
      -- differences of documents is merged
(3) : Union of documents is not identical
            -- add new document - flag both with 'conflict?'
            @TODO: think about changing 'conflict?' flag to list of _fields_ in conflict      
# @TODO: Derive a better way of determing the difference between two dicts
"""

import unittest
import db
import Document

class dbTest(unittest.TestCase):

    # instantiate the database controller
    def setUp(self):
        self.db = db.DB()

        # documents for testing
        test_doc_one = {'properties': {
             'author': [
                 {'family': 'smith', 'given': 'john'}
             ],
             'date': 1999,
             'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209    834',

             },
             'flags': {
                  'hasBeenParsed': False
             },
             'source': ['oai'],
             'raw': 'asdfjiuawhefuahdslfkjhsadlkfh'
        }
        self.doc_one = Document.Document(test_doc_one)
        test_doc_two = {'properties': {
             'author': [
                 {'family': 'smith', 'given': 'john'}
             ],
             'date': 1999,
             'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209    834',

             },
             'flags': {
                  'hasBeenParsed': False
             },
             'source': ['oai'],
             'raw': 'asdfjiuawhefuahdslfkjhsadlkfh'
        }
        self.doc_two = Document.Document(test_doc_two)
        test_doc_three = {'properties': {
             'author': [
                 {'family': 'smith', 'given': 'john'}
             ],
             'date': 1999,
             'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209    834',
             'first-page': '323',
             'last-page': '431',
             },
             'flags': {
                  'hasBeenParsed': False
             },
             'source': ['oai'],
             'raw': 'asdfjiuawhefuahdslfkjhsadlkfh'
        }
        self.doc_three = Document.Document(test_doc_three)
        test_doc_four = {'properties': {
             'author': [
                 {'family': 'smith', 'given': 'john'}
             ],
             'date': 1999,
             'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209    834',
             'first-page': '323',
             'last-page': '500',
             },
             'flags': {
                  'hasBeenParsed': False
             },
             'source': ['oai'],
             'raw': 'asdfjiuawhefuahdslfkjhsadlkfh'
        }
        self.doc_four = Document.Document(test_doc_four)
    
    # remove all new entries to the database
    def tearDown(self):
        self.db.documents.remove()

    # test ability to add an item to the database
    def testAdd(self):
        # get initial count of the database
        intial_count = self.db.documents.count()
        # add new document to the datbase
        self.db.add_or_update(self.doc_one)
        added = self.db.documents.find_one({'uid': self.doc_one.getUID()})
        # get the final count of database
        final_count = self.db.documents.count()
  
        # assert document added is equal to document stored 
        self.assertEqual(self.doc_one.document, added)
        # assert database increased by _one_ object
        self.assertEqual(intial_count, (final_count - 1)) 

    # test adding two identical documents
    def testAddWithIdenticalField(self):
        # get the initial count of the db
        initial_count = self.db.documents.count()
        
        # add the first document and get the db count
        self.db.add_or_update(self.doc_one)
        after_one_count = self.db.documents.count()
        
        # add the second document and get the db count
        self.db.add_or_update(self.doc_two)
        after_two_count = self.db.documents.count()
        
        # assert only one document was actually added
        self.assertEqual(after_one_count, after_two_count) 
        
        # assert database object is equivalent original document added
        added = self.db.documents.find({'uid': self.doc_two.getUID()})[0]
        self.assertEqual(self.doc_one.document, added)      

    # test adding a second document with an additional field
    def testAddWithNewField(self):
        # get the initial count of the db
        intial_count = self.db.documents.count()
        
        # add the first document and get the db count
        self.db.add_or_update(self.doc_one)
        after_one_count = self.db.documents.count()
        
        # add the second document and get the db count
        self.db.add_or_update(self.doc_three)
        after_two_count = self.db.documents.count()        

        # assert second document was merged with the first in the db
        self.assertEqual(after_one_count, after_two_count)
        final_doc = self.db.documents.find({'uid': self.doc_one.getUID()})[0]
        

    # test adding a third document with a conflicting field
    # @TODO: Potential issue -- should add_or_update() return the objectID from MongoDB?
    def testAddWithConflict(self):
        # get the initial count of the database
        initial_count = self.db.documents.count()

        # add the first document and get the db count
        self.db.add_or_update(self.doc_three)
        after_one_count = self.db.documents.count()

        # add the conflicting document and get the db count
        self.db.add_or_update(self.doc_four)
        after_two_count = self.db.documents.count()

        # assert both Documents were added to the db
        self.assertTrue((after_two_count - initial_count), 2)

        # assert both Documents have 'conflicts?' set to true
        first = self.db.documents.find({'flags.conflict?': True})[0]
        second = self.db.documents.find({'flags.conflict?': True})[1]
        self.assertEqual(first['flags']['conflict?'], second['flags']['conflict?'])
        # assert expected conflict fields are not equal
        self.assertNotEqual(first['properties']['last-page'], second['properties']['last-page'])

if __name__ == '__main__':
    unittest.main()
