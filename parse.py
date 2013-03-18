# encoding: utf-8

import re
import collections
import parsley

DASHES = ['-', u'–']
Reference = collections.namedtuple("Reference", "ref names year title journal edition pages doi")

with open("citation.parsley") as gfile:
    grammar = unicode(gfile.read())

def normalize(string):
    string = string.strip()
    string = re.sub(r'\s+', ' ', string)
    return string

parser = parsley.makeGrammar(grammar, dict(DASHES=DASHES,
                             Reference=Reference, normalize=normalize))
