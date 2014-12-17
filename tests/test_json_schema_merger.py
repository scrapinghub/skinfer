#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
from json_schema_merger.json_schema_merger import merge_schema
import unittest
from tests import fixtures


class TestJsonSchemaMerger(unittest.TestCase):

    def test_merge_with_empty_object(self):
        # when:
        first_copy = fixtures.REQUIRE_OBJECT_TYPE.copy()
        second_copy = fixtures.REQUIRING_SOME_PROPERTY.copy()

        merged = merge_schema(fixtures.REQUIRE_OBJECT_TYPE,
                              fixtures.REQUIRING_SOME_PROPERTY)

        # then:
        self.assertEqual(merged, {
            "type": "object",
            "required": [],
            "properties": {
                "something": {"type": "string"},
            }
        })
        # and:
        self.assertEqual(fixtures.REQUIRE_OBJECT_TYPE, first_copy)
        self.assertEqual(fixtures.REQUIRING_SOME_PROPERTY, second_copy)

    def test_merge_two_simple_objects(self):
        # when:
        merged = merge_schema(fixtures.REQUIRING_SOME_PROPERTY,
                              fixtures.REQUIRING_ANOTHER_PROPERTY)

        # then:
        self.assertEqual(merged, {
            "type": "object",
            "required": [],
            "properties": {
                "something": {"type": "string"},
                "another": {"type": "string"},
            }
        })

    def test_merge_nested_properties(self):
        # when:
        merged = merge_schema(
            fixtures.REQUIRING_SOME_PROPERTY,
            fixtures.REQUIRING_SOME_PROPERTY_WITH_NESTED_OPTIONAL_AND_REQUIRED_PROPERTY)

        self.assertEqual(merged, {
            "type": "object",
            "required": ["something"],
            "properties": {
                "something": {
                    "type": "object",
                    "required": [],
                    "properties": {
                        "nested_optional": {"type": "string"},
                        "nested_required": {"type": "string"},
                    }
                },
            }
        })
