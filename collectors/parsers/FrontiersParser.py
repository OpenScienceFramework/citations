
# Imports
from . import *
from ..utils import misc
from ..utils import pubtools

from ..parsing.grammars import frontiers

class FrontiersParser(Parser):
    '''Parser designed to interact with Frontiers
    
    '''
    
    def parse_document(self, document):
        '''Extract and parse references from a document.

        Args:
            document (str) : raw text of document
        Returns:
            list of parsed references

        '''
        
        # Extract raw reference strings
        raw_refs = self.extract_refs(document)
        
        # Parse reference strings
        parsed_refs = []
        for raw_ref in raw_refs:
            parsed_ref = self.parse_ref(raw_ref)
            ref_info = {
                'raw' : repr(raw_ref),
                'ref' : parsed_ref,
            }
            parsed_refs.append(ref_info)

        # Return parsed references
        return parsed_refs

    def extract_refs(self, html):
        '''Extract references from document.
        
        Args:
            html (str) : Document full text
        Return:
            refs : List of references
        
        '''
        
        # Parse HTML
        html_parse = BS(html)

        # Get references
        refs = html_parse.findAll(
           'div',
            {'class' : re.compile('references', re.I)}
        )
        
        # Return references
        return refs
      
    def parse_ref(self, ref):
        '''Parse a raw reference.

        '''
        
        # Get text from BeautifulSoup object
        ref_txt = ''.join(ref.findAll(text=True))
        
        # Extract reference
        parsed_ref = frontiers.scan(frontiers.reference, ref_txt)

        # Get first match, if any
        if parsed_ref:
            parsed_ref = parsed_ref[0]
        
        # Get DOI
        doi_link = ref.find(
            'a',
            href=re.compile('dx\.doi\.org')
        )
        if doi_link:
            try:
                doi_href = doi_link['href']
                doi_short = re.sub('(?:http://)?dx\.doi\.org/', '', doi_href)
                parsed_ref['doi'] = doi_short
            except:
                pass

        # Get PubMed ID
        pmid_text = ref.find(
            text=re.compile('pubmed abstract', re.I)
        )
        if pmid_text:
            try:
                pmid_link = pmid_text.findParent('a')
                pmid_href = pmid_link['href']
                pmid_match = re.search('termtosearch=(\d+)', pmid_href, re.I)
                pmid = pmid_match.groups()[0]
                parsed_ref['pmid'] = pmid
            except:
                pass
        
        # Return reference
        return parsed_ref
