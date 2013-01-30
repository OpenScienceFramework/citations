import re
import pickle

# class representing a citation
class Citation:

    rawData = None


    # regex script for breaking apart fields
    rex_authors = re.compile('(?P<authors>.*)\((?P<date>.*)\)(?P<postData>.*)', re.DOTALL)

    # constructor
    def __init__(self, data):
        self.rawData = data
        
    # parse and seperate fields from raw data
    def getFields(self):
        # seperate fields
        matches = self.rex_authors.match(self.rawData)

        # grab authors field
        self.setAuthors(matches.group('authors'))
        #print 'Authors: ' + self.getAuthors()
        # grab date field
        self.setDate(matches.group('date'))
        #print 'Date: ' + self.getDate()
        # grab postData field
        self.setPostData(matches.group('postData'))
        #print 'Post Data: ' + self.getPostData()        

    # get raw data
    def getRaw(self):
        return self.rawData

    # set/get author
    def setAuthors(self, authors):
        self.authors = authors
        return self 
    def getAuthors(self):
        return self.authors

    # set/get date
    def setDate(self, date):
        self.date = date
        return self
    def getDate(self):
        return self.date

    # set/get post data
    def setPostData(self, postData):
        self.postData = postData
        return self
    def getPostData(self):
        return self.postData



