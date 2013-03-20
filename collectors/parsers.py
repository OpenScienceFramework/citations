# -*- coding: UTF-8 -*-

'''
Parses, constructs, and returns document objects. Interacts with corresponding source CorpusController.

Parameters:
   html/xml/... : Raw document data to be parsed
Returns:
   Document : Document object constructed
'''

# Imports

import re
from BeautifulSoup import BeautifulSoup as BS

import Document

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
    'container-title' : {'tag' : 'source'},
    'title' : {'tag' : 'article-title'},
    'date' : {'tag' : 'year'},
    'volume' : {'tag' : 'volume'},
    'page-first' : {'tag' : 'fpage'},
    'page-last' : {'tag' : 'lpage'},
    'PMID' : {'tag' : 'pub-id', 'attrs' : {'pub-id-type' : 'pmid'}},
    'doi' : {'tag' : 'pub-id', 'attrs' : {'pub-id-type' : 'doi'}},
  }
  
  def parse_document(self, xml_parse):
    '''Parse a document and its references.

    Args:
      xml_parse: BeautifulSoup repr of <article> from OAI
    Returns:
      docs: List of Documents for main document docs[0] and its references d[1:]

    '''
    
    # Parse main reference
    main_ref = self.parse_ref(xml_parse.find('article'), True)
    main_dict = {
      'properties' : main_ref,
      'source' : ['oai'],
      'flags' : {},
      'raw' : str(xml_parse),
    }
    try:
      main_doc = Document.Document(main_dict)
    except:
      return []

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
      ref_parse = self.parse_ref(ref, False)
      ref_dict = {
        'properties' : ref_parse,
        'source' : ['oai'],
        'flags' : {},
      }
      try:
        ref_doc = Document.Document(ref_dict)
        ref_docs.append(ref_doc)
      except Document.IncompleteDocumentException:
        print 'incomplete document!'
    
    # Add <ref> UIDs to document
    main_doc['references'] = [doc.getUID() for doc in ref_docs]
    
    # Done
    return [main_doc] + ref_docs
  
  def parse_ref_typeR(self, citation):
    '''Get additional fields from <ref id="R*">s

    '''
    
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
          author_dict['family'] = author_split[0]
          if len(author_split) > 1:
            author_dict['given'] = ' '.join(author_split[1])
          authors_dict.append(author_dict)
        extra_fields['author'] = authors_dict
        extra_fields['title'] = title.strip()

      # Lastpage field
      lastpage_search = re.search('^–(\d+)', field)
      if lastpage_search:
        extra_fields['page-last'] = lastpage_search.groups()[0]
    
    # Return fields
    return extra_fields

  def parse_ref_typeB(self, citation):
    '''Get additional fields from <ref id="B*">s and <article>s

    '''
    
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
          author_dict['family'] = unicode(surname.string)
        given_names = author.find('given-names')
        if given_names and given_names.string:
          author_dict['given'] = ' '.join(given_names.string)
        authors_dict.append(author_dict)
      extra_fields['author'] = authors_dict
    
    # Done
    return extra_fields

  def parse_ref(self, ref, primary):
    
    # Initialize fields
    field_info = {}
    
    # Find <citation>
    if primary:
      citation = ref
    else:
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
    if re.search('^r', id, re.I):
      extra_fields = self.parse_ref_typeR(citation)
    elif re.search('^b', id, re.I) or ref.name == 'article':
      extra_fields = self.parse_ref_typeB(ref)
    
    # Add extra fields
    field_info.update(extra_fields)
    
    # Done
    return field_info
