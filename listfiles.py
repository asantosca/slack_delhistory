#!/usr/bin/python

import sys
import requests
import json

# https://api.slack.com/docs/oauth-test-tokens



if (len(sys.argv) == 1):
	print "Please provide a valid oAuth token from https://api.slack.com/docs/oauth-test-tokens as an argument"
	sys.exit(1)

params = {'token': sys.argv[1]}

r = requests.get("https://slack.com/api/files.list", params=params)

json_obj_history = json.loads(r.text)

for message in json_obj_history['files']:
	print message
