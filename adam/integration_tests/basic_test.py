# This is janky. Why do we have to do this?
import sys
sys.path.append('..')

from adam import Service
from adam import ConfigManager

import json
import unittest

import os

class BasicTest(unittest.TestCase):
    """Basic integration test to demonstrate use of service tester.
    
    """
    def setUp(self):
        config = ConfigManager(os.getcwd() + '/config.json').get_config()
        self.service = Service(config)
        self.assertTrue(self.service.setup())
        self.assertIsNotNone(self.service.new_working_project())

    def tearDown(self):
        self.service.teardown()
        
    def test_basic(self):
        print("Hello world")
        

if __name__ == '__main__':
    unittest.main()