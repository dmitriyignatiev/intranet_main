from app_main import db, login, ma

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime

from marshmallow_sqlalchemy.fields import Nested, fields
from sqlalchemy.orm import backref


#Для подгрузки счета на клиента + информация по счетам
class Invoicecust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fin_id = db.Column(db.Integer)
    path = db.Column(db.Text)
    prefin_id = db.Column(db.Integer, db.ForeignKey('prefin.id'))
    req_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    invoice_number = db.Column(db.Text)
    invoice_amount = db.Column(db.Float)
    invoice_vat = db.Column(db.Float)
    invoice_date = db.Column(db.DateTime)
    invoice_deadline_payment = db.Column(db.DateTime)
    invoice_tracking_number = db.Column(db.Text)
    invoice_tracking_company = db.Column(db.Text)
    invoice_tracking_day = db.Column(db.DateTime)
    dd = db.relationship('Invoice_payment_c', backref='inv_c', lazy='dynamic')
    invoiceadd = db.relationship('AddInvoiceCust', backref='inv_add',
                                                    lazy='dynamic')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    add = db.relationship('Add', backref='invadd',
                                                    lazy='dynamic')


    def all_payments(self):
        sum =0
        list = [i.summ for i in self.invoice_actual_payment]
        for i in list:
            print(i)
          
        return sum

    #задолженность по счету
    def debt_inv(self):
        sum =0
        list = [i.summ for i in self.invoice_actual_payment ]
        for i in list:
            sum +=i
        dept = self.invoice_amount - sum
        if dept > 0:
            return  dept
        else:
            return 0


    def debt(self):
        sum =0
        list = [self.invoice_number for self in c.invoices if self.debt_inv()]
        
        return list()









#детализация по счету
class Invoice_payment_c(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summ = db.Column(db.Float)
    date = db.Column(db.DateTime)
    invoice_number = db.Column(db.Text)
    invoicecust_id = db.Column(db.Integer, db.ForeignKey('invoicecust.id') )
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    

    def sum(self):
        payments = Invoicecust.query.filter_by(invoicecust_id=self.id).all()
        return payments

#Дополнительные строки в инвойсе

class Add(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoicecust_id = db.Column(db.Integer, db.ForeignKey('invoicecust.id') )

class AddInvoiceCust(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addNumber = db.Column(db.Integer)
    addDescription = db.Column(db.Text)
    addAmount=db.Column(db.Float)
    addVat = db.Column(db.Float)
    invoicecust_id = db.Column(db.Integer, db.ForeignKey('invoicecust.id') )

   
   





        
    

class AddInvoiceShema(ma.ModelSchema):
    class Meta:
        model=AddInvoiceCust
      

class InvoicecustShema(ma.ModelSchema):
    adds = ma.Nested(AddInvoiceShema, many=True)
    class Meta:
        model = Invoicecust


    
        
