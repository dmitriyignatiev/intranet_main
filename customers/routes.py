from flask import render_template, request, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g, Response
from suppliers import supp
from suppliers.models import Supplier, Prefin, Documents, Tn, Supp_payment 
from app_main.models import *
from app_main import db, app
from .forms import *
from .models import *

from customers import cust

from sqlalchemy import exc
from sqlalchemy import desc, or_, and_

import datetime
from datetime import timedelta
import json

@cust.route('/index')
def index():
    return "Privet customers"

@cust.route('/customers', methods=['POST', 'GET'])
def customers_payments():
    customers = Customer.query.all()
    invoices = Invoicecust.query.all()
    formName = CustomerForm()
    formName.name.choices = [(g.id, g.name) for g in customers]
    today = datetime.datetime.today()

    
   
    if formName.is_submitted():
        customer = Customer.query.get(formName.name.data)
        print(customer.id)

        all_payments = Invoice_payment_c.query.filter(Invoice_payment_c.customer_id==customer.id).\
            order_by(Invoice_payment_c.date.desc()).all()
        
        invoices_failed = Invoicecust.query.filter(and_(Invoicecust.customer_id==customer.id, Invoicecust.invoice_deadline_payment<today)).\
            order_by(Invoicecust.invoice_date.desc()).all()
        
    
        
    
        
        formInvoice = InvoiceForm()
        invoices = Invoicecust.query.filter(Invoicecust.customer_id==customer.id).\
            order_by(Invoicecust.invoice_date.desc()).all()
        formInvoice.number.choices=[(g.id, g.invoice_number) for g in invoices]


        return render_template('customers_payments.html', \
        customers=customers, formName=formName, customer=customer, invoices=invoices,\
            formInvoice=formInvoice, all_payments=all_payments, today=today, invoices_failed=invoices_failed)
    
    return render_template('customers_payments.html', \
        customers=customers, formName=formName, invoices=invoices)

@cust.route('add_payments', methods=['POST', 'GET'])
def add_payments():
    name = request.args.get('name')
    summ = request.args.get('summ')
    date = request.args.get('date')
    data=datetime.datetime.strptime(date,'%Y-%m-%d')
    invoice_number = request.args.get('c_inv_number')
    


    customer = Customer.query.filter_by(name=name).first()
    
    print(customer)

    invoicecust = Invoicecust.query.filter(and_(Invoicecust.customer_id==customer.id, Invoicecust.invoice_number==invoice_number)).first()
    print(invoicecust)

    payment = Invoice_payment_c(summ=summ, date=data,\
        invoice_number=invoice_number, invoicecust_id=invoicecust.id, customer_id=customer.id)
    db.session.add(payment)
    db.session.commit()



    
    print(type(data))
    return jsonify({'summ':summ , 'name':name, \
        'data': data, 'invoice':invoice_number, 'customer':customer.id})


@cust.route('remove_payments_c/<int:id>', methods=['POST', 'GET'])
def remove_payments_c(id):
    id = request.args.get('id')
    payment = Invoice_payment_c.query.get(int(id))
    if payment:
        db.session.delete(payment)
        db.session.commit()
        return jsonify({'success_remove':'Запись удалена'})
    else:
        return jsonify({'faile':'failed'})



    