#!/usr/bin/env python


import sys
import unittest
import json
import datetime

# Tested module commands
import l_temp

class TestLauncherMethods(unittest.TestCase):

    def test_EnviromentVariables(self):

        #Prepare message
        date=datetime.datetime.utcnow().isoformat()+"Z"
        probe="TEST0101010"
        temp=25678

        data={
            'date': date,
            'probe': probe,
            'temp': temp
            }

        #message=json.dumps({'default': json.dumps(data)})
        message=json.dumps(data)


        self.assertEqual(l_temp.dynamo_insert(message), 0)


if __name__ == '__main__':
    unittest.main()