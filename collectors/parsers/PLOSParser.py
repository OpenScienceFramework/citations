
# Imports
from . import *
from ..utils import misc
from ..utils import pubtools

from ..parsing.grammars import plos

import copy

plos_url_base = 'http://www.plosone.org'

class PLOSParser(Parser):
    '''Parser designed to interact with PLOS
    
    '''
    
    def parse_document(self, document):
        
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

        # Get reference container
        ref_container = html_parse.find('ol', {'class' : 'references'})
        if not ref_container:
            return

        # Get references
        refs_li = ref_container.findAll('li')
        #refs_txt = [''.join(ref.findAll(text=True)) for ref in refs_li]
        
        # Done
        return refs_li
        #return refs_txt

    # Extract reference fields and return list of references to be parsed
    def parse_ref(self, ref):
        
        # Get text from BeautifulSoup object
        ref_txt = ''.join(ref.findAll(text=True))
        
        # Extract reference
        parsed_ref = plos.scan(plos.reference, ref_txt)

        # Get first match, if any
        if parsed_ref:
            parsed_ref = parsed_ref[0]
        
        # Return reference
        return parsed_ref

        # Extract references
        ref_dicts = []
        for ref in refs:
            ref_txt = ''.join(ref.findAll(text=True))
            dois = misc.get_dois(ref_txt)
            if dois:
                pmid = misc.doi_to_pmid(dois[0])
                print 'argh', dois[0], pmid
                if pmid:
                    pubmed_xml = pubtools.efetch_pmid(pmid)
                    ref_dict = pubtools.PubMedXML(pubmed_xml).parse()
                    ref_dicts.append(ref_dict)
                    continue
            findcited_link = ref.find(
                'a',
                href=re.compile('findcited')
            )
            try:
                findcited_href = findcited_link['href']
            except:
                findcited_href = None
            if findcited_href:
                ref_scrape = misc.scrape_plos_findcited('%s/%s' % (plos_url_base, findcited_link['href']))
                if ref_scrape:
                    ref_dicts.append(ref_scrape)
                    continue
            try:
                ref_dict = parse.parse(ref_txt)._asdict()
                self._post_process(ref_dict)
                ref_dicts.append(ref_dict)
            except Exception as e:
                print e.message
                pass

        return ref_dicts
    
    def _post_process(self, ref):
        
        ref_proc = copy.deepcopy(ref)

        # Clean up journal title
        ref_proc['journal-title'] = ref_proc['journal']
        del ref_proc['journal']
        
        # Clean up authors
        for idx, author in enumerate(ref_proc['author']):
            new_author = {}
            author_tokens = author.split(' ')
            new_author['family'] = author_tokens[0]
            if len(author_tokens) > 1:
                new_author['given'] = author_tokens[1]
            ref_proc['author'][idx] = new_author

        return ref_proc

