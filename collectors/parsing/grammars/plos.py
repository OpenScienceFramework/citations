# encoding: utf-8

#from . import *
import pyparsing as pyp

def to_obj(result):
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
    
    return [to_obj(match[0]) for match in  
            pattern.scanString(string)]

# ParseAction functions

def joiner(delim):
    return lambda tokens: delim.join(tokens)

def parse_authors(tokens):
    authors = []
    # Note: Since this action is normally chained after
    # a joiner() action, only consider the 0th token
    for token in tokens[0].split(','):
        if not token:
            continue
        token_split = token.strip().split(' ')
        author = {}
        author['family'] = token_split[0]
        if len(token_split) > 1:
            author['given'] = token_split[1]
        authors.append(author)
    return authors

# Character sets

dash_chars = u'-–'
allowed_chars = ',;:\'"&?!'

# Elementary patterns

dashes = pyp.Word(dash_chars)
etal = pyp.Combine('et al' + pyp.ZeroOrMore('.'))
number = pyp.Word(pyp.nums)
words_neglook = ~number + ~etal + ~pyp.Literal('http') + ~pyp.Literal('doi')

word = pyp.Word(pyp.alphanums + dash_chars + allowed_chars)
words = pyp.OneOrMore(words_neglook + word).\
        setParseAction(joiner(' '))
word_journal = pyp.Word(pyp.alphanums + dash_chars + allowed_chars + '.')
words_journal = pyp.OneOrMore(words_neglook + word_journal).\
                setParseAction(joiner(' '))

test = words.setResultsName('test') + pyp.Optional(etal)

# Meta-data patterns

#authors = pyp.Group(words.setParseAction(joiner(' '), parse_authors)).\
#          setParseAction(joiner(' '), parse_authors).\
#          setResultsName('author') + \
#          pyp.Optional(etal)
authors = (pyp.Group(
              words.copy().setParseAction(joiner(' '), parse_authors))
          .setResultsName('author') + \
          pyp.Optional(etal))

date = '(' + number.setResultsName('date') + ')'

title = words.\
        setParseAction(joiner(' ')).\
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
      ).setParseAction(joiner('')).\
      setResultsName('doi')

reference = authors + \
            date + \
            title + \
            '.' + \
            journal + \
            volume + \
            pages + \
            pyp.Optional('.') + \
            doi
