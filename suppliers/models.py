from app_main import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class Supplier(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    llc = db.Column (db.String (240))
    llc_name = db.Column (db.String (240))
    legal_add = db.Column(db.String(240))
    fact_address = db.Column(db.String(240))
    inn = db.Column(db.String(240))
    kpp = db.Column(db.String(240))
    ogrn = db.Column(db.String(240))
    bank = db.Column(db.String(240))
    bik = db.Column(db.String(240))
    rc = db.Column(db.String(240))
    kc = db.Column(db.String(240))
    driver_director = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey ('user.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    finance = db.Column(db.Integer, db.ForeignKey('finance.id'))
    pay = db.Column(db.Integer, db.ForeignKey('paid.id'))
    prefin = db.relationship('Prefin', backref='supplier', lazy='dynamic')
    supp_payment = db.relationship('Supp_payment', backref='supp_payment', lazy='dynamic')
    inv = db.relationship('Invoicesup', backref='supplier', lazy='dynamic')

    def total_cost(self):
        total_summ = 0;
        for i in self.supp_payment:
            total_summ += i.s_inv_amount
        return total_summ

    #   показывает все номера  счетов от поставщика
    def invoices_list(self):
        list = []
        for invoice in self.prefin:
            
            list.append(invoice.s_invoice_number)
        return list
    
    # показывает суммы счетов
    def invoice_amount_list(self):
        new_list=[]
        for invoice in self.prefin:
            new_list.append(invoice.s_inv_amount)
        return new_list

            
        

   
    
    

#класс где мы будем разносить оплаты перевозчикам
class Supp_payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_inv_number = db.Column(db.String(120))
    s_invoice_date = db.Column(db.DateTime)
    s_inv_amount = db.Column(db.Integer)
    s_inv_currency = db.Column(db.String(120))
    s_inv_pay_day = db.Column(db.DateTime)
    s_payment_summ = db.Column(db.Integer)
    bank = db.Column(db.String(240))
    tora_red = db.Column(db.String(240))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id')) 
    fin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))
    day_plan_pay = db.Column(db.DateTime)

class newSup(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (240))
    path = db.Column(db.String(1000))



