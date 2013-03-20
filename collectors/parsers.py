# -*- coding: UTF-8 -*-

'''
Parses, constructs, and returns document objects. Interacts with corresponding source CorpusController.

Parameters:
   html/xml/... : Raw document data to be parsed
Returns:
   Document : Document object constructed
'''

# Imports

import Document
from BeautifulSoup import BeautifulSoup as BS

# Abstract parsing class
class Parser(object):
  
  # Extrapolates document fields and returns a document object
  def parse(self):
    raise NotImplementedError
  
  # Extracts and returns set of documents to be parsed
  def extract(self):
    raise NotImplementedError

# Parser designed to intereact with PLOS
class PLOSParser(Parser):
  
  # Extapolate document fields and return the corresponding document object
  def parse(self, html):
    
    # Parse HTML
    html_parse = BS(html)

    # Get reference container
    ref_container = html_parse.find('ol', {'class' : 'references'})
    if not ref_container:
      return

    # Get references
    refs = ref_container.findAll('li')
    refs = [{'text' : ''.join(ref.findAll(text=True))} for ref in refs]

    return refs
  
  # Extract reference fields and return list of references to be parsed
  def extract(self):
    
    pass

class OAIParser(Parser):
  
  # Generic XML fields
  fields = {
    'journal-title' : {'tag' : 'source'},
    'title' : {'tag' : 'article-title'},
    'date' : {'tag' : 'year'},
    'volume' : {'tag' : 'volume'},
    'first-page' : {'tag' : 'fpage'},
    'last-page' : {'tag' : 'lpage'},
    'pmid' : {'tag' : 'pub-id', 'attrs' : {'pub-id-type' : 'pmid'}},
    'doi' : {'tag' : 'pub-id', 'attrs' : {'pub-id-type' : 'doi'}},
  }
  
  def parse_document(self, xml_parse):
    
    # Parse main reference
    main_ref = self.parse_ref(xml_parse.find('article'))
    main_dict = {
      'data' : main_ref,
      'source' : ['oai'],
      'flags' : {},
    }
    main_doc = Document.Document(main_dict).document

    # Get <ref-list>
    ref_list = xml_parse.find('ref-list')

    # Quit if no <ref-list>
    if not ref_list:
      return
    
    # Get <ref>s
    refs = ref_list.findAll('ref')
    
    # Parse <ref>s
    ref_docs = []
    for ref in refs:
      ref_parse = self.parse_ref(ref)
      ref_dict = {
        'data' : ref_parse,
        'source' : ['oai'],
        'flags' : {},
      }
      try:
        ref_doc = Document.Document(ref_dict)
        ref_docs.append(ref_doc.document)
      except:
        pass
    
    # Add <ref> UIDs to document
    main_doc['references'] = [doc['uid'] for doc in ref_docs]
    
    # Done
    return [main_doc] + ref_docs
  
  def parse_ref_typeR(self, citation):
    
    # Initialize fields
    extra_fields = {}
    
    # Get all first-level text fields
    text_fields = citation.findAll(text=True, recursive=False)
    
    # Loop over unstructured fields
    for field in text_fields:

      # Author / title field
      if re.search('.+?:.+', field):
        authors_raw, title = field.split(':')
        authors = authors_raw.split(', ')
        authors_dict = []
        for author in authors:
          author_dict = {}
          author_split = author.split(' ')
          author_dict['family-name'] = author_split[0]
          if len(author_split) > 1:
            author_dict['given-names'] = ' '.join(author_split[1])
          authors_dict.append(author_dict)
        extra_fields['author'] = authors_dict
        extra_fields['title'] = title.strip()

      # Lastpage field
      lastpage_search = re.search('^–(\d+)', field)
      if lastpage_search:
        extra_fields['last-page'] = lastpage_search.groups()[0]
    
    # Return fields
    return extra_fields

  def parse_ref_typeB(self, citation):
    print 'BBB'
    
    # Initialize fields
    extra_fields = {}
    
    # Find authors
    author_group = citation.find(
      'person-group',
      {'person-group-type' : 'author'}
    )
    if author_group:
      authors = author_group.findAll('name')
      authors_dict = []
      for author in authors:
        author_dict = {}
        surname = author.find('surname')
        if surname:
          author_dict['family-name'] = unicode(surname.string)
        given_names = author.find('given-names')
        if given_names:
          author_dict['given-names'] = ' '.join(given_names.string)
        authors_dict.append(author_dict)
      extra_fields['author'] = authors_dict
    
    # Done
    return extra_fields

  def parse_ref(self, ref):
    
    # Initialize fields
    field_info = {}
    
    # Find <citation>
    citation = ref.find('citation')
    
    # Loop over generic fields
    for field in self.fields:
      tag = self.fields[field]['tag']
      if 'attrs' in self.fields[field]:
        attrs = self.fields[field]['attrs']
      else:
        attrs = {}
      container = citation.find(tag, attrs)
      if container:
        field_info[field] = unicode(container.string).strip()
    
    # Collect extra fields from specialized parsing functions
    extra_fields = {}
    try:
      id = ref['id']
    except:
      id = ''
    #if hasattr(ref, 'id'):
    #  id = getattr(ref, 'id')
    #  id = id if id else ''
    print 'argh', ref.name
    if re.search('^r', id, re.I):
      extra_fields = self.parse_ref_typeR(citation)
    elif re.search('^b', id, re.I) or ref.name == 'article':
      extra_fields = self.parse_ref_typeB(ref)
    
    # Add extra fields
    field_info.update(extra_fields)
    
    # Done
    return field_info
