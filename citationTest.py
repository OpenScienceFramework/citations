import unittest
import pickle
from Citation import Citation


class CitationTest(unittest.TestCase):
    
    def setUp(self):
        with open('/home/sphere/development/python/research/citationProject/citation_array.pickle' , 'r') as f:
            citation_list = pickle.load(f)  
        Citation(citation_list)
        Citation.rawData = citation_list[1]

    def testConstructor(self):
        with open('/home/sphere/development/python/research/citationProject/citation_array.pickle' , 'r') as q:
            result = pickle.load(q)
        self.assertEqual(result[1], Citation.rawData)        

    def testGetFields(self):
        Citation.getFields(self)
        

if __name__ == '__main__':
    unittest.main()
