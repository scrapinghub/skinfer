# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


def merge_property_list(first_properties, second_properties):
    result = {}

    for key, value in first_properties.items():
        if key in second_properties:
            # TODO: check types here -- if differ, generate an anyOf
            result[key] = merge_objects(value, second_properties[key])
        else:
            result[key] = value

    for key, value in second_properties.items():
        if key not in result:
            result[key] = value

    return result


def merge_objects(first, second):
    required = list(set(first.get('required', [])) &
                    set(second.get('required', [])))

    result = {
        'type': 'object',
        'properties': merge_property_list(first.get('properties', {}),
                                          second.get('properties', {})),
        'required': required
    }

    return result


def merge_schema(first, second):
    if not (type(first) == type(second) == dict):
        raise ValueError("Argument is not a schema")

    if not (first.get('type') == second.get('type') == 'object'):
        raise NotImplementedError("Unsupported root type")

    return merge_objects(first, second)
