from . import PublisherCorpusController

from ..listers import PLOSLister
from ..fetchers import PLOSFetcher
from ..parsers import PLOSParser

class PLOSCorpusController(PublisherCorpusController):
    
    lister = PLOSLister.PLOSLister
    fetcher = PLOSFetcher.PLOSFetcher
    parser = PLOSParser.PLOSParser
