from app_main import db, login

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime

subs = db.Table('subs',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('request_id', db.Integer, db.ForeignKey('request.id'))
                )

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    role = db.Column(db.String(120))
    password_hash = db.Column(db.String(120))
    requests = db.relationship('Request', secondary=subs,
                               backref=db.backref('users', lazy='dynamic'))
    post = db.relationship('Posts', backref = 'user', lazy = 'dynamic')
    request = db.relationship('Request', backref='user', lazy = 'dynamic')
    request_count = db.Column(db.Integer)

    agreement = db.relationship ('Agreement', backref='user', lazy='dynamic')

    user_email = db.Column(db.String(240))

    #adding for test еще не доделано!!!!
    messages_sent = db.relationship ('Message',
                                     foreign_keys='Message.sender_id',
                                     backref='author', lazy='dynamic')
    messages_received = db.relationship ('Message',
                                         foreign_keys='Message.recipient_id',
                                         backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column (db.DateTime)

    # ...

    email = db.Column(db.String(240))


    customer = db.relationship('Customer', backref='user', lazy='dynamic')

    competention = db.Column(db.String(240))
    active = db.Column(db.Integer)

    fio = db.Column(db.String(240))
    mobile = db.Column(db.String(120))
    external = db.Column(db.String(120))
    start_work = db.Column(db.DateTime)





    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime (1900, 1, 1)
        return Message.query.filter_by (recipient=self).filter (
            Message.timestamp > last_read_time).count ()
    ######



    def __repr__(self):
        return '<User> {}'.format (self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash (password)

    def check_password(self, password):
        return check_password_hash (self.password_hash, password)


class Incoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Request (db.Model):

    id = db.Column (db.Integer, primary_key=True)
    org = db.Column (db.String (120))
    user_id = db.Column (db.Integer, db.ForeignKey('user.id'))
    cost = db.Column (db.Integer)
    created = db.Column (db.DateTime, default=datetime.utcnow)
    cost_time = db.Column (db.Integer)
    update_time = db.Column (db.DateTime, default=datetime.utcnow())
    diff_time = db.Column (db.DateTime)
    feedback = db.Column (db.Text, default=update_time)
    comment = db.relationship('Posts', backref='request', lazy='dynamic')
    rate_idea = db.Column(db.Integer)
    cost_buyer = db.relationship('Costs', backref='request', lazy='dynamic')
    status = db.relationship('Status', backref='status', lazy='dynamic')
    redirect_comment = db.Column(db.String(120))
    direction = db.Column (db.String(120))
    cost_created = db.Column(db.DateTime, default=None)

    dest = db.Column (db.String (120))
    customer = db.relationship ('Customer', backref='request')
    customer_id = db.Column (db.Integer, db.ForeignKey ('customer.id'))

    customer_name = db.Column(db.String(120))
    payment_day = db.Column (db.Integer)

    cargo_type = db.Column(db.String(120))
    cargo_desciption = db.Column(db.String(120))
    cargo_value = db.Column(db.String(120))
    quantity = db.Column(db.Integer)

    Truck_type = db.Column(db.String(120))
    ttn = db.Column (db.String (140))

    type_of_loading = db.Column(db.String(120))
    type_of_truck = db.Column(db.String(120))
    weigth_cargo = db.Column(db.Integer)
    request_comments = db.Column(db.Text)

    pick_up_date = db.Column(db.DateTime)
    request_status = db.Column(db.String(120))
    request_order = db.Column(db.String(120))
    truck_available_opt = db.Column(db.Integer)
    dogovor_zayavka = db.Column(db.Integer)

    deadline_buyer = db.Column(db.DateTime)
    deadline_sale = db.Column(db.DateTime)
    questions = db.Column(db.String(800))

    actual = db.Column(db.String(120))

    min_sale = db.Column(db.Integer)

    #вопросы по запросом
    quest = db.Column(db.String(120))

    #0 не актуально, 1 - актуально
    nonactf_buyer = db.Column(db.Integer)




    def diff_time(self):
        delta = self.created - self.cost_created
        return str(delta)


    def test(self):
        return "{}".format(self.name)

    def append_to(self, user):
        self.users.append(user)

    def remove_from(self, user):
        self.users.remove(user)

    def is_in(self, user):
        pass

    def time(self):
        self.diff_time = self.created - self.update_time

    def __repr__(self):
        return "<Request> {}".format(self.org)


class Direction(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (120))
    request_id = db.Column(db.Integer, db.ForeignKey ('request.id'))

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    date = db.Column(db.DateTime, default = datetime.utcnow)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))


