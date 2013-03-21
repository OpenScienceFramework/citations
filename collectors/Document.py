
import re
import datetime

"""
Constructs and builds a document object.

Parameters:
raw_document : dictionary containing some number of fields used to populate the document
raw_document = {
               'properties' : { ... } -- dictionary containing meta properties for a document
               'flags' : { ... } -- dictionary  containing flags for analysis
               'source' : [ ... ] -- list containing all sources the document has obtained data from
               }

Returns:
document : a completed document object
document = {
            'uid' : '1234' -- unique identifier each document is given during insansiation
            'properties' : { ... } -- dictionary containing meta properties for a document - Follows
                                      csl-data.json schema located at:
                                      https://github.com/citation-style-language/schema/blob/master/csl-data.json
            'flags' : { ... } -- dictionary  containing flags for analysis
            'source' : [ ... ] -- list containing all sources the document has obtained data from
           }
"""

# Exception thrown when a document is missing required fields
class IncompleteDocumentException(Exception):
    pass


# represents a document object
class Document(dict):

    required_fields = ['author', 'title', 'date']
    copy_fields = ['flags', 'source', 'properties', 'raw', 'refs']

    def __init__(self, raw_document):
        self.document = {}
        # verify the raw_document has the minimal fields to build a document
        if self.hasMinData(raw_document):

            # grab the properties, flags, and source from the raw document
            for copy_field in self.copy_fields:
              if copy_field in raw_document:
                self.document[copy_field] = raw_document[copy_field]

            # Check for valid date
            idate = valid_date(self.document['properties']['date'])
            if idate:
              self.document['properties']['date'] = idate
            else:
              print 'bad'
              raise IncompleteDocumentException

            # generate and add the unique id
            self.document['uid'] = self.generateUID(raw_document)

            # @todo generate number of pages from front/last page

            # @todo add number of pages to raw_document['properties']

    def hasMinData(self, raw_document):
        """
        returns true if document has the minimum data for document construction
        minimum data: authors : [{ 'family-name': '...'}] -- family name of the documents first author
                      date : int -- date the document was published
                      title: str -- title of the document
        """
        hasFields = True
        for field in self.required_fields:
            if field not in raw_document['properties'] or not raw_document['properties'][field]:
                print 'missing field %s' % (field)
                print {k:v for k, v in raw_document.iteritems() if k != 'raw'}
                hasFields = False
                raise IncompleteDocumentException
        return hasFields

    def generateUID(self, raw_document):
        """
        returns a unique id for a document based on hash of the title, first
        author's last name, and date published stripped out white space, non-alphabetic,
        non-digit, and non-underscore characters.
        """
        title = raw_document['properties']['title'].replace(' ', '').lower()
        author = raw_document['properties']['author'][0]['family'].lower()
        date = raw_document['properties']['date']
        uid = '__'.join([title, unicode(date), author])
        uid = re.sub('[^a-z0-9_]', '', uid)
        return hash(uid)

    def getUID(self):
        """returns the UID for a document
        """
        return self.document['uid']

def valid_date(date):
  
  try:
    idate = int(date)
  except ValueError:
    return False
  if 1900 <= idate <= datetime.datetime.now().year:
    return idate
  return False
