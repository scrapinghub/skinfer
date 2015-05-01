#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import json
from tests import fixtures
from skinfer import schema_inferer
import subprocess


class TestJsonSchemaInferer(unittest.TestCase):

    def test_run_infering_schema_for_yelp_samples(self):
        sample1 = fixtures.get_sample('sample1-yelp.json')
        sample2 = fixtures.get_sample('sample2-yelp.json')
        schema = schema_inferer.generate_and_merge_schemas([sample1, sample2])
        self.assertTrue(type(schema) == dict)


class TestSchemaInfererScriptTest(unittest.TestCase):
    def test_run_with_json_samples_in_separate_files(self):
        # given:
        sample1 = fixtures.get_sample_path('minimal-1.json')
        sample2 = fixtures.get_sample_path('sample2-yelp.json')
        # when:
        output = subprocess.check_output(['bin/schema_inferer', sample1, sample2])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)

    def test_run_with_jsonlines_samples(self):
        # given:
        infile = fixtures.get_sample_path('jsonlines.jsonl')
        # when:
        output = subprocess.check_output(['bin/schema_inferer', '--jsonlines', infile])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)

    def test_run_with_jsonlines_samples_omitting_option(self):
        # given:
        infile = fixtures.get_sample_path('jsonlines.jsonl')
        # when:
        output = subprocess.check_output(['bin/schema_inferer', infile])
        # then:
        data = json.loads(output)
        self.assertIsNotNone(data)
        self.assertIn('required', data)
        self.assertIn('properties', data)
