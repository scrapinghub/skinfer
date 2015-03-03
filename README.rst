============================================
Skinfer - tool for working with JSON schemas
============================================

.. image:: https://badge.fury.io/py/skinfer.png
    :target: http://badge.fury.io/py/skinfer

.. image:: https://travis-ci.org/scrapinghub/skinfer.png?branch=master
        :target: https://travis-ci.org/scrapinghub/skinfer

.. image:: https://pypip.in/d/skinfer.png
        :target: https://pypi.python.org/pypi/skinfer


Simple tool to infer and/or merge JSON schemas

* Free software: BSD license
* Documentation: https://skinfer.readthedocs.org.

Features
--------

Use `schema_inferer` to generate a schema from a list of samples::

    $ cat samples.json
    {"name": "Claudio", "age": 29}
    {"name": "Roberto", "surname": "Gomez", "age": 72}
    $ ./bin/schema_inferer --jsonlines samples.json
    {
        "$schema": "http://json-schema.org/draft-04/schema",
        "required": [
            "age",
            "name"
        ],
        "type": "object",
        "properties": {
            "age": {
                "type": "number"
            },
            "surname": {
                "type": "string"
            },
            "name": {
                "type": "string"
            }
        }
    }


Use `json_schema_merger` to merge a list of JSON schemas into one
JSON schema that represents the common properties::

    $ cat schema1.json  # schema requiring name and age properties
    {
        "$schema": "http://json-schema.org/draft-04/schema",
        "required": [
            "age",
            "name"
        ],
        "type": "object",
        "properties": {
            "age": {
                "type": "number"
            },
            "name": {
                "type": "string"
            }
        }
    }
    $ cat schema2.json  # schema with no age, but requiring name
    {
        "$schema": "http://json-schema.org/draft-04/schema",
        "required": [
            "name"
        ],
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            }
        }
    }
    $ ./bin/json_schema_merger schema1.json schema2.json
    {
        "$schema": "http://json-schema.org/draft-04/schema",
        "required": [
            "name"
        ],
        "type": "object",
        "properties": {
            "age": {
                "type": "number"
            },
            "name": {
                "type": "string"
            }
        }
    }
