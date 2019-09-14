from flask_wtf import FlaskForm
from wtforms import StringField,TextField, \
    FloatField, FileField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app_main.models import User, Direction, Who_number, Customer, Truck, Quantity, Truck_opt, Ttn, Customer_base
from flask_login import current_user
from wtforms.fields.html5 import DateField
from suppliers.models import *
from flask import session,g
from app_main.models import *


class CustomerForm(FlaskForm):
    name = SelectField('Имя', coerce=str)
    submit_name = SubmitField(label='выбрать')

class InvoiceForm(FlaskForm):
    number = SelectField('номер', coerce=str)
    submit_invoice = SubmitField(label='выбрать')