class Costs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer)
    request_id = db.Column(db.ForeignKey('request.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow())


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post = db.Column(db.Text)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_date = db.Column(db.DateTime, index=True, default = datetime.utcnow)
    # adding notification



    def __repr__(self):
        return "<Post> {} for  <Request> {} by <User> {}".format(self.post, self.request_id, self.user_id)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)



# база данных клиентов
class Customer(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (240), unique=True)
    phone = db.Column (db.String (240))
    email = db.Column (db.String (240))
    payment_day = db.Column (db.Integer)
    dm = db.Column(db.String(240))
    payment_terms = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_creation = db.Column(db.DateTime, default= datetime.utcnow)
    customer_base = db.Column(db.String(240))
    customer_character = db.Column(db.String(120))
    customer_inn = db.Column(db.Integer)



    def __repr__(self):
        return "Customer <{}>".format(self.name, self.user.name)

#база контакный лиц

#база данных поставщиков, полностью дублирует заявку
# class Supplier(db.Model):
#     id = db.Column (db.Integer, primary_key=True)
#     llc = db.Column (db.String (240))
#     llc_name = db.Column (db.String (240))
#     legal_add = db.Column(db.String(240))
#     fact_address = db.Column(db.String(240))
#     inn = db.Column(db.String(240))
#     kpp = db.Column(db.String(240))
#     ogrn = db.Column(db.String(240))
#     bank = db.Column(db.String(240))
#     bik = db.Column(db.String(240))
#     rc = db.Column(db.String(240))
#     kc = db.Column(db.String(240))
#     driver_director = db.Column(db.String(240))
#     user_id = db.Column(db.Integer, db.ForeignKey ('user.id'))
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     finance = db.Column(db.Integer, db.ForeignKey('finance.id'))
#     pay = db.Column(db.Integer, db.ForeignKey('paid.id'))



#база данных договоров с клиентами
class Agreement(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   creation = db.Column (db.DateTime, default=datetime.utcnow)
   date = db.Column(db.String(120))
   user_id = db.Column(db.Integer, db.ForeignKey ('user.id'))
   date_agreement = db.Column(db.DateTime, default = datetime.utcnow)
   filename = db.Column(db.String(120))
   customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
   customer_name = db.Column(db.String(240), unique=True)
   number = db.Column(db.String(240))
   choice = db.Column(db.String(240))
   count = db.Column(db.Integer, unique = True)

#база данных договоров с поставщиками
class Agreement_supplier(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   creation = db.Column (db.DateTime, default=datetime.utcnow)
   date = db.Column(db.String(120))
   user_id = db.Column(db.Integer, db.ForeignKey ('user.id'))
   date_agreement = db.Column(db.DateTime, default = datetime.utcnow)
   filename = db.Column(db.String(120))
   supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
   supplier_name = db.Column(db.String(240), unique=True)
   number = db.Column(db.String(240))
   choice = db.Column(db.String(240))
   count = db.Column(db.Integer, unique = True)


class Agg_number(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    numb = db.Column(db.String(120))

class Who_number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

class Truck(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

class Quantity(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)

class Truck_opt(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String (120), unique=True)

class Ttn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

class Customer_base(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (120), unique=True)



class Finance(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (120), unique=True)
    dtae = db.Column (db.DateTime)
    cost  = db.Column (db.Integer)
    payid_off = db.relationship('Paid', backref='payd_off', lazy='dynamic')
    cost = db.relationship('Supplier', backref='supplier', lazy='dynamic')
    new_cost = db.Column(db.Integer)


    
    def newCost(self):

        self.new_cost = self.cost
        db.session.commit()
        
        for i in self.payid_off:
            self.new_cost -= i.summ
            db.session.commit()
        return self.new_cost


class Paid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summ = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    finance = db.Column(db.Integer, db.ForeignKey('finance.id'))









    


