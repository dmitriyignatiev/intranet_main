import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:Pangolin2208@localhost:8541/flask_home'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'redmessageinfo@gmail.com'
    MAIL_PASSWORD = '******'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOADER_FOLDER = 'intranet_main\app_main\templates\agreements'
    



