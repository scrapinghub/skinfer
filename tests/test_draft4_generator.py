#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
from skinfer.draft4_generator import IncompleteDraft4SchemaGenerator
import unittest
from tests import fixtures


def generate_schema(sample):
    return IncompleteDraft4SchemaGenerator(sample).to_dict()


class TestDraft4SchemaGenerator(unittest.TestCase):
    def test_empty_object(self):
        self.assertEqual(generate_schema({}), fixtures.REQUIRE_OBJECT_TYPE)

    def test_simple_object(self):
        self.assertEqual(generate_schema({"something": "ai"}),
                         fixtures.REQUIRING_SOME_PROPERTY)

    def test_object_with_nested_properties(self):
        self.assertEqual(generate_schema({"something": {"nested_required": "1"}}),
                         fixtures.REQUIRING_SOME_PROPERTY_WITH_NESTED_REQUIRED_PROPERTY)

    def test_with_linkedin_minimal_example(self):
        data = fixtures.get_sample('minimal-1.json')

        self.assertEqual(generate_schema(data), {
            '$schema': u'http://json-schema.org/draft-04/schema',
            'properties': {
                u'also_viewed': {'items': {'type': 'string'}, 'type': 'array'},
                u'family_name': {'type': 'string'},
                u'full_name': {'type': 'string'},
                u'given_name': {'type': 'string'},
                u'headline': {'type': 'string'},
                u'linkedin_id': {'type': 'string'},
                u'locality': {'type': 'string'},
                u'num_connections': {'type': 'string'},
                u'updated': {'type': 'string'},
                u'url': {'type': 'string'}},
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
