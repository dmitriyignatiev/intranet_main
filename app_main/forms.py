from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app_main.models import User, Direction, Who_number, Customer, Truck, Quantity, Truck_opt, Ttn, Customer_base
from flask_login import current_user
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#####################
#функция выбора направления
def choice_direction():
    buyer = Direction.query
    return buyer

def choice_customer():
    customer = Customer.query.filter(Customer.user_id==current_user.id)
    return customer

def choice_truck():
    truck = Truck.query
    return truck

def quantity_per_month():
    quantity = Quantity.query
    return quantity

def choice_truck_type():
    truck_type = Truck_opt.query
    return truck_type





class NewRequestForm(FlaskForm):
    org = StringField('Откуда', validators=[DataRequired()])
    dest = StringField ('Куда', validators=[DataRequired ()])
    direction = QuerySelectField ('Направление перевозки', query_factory=choice_direction, get_label='name')
    customer = QuerySelectField ('Клиент', query_factory=choice_customer, get_label='name')

    cargo_type = SelectField ('Тип перевозки', choices=[
                                ('FTL', 'FTL'),
                                ('LTL', 'LTL')
                            ], validators=[DataRequired()])

    cargo_desciption = StringField('Характер груза', validators=[DataRequired()])
    cargo_value = StringField('Стоимость груза, в Рублях или в Евро. Только цифры')
    quantity = QuerySelectField('Количество перевозок в месяц по данному направлению', query_factory=quantity_per_month, get_label='quantity')

    type_of_loading = SelectField('Способ погрузки', choices=[
                                                    ('зад', 'зад'),
                                                    ('бок', 'бок'),
                                                    ('верх', 'верх'),
                                                    ('бок и зад', 'бок и зад'),
                                                    ('полная растентовка', 'полная растентовка')
                                                ], validators=[DataRequired()])
    type_of_truck = SelectField('Тип транспорта', choices=[
                                ('до 500 кг', 'до 500 кг'),
                                ('до 1,5тн', 'до 1,5тн'),
                                 ('до 2тн', 'до 2тн'),
                                  ('до 3тн', 'до 3тн'),
                                   ('до 5тн', 'до 5тн'),
                                ('до 10тн', 'до 10тн'),
                                ('до 20тн', 'до 20тн'),
                                ('21тн', '21тн'),
                                ('Негабарит', 'Негабарит'),
                            ], validators=[DataRequired()])

    weigth_cargo = IntegerField('Вес груза. Только цифры', validators=[DataRequired()])
    request_comments = TextAreaField ('Комментарии')

    pick_up_date = DateField('Дата загрузки', format = '%Y-%m-%d')

    request_status = SelectField('Статус запроса', choices=[
        ('ИНДИКАТИВ', 'ИНДИКАТИВ'),
        ('СРОЧНЫЙ ЗАПРОС', 'СРОЧНЫЙ ЗАПРОС'),
        ('ТЕНДЕР', 'ТЕНДЕР'),
        ('ЕДЕМ', 'ЕДЕМ'),
        ('СТАВКА_ОК', 'СТАВКА_ОК'),
        ('СТАВКА_ОК, ТС', 'СТАВКА_ОК, ТС')
         ],
                                 validators=[DataRequired()])


    dogovor_zayavka = BooleanField()
    submit = SubmitField('Отправить на расчет')

######################

class ConfirmRate(FlaskForm):
    cost = IntegerField('стоимость')
    truck_available = BooleanField()
    vat = BooleanField()
    no_vat = BooleanField()
    submit = SubmitField('Подтвердить стоимость')

