import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db?check_same_thread=False')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_CREDENTIALS = {
        'vk': {
            'id': '',
            'secret': '',
            'redirect_uri': 'http://localhost:5000/get_access'
        }
    }

