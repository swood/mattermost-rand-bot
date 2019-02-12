#!/usr/bin/env python

import sys
import json
import bcrypt
import os
import re
#import MySQLdb
import datetime
import subprocess
from subprocess import call
import requests
import random

mattermost_base_url = ''
mattermost_integration_user = ''
mattermost_integration_token = ''
headers = {'Authorization': 'Bearer %s' % mattermost_integration_token}


def get_random_channel_member(channel_id):
    url = "api/v4/users?in_channel=%s&page=0&per_page=200&sort=status" % channel_id
    req = requests.get("%s/%s" % (mattermost_base_url, url), headers = headers)
    #print req.text
    res = req.json()
    users = [
        user['id']
        for user in res
        if user['delete_at'] == 0
    ]

    return random.choice(users)


def get_username_by_id(user_id):
    url = "/api/v4/users/%s" % user_id
    req = requests.get("%s/%s" % (mattermost_base_url, url), headers = headers)
    res = req.json()
    username = res['username']
    return username


def get_random_number(one, two):
    if one > two:
	f = two
	t = one
    else:
        f = one
	t = two
    return random.randint(f, t)
