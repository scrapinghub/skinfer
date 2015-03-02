from __future__ import absolute_import, division, print_function, unicode_literals

import json
import gzip
from skinfer.draft4_generator import IncompleteDraft4SchemaGenerator
from skinfer.json_schema_merger import merge_schema


def gzopen(filename):
    if '.gz' in filename:
        return gzip.open(filename)

    return open(filename)


def load_samples_from_jsonlines(file_list):
    for filename in file_list:
        with gzopen(filename) as f:
            for line in f:
                yield json.loads(line)


def load_samples_from_json(file_list):
    for filename in file_list:
        with gzopen(filename) as f:
            yield json.load(f)


def generate_schema_for_sample(sample):
    return IncompleteDraft4SchemaGenerator(sample).to_dict()


def generate_and_merge_schemas(samples):
    merged = generate_schema_for_sample(next(iter(samples)))

    for sample in samples:
        merged = merge_schema(merged, generate_schema_for_sample(sample))

    return merged
