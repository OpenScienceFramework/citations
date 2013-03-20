from Document import Document
import pprint

test_doc_one = {'data': {
    'author': [
        {'family-name': 'smith', 'given-name': 'john'}
    ],
    'date': 1999,
    'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209834',

},
    'flags': {
        'hasBeenParsed': False
    },
    'source': ['oai'],
}

test_doc_two = {'data': {
    'author': [
        {'family-name': 'smith', 'given-name': 'john'}
    ],
    'date': 1999,
    'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209834',

    },
           'flags': {
               'hasBeenParsed': False
           },
           'source': ['oai'],
           }

result_one = Document(test_doc_one)
result_two = Document(test_doc_two)

print 'here', result_one.document['uid']

print(result_one.document['uid'] == result_two.document['uid'])

