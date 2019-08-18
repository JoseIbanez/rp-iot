#!/usr/bin/env python


import sys
import unittest
import json
import datetime
import logging

# Tested module commands
import lambda_function

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig()



class Test_iot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        lambda_function.set_thing_state("v03", "led1", "OFF")


    def test_get(self):
        ret = lambda_function.get_thing_state("v03", "led1") 
        print(str(ret))


    def test_set(self):
        lambda_function.set_thing_state("v03", "led1", "ON")
        lambda_function.wait_thing_state("v03", "led1", "ON")





if __name__ == '__main__':
    unittest.main()