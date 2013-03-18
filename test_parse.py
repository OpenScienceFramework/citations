# encoding: utf-8

from parse import parser

class WhenParsingSingleEntry:
    def setup_method(self, method):
        text = u"""
        1. Marois R, Ivanoff J (2005) Capacity limits of information processing
        in the brain. Trends Cogn Sci 9: 296–305. doi:
        10.1016/j.tics.2005.04.010.  Find this article online
        """
        parsed = parser(text)
        self.result = parsed.line()

    def should_have_ref_number(self):
        assert self.result.ref == '1'

    def should_have_names(self):
        assert self.result.names == ['Marois R', 'Ivanoff J']

    def should_have_year(self):
        assert self.result.year == '2005'

    def should_have_title(self):
        assert self.result.title == "Capacity limits of information processing in the brain"
    
    def should_have_journal(self):
        assert self.result.journal == "Trends Cogn Sci"

    def should_have_edition(self):
        assert self.result.edition == '9'

    def should_have_doi(self):
        assert self.result.doi == '10.1016/j.tics.2005.04.010'

class _WhenParsingManyEntries:
    def setup_method(self, method):
        text = u"""
        1. Marois R, Ivanoff J (2005) Capacity limits of information processing
        in the brain. Trends Cogn Sci 9: 296–305. doi:
        10.1016/j.tics.2005.04.010. Find this article online

        1. Marois R, Ivanoff J (2005) Capacity limits of information processing
        in the brain. Trends Cogn Sci 9: 296–305. doi:
        10.1016/j.tics.2005.04.010. Find this article online
        """
        parsed = parser(text)
        self.result = parsed.lines()

    def should_gives_multiple_results(self):
        assert len(self.result) == 2


class CheckParseWords:
    def should_normalize_whitespace(self):
        text = "Capacity limits of information processing\n in the brain"
        parsed = parser(text)
        assert parsed.words() == "Capacity limits of information processing in the brain"

# TODO: Need to parse other formats.
class _CheckPsychologyArticle:
    def should_parse(self):
        text = """
        Aisenson, N. (1978). Fantasy and conservation among second
        grade children. The Journal of Genetic Psychology, 132, 155-156. 1
        10.1080/00221325.1978.10533325
        """

        parsed = parser(text)
        assert parsed.line() == object()
