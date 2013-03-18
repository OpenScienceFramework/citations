import json
import glob
import unittest
import networkx as nx
import matplotlib.pyplot as plt

from Citation import Citation

unneeded_tags = ['raw', 'type', 'style', 'post', 'page', 'volume', 'DOI',
                 'references', 'UID']

class CheckCitation(unittest.TestCase):
    pass

def create_tests():
    for name in glob.glob("tests/*.json"):
        with open(name) as f:
            citations = json.load(f)
        for citation in citations:
            test_name = 'test in {} - {}'.format(name, citation['raw'])
            a = Citation.parse(citation['raw'])
            b = Citation(**citation)
            for k in unneeded_tags:
                del a[k]
                del b[k]
            def test(self):
                assert a == b
            setattr(CheckCitation, test_name, test)

create_tests()
