import json
import glob
import unittest
import networkx as nx
import matplotlib.pyplot as plt

from Citation import Citation


class CitationTest(unittest.TestCase):
    pass

# returns a dynamic test function for comparing two dictionaries
def test_generator(a, b):
    def test(self):
        # assert citations are equal
        self.assertDictEqual(a, b)

    return test

# return dictionary less the key/values we don't want to test
def clean(d):
    for k in ['raw', 'type', 'style', 'post', 'page', 'volume', 'DOI', 'references', 'UID']:
        del d[k]
    return d


if __name__ == '__main__':
    MockDB = {}
    # for every json we have created in our tests directory
    for name in glob.glob("tests/*.json"):
        # open the json 
        with open(name) as f:
        #    #base = re.match('tests/(.+)\.json', name).group(1)
            citations = json.load(f)
            # for every citation in this json
            for citation in citations:
                # create a string identifying json file and raw citation data
                test_name = 'test in {} - {}'.format(name, citation['raw'])
                # create generator to compare Citation parse engine dictionary vs json manually edited dictionary
                test = test_generator(clean(Citation.parse(citation['raw'])), clean(Citation(**citation)))
                setattr(CitationTest, test_name, test)

                # networkX testing
                # add each citation generated to the mock database
                temp = Citation.parse(citation['raw'])
                tempUID = temp['UID']
                MockDB[tempUID] = temp

    # networkx testing cont'd
    # print(MockDB.keys())
    # create graph
    g = nx.Graph()
    # add nodes
    for article in MockDB:
        g.add_node(MockDB[article]['issued'])
    # add edges
    # draw graph
    pos = nx.shell_layout(g)
    nx.draw(g, pos)
    # show graph
    plt.show()


    unittest.main()
