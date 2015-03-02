#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import json_schema_generator
from json_schema_generator.schema_types import ArrayType, ObjectType


class Type(json_schema_generator.schema_types.Type):
    schema_version = u"http://json-schema.org/draft-04/schema"


class IncompleteDraft4SchemaGenerator(json_schema_generator.SchemaGenerator):
    """Patching json_schema_generator.SchemaGenerator to generate
    Draft4 valid schemas

    See original at:
    https://github.com/perenecabuto/json_schema_generator/blob/master/json_schema_generator/generator.py

    This is a hack, just a copy of the method from the base class with
    a few changes to generate a valid Draft4 schema.

    We should implement a full Draft4SchemaGenerator -- probably upstream.
    """
    def to_dict(self, base_object=None, object_id=None, first_level=True):
        schema_dict = {}

        if first_level:
            base_object = self.base_object
            schema_dict["$schema"] = Type.schema_version

        base_object_type = type(base_object)
        schema_type = Type.get_schema_type_for(base_object_type)

        schema_dict["type"] = schema_type.json_type

        if schema_type == ObjectType and len(base_object) > 0:
            schema_dict["properties"] = {}
            schema_dict["required"] = list(base_object.keys())

            for prop, value in base_object.items():
                schema_dict["properties"][prop] = self.to_dict(value, prop, False)

        elif schema_type == ArrayType and len(base_object) > 0:
            first_item_type = type(base_object[0])
            same_type = all((type(item) == first_item_type for item in base_object))

            if same_type:
                schema_dict['items'] = self.to_dict(base_object[0], 0, False)

            else:
                schema_dict['items'] = []

                for idx, item in enumerate(base_object):
                    schema_dict['items'].append(self.to_dict(item, idx, False))

        return schema_dict
