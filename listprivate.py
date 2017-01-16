#!/usr/bin/python

import sys
import requests
import json

# https://api.slack.com/docs/oauth-test-tokens



if (len(sys.argv) == 1):
	print "Please provide a valid oAuth token from https://api.slack.com/docs/oauth-test-tokens as an argument"
	sys.exit(1)

params = {'token': sys.argv[1]}

r = requests.get("https://slack.com/api/groups.list", params=params)

for x in json.loads(r.text)['groups']:
	print x['id'], x['name']
