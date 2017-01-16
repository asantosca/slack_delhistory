#!/usr/bin/python

import sys
import requests
import json

# https://api.slack.com/docs/oauth-test-tokens



if (len(sys.argv) < 2):
	print "Please provide a valid oAuth token from https://api.slack.com/docs/oauth-test-tokens as an argument"
	sys.exit(1)

params = {'token': sys.argv[1]}

# build name dict
r = requests.get("https://slack.com/api/users.list", params=params)
names = dict((x['id'], x['profile'].get("real_name")) for x in json.loads(r.text)['members'])

# get list of private ims
r = requests.get("https://slack.com/api/im.list", params=params)

# cross reference channel with user names
json_obj_history = json.loads(r.text)
print "Channel   User"
print "========= =============="
for message in json_obj_history['ims']:
	if (names.get(message.get("user")) != ""):
		print message.get("id"), names.get(message.get("user"))
