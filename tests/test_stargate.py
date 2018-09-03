import re
import os
import glob

import json
import pydash
import logging
import unittest

from mock import Mock
from mock import patch
from mock import MagicMock


class TestStargate(unittest.TestCase):

    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass
        # clean up logic for the test suite declared in the test module

    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass
        # initialization logic

    # code that is executed before each test
    def setUp(self):
        pass
        # clean up logic

    # code that is executed after each test
    def tearDown(self):
        pass
        # test method

    def camel_to_snake(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def camel_to_snake_upper(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

    # runs the unit tests in the module
