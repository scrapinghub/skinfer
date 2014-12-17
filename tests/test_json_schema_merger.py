#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_json_schema_merger
----------------------------------

Tests for `json_schema_merger` module.
"""

from __future__ import absolute_import, division, print_function
from json_schema_merger import merge_schema
import unittest


# Some fixtures:
REQUIRE_OBJECT_TYPE = {"type": "object"}

REQUIRING_SOME_PROPERTY = {
    "type": "object",
    "required": ['something'],
    "properties": {
        "something": {},
    }
}

REQUIRING_ANOTHER_PROPERTY = {
    "type": "object",
    "required": ['another'],
    "properties": {
        "another": {},
    }
}

REQUIRING_SOME_PROPERTY_WITH_NESTED_PROPERTIES = {
    "type": "object",
    "required": ["something"],
    "properties": {
        "something": {
            "type": "object",
            "required": ['nested_required'],
            "properties": {
                "nested_optional": {},
                "nested_required": {},
            }
        },
    }
}


class TestJsonSchemaMerger(unittest.TestCase):
    def test_merge_with_empty_object(self):
        # when:
        first_copy = REQUIRE_OBJECT_TYPE.copy()
        second_copy = REQUIRING_SOME_PROPERTY.copy()

        merged = merge_schema(REQUIRE_OBJECT_TYPE,
                              REQUIRING_SOME_PROPERTY)

        # then:
        self.assertEquals(merged, {
            "type": "object",
            "required": [],
            "properties": {
                "something": {},
            }
        })
        # and:
        self.assertEquals(REQUIRE_OBJECT_TYPE, first_copy)
        self.assertEquals(REQUIRING_SOME_PROPERTY, second_copy)

    def test_merge_two_simple_objects(self):
        # when:
        merged = merge_schema(REQUIRING_SOME_PROPERTY,
                              REQUIRING_ANOTHER_PROPERTY)

        # then:
        self.assertEquals(merged, {
            "type": "object",
            "required": [],
            "properties": {
                "something": {},
                "another": {},
            }
        })

    def test_merge_nested_properties(self):
        # when:
        merged = merge_schema(
            REQUIRING_SOME_PROPERTY,
            REQUIRING_SOME_PROPERTY_WITH_NESTED_PROPERTIES)

        self.assertEquals(merged, {
            "type": "object",
            "required": ["something"],
            "properties": {
                "something": {
                    "type": "object",
                    "required": [],
                    "properties": {
                        "nested_optional": {},
                        "nested_required": {},
                    }
                },
            }
        })

# if __name__ == '__main__':
#     unittest.main()
