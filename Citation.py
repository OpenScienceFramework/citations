import re


# class representing a citation
class Citation(dict):

    rawData = None

    # regex script for breaking apart fields
    rex_authors = re.compile('(?P<authors>.*)\((?P<date>.*)\)(?P<postData>.*)', re.DOTALL)

    # constructor
    def __init__(self, **kwargs):
    # for every key, populate the respective Citation field with its value
        for k, v in kwargs.iteritems():
            self[k] = v

    def __delitem__(self, key):
        if key in self:
            super(Citation, self).__delitem__(key)

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    # returns citation obj - subclass of dictionary
    # parse and separate fields from raw data
    @classmethod
    def parse(cls, raw):
    # create an empty Citation
        self = cls()
        self['raw'] = raw

        # separate fields
        matches = self.rex_authors.match(self.raw)

        # grab authors field
        authors = matches.group('authors')

        self.parse_authors(authors)
        # grab date field
        issued = matches.group('date')
        self.parse_date(issued)

        # grab postData field
        post = matches.group('postData')
        self.parse_post(post)
        return self

    #@TODO: Need to parse string and store name in array as, family:lastname given:first/second initial
    def parse_authors(self, authors):
        self['author'] = authors

    def parse_date(self, date):
        self['issued'] = date

    def parse_post(self, post):
        self['post'] = post
