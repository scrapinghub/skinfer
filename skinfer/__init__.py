# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__author__ = 'Scrapinghub'
__email__ = 'info@scrapinghub.com'
__version__ = '0.1.0'

from .json_schema_merger import merge_schema  # NOQA
from .schema_inferer import generate_schema_for_sample as generate_schema  # NOQA
from .schema_inferer import generate_and_merge_schemas as infer_schema  # NOQA
