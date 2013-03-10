citations
=========

1. Create test JSON

    Manually parse more citations into JSON -- Four done.

    Multiple JSON integration -- test.py handles this now? glob.glob /test/*JSON

1. Revise engine to extrapolate minimal data necessary for initialdatabase construction

    <ol>
    <li>authors</li>
    <li>issued</li>
    <li>title</li>
    <li>journal</li>
    </ol><br />

1. Choose database -- MongoDB, Neo4j, OrientDB, HyperGraphDB, Titan?

1. Heuristic approach to regexing citations

1. Implement re.verbose for readability of complex regular expressions

Schema we're using: https://github.com/citation-style-language/schema/blob/master/csl-data.json
