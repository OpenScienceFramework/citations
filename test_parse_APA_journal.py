# encoding: utf-8

import parse

class WhenParsingSingleEntry:
    def setup_method(self, method):
        text = u"""
        Aisenson, N. (1978). Fantasy and conservation among second
        grade children. The Journal of Genetic Psychology, 132, 155-156. doi:
        10.1080/00221325.1978.10533325
        """
        self.result = parse.parse(text)

    def should_have_names(self):
        assert self.result.names == ['Aisenson, N.']

    def should_have_year(self):
        assert self.result.year == '1978'

    def should_have_title(self):
        assert self.result.title == "Fantasy and conservation among second grade children"
    
    def should_have_journal(self):
        assert self.result.journal == "The Journal of Genetic Psychology"

    def should_have_edition(self):
        assert self.result.edition == '132'

    def should_have_pages(self):
        assert self.result.pages == '155-156'

    def should_have_doi(self):
        assert self.result.doi == '10.1080/00221325.1978.10533325'


class CheckParseWords:
    def should_normalize_whitespace(self):
        text = "Capacity limits of information processing\n in the brain"
        parsed = parse.parser(text)
        assert parsed.words() == "Capacity limits of information processing in the brain"

