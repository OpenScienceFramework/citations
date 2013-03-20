# encoding: utf-8

import collections
import glob
import re

import parsley

DASHES = ['-', u'–']
fields = "ref names year title journal edition pages doi".split()
Reference = collections.namedtuple("Reference", ' '.join(fields))

def normalize(string):
    string = string.strip()
    string = re.sub(r'\s+', ' ', string)
    return string

for gname in glob.glob("grammars/*.parsley"):
    with open(gname) as gfile:
        grammar = unicode(gfile.read())

parser = parsley.makeGrammar(grammar, dict(DASHES=DASHES,
                             Reference=Reference, normalize=normalize))

def to_dict(s):
    return parser(s).line()._asdict()
