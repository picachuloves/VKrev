from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dash import Dash
from app.dashapp.callbacks import register_callbacks
import dash_bootstrap_components as dbc
from flask_login import current_user
from app.dashapp import static_callbacks

server = Flask(__name__)
server.config.from_object(Config)
db = SQLAlchemy(server)
migrate = Migrate(server, db)
login = LoginManager(server)
login.init_app(server)
from app import routes, models
icons = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css"
bs = "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"

dash_app1 = Dash(__name__, server=server, url_base_pathname='/dashboard/',
                 external_stylesheets=[dbc.themes.BOOTSTRAP, icons, bs])
dash_app1.title = 'Анализ отзывов'
from app.dashapp.layout import layout
dash_app1.layout = layout
register_callbacks(dash_app1)


