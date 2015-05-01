#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from skinfer.json_schema_merger import merge_schema
import unittest
from tests import fixtures


def recursive_sort(obj):
    """
    Recursively sort list or dict nested lists
    """

    if isinstance(obj, dict):
        for key, val in obj.iteritems():
            obj[key] = recursive_sort(val)
        _sorted = obj

    elif isinstance(obj, list):
        new_list = []
        for val in obj:
            new_list.append(recursive_sort(val))
        _sorted = sorted(new_list)

    else:
        _sorted = obj

    return _sorted


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

    def test_merge_array_with_tuple_validation(self):
        self.check_merge_result(
            fixtures.REQUIRING_AN_ARRAY_PROPERTY_WITH_TUPLE_VALIDATION,
            fixtures.REQUIRING_AN_ARRAY_PROPERTY_WITH_TUPLE_VALIDATION,
            {
                '$schema': 'http://json-schema.org/draft-04/schema',
                "required": ["array_with_tuple"],
                'type': 'object',
                'properties': {
                    'array_with_tuple': {
                        'items': [{'type': 'string'}, {'type': 'string'}],
                        'type': u'array'
                    }
                }
            }
        )

    def test_merge_simple_numbers(self):
        self.check_merge_result(
            fixtures.REQUIRING_NUMBER_PROPERTY,
            fixtures.REQUIRING_NUMBER_PROPERTY,
            {
                '$schema': 'http://json-schema.org/draft-04/schema',
                'type': 'object',
                'required': ['number_of_followers'],
                'properties': {
                    'number_of_followers': {
                        'type': 'number',
                    }
                }
            }
        )

    def test_merge_simple_boolean(self):
        self.check_merge_result(
            fixtures.REQUIRING_BOOLEAN_PROPERTY,
            fixtures.REQUIRING_BOOLEAN_PROPERTY,
            {
                '$schema': 'http://json-schema.org/draft-04/schema',
                'type': 'object',
                'required': ['is_this_on'],
                'properties': {
                    'is_this_on': {
                        'type': 'boolean',
                    }
                }
            }
        )

    def assertSchemaEqual(self, first, second):
        self.assertEqual(recursive_sort(first), recursive_sort(second))

    def test_merge_string_and_null(self):
        merged = merge_schema(
            fixtures.REQUIRING_NULL_PROPERTY,
            fixtures.REQUIRING_SOME_PROPERTY,
        )
        expected = {
            '$schema': 'http://json-schema.org/draft-04/schema',
            'type': 'object',
            'required': ['something'],
            'properties': {
                'something': {
                    'anyOf': [
                        {'type': 'string'},
                        {'type': 'null'},
                    ]
                }
            }
        }
        self.assertSchemaEqual(merged, expected)

    def test_merge_anyof(self):
        schema_with_anyof = {
            '$schema': 'http://json-schema.org/draft-04/schema',
            'type': 'object',
            'required': ['something'],
            'properties': {
                'something': {
                    'anyOf': [
                        {'type': 'string'},
                        {'type': 'null'},
                    ]
                }
            }
        }
        merged = merge_schema(fixtures.REQUIRING_SOME_PROPERTY, schema_with_anyof)
        self.assertSchemaEqual(merged, schema_with_anyof)

    def test_merge_null(self):
        self.check_merge_result(
            fixtures.REQUIRING_NULL_PROPERTY,
            fixtures.REQUIRING_NULL_PROPERTY,
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "required": ["something"],
                "properties": {
                    "something": {"type": "null"},
                }
            }
        )

    def test_merge_tuple_with_loose_array(self):
        self.check_merge_result(
            fixtures.REQUIRING_AN_ARRAY_PROPERTY_WITH_TUPLE_VALIDATION,
            fixtures.REQUIRING_AN_ARRAY_PROPERTY_CONFLICTING_WITH_TUPLE,
            {
                '$schema': 'http://json-schema.org/draft-04/schema',
                "required": ["array_with_tuple"],
                'type': 'object',
                'properties': {
                    'array_with_tuple': {
                        'items': {'type': 'string'},
                        'type': u'array'
                    }
                }
            }
        )

    def test_merge_string_keeping_custom_props(self):
        self.check_merge_result(
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "default": "botemo"},
                }
            },
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "description": "Something"},
                }
            },
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "description": "Something", "default": "botemo"},
                }
            }
        )

    def test_merge_string_minlength_nolength(self):
        self.check_merge_result(
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "minLength": 2},
                }
            },
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string"},
                }
            },
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "minLength": 2},
                }
            },
        )

    def test_merge_string_maxlength_nolength(self):
        self.check_merge_result(
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "maxLength": 22},
                }
            },
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "minLength": 2},
                }
            },
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "minLength": 2, "maxLength": 22},
                }
            },
        )

    def test_merge_string_minlength_maxlength(self):
        self.check_merge_result(
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "minLength": 2, "maxLength": 10},
                }
            },
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "minLength": 4, "maxLength": 12},
                }
            },
            {
                '$schema': u'http://json-schema.org/draft-04/schema',
                "type": "object",
                "properties": {
                    "something": {"type": "string", "minLength": 2, "maxLength": 12},
                }
            }
        )
