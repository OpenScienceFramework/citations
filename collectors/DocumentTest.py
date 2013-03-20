from Document import Document
import pprint

# test doc one for uid only
test_doc_one = {'properties': {
    'author': [
        {'family': 'smith', 'given': 'john'}
    ],
    'date': 1999999999,
    'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209834',

    },
    'flags': {
         'hasBeenParsed': False
    },
    'source': ['oai'],
    'raw': 'asdfjiuawhefuahdslfkjhsadlkfh'
}

# test  doc two for uid only
test_doc_two = {'properties': {
    'author': [
        {'family': 'smith', 'given': 'john'}
    ],
    'date': 1999,
    'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209834',
    },
    'flags': {
        'hasBeenParsed': False
    },
    'source': ['oai'],
    'raw': 'SdFlweijrlsijerlkfjlsiejlijsliejrlijsdvlijwleijlijflijsdlijfwe'
}

# test creation of document objects
result_one = Document(test_doc_one)
result_two = Document(test_doc_two)

# test uids from to separate dicts with the same data are equal
print(result_one.document['uid'] == result_two.document['uid'])

# test doc one for data population
test_doc_three = {'properties': {
    'author': [
        {'family': 'smith', 'given': 'john'},
        {'family': 'johnson', 'given': 'joshua'}
    ],
    'date': 1999,
    'title': 'some randome title @#$@# 234 s0d9 2309 80928304982 209834',
    'front-page': '123',
    'last-page': '144',
    'container-title': 'Journal of flavor-flav',
    },
    'flags': {
        'hasBeenParsed': False
    },
    'source': ['oai'],
    'raw': 'ALDSKJFAWEOIJASD OFJA;OSIDJF ;OIJWAF ;OWAJEJW;OF;OWAJE;OIJFOIWAJOFAIWJEF OOISADJF;'
}

result_three = Document(test_doc_three)
print result_three.getUID()