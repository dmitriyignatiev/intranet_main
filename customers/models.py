from app_main import db, login

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime


#Для подгрузки счета на клиента + информация по счетам
class Invoicecust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fin_id = db.Column(db.Integer)
    path = db.Column(db.Text)
    prefin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))
    req_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    invoice_number = db.Column(db.Text)
    invoice_amount = db.Column(db.Float)
    invoice_date = db.Column(db.DateTime)
    invoice_deadline_payment = db.Column(db.DateTime)
    invoice_tracking_number = db.Column(db.Text)
    invoice_tracking_company = db.Column(db.Text)
    invoice_tracking_day = db.Column(db.DateTime)
    invoice_actual_payment = db.relationship('Invoice_payment_c', backref='inv_c', lazy='dynamic')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    

#детализация по счету
class Invoice_payment_c(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summ = db.Column(db.Float)
    date = db.Column(db.DateTime)
    invoice_number = db.Column(db.Text)
    invoicecust_id = db.Column(db.Integer, db.ForeignKey('invoicecust.id') )
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))