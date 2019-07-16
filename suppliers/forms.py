from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app_main.models import User, Direction, Who_number, Customer, Truck, Quantity, Truck_opt, Ttn, Customer_base
from flask_login import current_user
from wtforms.fields.html5 import DateField
from .models import *
from flask import session,g
from app_main.models import Request





def choice_supp():
    return Supplier.query

class formSupplier(FlaskForm):
    name = QuerySelectField('Поставщик', query_factory=choice_supp, get_label='llc_name')
    tora_red = SelectField('ТОРА или РЭД', choices=[('Тора', 'Тора'), ('РЭД', 'РЭД')], validators=[DataRequired()])
    date_order_C = DateField('Дата заявки с клиентом', validators=[DataRequired()], default=datetime.today())
    date_loading_plan = DateField('Дата загрузки', validators=[DataRequired()])
    date_unloading_plan = DateField('Дата планируемой выгрузки', validators=[DataRequired()])
    s_invoice_number=StringField('Номер счета подрядчика')
    s_inv_date = DateField('ДАТА')
    s_inv_amount = IntegerField('Сумма счета подрячика')
    s_inv_vat = SelectField('НДС', choices=[(20, 20), (0, 0), (1, 1)])
    c_inv_amount = IntegerField('Сумма счета на клиента')
    c_inv_currency = SelectField('Валюта', choices=[('RUR', 'RUR'), ('EUR', 'EUR'), ('USD', 'USD')])


    photo = FileField()
    status=SelectField('СТАТУС', choices=[
        ('ЗАПЛАНИРОВАН', 'ЗАПЛАНИРОВАН'),
        ('В ПУТИ', 'В ПУТИ'),
        ('ДОСТАВЛЕН', 'ДОСТАВЛЕН')], validators=[DataRequired()])
    submit = SubmitField('Подтвердить')

