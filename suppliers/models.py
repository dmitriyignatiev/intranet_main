from app_main import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


finsupp_table = db.Table('finsup',
                     db.Column('prefin_id', db.Integer, db.ForeignKey('prefin.id')),
                     db.Column('supp_ip', db.Integer, db.ForeignKey('supplier.id'))
                    )


comp_supp = db.Table('comp_supp',
            db.Column('supplier_id', db.Integer, db.ForeignKey('supplier.id')),
            db.Column('company_id', db.Integer, db.ForeignKey('companies.id'))
            )


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
    prefin = db.relationship('Prefin', secondary=finsupp_table,
                                backref=db.backref('supplier', lazy='dynamic'))
    supp_payment = db.relationship('Supp_payment', backref='supp_payment', lazy='dynamic')
    inv = db.relationship('Invoicesup', backref='supplier', lazy='dynamic')
    invoice_payment = db.relationship('Invoice_payment_s', backref='supplier', lazy='dynamic')

    company = db.relationship('Companies', secondary=comp_supp,
                               
                                backref=db.backref('supplier', lazy='dynamic')
    )
    docs = db.relationship('Supplierdocs', backref='supplier', lazy='dynamic')
    

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

    # показывает ссылки на счета 
    def invoice_link(self):
        new_list=[]
        for fin in self.prefin:
            for path in fin.invs:
                new_list.append(path.path)
        return new_list

    # итоговую задолженность
    def total_debt(self):
        inv = [i.s_inv_amount for i in self.supp_payment]
        payments = [p.summ_pay for p in self.invoice_payment if p.supp_payment_s in self.supp_payment]
        return sum(inv)-sum(payments)

    # работы без счетов
    def work_wo_inv(self):
        list = [x for x in self.supp_payment if not x.s_inv_number ]
        return list

    #показывает просроченные счета
    def bad_debt(self):
        day=datetime.today()
        list = [s for s in self.supp_payment if s.s_inv_number]
        inv_list = [s for s in list if s.s_invoice_date if s.day_plan_pay if s.day_plan_pay < day]
        return inv_list

    #есть счет но без даты когда надо платить
    def work_wo_inv_plan_day(self):
        list = [x for x in self.supp_payment if x.s_inv_number if not x.day_plan_pay ]
        return list

    # показывает сколько мы должны
    def total_credit(self):
        credit=0
        for invoice in self.supp_payment:
            credit += invoice.still_own()
        return credit

    def last_payment(self):
        try:
            payments_all = Invoice_payment_s.query.\
            filter_by(supplier_id=self.id).\
                order_by(Invoice_payment_s.date_payment.desc()).first()
            return payments_all.date_payment.strftime("%Y-%m-%d")
        except AttributeError:
            return "Платежей пока не было"


#класс где мы будем хранить документы
class Supplierdocs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.Text())
    confirmdoc = db.Column(db.Text())
    orderdoc = db.Column(db.Text())
    supp_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))


            

#класс где мы будем разносить оплаты перевозчикам
#storage for all invoices
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
    vat = db.Column(db.String(120))
    invoice_payment = db.relationship('Invoice_payment_s', backref='supp_payment_s', lazy='dynamic')
    invoice_path = db.relationship('Invoicesup', backref='supp_payment', lazy='dynamic')



    #возвращает значение сколько мы остаемся должны
    def still_own(self):
        summ = 0
        for payment in self.invoice_payment.all():
            summ += payment.summ_pay
        return self.s_inv_amount - summ

    def invoice(self):
        list = []
        for path in self.invoice_path:
            list.append(path.path)
        return(list)
    
    def count_payments(self):
        return self.invoice_payment.count()

    def last_payment(self):
        try:
            payments_all = Invoice_payment_s.query.\
            filter_by(supp_payment=self.id).\
                order_by(Invoice_payment_s.date_payment.desc()).first()
            return payments_all.date_payment.strftime("%Y-%m-%d")
        except AttributeError:
            return "Платежей пока не было"

    #показываем через кого платили
    def transit(self):
        list = [x for x in self.invoice_payment ]
        transit_list = [x.transit.all() for x in list]
        return transit_list

    
        
        
    

#class where payments will be store many-to-one with Supp_payment
class Invoice_payment_s(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_inv_number = db.Column(db.String(120))
    summ_pay = db.Column(db.Integer)
    transit = db.Column(db.String(120))
    date_payment = db.Column(db.DateTime)
    supp_payment = db.Column(db.Integer, db.ForeignKey('supp_payment.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    commision = db.Column(db.Float)
    cost_for_us = db.Column(db.Float)
    tr_payment = db.relationship('Tr_payments', backref='payment', lazy='dynamic')
    
    

    
    def cost_with_commision(self):
        if self.commision:
            self.cost_for_us=self.summ_pay/(100-self.commision)/100
            return self.cost_for_us
        else:
            return False



   



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
    #вместо invs используем supp_payment при обращениях
    invs = db.relationship('Invoicesup', backref='prefin_invs', lazy='dynamic')
    invc = db.relationship('Invoicecust', backref='prefin_invc', lazy='dynamic')
    tn_doc = db.relationship('Tn', backref='prefin', lazy='dynamic')
    supp_payments = db.relationship('Supp_payment', backref='supp_p', lazy='dynamic')
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
   
       

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
    supp_payment_id = db.Column(db.Integer, db.ForeignKey('supp_payment.id'))










class Pochta(db.Model):

    __tablename__='pochta'
    id = db.Column(db.Integer, primary_key=True)
    track_number = db.Column(db.String(500))
    cost = db.Column(db.Integer)
    fin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))


class Transit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inn = db.Column(db.String(10))
    name = db.Column(db.Text)
    payment = db.relationship('Tr_payments', backref='transit', lazy='dynamic')
    

    def invoices(self):
        list = [x for x in self.payment]
        return list

    def __repr__(self):
        return "{},  {}".format(self.name, self.inn)

class Tr_payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer)
    transit_id = db.Column(db.Integer, db.ForeignKey('transit.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('invoice_payment_s.id'))
    status = db.Column(db.Text)
    transit_date_send = db.Column(db.DateTime)
    transit_date_recieved = db.Column(db.DateTime)
    doc_path = db.Column(db.Text)
    confirm = db.Column(db.Integer)
    commision = db.Column(db.Float)

class Tr_status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)


#our company + many-to-many with suppliers


class Companies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inn = db.Column(db.Text)
    name = db.Column(db.Text)
    bank = db.relationship('Bank', backref='company', lazy='dynamic')
    

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    
    
















    




