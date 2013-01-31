import json
import glob
import unittest
import re

from Citation import Citation

class CitationTest(unittest.TestCase):
    pass

def test_generator(a, b):
    def test(self):
        self.assertDictEqual(a, b)
    return test

def clean(d):
    for k in ['raw', 'type', 'style']:
        del d[k]
    return d

if __name__ == '__main__':
    for name in glob.glob("tests/*.json"):
        with open(name) as f:
            #base = re.match('tests/(.+)\.json', name).group(1)
            citations = json.load(f)
            for citation in citations:
                test_name = 'test in {} - {}'.format(name, citation['raw'])
                test = test_generator(clean(Citation.parse(citation['raw'])), clean(Citation(**citation)))
                setattr(CitationTest, test_name, test)
    unittest.main()