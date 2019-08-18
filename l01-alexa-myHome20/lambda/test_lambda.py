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



class Test_discover(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Prepare message
        with open ("../notes/discover.req.json", "r") as myfile:
            data=myfile.read()
        #print(data)
        request = json.loads(data)
        

        #Call target function
        cls.response =  lambda_function.handle_discovery(request)



    def test_reponse_type(self):
        response = self.response
        
        #Asserts
        self.assertEqual(response["event"]["header"]["name"], "Discover.Response", "responseType")




if __name__ == '__main__':
    unittest.main()