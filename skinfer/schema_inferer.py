from __future__ import absolute_import, division, print_function, unicode_literals

import json
import gzip
from skinfer.draft4_generator import IncompleteDraft4SchemaGenerator
from skinfer.json_schema_merger import merge_schema


class GzipFileShim(gzip.GzipFile):
    """Python 2.6 Shim
    See https://mail.python.org/pipermail/tutor/2009-November/072959.html
    """
    def __enter__(self):
        if self.fileobj is None:
            raise ValueError("I/O operation on closed GzipFile object")
        return self

    def __exit__(self, *args):
        self.close()


def gzopen(filename):
    if '.gz' in filename:
        return GzipFileShim(filename)

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
    """Returns a schema generated for the given sample.
    """
    return IncompleteDraft4SchemaGenerator(sample).to_dict()


def generate_and_merge_schemas(samples):
    """Iterates through the given samples, generating schemas
    and merging them, returning the resulting merged schema.

    """
    merged = generate_schema_for_sample(next(iter(samples)))

    for sample in samples:
        merged = merge_schema(merged, generate_schema_for_sample(sample))

    return merged
