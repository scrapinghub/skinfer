#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from json_schema_merger.json_schema_merger import merge_schema
import unittest
from tests import fixtures


class TestJsonSchemaMerger(unittest.TestCase):
    def check_merge_result(self, first, second, expected):
        first_copy = first.copy()
        second_copy = second.copy()

        merged = merge_schema(first, second)
        merged_reversed = merge_schema(second, first)

        self.assertEqual(merged, expected)
        self.assertEqual(merged_reversed, expected)
        self.assertEqual(merged, merged_reversed)

        # ensuring we're not touching the originals:
        self.assertEqual(first, first_copy)
        self.assertEqual(second, second_copy)

    def test_merge_required_property_with_empty_object_schema(self):
        self.check_merge_result(
            fixtures.REQUIRE_OBJECT_TYPE,
            fixtures.REQUIRING_SOME_PROPERTY,
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string"},
                }
            }
        )

    def test_merge_schemas_with_different_required_properties(self):
        self.check_merge_result(
            fixtures.REQUIRING_SOME_PROPERTY,
            fixtures.REQUIRING_ANOTHER_PROPERTY,
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string"},
                    "another": {"type": "string"},
                }
            }
        )

    def test_merge_same_schema_gives_itself(self):
        self.check_merge_result(
            fixtures.REQUIRING_SOME_PROPERTY,
            fixtures.REQUIRING_SOME_PROPERTY,
            fixtures.REQUIRING_SOME_PROPERTY,
        )
        self.check_merge_result(
            fixtures.REQUIRING_SOME_PROPERTY_WITH_NESTED_OPTIONAL_AND_REQUIRED_PROPERTY,
            fixtures.REQUIRING_SOME_PROPERTY_WITH_NESTED_OPTIONAL_AND_REQUIRED_PROPERTY,
            fixtures.REQUIRING_SOME_PROPERTY_WITH_NESTED_OPTIONAL_AND_REQUIRED_PROPERTY,
        )
        self.check_merge_result(
            fixtures.REQUIRING_AN_ARRAY_PROPERTY,
            fixtures.REQUIRING_AN_ARRAY_PROPERTY,
            fixtures.REQUIRING_AN_ARRAY_PROPERTY,
        )

    def test_merge_schemas_with_nested_properties(self):
        self.check_merge_result(
            fixtures.REQUIRING_SOME_OBJECT_PROPERTY,
            fixtures.REQUIRING_SOME_PROPERTY_WITH_NESTED_OPTIONAL_AND_REQUIRED_PROPERTY,
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "required": ["something"],
                "properties": {
                    "something": {
                        "type": "object",
                        "properties": {
                            "nested_optional": {"type": "string"},
                            "nested_required": {"type": "string"},
                        }
                    },
                }
            }
        )

    def test_merge_one_schema_with_nested_array_property(self):
        self.check_merge_result(
            fixtures.REQUIRING_SOME_PROPERTY,
            fixtures.REQUIRING_AN_ARRAY_PROPERTY,
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "a_list": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "something": {"type": "string"}
                }
            }
        )

    def test_merge_both_schemas_with_nested_array_property(self):
        self.check_merge_result(
            fixtures.REQUIRING_AN_ARRAY_PROPERTY,
            fixtures.REQUIRING_AN_ARRAY_PROPERTY_PLUS_ANOTHER,
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "required": ["a_list"],
                "properties": {
                    "a_list": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "another_list": {
                        "type": "array",
                        "items": {"type": "number"},
                    }
                }
            }
        )
