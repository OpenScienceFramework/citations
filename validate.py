import sys

import json, jsonschema

with open("csl-data.json") as f:
    schema = json.load(f)

with open(sys.argv[1]) as f:
    data = json.load(f)

print jsonschema.validate(data, schema)
