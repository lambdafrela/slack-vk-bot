from flask import Flask, abort, request, render_template

from config import PATH, auth_slack
from auth import auth_slack
from message import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route(PATH, methods=['GET', 'POST'])
def callback():
    if not request.json or 'type' not in request.json:
        abort(400)

    if request.json['type'] == 'confirmation':
        return confirmation_token_

    if request.json['type'] == 'wall_post_new':
        post = request.json['object']

        attachments = Slack(post=post).create_attachments()
        Slack.send_message(auth=slack, channel=channel_, text=text_,
                           attachments=attachments)

        return 'ok', 200


slack = auth_slack()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
