# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import itertools
import sys


def merge_property_list(first_properties, second_properties):
    result = {}

    for key, value in first_properties.items():
        if key in second_properties:
            result[key] = _merge_schema(value, second_properties[key])
        else:
            result[key] = value

    for key, value in second_properties.items():
        if key not in result:
            result[key] = value

    return result


def get_reserved_keys(schema_type):
    if (schema_type not in SCHEMA_TYPES or
            'reserved_keys' not in SCHEMA_TYPES[schema_type]):
        mesg = "Missing implementation for schema type: %s" % schema_type
        raise NotImplementedError(mesg)

    return SCHEMA_TYPES[schema_type]['reserved_keys']


def copy_nonreserved_keys(first, second):
    reserved_keys = get_reserved_keys(first.get('type'))

    return ((key, value)
            for key, value in itertools.chain(first.items(), second.items())
            if key not in reserved_keys)


def merge_objects(first, second):
    required = list(set(first.get('required', [])) &
                    set(second.get('required', [])))

    result = {
        'type': 'object',
        'properties': merge_property_list(first.get('properties', {}),
                                          second.get('properties', {})),
    }

    if required:
        result['required'] = required

    result.update(copy_nonreserved_keys(first, second))

    return result


def min_or_none(val1, val2):
    """Returns min(val1, val2) returning None only if both values are None"""
    return min(val1, val2, key=lambda x: sys.maxint if x is None else x)


def max_or_none(val1, val2):
    """Returns max(val1, val2) returning None only if both values are None"""
    return max(val1, val2, key=lambda x: -sys.maxint if x is None else x)


def merge_strings(first, second):
    result = {'type': 'string'}

    result.update(copy_nonreserved_keys(first, second))

    minLength = min_or_none(first.get('minLength'), second.get('minLength'))
    if minLength:
        result['minLength'] = minLength

    maxLength = max_or_none(first.get('maxLength'), second.get('maxLength'))
    if maxLength:
        result['maxLength'] = maxLength

    return result


def merge_numbers(first, second):
    return {"type": "number"}


def merge_booleans(first, second):
    return {"type": "boolean"}


def merge_nulls(first, second):
    return {"type": "null"}


def merge_arrays(first, second):
    def is_schema_tuple(item):
        return isinstance(item, list)

    def are_json_schema_tuples(first_items, second_items):
        return all([
            is_schema_tuple(first_items),
            is_schema_tuple(second_items),
            len(first_items) == len(second_items)
        ])

    def merge_tuples(first_items, second_items):
        return [_merge_schema(e1, e2) for e1, e2 in zip(first_items, second_items)]

    def merge_array_list_with_array_tuple(first_items, second_items):
        tuple_items, merged = first_items, second_items

        if is_schema_tuple(merged):
            tuple_items, merged = merged, tuple_items

        for schema in tuple_items:
            merged = _merge_schema(merged, schema)

        return merged

    def merge_items(first_items, second_items):
        if not (first_items and second_items):
            return None

        if are_json_schema_tuples(first_items, second_items):
            return merge_tuples(first_items, second_items)

        if is_schema_tuple(first_items) or is_schema_tuple(second_items):
            return merge_array_list_with_array_tuple(first_items, second_items)

        return _merge_schema(first_items, second_items)

    items = merge_items(first.get('items'), second.get('items'))

    result = {
        'type': 'array',
    }

    if items:
        result['items'] = items

    result.update(copy_nonreserved_keys(first, second))

    return result


def merge_with_any_of(first, second):
    first_any_of = first['anyOf'] if 'anyOf' in first else [first]
    second_any_of = second['anyOf'] if 'anyOf' in second else [second]

    any_of = []
    for schema in first_any_of + second_any_of:
        if schema not in any_of:
            any_of.append(schema)

    return {"anyOf": any_of}


def _merge_schema(first, second):
    if first.get('type') != second.get('type'):
        return merge_with_any_of(first, second)

    if 'anyOf' in first or 'anyOf' in second:
        return merge_with_any_of(first, second)

    schema_type = first.get('type')

    if schema_type not in SCHEMA_TYPES:
        raise NotImplementedError("Type %s is not yet supported" % schema_type)

    merge_function = SCHEMA_TYPES[schema_type]['merge_function']
    return merge_function(first, second)


def merge_schema(first, second):
    """Returns the result of merging the two given schemas.
    """
    if not (type(first) == type(second) == dict):
        raise ValueError("Argument is not a schema")

    if not (first.get('type') == second.get('type') == 'object'):
        raise NotImplementedError("Unsupported root type")

    return merge_objects(first, second)


SCHEMA_TYPES = {
    'object': {
        'merge_function': merge_objects,
        'reserved_keys': set(['type', 'properties', 'required']),
    },
    'string': {
        'merge_function': merge_strings,
        'reserved_keys': set(['type', 'minLength', 'maxLength']),
    },
    'array': {
        'merge_function': merge_arrays,
        'reserved_keys': set(['type', 'items']),
    },
    'number': {
        'merge_function': merge_numbers,
    },
    'boolean': {
        'merge_function': merge_booleans,
    },
    'null': {
        'merge_function': merge_nulls,
    },
}
