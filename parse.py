# encoding: utf-8

import re
import collections
import parsley

DASHES = ['-', u'–']
fields = "ref names year title journal edition pages doi".split()
Reference = collections.namedtuple("Reference", ' '.join(fields))

def to_dict(*reference):
    return dict(zip(fields, reference))

def normalize(string):
    string = string.strip()
    string = re.sub(r'\s+', ' ', string)
    return string

with open("citation.parsley") as gfile:
    grammar = unicode(gfile.read())

parser = parsley.makeGrammar(grammar, dict(DASHES=DASHES,
                             Reference=Reference, normalize=normalize))
