#!/usr/bin/env python


import sys
import unittest
import json
import datetime
import logging

# Tested module commands
#import lambda_function
import discover_csv


# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig()



class Test_response(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Prepare message
        with open ("../notes/discover.req.json", "r") as myfile:
            data=myfile.read()
        #print(data)
        request = json.loads(data)

        myHome = { "user_id": "amzn1.account.TEST"}

        
        #Call target function
        cls.response =  discover_csv.handle_discovery(myHome,request)

    def test_endpoints_len(self):
        response = self.response
        
        #Asserts
        self.assertGreater(len(response["event"]["payload"]["endpoints"]), 2, "List endpoints is not empty")


    def test_sw1_displayCategories(self):
        response = self.response
            
        sw1 = response["event"]["payload"]["endpoints"][0]
        
        #print "#sw1"
        #print sw1
        #print "#sw1[displayCategories]"
        #print sw1["displayCategories"]
        self.assertEqual(sw1["displayCategories"][0], "SWITCH", "displayCategories value")




if __name__ == '__main__':
    unittest.main()