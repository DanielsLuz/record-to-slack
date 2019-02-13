from record_to_slack import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String)
    user_id = db.Column(db.String)
    access_token = db.Column(db.String)
    _scopes = db.Column(db.Text)

    def __init__(self, team_id, user_id, access_token=None, _scopes=None):
        self.team_id = team_id
        self.user_id = user_id
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
