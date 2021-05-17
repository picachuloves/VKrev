from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    token = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    # expires_in = db.Column(db.Integer, unique=True)
    # created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id, token):
        self.id = id
        self.token = token
    
    def __repr__(self):
        return f'<User {self.id}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# class Last(db.Model):
#     id = db.Column(db.Integer, index=True, primary_key=True)
#
#     def __init__(self, id):
#         self.id = id
#
# class Session(db.Model):
#     id = db.Column(db.Integer, index=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     session_name = db.Column(db.String(64), default=datetime.utcnow)
#     group_id = db.Column(db.Integer, index=True)
#     board_id = db.Column(db.Integer, index=True)
#
#     def __init__(self, user_id, group_id, board_id, session_name = ''):
#         self.user_id = user_id
#         self.group_id = group_id
#         self.board_id = board_id
#         if session_name:
#             self.session_name = session_name
#
#     def __repr__(self):
#         return f'Session {self.session_name}'
#
#
# class Comment(db.Model):
#     id = db.Column(db.Integer, index=True, primary_key=True)
#     session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
#     author_id = db.Column(db.Integer, index=True)
#     likes = db.Column(db.Integer)
#     text = db.Column(db.String(500))
#
#     def __init__(self, session_id, author_id, likes):
#         self.session_id = session_id
#         self.author_id = author_id
#         self.likes = likes
#
#     def __repr__(self):
#         return f'Comment {self.id}'
