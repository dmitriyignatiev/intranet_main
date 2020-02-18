from celery import Celery
import os
from app_main import app, mail, db
from app_main.models import Request
from flask_mail import Mail, Message
from flask import Flask
from flask_login import current_user

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])


#проверяем работоспособность Celery
@celery.task(name='celery_task.reverse')
def reverse(string):
    return string[::-1]

@celery.task(name='celery_task.sendmail')
def sendmail(id, email, comment):
    msg = Message("New comment in request {}".format(id),
                    sender= 'dmitriy.ignatiev83@gmail.com',
                    recipients=[email])
    msg.body="{}, \n \n http://192.168.1.117:5000/feedback/{}".format(comment, id)
    with app.app_context():
        mail.send(msg)
    return 'mail in discuss was sent'


@celery.task(name='celery_task.confirm_rate')
def confirm_rate(id, truck_option, cost, sale_email):
    
    update_request = Request.query.get(id)
    # sale_email=update_request.user.email or update_request.user.user_email 
    if truck_option==True:
        update_request.truck_option=1
        msg = Message ('ЕСТЬ АВТО!!!!Получена ставка по запросу {}'.format(str(update_request.id)), sender='dmitriy.ignatiev83@gmail.com',
                               recipients=[sale_email])
        msg.body = "{}, \n \n http://192.168.1.117:5000/feedback/{}".format(cost, str(update_request.id))
    else:
        update_request.truck_available_opt=0
        msg = Message('АВТО НЕТ!!!!Получена ставка по запросу {}'.format(str(update_request.id)),
                          sender='dmitriy.ignatiev83@gmail.com',
                          recipients=[sale_email])
        msg.body = "{}, \n \n http://192.168.1.117:5000/feedback/{}".format(cost, str(update_request.id))
    update_request.cost=cost
    db.session.commit()
    with app.app_context():
        mail.send(msg)
    return('cost confirmed!!!')