class EditForm(FlaskForm):
    org = StringField ('Откуда', validators=[DataRequired ()])
    dest = StringField ('Куда', validators=[DataRequired ()])
    direction = QuerySelectField ('Направление перевозки', query_factory=choice_direction, get_label='name')
    customer = QuerySelectField ('Клиент', query_factory=choice_customer, get_label='name')

    cargo_type = SelectField ('Тип перевозки', choices=[
                                ('FTL', 'FTL'),
                                ('LTL', 'LTL')
                            ], validators=[DataRequired()])

    cargo_desciption = StringField ('Характер груза', validators=[DataRequired()])
    cargo_value = IntegerField ('Стоимость груза, в рублях')
    quantity = QuerySelectField ('Частота отправок в месяц', query_factory=quantity_per_month, get_label='quantity')

    type_of_loading = StringField ('Способ погрузки', validators=[DataRequired ()])
    type_of_truck = SelectField('Тип транспорта', choices=[
                                ('до 500 кг', 'до 500 кг'),
                                ('до 1,5тн', 'до 1,5тн'),
                                 ('до 2тн', 'до 2тн'),
                                  ('до 3тн', 'до 3тн'),
                                   ('до 5тн', 'до 5тн'),
                                ('до 10тн', 'до 10тн'),
                                ('до 20тн', 'до 20тн'),
                                ('21тн', '21тн'),
                                ('Негабарит', 'Негабарит'),
                            ], validators=[DataRequired()])

    weigth_cargo = IntegerField ('Вес груза', validators=[DataRequired()])
    request_comments = TextAreaField ('Комментарии')
    pick_up_date = DateField('Дата загрузки', format='%Y-%m-%d')

    request_status = SelectField('Статус запроса', choices=[
                                    ('ИНДИКАТИВ', 'ИНДИКАТИВ'),
                                    ('СРОЧНЫЙ ЗАПРОС', 'СРОЧНЫЙ ЗАПРОС'),
                                    ('ТЕНДЕР', 'ТЕНДЕР'),
                                    ('ЕДЕМ', 'ЕДЕМ'),
        ('СТАВКА_ОК', 'СТАВКА_ОК'),
        ('СТАВКА_ОК, ТС', 'СТАВКА_ОК, ТС')
                                                ],
                                    validators = [DataRequired()])

    submit = SubmitField ('Отправить на расчет')


#####################
#функция выборки всех юзеров (байеров)
def choice_buyer():
    buyer = User.query.filter(User.role=='buyer').filter(User.id != current_user.id)
    return buyer

class RedirectForm(FlaskForm):
    buyer = QuerySelectField('Кому перенаправить', query_factory=choice_buyer, get_label='name')
    submit = SubmitField('Отправить')
#######################

#функция выборки клиентов



#функция выборки запросов
# def choice_request():
#     from app_main import Request, current_user
#     return Request.query.filter(Request.id =!)

class Remove(FlaskForm):
    remove = IntegerField('delete request')
    submit = SubmitField('delete')

# форма договора-заявки
class Order_doc(FlaskForm):
    origin = StringField('откуда')
    submit = SubmitField('оформить')

#обратная связь
class FeedBack(FlaskForm):
    comments = TextAreaField('обратная связь')
    ask_buyer = BooleanField()
    ask_sale = BooleanField ()
    deadline = BooleanField()
    deadline_answer = DateField('Дата ответа', format='%Y-%m-%d')
    quest = BooleanField()
    noquest = BooleanField()
    submit = SubmitField('отправить')


#форма договора с клиентом
class Agreement_form(FlaskForm):
    date = StringField('дата договора')
    number = StringField('номер договора')
    customer_type = StringField('указать форму юр лица ООО/ЗАО/ПАО и т.д')
    customer_name = StringField("наименование клиента, пример: Супер Компания ")
    by_who = StringField('в лице кого?, в родительном падеже, пример: Генерального директора')
    name = StringField('ФИО подписанта')
    basis_on = StringField('на основании чего подписант действует (устава или доверенности)? пример:  доверенности №1 от 01.01.2018г., в родительном падеже')
    untill = StringField('дата, до которой действует договор')
    legal_add = StringField('юр адрес, пример: 445046, РФ, Самарская область, г. Тольятти ул. Коммунистическая 13-141')
    fact_add = StringField('фактический адрес: г. Тольятти,  Самарская область, ул. Маршала Жукова, д.27 оф. 202')
    inn = StringField('ИНН')
    kpp = StringField('КПП')
    ogrn = StringField('ОГРН')
    bank = StringField('Банк, пример: Филиал "НИЖЕГОРОДСКИЙ" АО "АЛЬФА-БАНК"')
    bic = StringField('БИК')
    kor_acc = StringField('Кор.счет')
    acc_number = StringField('Расчетный счет')
    submit = SubmitField('отправить')

