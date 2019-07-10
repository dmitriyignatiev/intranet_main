from app_main import db
from datetime import datetime

class Supplier(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    llc = db.Column (db.String (240))
    llc_name = db.Column (db.String (240))
    legal_add = db.Column(db.String(240))
    fact_address = db.Column(db.String(240))
    inn = db.Column(db.String(240))
    kpp = db.Column(db.String(240))
    ogrn = db.Column(db.String(240))
    bank = db.Column(db.String(240))
    bik = db.Column(db.String(240))
    rc = db.Column(db.String(240))
    kc = db.Column(db.String(240))
    driver_director = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey ('user.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    finance = db.Column(db.Integer, db.ForeignKey('finance.id'))
    pay = db.Column(db.Integer, db.ForeignKey('paid.id'))

class newSup(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (240))
    path = db.Column(db.String(1000))

class preFin(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    llc = db.Column (db.String (240))
    supplier = db.Column (db.String (240))
    req_id = db.Column(db.Integer, unique=True)
    date_request = db.Column(db.DateTime)
    complete = db.Column(db.Integer)
    




