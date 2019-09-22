from flask import render_template, request, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g, Response
from suppliers import supp
from suppliers.models import Supplier, Prefin, Documents, Tn, Supp_payment 
from app_main.models import *
from app_main import db, app
from .forms import *
from .models import *

from agreements_word import agr

from mailmerge import MailMerge

from datetime import date

@agr.route('/', methods=['POST', 'GET'])
def index():
    form = OrderForm()
   
    form.customer_name.choices = [(g.name, g.name) for g in Customer.query.all()]
    
    path = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\argeement\{}"
    
    template = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\argeement\order_rosexp_customer.docx"
    document = MailMerge(template)
    print(document.get_merge_fields())

    if request.method =='POST':
        print(form.customer_name.data)
        agr = Agreements()
        db.session.add(agr)
        db.session.commit()

        document = MailMerge(template)
        document.merge(
            order_number = str(agr.id),
            date_order = str(form.date_order.data),
            date_loading = str(form.date_loading.data),
            org = form.o_from.data,
            dest = form.o_to.data,
            address_loading = form.address_loading.data,
            contacts_loading = form.contacts_loading.data,
            cargo_description  = form.cargo_description.data,
            quantity_pallets = form.quantity_pallets.data,
            weigth = form.weigth.data,
            shipper_name=form.shipper_name.data,
            cnee_name=form.cnee_name.data,
            cnee_contact=form.cnee_contact.data,
            cost = form.cost.data



        )
        document.write(path.format('Заявка{}.docx'.format(agr.id)))

    print(document.get_merge_fields())
    return render_template('order_form.html', \
        form=form)