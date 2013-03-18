import json
import glob
import unittest
import networkx as nx
import matplotlib.pyplot as plt

from Citation import Citation


class CheckCitation(unittest.TestCase):
    pass

def test_generator(a, b):
    """Return a dynamic test function for comparing two dictionaries."""
    def test(self):
        self.assertDictEqual(a, b)

    return test

def clean(d):
    """Return dictionary with the key/values we don't want to test removed."""
    for k in ['raw', 'type', 'style', 'post', 'page', 'volume', 'DOI', 'references', 'UID']:
        del d[k]
    return d

def graph(results):
    """Graph the resulting citation graph."""
    g = nx.Graph()
    for article in results:
        g.add_node(results[article]['issued'])
    pos = nx.shell_layout(g)
    nx.draw(g, pos)
    plt.show()

def create_tests():
    results = {}
    for name in glob.glob("tests/*.json"):
        with open(name) as f:
            citations = json.load(f)
            for citation in citations:
                test_name = 'test in {} - {}'.format(name, citation['raw'])
                test = test_generator(clean(Citation.parse(citation['raw'])), clean(Citation(**citation)))
                setattr(CheckCitation, test_name, test)

                temp = Citation.parse(citation['raw'])
                tempUID = temp['UID']
                results[tempUID] = temp
    return results

results = create_tests()

if __name__ == '__main__':
    graph(results)
    unittest.main()
