#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
from tests import fixtures
from skinfer import schema_inferer


class TestJsonSchemaInferer(unittest.TestCase):

    def test_run_infering_schema_for_yelp_samples(self):
        sample1 = fixtures.get_sample('sample1-yelp.json')
        sample2 = fixtures.get_sample('sample2-yelp.json')
        schema = schema_inferer.generate_and_merge_schemas([sample1, sample2])
        self.assertTrue(type(schema) == dict)
