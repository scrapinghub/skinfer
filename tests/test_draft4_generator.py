#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
from json_schema_merger.draft4_generator import IncompleteDraft4SchemaGenerator
import unittest
from tests import fixtures
import os
import json


TEST_DIR = os.path.dirname(__file__)
SAMPLES_DIR = os.path.join(TEST_DIR, 'samples')


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
        with open(os.path.join(SAMPLES_DIR, 'minimal-1.json')) as f:
            data = json.load(f)

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
