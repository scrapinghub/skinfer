from __future__ import unicode_literals
import os
import json


TEST_DIR = os.path.dirname(__file__)
SAMPLES_DIR = os.path.join(TEST_DIR, 'samples')


def get_sample_path(sample_filename):
    return os.path.join(SAMPLES_DIR, sample_filename)


def get_sample(sample_filename):
    with open(get_sample_path(sample_filename)) as f:
        return json.load(f)


REQUIRE_OBJECT_TYPE = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    'type': 'object',
}

REQUIRING_SOME_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    'type': 'object',
    "required": ['something'],
    "properties": {
        "something": {"type": "string"},
    }
}

REQUIRING_NULL_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    'type': 'object',
    "required": ['something'],
    "properties": {
        "something": {"type": "null"},
    }
}

REQUIRING_NUMBER_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    'type': 'object',
    "required": ['number_of_followers'],
    "properties": {
        "number_of_followers": {"type": "number"},
    }
}

REQUIRING_BOOLEAN_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    'type': 'object',
    "required": ['is_this_on'],
    "properties": {
        "is_this_on": {"type": "boolean"},
    }
}

REQUIRING_ANOTHER_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    "type": "object",
    "required": ['another'],
    "properties": {
        "another": {"type": "string"},
    }
}

REQUIRING_SOME_OBJECT_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    'type': 'object',
    "required": ['something'],
    "properties": {
        "something": {"type": "object"},
    }
}


REQUIRING_SOME_PROPERTY_WITH_NESTED_REQUIRED_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    "type": "object",
    "required": ["something"],
    "properties": {
        "something": {
            "type": "object",
            "required": ['nested_required'],
            "properties": {
                "nested_required": {"type": "string"},
            }
        },
    }
}

REQUIRING_SOME_PROPERTY_WITH_NESTED_OPTIONAL_AND_REQUIRED_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    "type": "object",
    "required": ["something"],
    "properties": {
        "something": {
            "type": "object",
            "required": ['nested_required'],
            "properties": {
                "nested_required": {"type": "string"},
                "nested_optional": {"type": "string"},
            }
        },
    }
}

REQUIRING_AN_ARRAY_PROPERTY = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    "type": "object",
    "required": ["a_list"],
    "properties": {
        "a_list": {
            "type": "array",
            "items": {"type": "string"},
        }
    }
}

REQUIRING_AN_ARRAY_PROPERTY_PLUS_ANOTHER = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    "type": "object",
    "required": ["a_list", "another_list"],
    "properties": {
        "a_list": {
            "type": "array",
            "items": {"type": "string"},
        },
        "another_list": {
            "type": "array",
            "items": {"type": "number"},
        },
    }
}


REQUIRING_AN_ARRAY_PROPERTY_WITH_TUPLE_VALIDATION = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    "type": "object",
    "required": ["array_with_tuple"],
    "properties": {
        "array_with_tuple": {
            "type": "array",
            "items": [
                {"type": "string"},
                {"type": "string"},
            ],
        },
    }
}

REQUIRING_AN_ARRAY_PROPERTY_CONFLICTING_WITH_TUPLE = {
    '$schema': u'http://json-schema.org/draft-04/schema',
    "type": "object",
    "required": ["array_with_tuple"],
    "properties": {
        "array_with_tuple": {
            "type": "array",
            "items": {"type": "string"},
        },
    }
}
