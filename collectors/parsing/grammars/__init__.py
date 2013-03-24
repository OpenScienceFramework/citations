# encoding: utf-8

import pyparsing as pyp
import re

def to_obj(result):
    '''Convert nested ParseResults structure to list / dict.

    Args:
        result (ParseResults) : pyparsing result
    Returns:
        list / dict containing results

    '''
    d = result.asDict()
    if d:
        for k in d:
            if isinstance(d[k], pyp.ParseResults):
                d[k] = to_obj(d[k])
        return d
    l = result.asList()
    for idx, v in enumerate(l):
        if isinstance(v, pyp.ParseResults):
            l[idx] = to_obj(v)
    return l

def scan(pattern, string):
    '''Scan a string for repeated occurrences of a pattern.

    Args:
        pattern (pyparsing pattern) : pattern to be applied
        string (str) : text to be parsed
    Returns:
        list of matches as list / dict
    '''
    
    return [to_obj(match[0]) for match in 
            pattern.scanString(string)]

# ParseAction functions

def joiner(delim):
    return lambda tokens: delim.join(tokens)

def parse_authors_factory(author_splitter, name_splitter):
    '''Create a function for splitting author strings.

    Args:
        author_splitter (str) : pattern for splitting authors
        name_splitter (str) : pattern for splitting names w/in an author
    Returns:
        author-splitter function

    '''
    def parse_authors(tokens):
        authors = []
        # Note: Since this action is normally chained after
        # a joiner() action, only consider the 0th token
        for token in re.split(author_splitter, tokens[0]):
            if not token:
                continue
            token_split = re.split(name_splitter, token)
            author = {}
            author['family'] = token_split[0]
            if len(token_split) > 1:
                author['given'] = token_split[1]
            authors.append(author)
        return authors
    return parse_authors

# Character sets
dash_chars = u'-–'
allowed_chars = u',;:\'"’&?!()'

# Elementary patterns
dashes = pyp.Word(dash_chars)
etal = pyp.Combine('et al' + pyp.ZeroOrMore('.'))
number = pyp.Word(pyp.nums)
date = '(' + number.setResultsName('date') + ')' + pyp.Optional('.')
words_neglook = ~date + ~number + ~etal + ~pyp.Literal('http') + ~pyp.Literal('doi')

word = pyp.Word(pyp.alphanums + dash_chars + allowed_chars)
words = pyp.OneOrMore(words_neglook + word).\
        setParseAction(joiner(' '))
word_journal = pyp.Word(pyp.alphanums + dash_chars + allowed_chars + '.')
words_journal = pyp.OneOrMore(words_neglook + word_journal).\
                setParseAction(joiner(' '))

# Meta-data patterns

# Note: Remember to copy words pattern to avoid 
# changing other patterns
authors = pyp.Group(
              words_journal.copy().\
              addParseAction(parse_authors_factory(',', '\s'))
          ).setResultsName('author') + \
          pyp.Optional(etal)

title = words.\
        setResultsName('title')

journal = words_journal.\
          setParseAction(joiner(' ')).\
          setResultsName('journal-title')

volume = pyp.Optional(
             number.\
             setResultsName('volume') + \
             pyp.Word(',:')
         )

page_range = number + pyp.Suppress(dashes) + number
page_plos = pyp.Combine('e' + number)
pages = pyp.Optional(pyp.Group(page_range | page_plos).\
        setResultsName('pages'))

doi = pyp.Optional(
          pyp.Suppress(
              pyp.Optional('doi:') + \
              pyp.Optional('http://dx.doi.org/')
          ) + \
          pyp.Regex(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b')
      ).setResultsName('doi')

reference = authors + \
            date + \
            title + \
            '.' + \
            journal + \
            volume + \
            pages + \
            pyp.Optional('.') + \
            doi
