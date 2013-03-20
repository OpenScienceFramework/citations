# encoding: utf-8

import parse

class WhenParsingSingleEntry:
    def setup_method(self, method):
        text = u"""
        1. Marois R, Ivanoff J (2005) Capacity limits of information processing
        in the brain. Trends Cogn Sci 9: 296–305. doi:
        10.1016/j.tics.2005.04.010.  Find this article online
        """

        self.result = parse.parse(text)

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


class _WhenParsingSingleEntryExtended1:
    # et al. in author list, slash in title, unicode in page reference
    
    def setup_method(self, method):
        text = u"""
        9. Veronese F, Devico A, Copeland T, Oroszlan S, Gallo R, et al. (1985) Characterization
        of gp41 as the transmembrane protein coded by the HTLV-III/LAV envelope gene. Science 229:
        1402\u20131405. doi:10.1126/science.2994223. Find this article online
        """
        parsed = parser(text)
        self.result = parsed.line()

    def should_have_ref_number(self):
        assert self.result.ref == '9'

    def should_have_names(self):
        assert self.result.names == ['Veronese F', 'Devico A','Copeland T', 'Oroszlan S', 'Gallo R']

    def should_have_more_names_flag(self):
        assert self.result.more.names == True

    def should_have_year(self):
        assert self.result.year == '1985'

    def should_have_title(self):
        assert self.result.title == "Characterization of gp41 as the transmembrane protein coded by the HTLV-III/LAV envelope gene"
    
    def should_have_journal(self):
        assert self.result.journal == "Science"

    def should_have_edition(self):
        assert self.result.edition == '229'
        
    def should_have_pages(self):
        assert self.result.pages == '1402-1405'

    def should_have_doi(self):
        assert self.result.doi == '10.1126/science.2994223'
        

class _WhenParsingSingleEntryExtended2:
    # et al. in author list, hyphen and numbers in title, long journal name, single page number
        
    def setup_method(self, method):
        text = u"""
        23. Klein JS, Gnanapragasam PNP, Galimidi RP, Foglesong CP, West AP, et al. (2009)
        Examination of the contributions of size and avidity to the neutralization mechanisms
        of the anti-HIV antibodies b12 and 4E10. Proceedings Of The National Academy Of Sciences
        Of The United States Of America 106: 7385. doi:10.1073/pnas.0811427106. Find this article online      
        """
        parsed = parser(text)
        self.result = parsed.line()

    def should_have_ref_number(self):
        assert self.result.ref == '23'

    def should_have_names(self):
        assert self.result.names == ['Klein JS', 'Gnanapragasam PNP', 'Galimidi RP', 'Foglesong CP', 'West AP']

    def should_have_more_names_flag(self):
        assert self.result.more.names == True

    def should_have_year(self):
        assert self.result.year == '2009'

    def should_have_title(self):
        assert self.result.title == "Examination of the contributions of size and avidity to the neutralization mechanisms of the anti-HIV antibodies b12 and 4E10"
    
    def should_have_journal(self):
        assert self.result.journal =="Proceedings Of The National Academy Of Sciences Of The United States Of America"

    def should_have_edition(self):
        assert self.result.edition == '106'

    def should_have_pages(self):
        assert self.result.pages == '7385'

    def should_have_doi(self):
        assert self.result.doi == '10.1073/pnas.0811427106'


class _WhenParsingSingleEntryExtended3:
    # unicode in page reference

    def setup_method(self, method):
        text = u"""
        34. Celik L, Schi\u00f8tt B, Tajkhorshid E (2008) Substrate binding and formation of an occluded
        state in the leucine transporter. Biophys J 94: 1600\u20131612 doi:10.1529/biophysj.107.117580. Find this article online
        """
        parsed = parser(text)
        self.result = parsed.line()

    def should_have_ref_number(self):
        assert self.result.ref == '34'

    def should_have_names(self):
        assert self.result.names == ['Celik L', 'Schi\u00f8tt B', 'Tajkhorshid E']

    def should_have_more_names_flag(self):
        assert self.result.more.names == False

    def should_have_year(self):
        assert self.result.year == '2008'

    def should_have_title(self):
        assert self.result.title == "Substrate binding and formation of an occluded state in the leucine transporter"
    
    def should_have_journal(self):
        assert self.result.journal =="Biophys J"

    def should_have_edition(self):
        assert self.result.edition == '94'

    def should_have_pages(self):
        assert self.result.pages == '1600-1612'

    def should_have_doi(self):
        assert self.result.doi == '10.1529/biophysj.107.117580'


