#@TODO: How to handle exceptions for when regular expressions fail to find matches...
#@TODO: create try/catch blocks for regular expression failures
import re


# class representing a citation
class Citation(dict):
    rawData = None

    # regex script for breaking apart fields
    rex_initial = re.compile('(?P<authors>.*)\((?P<date>.*)\)(?P<postData>.*)', re.DOTALL)

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
        rex_author_list = re.compile('[A-Z][a-z]+,\s[A-Z]\.\s+[A-Z]\.|[A-Z][a-z]+,\s[A-Z]\.', re.DOTALL)
        # (2) populate list with unique authors
        matches = re.findall(rex_author_list, authors)
        # (3) regex for separating an authors family name from his given initial(s)
        rex_authors = re.compile('(?P<family>[A-Z][a-z]*),\s+(?P<givenList>.+\.)', re.DOTALL)
        # (4) regex for separating given initials
        rex_given_list = re.compile('([A-Z])\.', re.DOTALL)
        # (5) for each author found, dissect family and given names and add to 'authors' dict
        for author in matches:
            # (5.1) separate family name from given initial(s)
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
            authorComplete = {unicode('given'): givenComposite, unicode('family'): uniqueAuthor.group('family')}
            # (5.6) append completed author to composite author dictionary
            authorList.append(authorComplete)
        self[unicode('author')] = authorList

    def parse_date(self, date):
        # store issued
        self[unicode('issued')] = int(date)

    def parse_post(self, post):
        # store post
        self['post'] = post

        # parse DOI
        # REGEX expression for grabbing everything before and after doi
        #@TODO: not grabbing "doi:"
        rex_DOI = re.compile('(?P<preDOI>.*)([Dd][Oo][Ii]:?)?\s(?P<doi>.*)$')
        currentMatches = rex_DOI.match(post)
        if currentMatches == None:
            print('Big Failure.')
        elif None == currentMatches.group('doi'):
            print('No doi found.')
        else:
            # save pre-doi string
            preDOI = currentMatches.group('preDOI')
            # grab, clean, and prepare doi
            doi = currentMatches.group('doi')
            doi = doi.lstrip()
            self[unicode('DOI')] = unicode(doi)

        # parse "page"
        # (lazy search everything)(digits - digits)(everything else from the end of the string)
        rex_page = re.compile('(?P<prePage>.*?)(?P<page>\d+[-]+\d+)(.*)$')
        currentMatches = rex_page.match(preDOI)
        if currentMatches == None:
            print('Big Failure')
        elif currentMatches.group('page') == None:
            print('No page found.')
        else:
            # save pre-page string
            prePage = currentMatches.group('prePage')
            # grab, clean, and store page
            page = currentMatches.group('page')
            page = page.lstrip()
            self[unicode('page')] = unicode(page)

        # grab "volume"
        # (everything before a comma) 0 or more whitespaces(everything before comma) comma (trash)
        rex_volume = re.compile('(?P<preVolume>.*),\s*(?P<volume>\d+),(.*)')
        currentMatches = rex_volume.match(prePage)
        if currentMatches == None:
            print('Big Failure.')
        elif currentMatches.group('volume') == None:
            print('No volume found.')
        else:
            # save pre-volume string
            preVolume = currentMatches.group('preVolume')
            # grab, clean, and store volume
            volume = currentMatches.group('volume')
            volume = volume.lstrip()
            self[unicode('volume')] = int(volume)

        # grab "container-title"
        # (everything until . || ? || !)(everything from the end of the string)
        rex_container_title = re.compile('(?P<preContainerTitle>.*[\.\?!])*(?P<containerTitle>.*)$')
        currentMatches = rex_container_title.match(preVolume)
        if currentMatches == None:
            print('Big Failure.')
        elif currentMatches.group('containerTitle') == None:
            print('No container title found.')
        else:
            # save pre-container-title string
            preContainerTitle = currentMatches.group('preContainerTitle')
            # grab, clean, and store container-title
            containerTitle = currentMatches.group('containerTitle')
            containerTitle = containerTitle.lstrip()
            self[unicode('container-title')] = unicode(containerTitle)

        # grab "title"
        # (everything from the end of the string until a period followed by whitespace)
        rex_title = re.compile('\s*\.\s*(?P<title>.*)$')
        currentMatches = rex_title.match(preContainerTitle)
        if currentMatches == None:
            print('Big Failure.')
        elif currentMatches.group('title') == None:
            print('No title found.')
        else:
            # grab, clean, and store title
            title = currentMatches.group('title')
            title = title.lstrip()
            self[unicode('title')] = unicode(title)
