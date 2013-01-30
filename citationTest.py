import unittest
import json
from Citation import Citation


class CitationTest(unittest.TestCase):

    # sample raw citations to compare against JSON library
    testCitations = ( 
        ('Aisenson , N. (1978). Fantasy and conservation among second grade children. The Journal of Genetic Psychology, 132, 155-156. 1 10.1080/00221325.1978.10533325'),
        ('Albertson , K. Shore , C. (2009). Holding in mind conflicting information: Pretending, working memory, and executive control. Journal of Cognition and Development, 9, 390-410. doi: 10.1080/15248370802678240'),
        ('Alfieri , L. Brooks , P. J. Aldrich , N. J. Tenenbaum , H. R. (2011). Does discovery-based instruction enhance learning? Journal of Educational Psychology, 103, 1-18. doi: 10.1037/a0021017'))
    
    # initilizer
    def setUp(self):
        # load in current JSON library for test data
        json_data=open('./tests/tests.json')
        self.jsonLib = json.load(json_data)

    # test Citation getRaw()
    def testCitationRawData(self):
        # @FIXME: Is there a better solution to this counter?
        # counter for iterating through JSON library
        counter = 0
        # iterate through each test citation
        for citation in self.testCitations:
            # create Citation object
            testObj = Citation(citation)
            # have citation parse raw data
            testObj.getFields() 
            # grab respecitve JSON dictionary index
            data = self.jsonLib[counter]
            # assert testCitation raw data matches JSON library raw data
            self.assertEqual(testObj.getRaw(), data['raw'])
            counter += 1

    # test Citation getAuthor()
    def testCitation(self):
        # @FIXME: Is there a better solution to this counter?
        # counter for iterating through JSON library
        counter = 0
        # iterate through each test citation
        for citation in self.testCitations:
            # create Citation object
            testObj = Citation(citation)
            # have citation parse raw data
            testObj.getFields() 
            # grab respecitve JSON dictionary index
            data = self.jsonLib[counter]
            # assert testCitation author matches JSON library author
            self.assertEqual(testObj.getAuthors(), data['author'])
            counter += 1

    # test Citation getDate()
    def testCitation(self):
        # @FIXME: Is there a better solution to this counter?
        # counter for iterating through JSON library
        counter = 0
        # iterate through each test citation
        for citation in self.testCitations:
            # create Citation object
            testObj = Citation(citation)
            # have citation parse raw data
            testObj.getFields() 
            # grab respecitve JSON dictionary index
            data = self.jsonLib[counter]
            # assert testCitation date matches JSON library date
            self.assertEqual(testObj.getDate(), data['issued'])
            counter += 1

if __name__ == '__main__':
    unittest.main()
