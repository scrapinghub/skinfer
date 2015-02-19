#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from json_schema_merger.draft4_generator import Draft4SchemaGeneratorWithLength
import unittest
from tests import fixtures


def generate_schema(sample):
    return Draft4SchemaGeneratorWithLength(sample).to_dict()


class TestDraft4SchemaGeneratorWithLenght(unittest.TestCase):

    def test_empty_object(self):
        self.assertEqual(generate_schema({}), fixtures.REQUIRE_OBJECT_TYPE)

    def test_simple_object(self):
        self.assertEqual(generate_schema({"something": "ai"}),
                fixtures.REQUIRING_SOME_PROPERTY_WITH_LENGTH)

    def test_object_with_nested_properties(self):
        self.assertEqual(generate_schema({"something": {"nested_required": "1"}}),
                fixtures.REQUIRING_SOME_PROPERTY_WITH_NESTED_REQUIRED_PROPERTY_WITH_LENGTH)

    def test_with_linkedin_minimal_example(self):
        data = fixtures.get_sample('minimal-1.json')

        self.assertEqual(generate_schema(data), {
            '$schema': u'http://json-schema.org/draft-04/schema',
            'properties': {
                u'also_viewed': {'items': {'type': 'string', 'sampled_max_length': 71}, 'type': 'array'},
                u'family_name': {'type': 'string', 'sampled_max_length': 22},
                u'full_name': {'type': 'string', 'sampled_max_length': 32},
                u'given_name': {'type': 'string', 'sampled_max_length': 9},
                u'headline': {'type': 'string', 'sampled_max_length': 2},
                u'linkedin_id': {'type': 'string', 'sampled_max_length': 9},
                u'locality': {'type': 'string', 'sampled_max_length': 7},
                u'num_connections': {'type': 'string', 'sampled_max_length': 1},
                u'updated': {'type': 'string', 'sampled_max_length': 19},
                u'url': {'type': 'string', 'sampled_max_length': 71}},
            'required': [
                u'family_name',
                u'updated',
                u'linkedin_id',
                u'locality',
                u'headline',
                u'num_connections',
                u'url',
                u'also_viewed',
                u'given_name',
                u'full_name'],
            'type': 'object'
        })
