"""
Tests db class functionality
(1) : Documents are identical -- keep original
(2) : Union of documents is identical
      -- differences of documents is merged
(3) : Union of documents is not identical
      -- add new document - flag both with 'conflict?'
@TODO: modularize the tests to a JSON library
@TODO: think about changing 'conflict?' flag to list of _fields_ in conflict      
"""

from pymongo import MongoClient
import Document
import db

# setup a MongoClient
#testCollection = MongoClient()
# instantiate the database
#testDB = testCollection.DB
# setup a collection within the database
#testDocuments = testDB.documents

# instantiate the db object
db = db.DB() 

##############
# test input #
##############


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
document_one = Document.Document(test_doc_one)
#print document_one.document

# document two -- replicates document one
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

document_two = Document.Document(test_doc_two)

# test that insertions of equal documents don't duplicate
db.add_or_update(document_one)
db.add_or_update(document_two)
print(db.documents.find({'uid' : document_two.getUID()}))
print(db.documents.count())

# document three -- replicates document one with additional fields
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

# create document three
document_three = Document.Document(test_doc_three)

# add document to the database 
db.add_or_update(document_three)
# ensure that there is not additional entry in the db
# and that the new fields have been merged with the existing
# document
print(db.documents.find({'uid': document_one.getUID()})[0]['properties'])
print(db.documents.count())


# document three -- replicates document three with fields that have conflict
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

# create document four
document_four = Document.Document(test_doc_four)
# add document to the database
db.add_or_update(document_four)
# ensure that an additional entry exists and that both have 'conflict?' flags set to True
for document in db.documents.find({'uid': document_one.getUID()}):
    print '\n', document
print(db.documents.count())

# purge the database of alterations
db.documents.remove()
