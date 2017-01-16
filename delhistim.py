#!/usr/bin/python

import sys
import requests
import json

# https://api.slack.com/docs/oauth-test-tokens

if (len(sys.argv) < 3):
	print "Please provide a valid oAuth token from https://api.slack.com/docs/oauth-test-tokens as an argument"
	print "and the ID of the chat that should be deleted"
	sys.exit(1)

params = {'token': sys.argv[1], 'channel': sys.argv[2]}

r = requests.get("https://slack.com/api/users.list", params=params)

names = dict((x['id'], x['profile'].get("real_name")) for x in json.loads(r.text)['members'])

tracking_latest = 0.0
latest = 0.0
# delete messages
while False :

	r = requests.get("https://slack.com/api/im.history", params=params)

	json_obj = json.loads(r.text)

	if (not json_obj.get("ok")):
		print json_obj.get("error")
		sys.exit(1)

	for message in json_obj['messages']:
		if latest > message.get("ts") or latest == 0.0:
			latest = message.get("ts")

		print message.get("ts"), message.get("text")

	if tracking_latest == latest:
		break;

	tracking_latest = latest

	params = {'token': sys.argv[1], 'channel': sys.argv[2], 'latest': latest, 'inclusive': '1'}

	# delete message
	for message in json_obj['messages']:
		paramsdeletemsg = {'token': sys.argv[1], 'channel': sys.argv[2], 'ts': message.get("ts")}
		requests.get("https://slack.com/api/chat.delete", params=paramsdeletemsg)




paramsdel = {'token': sys.argv[1], 'channel': sys.argv[2]}

# delete files
while True :

	r = requests.get("https://slack.com/api/files.list", params=paramsdel)

	json_obj = json.loads(r.text)

	if len(json_obj['files']) == 0:
		break

	# delete file
	for message in json_obj['files']:
		paramsdelfile = {'token': sys.argv[1], 'file': message["id"]}
		r = requests.get("https://slack.com/api/files.delete", params=paramsdelfile)
		print "deleting the file", message.get("name"), message.get("id")

	break
