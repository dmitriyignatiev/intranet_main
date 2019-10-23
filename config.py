import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:*******@localhost:8889/v33'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'Dmitriy.******@gmail.com'
    MAIL_PASSWORD = '********'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOADED_PATH = 'intranet_main\app_main\templates\agreements'
    
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://locallhost:9200'
    
    DROPZONE_ALLOWED_FILE_CUSTOM = True
   
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image/*, .txt'
    DROPZONE_MAX_FILE_SIZE=3
    DROPZONE_MAX_FILES=30



