from __future__ import unicode_literals

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
