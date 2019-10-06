from app_main.models import *

class Agreements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Text)
    path = db.Column(db.Text)
    shipper_name = db.Column(db.Text)
    shipper_address = db.Column(db.Text)
    shipper_phone = db.Column(db.Text)
    cnee_name = db.Column(db.Text)
    cnee_address = db.Column(db.Text)
    cnee_phone = db.Column(db.Text)
    cargo = db.Column(db.Text)
    date_loading = db.Column(db.DateTime)
    date_unloading = db.Column(db.DateTime)
    driver = db.Column(db.Text)
    date_order = db.Column(db.DateTime)
    