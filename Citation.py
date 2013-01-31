import re
import pickle

# class representing a citation
class Citation(dict):

    rawData = None

    # regex script for breaking apart fields
    rex_authors = re.compile('(?P<authors>.*)\((?P<date>.*)\)(?P<postData>.*)', re.DOTALL)

    # constructor
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            self[k] = v

    def __delitem__(self, key):
        if key in self:
            super(Citation, self).__delitem__(key)

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    # parse and seperate fields from raw data
    @classmethod
    def parse(cls, raw):
        self = cls()
        self['raw'] = raw

        # seperate fields
        matches = self.rex_authors.match(self.raw)

        # grab authors field
        authors = matches.group('authors')
        print authors
        self.parse_authors(authors)
        #print 'Authors: ' + self.getAuthors()
        # grab date field
        issued = matches.group('date')
        self.parse_date(issued)
        #print 'Date: ' + self.getDate()
        # grab postData field
        post = matches.group('postData')
        self.parse_post(post)
        #print 'Post Data: ' + self.getPostData()
        return self

    def parse_authors(self, raw_authors):
        self['author'] = []

    def parse_date(self, raw_date):
        self['issued'] = None

    def parse_post(self, raw_post):
        self['post'] = None