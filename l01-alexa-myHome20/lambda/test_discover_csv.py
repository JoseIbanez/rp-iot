#!/usr/bin/env python


import sys
import unittest
import json
import datetime

# Tested module commands
#import lambda_function
import discover_csv

class Test_response(unittest.TestCase):

    def setUp(self):
        #Prepare message
        with open ("../notes/discover.req.json", "r") as myfile:
            data=myfile.read()
        #print(data)
        request = json.loads(data)
        
        #Call target function
        self.response =  discover_csv.handle_discovery(request)

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