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
    form = OrderForm_a()
    
    target = os.path.join(APP_ROOT, 'agreements_TEST/')
    if not os.path.isdir(target):
         os.mkdir(target)
   
    form.customer_name.choices = [(g.name, g.name) for g in Customer.query.all()]
    
    path = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\argeement\{}"
    
    template_test = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\argeement\order_rosexp_customer.docx"
    template_r_ttg = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\a\r.docx"
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
     
        
        

        for i in list:
            agr = Agreements()
            db.session.add(agr)
            db.session.commit()

            document = MailMerge(i)
            new_list=[i for i in document.get_merge_fields()]
            print(new_list)
            document.merge(
            
            #date_order
            date_order = str(form.date_order.data),
            #номер заявки
            order_number = str(agr.id),

            #loading
            org = form.o_from.data,
            date_loading = str(form.date_loading.data),
            
            address_loading = form.address_loading.data,
            time_loadding =form.time_loading.data,
            contacts_loading = form.contacts_loading.data,

            #dest
            dest = form.o_to.data ,
            date_unloading = form.date_unloading.data,
            time_unloading = form.time_unloading.data, 
            address_unloading = form.address_unloading.data,
            contacts_unloading = form.contacts_unloading.data,

            #cargo
            cargo_description = form.cargo_description.data, 
            quantity_pallets = form.quantity_pallets.data,
            weigth = form.weigth.data,
            type_loading = form.type_loading.data,
            type_unloading = form.type_unloading.data,
            cargo_cost = form.cargo_cost.data,
            volume = form.volume.data,
            comments = form.cargo_comments.data,

            #auto
            model = form.model.data,
            auto_number = form.auto_number.data,
            driver_name = form.driver_name.data,
            driver_phone = form.driver_phone.data,
            passport = form.passport.data,
            driver_license = form.driver_license.data,
            type_truck = form.type_truck.data,

            #cost_agreem
            cost = form.cost.data,
            date_payment = form.date_payment.data,
            org_scan = form.org_scan.data,

            #cnee
            legal_add = form.cust_legal_address.data, 
            fact_add = form.cust_fact_address.data,
            inn = form.cust_inn.data,
            kpp = form.cust_kpp.data,
            bank = form.cust_bank.data,
            cust_bik_bank = form.cust_bik_bank.data, 
            cust_bank_kc = form.cust_bank_kc.data,
            cust_acc_test = form.cust_accout.data,
            cust_sign_fio = form.cust_sign_fio.data,





            

            

           
            
            
            
            
          



        )
            agr.shipper_name = form.shipper_name.data
            agr.shipper_address = form.address_loading.data
            agr.shipper_phone = form.contacts_loading.data

            agr.cnee_name = form.cnee_name.data 
            agr.cnee_address = form.address_unloading.data
            agr.cnee_phone = form.contacts_unloading.data
            db.session.commit()

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
                
            
         
            
            
            if 'r_ttg' in new_list:
                agr.path = 'Заявка №  {} между  Росэкспорт и клиент {}.docx'.format(agr.id, form.customer_name.data)
                destination = "/".join([target, agr.path])
                document.write(destination)
                db.session.commit()
            elif 'r_ttg' not in new_list:
                agr.path = 'Заявка №  {} между  Test и {}.docx'.format(agr.id, form.customer_name.data)
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
    return redirect_url('.index')
   
    