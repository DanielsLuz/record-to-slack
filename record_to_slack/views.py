import os
import datetime as DT

from record_to_slack import app, db, login_manager
from record_to_slack.models import User
from flask import render_template, request, redirect, url_for, session
from requests_oauthlib import OAuth2Session
from flask_login import login_required, current_user, login_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()

def get_slack_auth(state=None, token=None):
    if token:
        return OAuth2Session(os.getenv('SLACK_CLIENT_ID'), token=token)
    if state:
        return OAuth2Session(os.getenv('SLACK_CLIENT_ID'), state=state, redirect_uri=os.getenv('SLACK_REDIRECT_URI'))

    oauth = OAuth2Session(
        os.getenv('SLACK_CLIENT_ID'),
        redirect_uri=os.getenv('SLACK_REDIRECT_URI')
    )
    return oauth

@app.route("/")
@login_required
def home():
    if "files:write:user" in current_user._scopes:
        return redirect(url_for('record'))
    else:
        return render_template('home.html')

@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('record'))
    # slack = get_slack_auth()
    # auth_url, state = slack.authorization_url(Auth.AUTH_URI, access_type='offline')
    # session['oauth_state'] = state
    # return render_template('login.html', auth_url=auth_url)
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/slack/auth/redirect")
def oauth_redirect():
    if current_user is None and current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        code = request.args.get('code')
        oauth = get_slack_auth()
        token_response = oauth.fetch_token(
            'https://slack.com/api/oauth.access',
            code=code,
            client_secret=os.getenv('SLACK_CLIENT_SECRET')
        )
        user = User.query.filter_by(user_id=token_response['user']['id']).first()
        if user is None:
            user = User(
                token_response['team']['id'],
                token_response['user']['id'],
            )
        user.access_token = token_response['access_token']
        user._scopes = token_response['scope']
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('home'))

@app.route("/record", methods=['GET'])
@login_required
def record():
    return render_template('record.html')

@app.route("/recording", methods=['POST'])
@login_required
def post_recording():
    payload = {
        "filename": "{}.{}".format(DT.datetime.now().strftime("%c"), 'mp3'),
        "channels": ["#general"],
        "token": current_user.access_token
    }

    oauth = get_slack_auth()
    r = oauth.post(
        'https://slack.com/api/files.upload',
        params=payload,
        files= {
            'file' : request.files.get('recording')
        },
    )
    return "200 OK"
