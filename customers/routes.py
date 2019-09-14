from flask import render_template, request, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g, Response
from suppliers import supp
from suppliers.models import Supplier, Prefin, Documents, Tn, Supp_payment 
from app_main.models import *
from app_main import db, app

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
    return render_template('customers_payments.html', customers=customers)