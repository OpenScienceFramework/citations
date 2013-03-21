# encoding: utf-8
"""
Parse module for parsing citations into structured data. Currently this uses
the Parsley library to do this, the grammars are defined in the grammars/
folder and cycled through until one is found that works.

to_dict will convert the Reference named tuple into a dictionary, which allows
for easy transformation into JSON.
"""
import collections
import glob
import re

import parsley

DASHES = ['-', u'–']

fields = "ref names year title journal edition pages doi".split()
Reference = collections.namedtuple("Reference", ' '.join(fields))

def normalize(string):
    """Normalize whitespace."""
    string = string.strip()
    string = re.sub(r'\s+', ' ', string)
    return string

parsers = []
for gname in glob.glob("grammars/*.parsley"):
    with open(gname) as gfile:
        grammar = unicode(gfile.read())
        parser = parsley.makeGrammar(grammar, dict(DASHES=DASHES,
                                     Reference=Reference, normalize=normalize))
        parsers.append(parser)

def parse(text):
    """
    Attempt to parse data into a Reference named tuple. Returns None if it
    fails.
    """
    for parser in parsers:
        try:
            return parser(text).line()
        except Exception:
            pass

def to_dict(s):
    """Turns a citation into a dictioarny that can then be turned into JSON."""
    return parser(s).line()._asdict()
