from flask_wtf import FlaskForm
from wtforms import StringField,TextField, FormField, \
    FloatField, FileField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app_main.models import User, Direction, Who_number, Customer, Truck, Quantity, Truck_opt, Ttn, Customer_base
from flask_login import current_user
from wtforms.fields.html5 import DateField
from suppliers.models import *
from flask import session,g
from app_main.models import *
from .models import *




class OrderForm(FlaskForm):
    customer_name = SelectField('Имя клиента', coerce=str)
    date_order = DateField('Дата_заявки', )
    date_loading = DateField('Дата погрузки')
    time_loading = TextField('Время погрузки')
    o_from = TextField('Откуда')
    o_to  = TextField('Куда')
    address_loading = TextField('Адрес загрузки')
    contacts_loading = TextField('Контакт на загрузке')                   
    cargo_description = TextField('Характер груза')
    quantity_pallets = TextField('Количество мест')
    weigth = TextField('Вес')
    shipper_name = TextField('Наименование отправителя')
    cnee_name = TextField('Наименование получателя')
    cnee_contact = TextField('Контакты на выгрузке')
    cost = TextField('Стоимость перевозки ')
    submit = SubmitField('записать')

