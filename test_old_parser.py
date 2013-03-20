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

def pytest_generate_tests(metafunc):
    names = glob.glob("tests/*.json")
    for name in names:
        with open(name) as f:
            citations = json.load(f)
        metafunc.parametrize('cit', citations)
        metafunc.parametrize('name', names)

def check_parse(name, cit):
    test_name = 'test in {} - {}'.format(name, cit['raw'])
    a = citation.Citation.parse(cit['raw'])
    b = cit
    for k in unneeded_tags:
        if k in a:
            del a[k]
        if k in b:
            del b[k]
    assert a == b
