import json
import glob
import unittest
import networkx as nx
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

import citation

unneeded_tags = ['raw', 'type', 'style', 'post', 'page', 'volume', 'DOI',
                 'references', 'UID']

class CheckCitation(unittest.TestCase):
    pass

def create_tests():
    for name in glob.glob("tests/*.json"):
        with open(name) as f:
            citations = json.load(f)
        for cit in citations:
            test_name = 'test in {} - {}'.format(name, cit['raw'])
            a = citation.Citation.parse(cit['raw'])
            b = cit
            for k in unneeded_tags:
                if k in a:
                    del a[k]
                if k in b:
                    del b[k]
            def test(self):
                assert a == b
            setattr(CheckCitation, test_name, test)

create_tests()
