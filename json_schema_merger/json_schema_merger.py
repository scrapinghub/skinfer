# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import itertools


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
    if schema_type == 'object':
        return set(['type', 'properties', 'required'])
    if schema_type == 'array':
        return set(['type', 'items'])
    else:
        raise NotImplementedError(
            "Missing implementation for schema type: %s" % schema_type)


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


def merge_strings(first, second):
    # TODO: add support for schemas more complex than {"type": "string"}
    return second


def merge_numbers(first, second):
    return {"type": "number"}


def merge_booleans(first, second):
    return {"type": "boolean"}


def merge_nulls(first, second):
    return {"type": "null"}


def merge_arrays(first, second):
    def are_json_schema_tuples(first_items, second_items):
        return all([
            isinstance(first_items, list),
            isinstance(second_items, list),
            len(first_items) == len(second_items)
        ])

    def merge_tuples(first_items, second_items):
        return [_merge_schema(e1, e2) for e1, e2 in zip(first_items, second_items)]

    def merge_items(first_items, second_items):
        if not (first_items and second_items):
            return None

        if are_json_schema_tuples(first_items, second_items):
            return merge_tuples(first_items, second_items)

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

    if schema_type == 'object':
        return merge_objects(first, second)
    elif schema_type == 'string':
        return merge_strings(first, second)
    elif schema_type == 'array':
        return merge_arrays(first, second)
    elif schema_type == 'number':
        return merge_numbers(first, second)
    elif schema_type == 'boolean':
        return merge_booleans(first, second)
    elif schema_type == 'null':
        return merge_nulls(first, second)
    else:
        raise NotImplementedError("Type %s is not yet supported" % schema_type)


def merge_schema(first, second):
    if not (type(first) == type(second) == dict):
        raise ValueError("Argument is not a schema")

    if not (first.get('type') == second.get('type') == 'object'):
        raise NotImplementedError("Unsupported root type")

    return merge_objects(first, second)