#форма договора-заявки с поставщиком
class Agreement_zyavka_supplier(FlaskForm):
    from_ = StringField('Откуда')
    to = StringField('Куда')
    date_loading = StringField('Дата загрузки')
    time_loading = StringField('Время загрузки')
    shipper_name = StringField('Наименование отправителя')
    shipper_address = StringField('Адрес отправителя')
    shipper_phone = StringField('Телефон отправителя')
    date_unloading = StringField('Дата выгрузки')
    time_unloading = StringField('Время выгрузки')
    cnee_name = StringField('Наименование получателя')
    cnee_address = StringField('Адрес получателя')
    cnee_fio = StringField('ФИО получателя')
    cargo_description = StringField('Характер груза')
    number_request = StringField("Номер заказа, если неизвестно, ставим '-'")
    cargo_value = StringField('Стоимость груза в рублях')
    loading_type = StringField('Способ погрузки')
    unloading_type = StringField('Способ выгрузки')
    cargo_pallets = StringField(' Количество паллет или мест к загрузке')
    cargo_total_weight = StringField('Общий вес груза')
    cargo_m3 = StringField('Объем груза в м3')
    truck_description = StringField('Требования к авто')
    truck_type = StringField('Тип авто')
    special = StringField('Специальные требования, если есть')
    truck_cost = StringField('Стоимость перевозки в рублях с НДС')
    cost_payment_day = StringField('Срок оплаты в календарных днях')
    truck_model = StringField('Марка ТС ')
    driver_fio = StringField(' ФИО водителя')
    passort_seria_nomer = StringField('Паспортные данные: Серия, Номер')
    passport_vydan = StringField(' Кем и когда выдан')
    truck_plate = StringField('Номер авто')
    cargo_phone = StringField('Номер телефона водителя')
    driver_license = StringField('Номер водительского удостоверения')
    contact_name = StringField('ФИО логиста от РЭД')
    contact_phone = StringField('Контактный телефон логиста РЭД')
    cargo_name = StringField(' ФИО водителя')
    driver_phone = StringField('Сотовый водителя')
    llc = StringField('Форма юр лица перевоза, ИП/ООО')
    llc_name = StringField('Наименование юр лица')
    legal_add = StringField('Юр адрес перевоза')
    fact_address = StringField('Факт адрес перевоза')
    inn = StringField('ИНН перевоза')
    kpp = StringField('КПП перевоза')
    ogrn = StringField('ОГРН перевоза')
    bank = StringField('Банк Перевоза')
    bik = StringField('БИК перевоза')
    rc = StringField('Расчетный счет перевоза')
    kc = StringField( 'Кор/счет перевоза')
    driver_director = StringField('ФИО подписанта от перевоза')

    submit = SubmitField('Подтвердить')
#######

#форма выбора наш номер договора или клиента, реализовал по другому сценарию
def choice_number():
    who_number = Who_number.query
    return who_number

class Who(FlaskForm):
    who_number = QuerySelectField ('чей номер договора', query_factory=choice_number, get_label='name')
    submit = SubmitField('подтвердить выбор')

########

def choice_ttn():
    ttn = Ttn.query
    return ttn

def choice_base():
    base = Customer_base.query
    return base


