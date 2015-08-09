#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import unittest
import json
from tests import fixtures
from skinfer import schema_inferer
from subprocess import check_output


class TestJsonSchemaInferer(unittest.TestCase):

    def test_run_infering_schema_for_yelp_samples(self):
        sample1 = fixtures.get_sample('sample1-yelp.json')
        sample2 = fixtures.get_sample('sample2-yelp.json')
        schema = schema_inferer.generate_and_merge_schemas([sample1, sample2])
        self.assertTrue(type(schema) == dict)

    def test_load_json_samples(self):
        # given:
        sample1 = fixtures.get_sample_path('sample1-yelp.json')
        sample2 = fixtures.get_sample_path('sample2-yelp.json')

        # when:
        samples = list(schema_inferer.load_samples_from_json([sample1, sample2]))

        # then:
        self.assertEquals(2, len(samples))

    def test_load_jsonlines_samples(self):
        # given:
        infile = fixtures.get_sample_path('jsonlines.jsonl.gz')

        # when:
        samples = list(schema_inferer.load_samples_from_jsonlines([infile]))

        # then:
        self.assertEquals(3, len(samples))


class TestCasePython26Shim(unittest.TestCase):
    def assertIsNotNone(self, value):
        self.assertFalse(value is None, "%r is not None" % value)

    def assertIn(self, value, seq):
        self.assertTrue(value in seq, "%r is not in %r" % (value, seq))


class TestSchemaInfererScriptTest(TestCasePython26Shim):
    def test_run_with_json_samples_in_separate_files(self):
        # given:
        sample1 = fixtures.get_sample_path('minimal-1.json')
        sample2 = fixtures.get_sample_path('sample2-yelp.json')
        # when:
        output = check_output(['bin/schema_inferer', sample1, sample2])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)

    def test_run_with_jsonlines_samples(self):
        # given:
        infile = fixtures.get_sample_path('jsonlines.jsonl')
        # when:
        output = check_output(['bin/schema_inferer', '--jsonlines', infile])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)

    def test_run_with_jsonlines_samples_omitting_option(self):
        # given:
        infile = fixtures.get_sample_path('jsonlines.jsonl')
        # when:
        output = check_output(['bin/schema_inferer', infile])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)
