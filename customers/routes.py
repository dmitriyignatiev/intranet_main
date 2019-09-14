from flask import render_template, request, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g, Response
from suppliers import supp
from suppliers.models import Supplier, Prefin, Documents, Tn, Supp_payment 
from app_main.models import *
from app_main import db, app
from .forms import *

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
    formName = CustomerForm()
    formName.name.choices = [(g.id, g.name) for g in customers]

    # invoices = Invoicecust.query.all()
    # formInvoice=InvoiceForm()
    # formInvoice.invoice_number.choices=[(g.ig, g.invoice_number)]
    
    if formName.is_submitted():
        customer = Customer.query.get(formName.name.data)
        print('yes : ' + str(customer.name))
        
        return render_template('customers_payments.html', \
        customers=customers, formName=formName, customer=customer)

    else:
        print('no')

    return render_template('customers_payments.html', \
        customers=customers, formName=formName)