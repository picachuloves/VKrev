from app import server
from requests import PreparedRequest
import requests
from app.models import User
from app import db
from flask_login import login_user, logout_user


class VkAuth:
    url_auth = 'https://oauth.vk.com/authorize'
    url_token = 'https://oauth.vk.com/access_token'

    def __init__(self):
        credentials = server.config['OAUTH_CREDENTIALS']['vk']
        self.id = credentials['id']
        self.secret = credentials['secret']
        self.redirect_uri = credentials['redirect_uri']

    def authorize(self):
        params = {'client_id': self.id,
                   'redirect_uri': self.redirect_uri,
                   'display': 'page',
                   'scope': 'stats, offline',
                   'response_type': 'code'
                   }
        req = PreparedRequest()
        req.prepare_url(self.url_auth, params)
        return req.url

    def get_session(self, client_code):
        params = {'client_id': self.id,
                  'client_secret': self.secret,
                  'redirect_uri': self.redirect_uri,
                  'code': client_code}
        answer = requests.get(self.url_token, params=params)
        token = answer.json()['access_token']
        id = answer.json()['user_id']

        user = User.query.filter_by(id=id).first()
        if not user:
            user = User(id=id, token=token)
            db.session.add(user)
            db.session.commit()
        login_user(user, remember=True)
        return token

    def logout(self):
        logout_user()
