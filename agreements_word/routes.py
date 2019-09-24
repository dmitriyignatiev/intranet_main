from flask import render_template, request, current_app, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g, Response
from suppliers import supp
from suppliers.models import Supplier, Prefin, Documents, Tn, Supp_payment 
from app_main.models import *
from app_main import db, app
from .forms import *
from .models import *
from flask import jsonify


from agreements_word import agr

from mailmerge import MailMerge

from datetime import date
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@agr.route('/', methods=['POST', 'GET'])
def index():
    form = OrderForm()
    target = os.path.join(APP_ROOT, 'agreements_TEST/')
    if not os.path.isdir(target):
         os.mkdir(target)
   
    form.customer_name.choices = [(g.name, g.name) for g in Customer.query.all()]
    
    path = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\argeement\{}"
    
    template_test = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\argeement\order_rosexp_customer.docx"
    template_r_ttg = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\argeement\r_ttg.docx"
    document_test = MailMerge(template_test)
    document_r_ttg = MailMerge(template_r_ttg)

    print(document_test.get_merge_fields())
    print(document_r_ttg.get_merge_fields())
   
    list=[]
    list.extend((template_test, template_r_ttg))
    print(list)
    count = 0
    new_list=[]

    all_agr_db = Agreements.query.all()

    if request.method == 'POST' and form.validate():
        print(form.customer_name.data)
        
        

        for i in list:
            agr = Agreements()
            db.session.add(agr)
            db.session.commit()

            document = MailMerge(i)
            new_list=[i for i in document.get_merge_fields()]
            print(new_list)
            document.merge(
            time_loading = form.time_loading.data,
            order_number = str(agr.id),
            date_order = str(form.date_order.data),
            date_loading = str(form.date_loading.data),
            tima_loading = form.time_loading,
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
            cost = form.cost.data,
            
            
            
            
            
          



        )
            count +=1
            if 'r_ttg' in new_list:
                document.merge(
                    who_customer = ' "ООО Росэкспортдизайн" ',
                    who_supplier = ' "ООО ТТГ" ',
                )
                

                
                
            elif 'r_ttg' not in new_list:
                 document.merge(
                    who_customer = 'test customer',
                    who_supplier = 'test supplier',
                )

            document.write(path.format('Заявка №  {} между  {}.docx'.format(agr.id, count)))
            

            agr.path = 'Заявка №  {} между  {}.docx'.format(agr.id, count)
            destination = "/".join([target, agr.path])
            document.write(destination)
            db.session.commit()
        return redirect(request.url)
                
   
    return render_template('order_form.html', \
        form=form, all_agr_db = all_agr_db)

@agr.route('/download_agr/<path:filename>', methods=['GET', 'POST'])
def download_agr(filename):
    return send_from_directory(os.path.join(APP_ROOT, 'agreements_TEST/'),
                                filename, as_attachment=True)


@agr.route('/delete_agr/<int:id>', methods=['POST', 'GET'])
def delete_agr(id):
    id = request.args.get('id')

    agr_db = Agreements.query.get(id)
    os.remove(os.path.join(APP_ROOT, 'agreements_TEST/', agr_db.path))
    db.session.delete(agr_db)
    db.session.commit()
   
    