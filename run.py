from flask import Flask
from flask import request
from flask import send_from_directory
import sys
import requests
import json
import os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
                               
reload(sys)
sys.setdefaultencoding('utf-8')                              

@app.route('/')
def nothing():
    return '''
    <html>
      <head>
        <title>Slack Chats</title>
      </head>
      <body>
      Please provide a valid oAuth token from <a target='_blank' href=https://api.slack.com/docs/oauth-test-tokens>https://api.slack.com/docs/oauth-test-tokens</a> as an argument
      in the URL path http://localhost:5000/token_here
      </body>
    </html>
    '''

@app.route('/<token>')
def gettoken(token):
    # https://api.slack.com/docs/oauth-test-tokens

    params = {'token': token}

    # build name dict
    userlist = requests.get("https://slack.com/api/users.list", params=params)
    names = dict((x['id'], x['profile'].get("real_name")) for x in json.loads(userlist.text)['members'])

    # get list of private ims
    r = requests.get("https://slack.com/api/im.list", params=params)

    # cross reference channel with user names
    json_obj_history = json.loads(r.text)

    body = '''
    <html>
      <head>
        <title>Slack Chats</title>
      </head>
      <body>
      <table><tr><td>User</td></tr>
    '''

    for message in json_obj_history['ims']:
        if (names.get(message.get("user")) != ""):
            body = body + "<tr><td><a href='delhist?token="+token+'&id='+message.get("id")+"'>Delete entries from chat with "+names.get(message.get("user"))+"</td></tr>"

    return body + '''</table>
      </body>
    </html>
    '''


@app.route('/delhist/')
def delhist():

    token = request.args.get('token')
    channel = request.args.get('id')

    params = {'token': token, 'channel': channel}

    userlist = requests.get("https://slack.com/api/users.list", params=params)
    names = dict((x['id'], x['profile'].get("real_name")) for x in json.loads(userlist.text)['members'])

    tracking_latest = 0.0
    latest = 0.0

    # delete messages
    while True:

        r = requests.get("https://slack.com/api/im.history", params=params)

        json_obj = json.loads(r.text)

        if (not json_obj.get("ok")):
            print json_obj.get("error")
            sys.exit(1)

        for message in json_obj['messages']:
            if latest > message.get("ts") or latest == 0.0:
                latest = message.get("ts")

            print message.get("ts")
            print names.get(message.get("user"),"UNKOWN")
            print message.get('text')
            print ""

        if tracking_latest == latest:
            break;

        tracking_latest = latest

        params = {'token': token, 'channel': channel, 'latest': latest, 'inclusive': '1'}

        # delete message
        for message in json_obj['messages']:
            paramsdeletemsg = {'token': token, 'channel': channel, 'ts': message.get("ts")}
            requests.get("https://slack.com/api/chat.delete", params=paramsdeletemsg)

    paramsdel = {'token': token, 'channel': channel}

    # delete files
    while True:

        r = requests.get("https://slack.com/api/files.list", params=paramsdel)

        json_obj = json.loads(r.text)

        if len(json_obj['files']) == 0:
            break

        # delete file
        for file in json_obj['files']:
            print "deleting the file", file.get("name"), file.get("id")
            paramsdelfile = {'token': token, 'file': file["id"]}
            requests.get("https://slack.com/api/files.delete", params=paramsdelfile)

        break

    return "<html><head><title>Slack Chats</title></head><body>deleted all text and files for this chat</body></html>"


if __name__ == '__main__':
    app.run(host='0.0.0.0')

