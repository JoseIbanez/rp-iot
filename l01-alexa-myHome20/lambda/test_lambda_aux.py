#!/usr/bin/env python


import sys
import unittest
import json
import datetime
import logging

# Tested module commands
import lambda_aux

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig()



class Test_discover(unittest.TestCase):

    def test_get_user_0(self):

        token = "Atza|IwEBIJD4XEcD7VjOmNzFBKAhnGcONe_DWWytWLPC6KdIo9PfTMMWkTq4EmgdG90nolZByqzjIvgPRm4JfEQuXj9sdbFpsCRYKTtQaP4z7BqziK9fGgk8rk2rqJLarQmzG5KC_HhbR9TH_NRqzorf7_TlQzDsbRqS8Fg94EQZv3CiBqU4X_uTsyM6tFmU_aRT7J5MIlfVTrV3MK9mUZOmVBtTOj9hCQaug1Hcklvwfuu4unX7tBrMgSYONakO_oIcFPSYqRPtna5PGUWQS1yiFNxDpbjZVxbN4XZfaotGZDKgJbIopqDU1nFr0xkmtDE2wFgKPUg0VHXJU5ziaOJIoEEUiJ8mPm9_FhKUzhAXzNE3SkIalabrTQ32U6u6Dix5QRIE3mahFBTz_TLQBGAg5m3ifMcXcKucrTt_SVhdv2Pi-DGyHuc9F8rQIyDjaBXUtyHDL9GCNPlZirII1Arkj8guIa0TmmaxVseBDtPAx-TCLdGfrt_nRWPx_XZQort004pc5kjBQUrdO2Qh-uRzeewPGMWH"
        user_id = lambda_aux.get_user(token)
        
        #Asserts
        self.assertGreater(len(user_id), 0, "user_id is empty")




if __name__ == '__main__':
    unittest.main()