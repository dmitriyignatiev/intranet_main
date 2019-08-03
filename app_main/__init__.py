from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# from mailmerge import MailMerge

from flask_bootstrap import WebCDN
from flask_dropzone import Dropzone
from flask_mail import Mail




app = Flask(__name__)
app.config.from_object(Config)

import os

from flask import Flask, render_template, request
from flask_dropzone import Dropzone

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app.config.update(
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
   
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image/*, .txt',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
    
    
)




db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

bootstrap = Bootstrap(app)
dropzone = Dropzone(app)
app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
    '//cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/'
)



moment = Moment(app)

from app_main import routes, models

from suppliers.routes import supp
app.register_blueprint(supp, url_prefix='/suppliers')

