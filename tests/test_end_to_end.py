import json
import sys
import tempfile
import unittest
from subprocess import check_output
from tests import fixtures


FALLBACK_ENCODING = 'utf-8'
STDOUT_ENCODING = sys.stdout.encoding or FALLBACK_ENCODING


def run(cmdline):
    '''
    Run a cmdline spec and return its decoded output
    :param cmdline:
    :return: decoded output
    '''
    return check_output(cmdline).decode(STDOUT_ENCODING)


class SkinferScriptTest(unittest.TestCase):
    script = 'skinfer'
    def test_end_to_end_simple_run(self):
        # given:
        _, filename = tempfile.mkstemp()
        with open(filename, 'w') as f:
            f.write('{"one": "two"}')

        expected = {
            "$schema": "http://json-schema.org/draft-04/schema",
            "required": [
                "one"
            ],
            "type": "object",
            "properties": {
                "one": {
                    "type": "string"
                }
            }
        }

        # when:
        output = run([self.script, filename])
        # then:
        self.assertEqual(expected, json.loads(output))

    def test_run_with_json_samples_in_separate_files(self):
        # given:
        sample1 = fixtures.get_sample_path('minimal-1.json')
        sample2 = fixtures.get_sample_path('sample2-yelp.json')
        # when:
        output = run([self.script, sample1, sample2])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)

    def test_run_with_jsonlines_samples(self):
        # given:
        infile = fixtures.get_sample_path('jsonlines.jsonl')
        # when:
        output = run([self.script, '--jsonlines', infile])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)

    def test_run_with_gzipped_jsonlines(self):
        # given:
        infile = fixtures.get_sample_path('jsonlines.jsonl.gz')
        # when:
        output = run([self.script, '--jsonlines', infile])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)

    def test_run_with_jsonlines_samples_omitting_option(self):
        # given:
        infile = fixtures.get_sample_path('jsonlines.jsonl')
        # when:
        output = run([self.script, infile])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)
