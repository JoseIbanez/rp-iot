#!/usr/bin/env python

import os
#from flask import Flask, request, send_from_directory
import json
import getMaxMin



def main():
    print("Test Case 1, 19250 - Siguenza")
    out=getMaxMin.getMaxMin(probe="b827eb.300520.c3",hours=24,param="temp")

    print(out)
    file = open("/var/lib/balcon/19250.json","w")
    file.write(str(out))
    file.close


    print("Test Case 2, 28039 - Balcon")
    out=getMaxMin.getMaxMin(probe="b827eb.61eb84.c2",hours=24,param="temp")

    print(out)
    file = open("/var/lib/balcon/28039.json","w")
    file.write(json.dumps(out))
    file.close




if __name__ == "__main__":
    main()