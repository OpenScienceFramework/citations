import json
import glob
import unittest

from Citation import Citation


class CitationTest(unittest.TestCase):
    pass

# returns a dynamic test function for comparing two dictionaries
def test_generator(a, b):
    def test(self):
        self.assertDictEqual(a, b)

    return test

# return dictionary less the key/values we don't want to test
def clean(d):
    for k in ['raw', 'type', 'style']:
        del d[k]
    return d


if __name__ == '__main__':
    # for every json we have created in our tests directory
    for name in glob.glob("tests/*.json"):
        # open the json 
        with open(name) as f:
        #    #base = re.match('tests/(.+)\.json', name).group(1)
            citations = json.load(f)
            # for every citation in this json
            for citation in citations:
                print(citation)
                print("citation\n\n")
                # create a string identifying json file and raw citation data
                test_name = 'test in {} - {}'.format(name, citation['raw'])
                print(test_name)
                print("testname\n\n")
                # creat generator to compare Citation parse engine dictionary vs json manually edited dictionary
                test = test_generator(clean(Citation.parse(citation['raw'])), clean(Citation(**citation)))
                # @fixme: CitationTest.test_name() will run test_generator(Citation parse eng dict, json dictionary)
                setattr(CitationTest, test_name, test)
    unittest.main()
