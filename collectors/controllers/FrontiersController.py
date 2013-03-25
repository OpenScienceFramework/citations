from . import PublisherCorpusController

from ..listers import FrontiersLister
from ..fetchers import FrontiersFetcher
from ..parsers import FrontiersParser

class FrontiersCorpusController(PublisherCorpusController):
    
    lister = FrontiersLister.FrontiersLister
    fetcher = FrontiersFetcher.FrontiersFetcher
    parser = FrontiersParser.FrontiersParser
