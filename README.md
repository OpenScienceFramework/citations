Citations
=========

This is the part of the Open Science Foundation that parses citations in
various formats.

Example
-------
    cat > citation.txt
    1. Monty P, Circus F (1969) How Not To Be Seen.  Now For Something
    Completely Different 9: 296–305. doi: 42.1024/c.l.py.
    ^D

    citebite citation.txt

    {
        ...
    }


The output follows the schema defined here:
    https://github.com/citation-style-language/schema/blob/master/csl-data.json

Grammars for various formats are in the grammars/ subfolder.
