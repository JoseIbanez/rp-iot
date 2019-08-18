#!/usr/bin/env python

import logging
import urllib2
import json



# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_user(bearerToken):

    try:
        data = urllib2.urlopen("https://api.amazon.com/user/profile?access_token="+bearerToken).read()
        profile = json.loads(data)
        user_id = profile["user_id"]
    except:
        user_id = None

    if not user_id:
        user_id = "amzn1.account.TEST"

    logger.info("getUser: user_id: "+user_id)
    return user_id
