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

@agr.route('/index', methods=['POST', 'GET'])
def index():
    form = OrderForm_a()
    
    target = os.path.join(APP_ROOT, 'agreements_TEST/')
    if not os.path.isdir(target):
         os.mkdir(target)
   
    form.customer_name.choices = [(g.name, g.name) for g in Customer.query.all()]
    form.supplier_name.choices = [(g.llc_name, g.llc_name) for g in Supplier.query.all()]

    path = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\argeement\{}"
    
   
    template_with_customer = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\a\r_with_custt.docx"
    template_with_supplier = r"C:\Users\Dmitriy\Desktop\intr\intranet_main\agreements_word\a\r_with_supp.docx"

    

   
    list=[]
    
    
        
    if request.form.getlist('add_supp') and request.form.getlist('add_cust'):
        list.extend((template_with_customer, template_with_supplier ))
    
    elif request.form.getlist('add_supp'):
        list.append(template_with_supplier)
    elif request.form.getlist('add_cust'):
        list.append(template_with_customer)
    
    print('this is a list: ',  list)
    

   
    count = 0

    
    new_list = []

    all_agr_db = Agreements.query.filter(Agreements.user_id==current_user.id).order_by(Agreements.date_order.desc()).all()
   
    if request.method == 'POST':

        for i in list:

            agr = Agreements(user_id=current_user.id)
            db.session.add(agr)
            db.session.commit()

            document = MailMerge(i)
            new_list=[i for i in document.get_merge_fields()]
            print('this a new list' + str(new_list))
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
            drive_license = form.driver_license.data,
            type_truck = form.type_truck.data,

            #cost_agreem_with_supp
            cost = form.cost.data,
            date_payment = form.date_payment.data,
            org_scan = form.org_scan.data,

             #cost_agreem_with_cust
            cost_c = form.cost_c.data,
            org_scan_с = form.org_scan_с.data,
            date_payment_с = form.date_payment_с.data,

            #cnee
            who_cust = form.customer_name.data, 
            legal_add = form.cust_legal_address.data, 
            fact_add = form.cust_fact_address.data,
            inn = form.cust_inn.data,
            kpp = form.cust_kpp.data,
            bank = form.cust_bank.data,
            cust_bik_bank = form.cust_bik_bank.data, 
            cust_bank_kc = form.cust_bank_kc.data,
            cust_acc_test = form.cust_accout.data,
            cust_sign_fio = form.cust_sign_fio.data,
            
            #supplier

            who_supplier = form.supplier_name.data, 
            supp_legal_address = form.supp_legal_address.data, 
            supp_fact_address = form.supp_fact_address.data,
            supp_inn = form.supp_inn.data,
            supp_kpp = form.supp_kpp.data,
            supp_bank = form.supp_bank.data,
            supp_bank_kc = form.supp_bank_kc.data, 
            supp_account = form.supp_accout.data,
            supp_bank_bik = form.supp_bank_bik.data,
            supp_sign_fio = form.supp_sign_fio.data,


        )
            
               




            agr.date_loading = form.date_loading.data
            agr.date_order = form.date_order.data
            agr.driver =form.driver_name.data,
            agr.shipper_name = form.shipper_name.data
            agr.shipper_address = form.address_loading.data
            agr.shipper_phone = form.contacts_loading.data

            agr.cnee_name = form.cnee_name.data 
            agr.cnee_address = form.address_unloading.data
            agr.cnee_phone = form.contacts_unloading.data
            db.session.commit()

            count +=1
         
                
                
            
           
            if  request.form.getlist('add_supp'):
                agr.path = 'Заявка №  {} между Росэкспортом и  Перевозом: {}  .docx'.format(agr.id, form.supplier_name.data)
                destination = "/".join([target, agr.path])
                document.write(destination)
                db.session.commit()
               
            
            if request.form.getlist('add_cust') and not request.form.getlist('add_supp'):
                
                agr.path = 'Заявка №  {} между Росэкспортом и  Клиентом: {}  .docx'.format(agr.id, form.customer_name.data)
                destination = "/".join([target, agr.path])
                document.write(destination)
                db.session.commit()
                

            if request.form.getlist('add_supp') and request.form.getlist('add_cust'):
                if i == list[0]:
                    agr.path = 'Заявка №  {} между Росэкспортом и  Клиентом: {}  .docx'.format(agr.id, form.customer_name.data)
                    destination = "/".join([target, agr.path])
                    document.write(destination)
                    db.session.commit()
                
                    
                elif i==list[1]:
                    agr.path='Заявка №  {} между Росэкспортом и  Перевозом: {}  .docx'.format(agr.id, form.supplier_name.data)
                    destination = "/".join([target, agr.path])
                    document.write(destination)
                    db.session.commit()
                    
        return redirect(url_for('.index'))

            

            
           
            
            
                
            
            
            

            
        

            
        
                
   
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
    return redirect(url_for('.index'))
   
    