import os
import datetime as DT

from record_to_slack import app, db, login_manager
from record_to_slack.models import User
from flask import render_template, request, redirect, url_for, session
from requests_oauthlib import OAuth2Session
from flask_login import login_required, current_user, login_user, logout_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()


def get_slack_auth(state=None, token=None, redirect_uri=None):
    if token:
        return OAuth2Session(os.getenv('SLACK_CLIENT_ID'), token=token)
    if state:
        return OAuth2Session(os.getenv('SLACK_CLIENT_ID'), state=state, redirect_uri=os.getenv('SLACK_REDIRECT_URI'))

    oauth = OAuth2Session(
        os.getenv('SLACK_CLIENT_ID'),
        redirect_uri=redirect_uri or os.getenv('SLACK_REDIRECT_URI')
    )
    return oauth


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('record'))
    return render_template('login.html', redirect_uri=os.getenv('SLACK_REDIRECT_URI'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/", methods=['GET'])
@login_required
def home():
    return redirect(url_for('record'))


@app.route("/record", methods=['GET'])
@login_required
def record():
    channels = get_slack_channels()
    return render_template('record.html', channels=channels)


def get_slack_channels():
    token = current_user.access_token
    oauth = get_slack_auth()
    url = 'https://slack.com/api/conversations.list'
    payload = {
        "token": token,
        "types": "public_channel,private_channel"
    }
    response = oauth.get(url, params=payload)
    return [{"name": channel["name"], "id": channel["id"]} for channel in response.json()["channels"]]


@app.route("/slack/login/redirect")
def oauth_login_redirect():
    if current_user is None and current_user.is_authenticated:
        return redirect(url_for('record'))
    else:
        code = request.args.get('code')
        oauth = get_slack_auth()
        token_response = oauth.fetch_token(
            'https://slack.com/api/oauth.access',
            code=code,
            client_secret=os.getenv('SLACK_CLIENT_SECRET')
        )
        user = User.query.filter_by(user_id=token_response['user_id']).first()
        if user is None:
            user = User(
                user_id=token_response['user_id'],
                team_id=token_response['team_id']
            )
        user.access_token = token_response['access_token']
        user._scopes = token_response['scope']
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('record'))


@app.route("/recording", methods=['POST'])
@login_required
def post_recording():
    url = 'https://slack.com/api/files.upload'
    payload = {
        "filename": "{}.{}".format(DT.datetime.now().strftime("%c"), 'mp3'),
        "channels": [request.form.get("channel")],
        "token": current_user.access_token,
    }

    oauth = get_slack_auth()
    oauth.post(
        url,
        params=payload,
        files={
            'file': request.files.get('recording')
        },
    )

    return "200 OK"
