from record_to_slack import db
from sqlalchemy.dialects.postgresql import JSON

class SlackBot(db.Model):
    __tablename__ = 'slack_bots'

    id = db.Column(db.Integer, primary_key=True)
    bot_user_id = db.Column(db.String)
    bot_access_token = db.Column(db.String)
    team_name = db.Column(db.String)
    team_id = db.Column(db.String)
    _scopes = db.Column(db.Text)

    def __init__(self, bot_user_id, bot_access_token, team_name, team_id, _scopes):
        self.bot_user_id = bot_user_id
        self.bot_access_token = bot_access_token
        self.team_name = team_name
        self.team_id = team_id
        self._scopes = _scopes

    def __repr__(self):
        return '<id {}>'.format(self.id)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String)
    user_id = db.Column(db.String)
    user_name = db.Column(db.String)
    access_token = db.Column(db.String)
    _scopes = db.Column(db.Text)

    def __init__(self, team_id, user_id, user_name, access_token=None, _scopes=None):
        self.team_id = team_id
        self.user_id = user_id
        self.user_name = user_name
        self.access_token = access_token
        self._scopes = _scopes

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def get_access_token(user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return user.access_token

    def get_id(self):
        return self.user_id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True
