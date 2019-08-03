import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:root@localhost:3306/rosexp_final'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'redmessageinfo@gmail.com'
    MAIL_PASSWORD = '******'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOADED_PATH = 'intranet_main\app_main\templates\agreements'
    
    



