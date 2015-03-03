========
Usage
========


Infering schemas from multiple samples
--------------------------------------

Use the `schema_inferer` script to generate a schema from a list of samples::

    $ ./bin/schema_inferer --help
    usage: schema_inferer [-h] [-o OUTPUT] [--jsonlines] SAMPLE [SAMPLE ...]

    Generates a JSON schema based on samples

    positional arguments:
      SAMPLE       JSON data sample files

    optional arguments:
      -h, --help   show this help message and exit
      -o OUTPUT    Write JSON schema to this file
      --jsonlines  Assume samples are in JSON lines format


You can also do schema inference programatically::

    >>> import json
    >>> sample1 = {'name': 'Claudio'}
    >>> sample2 = {'name': 'Roberto', 'surname': 'Salazar'}
    >>> from skinfer.schema_inferer import generate_and_merge_schemas
    >>> schema = generate_and_merge_schemas([sample1, sample2])
    >>> import pprint
    >>> pprint.pprint(schema)
    {'$schema': u'http://json-schema.org/draft-04/schema',
     u'properties': {'name': {'type': 'string'}, 'surname': {'type': 'string'}},
     u'required': ['name'],
     u'type': u'object'}


Merging existing JSON Schemas
-----------------------------

Use `json_schema_merger` to merge a list of JSON schemas into one
JSON schema that represents the common properties::

    $ ./bin/json_schema_merger --help
    usage: json_schema_merger [-h] [-o OUTPUT] schemas [schemas ...]

    Merges given JSON Schemas, inferring the required properties

    positional arguments:
      schemas     List of JSON schema files to merge

      optional arguments:
        -h, --help  show this help message and exit
        -o OUTPUT   Write JSON schema to this file


You can also use the schema merging programatically::


    >>> any_object = {'type': 'object'}
    >>> requires_name = {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}}}
    >>> from skinfer.json_schema_merger import merge_schema
    >>> merged_schema = merge_schema(any_object, requires_name)
    >>> import pprint
    >>> pprint.pprint(merged_schema)
    {u'properties': {'name': {'type': 'string'}}, u'type': u'object'}

