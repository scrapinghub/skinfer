========
Usage
========


Infering schemas from multiple samples
--------------------------------------

Use the `skinfer` script to generate a schema from a list of samples::

    $ skinfer --help
    usage: skinfer [-h] [--jsonlines] SAMPLE [SAMPLE ...]

    Generates a JSON schema based on samples

    positional arguments:
      SAMPLE       JSON data sample files

    optional arguments:
      -h, --help   show this help message and exit
      --jsonlines  Assume samples are in JSON lines format


You can also infer the schema programatically::

    >>> import skinfer, json
    >>> sample1 = {'name': 'Claudio'}
    >>> sample2 = {'name': 'Roberto', 'surname': 'Salazar'}
    >>> schema = skinfer.infer_schema([sample1, sample2])
    >>> import pprint
    >>> pprint.pprint(schema)
    {'$schema': u'http://json-schema.org/draft-04/schema',
     u'properties': {'name': {'type': 'string'}, 'surname': {'type': 'string'}},
     u'required': ['name'],
     u'type': u'object'}

Using the API, you can also generate a schema for only one sample::

    >>> skinfer.generate_schema({"name": "Claudio", "surname": "Salazar"})
    {'$schema': u'http://json-schema.org/draft-04/schema',
     'properties': {'name': {'type': 'string'}, 'surname': {'type': 'string'}},
     'required': ['surname', 'name'],
     'type': 'object'}


Merging existing JSON Schemas
-----------------------------

Use `schema_merger` to merge a list of JSON schemas into one
JSON schema that represents the common properties::

    $ schema_merger --help
    usage: schema_merger [-h] [-o OUTPUT] schemas [schemas ...]

    Merges given JSON Schemas, inferring the required properties

    positional arguments:
      schemas     List of JSON schema files to merge

      optional arguments:
        -h, --help  show this help message and exit
        -o OUTPUT   Write JSON schema to this file


You can also merge the schema programatically::


    >>> import skinfer
    >>> any_object = {'type': 'object'}
    >>> requires_name = {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}}}
    >>> merged_schema = skinfer.merge_schema(any_object, requires_name)
    >>> import pprint
    >>> pprint.pprint(merged_schema)
    {u'properties': {'name': {'type': 'string'}}, u'type': u'object'}
