import re
"""
Constructs and builds a document object.

Parameters:
raw_document : dictionary containing some number of fields used to populate the document
raw_document = {
               'data' : { ... } -- dictionary containing meta data for a document
               'flags' : { ... } -- dictionary  containing flags for analysis
               'source' : [ ... ] -- list containing all sources the document has obtained data from
               }

Returns:
document : a completed document object
document = {
            'uid' : '1234' -- unique identifier each document is given during insansiation
            'properties' : { ... } -- dictionary containing meta data for a document - Follows
                                      csl-data.json schema located at:
                                      https://github.com/citation-style-language/schema/blob/master/csl-data.json
            'flags' : { ... } -- dictionary  containing flags for analysis
            'source' : [ ... ] -- list containing all sources the document has obtained data from
           }
"""


class IncompleteDocumentException(Exception):
    pass


# represents a document object
class Document(dict):

    required_fields = ['author', 'title', 'date']

    def __init__(self, raw_document):
        self.document = {}
        # verify the raw_document has the minimal fields to build a document
        if self.hasMinData(raw_document):
            # construct the unique id ofr this file
            print self.generateUID(raw_document)
            self.document['uid'] = self.generateUID(raw_document)
            print(self.document['uid'])

            # grab the flags and source from the raw document
            self.document['flags'] = raw_document['flags']
            self.document['source'] = raw_document['source']

    def hasMinData(self, raw_document):
        """
        returns true if document has the minimum data for document construction
        minimum data: authors : [{ 'family-name': '...'}] -- family name of the documents first author
                      date : int -- date the document was published
                      title: str -- title of the document
        """
        hasFields = True
        for field in self.required_fields:
            if field not in raw_document['data'] or not raw_document['data'][field]:
                print 'fuck missing %s' % (field)
                hasFields = False
                raise IncompleteDocumentException
        return hasFields

    def generateUID(self, raw_document):
        """
        returns a unique id for a document based on hash of the title, first
        author's last name, and date published stripped out white space, non-alphabetic,
        non-digit, and non-underscore characters.
        """
        title = raw_document['data']['title'].replace(' ', '').lower()
        author = raw_document['data']['author'][0]['family-name'].lower()
        date = raw_document['data']['date']
        uid = '__'.join([title, str(date), author])
        uid = re.sub('[^a-z0-9_]', '', uid)
        return hash(uid)
