from flask_wtf import FlaskForm
from wtforms import StringField,TextField, FormField, TextAreaField, \
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




class OrderForm_a(FlaskForm):

    customer_name = SelectField('Имя клиента', coerce=str)
    supplier_name = SelectField('Имя поставщика', coerce=str)
    date_order = DateField('Дата_заявки')
    
    o_from = TextField('Город')
    date_loading = DateField('Дата погрузки')
    time_loading = TextField('Время погрузки')
    address_loading = TextAreaField('Адрес загрузки')
    shipper_name = TextAreaField('Наименование отправителя')
    contacts_loading = TextAreaField('Контакт на загрузке')
    
    
    
    o_to  = TextField('Город')
    address_unloading = TextAreaField('Адрес загрузки')
    cnee_name = TextAreaField('Наименование получателя')
    contacts_unloading = TextAreaField('Контакт на выгрузке')
    date_unloading = DateField('Дата выгрузки')
    time_unloading = TextField('Время выгрузки')

    #все о грузе                    
    cargo_description = TextAreaField('Характер груза')
    quantity_pallets = TextField('Количество мест')
    weigth = TextField('Вес')
    type_loading = TextField('Тип погрузки')
    type_unloading = TextField('Тип выгрузки')
    cargo_cost = TextField('Стоимость груза')
    volume = TextField('Кубатура')
    cargo_comments = TextAreaField('Комментарии')
    
    

    #Авто
    model = TextField('Марка авто')
    auto_number = TextField('Номер авто')
    driver_name = TextField('ФИО водителя')
    driver_phone = TextField('Телефон водителя')
    passport = TextField('Данные паспорта')
    driver_license = TextField('Водительское уд')
    type_truck = TextField('ТИП полуприцепа')

    #данные подрядчика
    who_supplier = TextField('наименование')
    supp_legal_address = TextField('юр адрес')
    supp_fact_address = TextField('факт адрес')
    supp_accout = TextField('р/с')
    supp_bank_kc = TextField('к/с')
    supp_bank = TextField('Банк')
    supp_bank_bik = TextField('БИК')
    supp_inn = TextField('ИНН')
    supp_kpp = TextField('КПП')
    supp_sign_fio = TextField('Расшифровка подписи')

    #данные клиента
    who_customer = TextField('наименование')
    cust_legal_address = TextField('юр адрес')
    cust_fact_address = TextField('факт адрес')
    cust_accout = TextField('р/с')
    cust_bank_kc = TextField('к/с')
    cust_bank = TextField('Банк')
    cust_bik_bank = TextField('БИК')
    cust_inn = TextField('ИНН')
    cust_kpp = TextField('КПП')
    cust_sign_fio = TextField('Расшифровка подписи')


    

    #стоимость и срок оплаты c перевозом
    cost = TextField('Стоимость перевозки ')
    org_scan = TextAreaField('Условия оплаты')
    date_payment = TextAreaField('Срок оплаты')

    #стоимость и срок оплаты с клиентом
    cost_c = TextField('Стоимость перевозки ')
    org_scan_с = TextAreaField('Условия оплаты')
    date_payment_с = TextAreaField('Срок оплаты')
    


    submit = SubmitField('записать')


    


