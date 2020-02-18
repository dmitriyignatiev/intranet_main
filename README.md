Intranet for small logistics company in order to make clear cooperation between sales and operation departments within one company. Control, follow up and maintain all the requests sales dept.

To install makes the following (for windows users):

clone or download https://github.com/dmitriyignatiev/intranet_main.git

create virtual env: python3 -m venv venv

activate env: venv/Scripts/activate

install celery: pip install celery

create db on you machine after makes all migrations: flask db init flask db migrate flask db upgrade

open config.py and change to your credentials following options SQLALCHEMY_DATABASE_URI MAIL_USERNAME MAIL_PASSWORD MAIL_DEFAULT_SENDER = os.environ.get('mail_sender')

set FLASK_APP=intranet.py

open celery_task.py file and change sender mail in sendmail and confirm_rate functions to your default email

open new terminal window, activate venv then do docker-compose up (to set up MYSQL, Celery, Redis services)

open a new terminal, activate vevn then do "celery -A app_main.celery_task.celery worker --loglevel=info --pool=solo"

In new terminal do flask run

Enjoy
