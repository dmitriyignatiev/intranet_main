from app_main.models import *

class Agreements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Text)
    