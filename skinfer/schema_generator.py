#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import six


def infer_type(obj):
    '''
    Return the inferred JSON schema type for a given JSON object
    :param obj: JSON object
    :return: schema type
    '''
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'boolean'
    if isinstance(obj, six.string_types):
        return 'string'
    if isinstance(obj, (six.integer_types, float)):
        return 'number'
    if isinstance(obj, (list, tuple)):
        return 'array'
    if isinstance(obj, dict):
        return 'object'
    raise ValueError("Unsupported type: %s" % obj.__class__)


def gen_array_schema(obj):
    '''
    Generate JSON schema for an array
    :param obj: array
    :return: schema
    '''
    schema = dict(type='array')
    if len(obj):
        schemas = [generate_schema(e) for e in obj]
        first_schema = schemas[0]
        if all(first_schema == s for s in schemas):
            schema['items'] = first_schema
        else:
            schema['items'] = schemas
    return schema


def gen_object_schema(obj):
    '''
    Generate JSON schema for an object
    :param obj: JSON object
    :return: schema
    '''
    schema = dict(type='object')
    if len(obj):
        schema['properties'] = {}
        for key, value in six.iteritems(obj):
            schema['properties'][key] = generate_schema(value)
        schema['required'] = list(obj.keys())
    return schema


SCHEMA_TYPES = {
    'null': lambda _: dict(type='null'),
    'string': lambda _: dict(type='string'),
    'object': gen_object_schema,
    'array': gen_array_schema,
    'boolean': lambda _: dict(type='boolean'),
    'number': lambda _: dict(type='number'),
}


def generate_schema(obj, top_level=False):
    schema_type = infer_type(obj)
    schema = SCHEMA_TYPES[schema_type](obj)
    if top_level:
        schema['$schema'] = "http://json-schema.org/draft-04/schema"
    return schema


class JsonSchemaGenerator(object):
    def __init__(self, base_object):
        self.base_object = base_object

    def generate(self):
        return generate_schema(self.base_object, top_level=True)