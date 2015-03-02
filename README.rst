================================================
Skinfer - JSON Schema Inferring and Merging Tool
================================================

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
