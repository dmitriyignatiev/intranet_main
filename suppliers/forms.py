from flask_wtf import FlaskForm
from wtforms import StringField,TextField, \
    FloatField, FileField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
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
    # name = QuerySelectField('Поставщик', query_factory=choice_supp, get_label='llc_name')
    name = SelectField('Имя', coerce=str)
    inn = StringField('INN', validators=[DataRequired()])
    check_inn = SelectField('INN', coerce=str)
    tora_red = SelectField('ТОРА или РЭД', choices=[('Тора', 'Тора'), ('РЭД', 'РЭД'), ('Гунвор', 'Гунвор')], validators=[DataRequired()])
    date_order_C = DateField('Дата заявки с клиентом', validators=[DataRequired()], default=datetime.today())
    date_loading_plan = DateField('Дата загрузки', validators=[DataRequired()])
    date_unloading_plan = DateField('Дата планируемой выгрузки', validators=[DataRequired()])
    
    #от поставщика
    s_invoice_number=StringField('Номер счета подрядчика')
    #полный перечень счетов
    s_n_all_invoices = SelectField('Все счета', coerce=str)
    s_inv_date = DateField('ДАТА')
    s_inv_das_inv_date_to_pay = DateField('ДАТА')
    s_inv_amount = IntegerField('Сумма счета подрячика')
    s_inv_vat = SelectField('НДС', choices=[('НДС', 'НДС'), ('БЕЗ НДС', 'БЕЗ НДС'), ('НОЛЬ', 'НОЛЬ')])
    s_inv_currency = SelectField('Валюта', choices=[('RUR', 'RUR'), ('EUR', 'EUR'), ('USD', 'USD')])
    s_inv_pay_day = DateField('ДАТА')
    s_payment_summ = IntegerField('Сумма  оплаты')
    bank = SelectField('Банк', choices=[('Модуль', 'Модуль'), ('Точка', 'Точка'), ('Альфа', 'Альфа'), ('УБИР', 'УБРИР')]) 

    ##на клиента
    c_inv_number = TextField('Номер счета на клиента')
    c_invoice_date = DateField('ДАТА')
    c_inv_amount = IntegerField('Сумма счета на клиента с НДС')
    c_inv_currency = SelectField('Валюта', choices=[('RUR', 'RUR'), ('EUR', 'EUR'), ('USD', 'USD')])
    c_inv_amount = IntegerField('Сумма счета на клиента')
    c_inv_plan_pay = DateField('ДАТА')

   
    

    photo = FileField()
    status=SelectField('СТАТУС', choices=[
        ('ЗАПЛАНИРОВАН', 'ЗАПЛАНИРОВАН'),
        ('В ПУТИ', 'В ПУТИ'),
        ('ДОСТАВЛЕН', 'ДОСТАВЛЕН')], validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


#форма для поиска по ИНН
class formSupplierInn(FlaskForm):
     check_inn = SelectField('INN', coerce=str)
     submit = SubmitField('Подтвердить')

class formSupplierName(FlaskForm):
     name = SelectField('Имя', coerce=str)
     submit = SubmitField('Подтвердить Выбор')

class formSupplierInv(FlaskForm):
    supp_all_invoices = SelectField('Все счета', coerce=str)
    summ_pay = IntegerField('сумма платежа')
    transit = StringField('через кого платим')
    commision = SelectField('коммисия транзитера', choices=[
      (2, 2), (2.5, 2.5), (3.5, 3.5), (4, 4), (4.5, 4.5), (5, 5), (5.5, 5.5),(6, 6), (6.5, 6.5), (7, 7), (7.5, 7.5), (8, 8), (8.5, 8.5) 
      ], validators=[DataRequired()]
    )
    date_payment = DateField('Дата платежа')
    submit = SubmitField('Подтвердить Выбор')



   



class PochtaForm(FlaskForm):
    pass

from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadForm(FlaskForm):
    photo = FileField('Image', validators=[
        FileRequired(),
        
    ])
    submit = SubmitField('Submit')

class FormTransit(FlaskForm):
    innadd = StringField('ИНН')
    name_tr = SelectField('Имя', coerce=str)
    status_tr = SelectField('статус', choices=[('неуспешно', 'неуспешно'), ('успешно', 'успешно')])
    submit = SubmitField('Записать в базу')

