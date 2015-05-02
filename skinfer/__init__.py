# -*- coding: utf-8 -*-
"""
Skinfer - tools for inferring and merging JSON schemas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic usage of inferring schemas:

    >>> import skinfer, pprint
    >>> sample1 = {'name': 'Claudio'}
    >>> sample2 = {'name': 'Roberto', 'surname': 'Salazar'}
    >>> merged_schema = skinfer.infer_schema([sample1, sample2])
    >>> pprint.pprint(merged_schema)
    {'$schema': u'http://json-schema.org/draft-04/schema',
      u'properties': {'name': {u'type': u'string'}, 'surname': {'type': 'string'}},
      u'required': ['name'],
      u'type': u'object'}

and merging schemas manually:

    >>> schema1 = skinfer.generate_schema(sample1)
    >>> schema2 = skinfer.generate_schema(sample2)
    >>> final_schema = skinfer.merge_schema(schema1, schema2)
    >>> assert merged_schema == final_schema

"""

from __future__ import absolute_import, division, print_function


__author__ = 'Scrapinghub'
__email__ = 'info@scrapinghub.com'
__version__ = '0.1.1'


from .json_schema_merger import merge_schema  # NOQA
from .schema_inferer import generate_schema_for_sample as generate_schema  # NOQA
from .schema_inferer import generate_and_merge_schemas as infer_schema  # NOQA