class _WhenParsingSingleEntryExtended4:
    # parens in title; no journal name, volume; includes url for e-pub
    
    def setup_method(self, method):
        text = u"""
        37. Buddenhagen J, Kottwitz D (2001) Multiplicity and symmetry breaking in (conjectured) densest packings of congruent
        circles on a sphere. E-pub ahead of print. Available at http://home.earthlink.net/wjbuddenh/pack\u200b/sphere/intro.htm. 
        """
        parsed = parser(text)
        self.result = parsed.line()

    def should_have_ref_number(self):
        assert self.result.ref == '37'

    def should_have_names(self):
        assert self.result.names == ['Buddenhagen J', 'Kottwitz D']

    def should_have_more_names_flag(self):
        assert self.result.more.names == False

    def should_have_year(self):
        assert self.result.year == '2001'

    def should_have_title(self):
        assert self.result.title == "Multiplicity and symmetry breaking in (conjectured) densest packings of congruent circles on a sphere"
    
    def should_have_journal(self):
        assert self.result.journal == ""

    def should_have_edition(self):
        assert self.result.edition == ""

    def should_have_doi(self):
        assert self.result.doi == ""

    def should_have_url(self):
        assert self.result.url == "http://home.earthlink.net/wjbuddenh/pack\u200b/sphere/intro.htm"

class _WhenParsingSingleEntryExtended5:
    # et al. in author list, unicode in page reference, parens and hyphen in DOI

    def setup_method(self, method):
        text = u"""
        61. Atilgan AR, Durell SR, Jernigan RL, Demirel MC, Keskin O, et al. (2001) Anisotropy
        of fluctuation dynamics of proteins with an elastic network model.
        Biophys J 80: 505\u2013515. doi:10.1016/S0006-3495(01)76033-X. Find this article online                  
        """
        parsed = parser(text)
        self.result = parsed.line()

    def should_have_ref_number(self):
        assert self.result.ref == '61'

    def should_have_names(self):
        assert self.result.names == ['Atilgan AR', 'Durell SR', 'Jernigan RL', 'Demirel MC', 'Keskin O']

    def should_have_more_names_flag(self):
        assert self.result.more.names == True

    def should_have_year(self):
        assert self.result.year == '2001'

    def should_have_title(self):
        assert self.result.title == "Anisotropy of fluctuation dynamics of proteins with an elastic network model"
    
    def should_have_journal(self):
        assert self.result.journal == "Biophys J"

    def should_have_edition(self):
        assert self.result.edition == "80"

    def should_have_pages(self):
        assert self.result.pages == '505-515'

    def should_have_doi(self):
        assert self.result.doi == "10.1016/S0006-3495(01)76033-X"
        

class _WhenParsingSingleEntryExtended5:
    # colon in title, unicode in page range
    
    def setup_method(self, method):
        text = u"""
        62. Eyal E, Yang LW, Bahar I (2006) Anisotropic network model: systematic evaluation and a new
        web interface. Bioinformatics 22: 2619\u20132627.\n doi:10.1093/bioinformatics/btl448. Find this article online"                 
        """
        parsed = parser(text)
        self.result = parsed.line()

    def should_have_ref_number(self):
        assert self.result.ref == '62'

    def should_have_names(self):
        assert self.result.names == ['Eyal E', 'Yang LW', 'Bahar I']

    def should_have_more_names_flag(self):
        assert self.result.more.names == False

    def should_have_year(self):
        assert self.result.year == '2006'

    def should_have_title(self):
        assert self.result.title == "Anisotropic network model: systematic evaluation and a new web interface"
    
    def should_have_journal(self):
        assert self.result.journal == "Bioinformatics"

    def should_have_edition(self):
        assert self.result.edition == "22"

    def should_have_pages(self):
        assert self.result.pages == '2619-2627'

    def should_have_doi(self):
        assert self.result.doi == "10.1093/bioinformatics/btl448"



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
        parsed = parse.parser(text)
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