class Prefin(db.Model):

    id = db.Column (db.Integer, primary_key=True)
    tora_red = db.Column(db.String(120))
    supplier_name = db.Column (db.String (240))
    req_id = db.Column(db.Integer, unique=True)
    tora_red = db.Column(db.String(120))
    direction = db.Column(db.String(120))
    sale = db.Column(db.String(120))
    buyer = db.Column(db.String(120))
    status_of_request=db.Column(db.String(120))
    blank_option_1 = db.Column(db.String(120))
    customer_name = db.Column(db.String(120))
    customer_accept_invoice_status = db.Column(db.String(120))
    customer_order_number = db.Column(db.String(120))
    customer_order_date = db.Column(db.DateTime)
    customer_order_month = db.Column(db.Integer)
    loading_place = db.Column(db.String(120))
    loading_date = db.Column(db.DateTime)
    cargo_character = db.Column(db.Text)
    unloading_place = db.Column(db.String(120))
    unloading_date = db.Column(db.DateTime)
    supplier_name = db.Column(db.String(120))
    s_invoice_number = db.Column(db.String(120))
    ttn_cmr_available = db.Column(db.String(120))
    s_inv_date = db.Column(db.DateTime)
    s_inv_amount = db.Column(db.Float, nullable=True)
    s_inv_vat = db.Column(db.Text)
    s_inv_currency = db.Column(db.String(120))
    s_prepaid_amount = db.Column(db.Integer)
    s_prepaid_data = db.Column(db.DateTime)
    cost_with_vat = db.Column(db.Integer)
    cost_pochta = db.Column(db.Integer)
    cost_final = db.Column(db.Integer)
    cost_we_still_need_pay = db.Column(db.Integer)
    s_inv_status_payment = db.Column(db.String(120))
    s_inv_credit_terms = db.Column(db.Integer)
    s_credit_terms_scan_org = db.Column(db.String(120))
    s_inv_status = db.Column(db.String(120)) # ЗНАЧ!!!
    blank_option_2 = db.Column(db.String(120))
    s_inv_act_date_payment = db.Column(db.DateTime)
    s_invoice_transit_name = db.Column(db.String(120))
    c_inv_number = db.Column(db.String(120))
    c_invoice_date = db.Column(db.DateTime)
    c_inv_amount = db.Column(db.String(120))
    c_inv_currency = db.Column(db.String(120))
    c_invfacture_number = db.Column(db.String(120))
    c_invfacture_data = db.Column(db.DateTime)
    c_inv_issue = db.Column(db.String(120))#42
    c_ems_tracking = db.Column(db.String(120))
    c_inv_post_send_data = db.Column(db.DateTime)
    c_inv_plan_pay = db.Column(db.DateTime)
    c_inv_week_plan_pay = db.Column(db.Integer)
    c_inv_status_payment = db.Column(db.String(120))
    c_inv_act_pay_date = db.Column(db.DateTime)
    profit = db.Column(db.Integer)
    month_number = db.Column(db.Integer)
    comments = db.Column(db.Text)
    s_inv_put_reestr = db.Column(db.Integer)
    s_np_ati = db.Column(db.String(120))
    s_inv_part_payment_16wk = db.Column(db.Integer)
    s_inv_part_pay_issue = db.Column(db.String(120))
    s_inv_part_payment_17wk = db.Column(db.Integer)
    s_inv_part_payment_18wk_2019= db.Column(db.Integer)
    s_inv_part_payment_20wk_2019 = db.Column(db.Integer)
    s_inv_part_payment_21wk_2019 = db.Column(db.Integer)
    s_inv_part_payment_22wk_2019 = db.Column(db.Integer)
    s_inv_part_payment_23wk_2019 = db.Column(db.Integer)
    s_inv_part_payment_24wk_2019 = db.Column(db.Integer)
    s_inv_part_payment_25wk_2019 = db.Column(db.Integer)
    s_inv_part_payment_26wk_2019 = db.Column(db.Integer)
    s_inv_part_payment_27wk_2019= db.Column(db.Integer)
    s_inv_part_payment_28wk_2019= db.Column(db.Integer)
    blank_option_3 = db.Column(db.String(120))
    s_inv_part_payment_29wk_2019 = db.Column(db.Integer)
    blank_option_4 = db.Column(db.String(120))
    s_inv_part_march_2019 = db.Column(db.Integer)
    blank_option_5 = db.Column(db.String(120))
    blank_option_6 = db.Column(db.String(120))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    vat = db.Column(db.Integer)
    pochta = db.relationship('Pochta', backref='fin', lazy='dynamic')
    pochta_full_cost = db.Column(db.Integer)
    s_inv_date_to_pay = db.Column(db.DateTime)
    s_inv_date = db.Column(db.DateTime)
    #Доки
    zayvka = db.relationship('Zayvka', backref='prefin_z', lazy='dynamic')
    docs = db.relationship('Documents', backref='prefin_docs', lazy='dynamic')
    invs = db.relationship('Invoicesup', backref='prefin_invs', lazy='dynamic')
    invc = db.relationship('Invoicecust', backref='prefin_invc', lazy='dynamic')
    tn_doc = db.relationship('Tn', backref='prefin', lazy='dynamic')


       

    def pochta_cost(self):
        summ = 0
        for p in self.pochta.all():
            summ +=p.cost
            self.pochta_full_cost = summ 
            db.session.commit()
        return summ

        
    
   
    


#Для подгрузки ТН
class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    req_id = db.Column(db.Integer)
    path = db.Column(db.Text)
    req_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    prefin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))

class Tn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    req_id = db.Column(db.Integer)
    path = db.Column(db.Text)
    req_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    prefin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))

#Для подрузки счета от Поставщика
class Invoicesup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fin_id = db.Column(db.Integer)
    path = db.Column(db.Text)
    prefin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))
    req_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    supp_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
#Для подгрузки счета на клиента
class Invoicecust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fin_id = db.Column(db.Integer)
    path = db.Column(db.Text)
    prefin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))
    req_id = db.Column(db.Integer, db.ForeignKey('request.id'))



class Pochta(db.Model):

    __tablename__='pochta'
    id = db.Column(db.Integer, primary_key=True)
    track_number = db.Column(db.String(500))
    cost = db.Column(db.Integer)
    fin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))


class Parent(db.Model):
    
    id = db.Column(db.Integer, primary_key=True) 
    children = db.relationship("Child")

class Child(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))










    




