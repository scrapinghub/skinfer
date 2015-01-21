from __future__ import absolute_import, division, print_function, unicode_literals

import json
from json_schema_merger.draft4_generator import IncompleteDraft4SchemaGenerator
from json_schema_merger.json_schema_merger import merge_schema


def load_samples_from_jsonlines(file_list):
    for filename in file_list:
        with open(filename) as f:
            for line in f:
                yield json.loads(line)


def load_samples_from_json(file_list):
    for filename in file_list:
        with open(filename) as f:
            yield json.load(f)


def generate_schema_for_sample(sample):
    return IncompleteDraft4SchemaGenerator(sample).to_dict()


def generate_and_merge_schemas(samples):
    merged = generate_schema_for_sample(next(iter(samples)))

    for sample in samples:
        merged = merge_schema(merged, generate_schema_for_sample(sample))

    return merged
