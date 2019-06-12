from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app_main.models import User, Direction, Who_number, Customer, Truck, Quantity, Truck_opt, Ttn, Customer_base
from flask_login import current_user
from wtforms.fields.html5 import DateField
from .models import *

def choice_supp():
    return Supplier.query

class formSupplier(FlaskForm):
    name = QuerySelectField('Поставщик', query_factory=choice_supp, get_label='llc_name')
    tora_red = SelectField('ТОРА или РЭД', choices=[('Тора', 'Тора'), ('РЭД', 'РЭД')], validators=[DataRequired()])
    date_order_C = DateField('Дата заявки с клиентом', validators=[DataRequired()])
    date_loading_plan = DateField('Дата заявки с клиентом', validators=[DataRequired()])
    date_unloading_plan = DateField('Дата планируемой выгрузки', validators=[DataRequired()])
    inv_n_S=StringField('Номер счета подрядчика')
    photo = FileField()
    submit = SubmitField('Подтвердить')
