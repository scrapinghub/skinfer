===============================
JSON Schema Merger
===============================

.. image:: https://badge.fury.io/py/json_schema_merger.png
    :target: http://badge.fury.io/py/json_schema_merger

.. image:: https://travis-ci.org/scrapinghub/json_schema_merger.png?branch=master
        :target: https://travis-ci.org/scrapinghub/json_schema_merger

.. image:: https://pypip.in/d/json_schema_merger/badge.png
        :target: https://pypi.python.org/pypi/json_schema_merger


Simple tool to merge JSON schemas

* Free software: BSD license
* Documentation: https://json_schema_merger.readthedocs.org.

Features
--------

A tool that tries to merge a given a list of JSON schemas into one JSON schema
that represents the common properties::

    $ ./bin/json_schema_merger --help
    usage: json_schema_merger [-h] [-o OUTPUT] schemas [schemas ...]
    
    Simple JSON Schema Merger Tool
    
    positional arguments:
      schemas     List of JSON schema files to merge
    
      optional arguments:
        -h, --help  show this help message and exit
        -o OUTPUT   Write JSON schema to this file


A tool that given a list of JSON files, tries to infer the common schema among them::

    $ ./bin/schema_inferer --help
    usage: schema_inferer [-h] [-o OUTPUT] [--jsonlines] SAMPLE [SAMPLE ...]
    
    Generates a JSON schema based on samples
    
    positional arguments:
      SAMPLE       JSON data sample files
    
    optional arguments:
      -h, --help   show this help message and exit
      -o OUTPUT    Write JSON schema to this file
      --jsonlines  Assume samples are in JSON lines format