class CustomerForm(FlaskForm):
    customer_character = SelectField('Экспедитор или Компания?', choices=[
        ('ЭКСЕПИТОР', 'ЭКСПЕДИТОР'),
        ('КОМПАНИЯ', 'КОМПАНИЯ')], validators=[DataRequired()])

    name = StringField('наименование клиента, пример:ООО Росэкспорт', validators=[DataRequired()])
    dm = StringField('ФИО Контактное лицо', validators=[DataRequired()])
    phone = StringField('контактный  телефон, пример: +78482555555', validators=[DataRequired()])
    email = StringField('электронная почта, пример: info@rosexport.su', validators=[DataRequired()])
    payment_day = IntegerField('Срок оплаты', validators=[DataRequired()])
    payment_terms = SelectField('Копия или Оригинал?', choices=[
        ('КОПИЯ', 'КОПИЯ'),
        ('ОРИГИНАЛ', 'ОРИГИНАЛ')
    ]

                                )
    customer_base = SelectField('Какая база клиентов используется?',  choices=[
        ('ОБЩАЯ', 'ОБЩАЯ'),
        ('КАЗАНЬ', 'КАЗАНЬ'),
        ('НИЖНИЙ НОВГОРОД', 'НИЖНИЙ НОВГОРОД'),
        ('МОСКВА', 'МОСКВА'),
        ('РЯЗАНЬ', 'РЯЗАНЬ'),
        ('ЧУВАШИЯ', 'ЧУВАШИЯ'),
        ('ВОРОНЕЖ', 'ВОРОНЕЖ')
    ], validators=[DataRequired()])




    submit = SubmitField('записать')
########


#####в процессе, еще не делал маршрут
class Customer_name(FlaskForm):
    name = StringField('ФИО')
    phone = StringField('контактный  телефон, пример: +78482555555')
    email = StringField ('электронная почта, пример: info@rosexport.su')


class StatusForm(FlaskForm):
    name = SelectField('Статус запроса', choices=[
                                    ('ИНДИКАТИВ', 'ИНДИКАТИВ'),
                                    ('СРОЧНЫЙ ЗАПРОС', 'СРОЧНЫЙ ЗАПРОС'),
                                    ('ТЕНДЕР', 'ТЕНДЕР'),
                                    ('ЕДЕМ', 'ЕДЕМ'),
                                    ('НЕАКТУАЛЬНО', 'НЕАКТУАЛЬНО'),
        ('СТАВКА_ОК', 'СТАВКА_ОК'),
        ('СТАВКА_ОК, ТС', 'СТАВКА_ОК, ТС'),
                                    ],
                                    validators = [DataRequired()])
    submit = SubmitField('записать')


#####Отчеты для менеджмента
class ManageForm_first(FlaskForm):
    date = DateField('Дата загрузки', format='%Y-%m-%d')
    submit = SubmitField('записать')

###форма для менеджмента
class DateForm(FlaskForm):
    date = DateField('Choose date', format='%Y-%m-%d')
    date_sec = DateField('Choose date #2', format='%Y-%m-%d')
    submit = SubmitField('confirm')

def choice_employee():
    employee=User.query
    return employee

class EmployeesForm(FlaskForm):
    choose_emloyee = QuerySelectField('выберите сотрудника', query_factory=choice_employee, get_label='name')
    fio = StringField()
    mobile = StringField()
    external = StringField()
    start_work = DateField('Дата начала работы', format='%Y-%m-%d')

    submit = SubmitField('confirm')

#выбор только для продавцов
def ChoiceCustomer():
    return Customer.query.filter(Customer.user_id==current_user.id)

class ch_customer(FlaskForm):
    cust = QuerySelectField('выбрать клиента', query_factory=ChoiceCustomer, get_label='name')
    submit = SubmitField('confirm')
############################

#выбор для всех
def ChoiceAllCustomer():
    return Customer.query

class ch_all_customer(FlaskForm):
    cust = QuerySelectField('выбрать клиента', query_factory=ChoiceAllCustomer, get_label='name')
    submit = SubmitField('confirm')

class formForBuyer(FlaskForm):
    question = BooleanField()
