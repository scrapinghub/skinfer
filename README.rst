============================================
Skinfer - tool for working with JSON schemas
============================================

.. image:: https://badge.fury.io/py/skinfer.png
    :target: http://badge.fury.io/py/skinfer

.. image:: https://travis-ci.org/scrapinghub/skinfer.png?branch=master
        :target: https://travis-ci.org/scrapinghub/skinfer

.. image:: https://pypip.in/d/skinfer/badge.png
        :target: https://pypi.python.org/pypi/skinfer

Data by itself is not that useful if you don't have a way to describe it. `Scrapinghub`_ engineers developed Skinfer to automatically discover the schema of a dataset by analyzing multiple JSON samples and merging the schemas from them.

.. _Scrapinghub: http://scrapinghub.com

Skinfer is a simple tool to infer and/or merge JSON schemas

* Free software: BSD license
* Documentation: https://skinfer.readthedocs.org.

Features
--------

* Generating schema in **JSON Schema draft 4** format
* Inferring schema from multiple samples
* Merging schemas - nice for generating schema in Map-Reduce fashion
  or updating an old schema with new data


Example of using `skinfer` to generate a schema from a list of samples::

    $ cat samples.jsonl
    {"name": "Claudio", "age": 29}
    {"name": "Roberto", "surname": "Gomez", "age": 72}
    $ skinfer --jsonlines samples.jsonl
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


Install with::

    $ pip install skinfer

Or, if you don't have ``pip``, you can still install it with::

    $ easy_install skinfer
