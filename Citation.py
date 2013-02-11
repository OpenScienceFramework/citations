import re


# class representing a citation
class Citation(dict):

    rawData = None

    # regex script for breaking apart fields
    rex_initial = re.compile('(?P<authors>.*)\((?P<date>.*)\)(?P<postData>.*)', re.DOTALL)

    # constructor
    def __init__(self, **kwargs):
    # for every key, populate the respective Citation field with its value
        for k,v in kwargs.iteritems():
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
        matches = self.rex_initial.match(self.raw)

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
        authorList = []
        # (1) regex expression for grabbing 'Familyname, I1.' || 'Familyname, I1. I2.'
        rex_author_list = re.compile('[A-Z][a-z]+\,\s[A-Z]\.\s+[A-Z]\.|[A-Z][a-z]+\,\s[A-Z]\.', re.DOTALL)
        # (2) populate list with unique authors
        matches = re.findall(rex_author_list, authors)
        # (3) regex for seperateing an authors family name from his given initial(s)
        rex_authors = re.compile('(?P<family>[A-Z][a-z]*),\s+(?P<givenList>.+\.)', re.DOTALL)
        # (4) regex for seperating given initals
        rex_given_list = re.compile('([A-Z])\.', re.DOTALL)
        # (5) for each author found, disect family and given names and add to 'authors' dict
        for author in matches:
            # (5.1) seperate family name from given initial(s)
            uniqueAuthor = rex_authors.match(author)
            # (5.2) find all initials of an authors given name and populate an array with strings
            givenMatches = re.findall(rex_given_list, uniqueAuthor.group('givenList')) 
            # (5.3) for each given initial add it to a composite string
            givenComposite = ''
            for given in givenMatches:
                givenComposite = givenComposite + ' ' + given 
            # (5.4) strip leading whitespace
            givenComposite = givenComposite.lstrip()
            # (5.5) add given initials and family to dictionary
            authorComplete = {'given' : givenComposite, 'family' : uniqueAuthor.group('family')}
            # (5.6) append completed author to composite author dictionary
            authorList.append(authorComplete)
        self['author'] = authorList

    def parse_date(self, date):
        self['issued'] = date

    def parse_post(self, post):
        self['post'] = post
