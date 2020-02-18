import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://root:root@localhost:5883/rosexp?charset=utf8mb4'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('mail_username')
    MAIL_PASSWORD = os.environ.get('mail_password')
    MAIL_DEFAULT_SENDER = os.environ.get('mail_sender')
   
    UPLOADED_PATH = 'intranet_main\app_main\templates\agreements'
            
    DROPZONE_ALLOWED_FILE_CUSTOM = True
   
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image/*, .txt'
    DROPZONE_MAX_FILE_SIZE=3
    DROPZONE_MAX_FILES=30

    CELERY_BROKER_URL =  'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'



