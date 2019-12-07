from flask import render_template, request, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g, Response
from suppliers import supp
from .models import Supplier, Prefin, Documents, Tn, Supp_payment 
from app_main.models import *
from app_main import db, app
from .forms import *
from sqlalchemy import exc
from sqlalchemy import desc, or_, and_

from customers.models import *

import datetime
from datetime import timedelta
import json

from flask_login import current_user, login_required, login_user, logout_user









@supp.route('/index')
def index():
    return render_template('app_main.base.html')


@supp.route('/add_supplier/<int:id>', methods=['GET', 'POST'])
def add_supplier(id):
    
    req = Request.query.get(id)
    session['id']=req.id
    fin = Prefin.query.filter(Prefin.req_id==session['id']).first()
    docs = Documents.query.filter(Documents.req_id==session['id'])
    id = req.id
    pick_up_date = req.pick_up_date


    
    
    z_id = session['id']
    z_doc = Zayvka.query.filter(Zayvka.req_id==z_id)
    print('z_doc is:' + str(z_id ))
    
    session['pick_up_date'] = pick_up_date

    new_id = session['id']
    print(new_id, pick_up_date)
    
    date = req.pick_up_date
    form=formSupplier()
    form.name.choices = [(g.llc_name, g.llc_name) for g in Supplier.query.order_by('llc_name')]
    
    
    if fin:
        form.tora_red.data = fin.tora_red
        form.name.data = fin.supplier_name
        form.status.data = fin.status_of_request



    return render_template('add_supplier.html', form=form, req=req, date=date, docs=docs, fin=fin, z_doc=z_doc)

@supp.route('/add_supplier_to_db', methods=['POST', 'GET'])
def add_supplier_to_db():

    form=Supplier()
    name = request.args.get('name')
    form_inn = request.args.get('inn')
    
    

    print(name)
    new_supp = Supplier.query.filter_by(llc_name=name).first() or Supplier.query.filter_by(inn=form_inn).first()
    if new_supp:
         return jsonify({'error': 'поставщик уже есть в базе данных с таким именем или с ИНН'})

    elif not new_supp:
    
        print('dewde')
        new_supp = Supplier(llc_name=name, inn=form_inn)
        db.session.add(new_supp)
        db.session.commit()
        return jsonify({'success': 'Поставщик упешно внесен в базу данных'})
    









import os

from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pdf'])



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@supp.route('/new')
def new():
    return render_template("upload.html")

@supp.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'documents/')
    r_id = request.args.get('req_id')
    print(r_id)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        if file and allowed_file(file.filename):
            print(file)
            new_d = Documents(req_id=session['id'])
            db.session.add(new_d)
            db.session.commit()
            filename=str(new_d.req_id) + file.filename
            new_d.path=str(filename)
            db.session.commit()

            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
            return jsonify({'success':'файлы успешно сохранены'})
        else:
            return jsonify({'success':'файлы запрещен к загрузке'})




@supp.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(os.path.join(APP_ROOT, 'documents/'),
                               filename, as_attachment=True)



@supp.route('/prefin', methods=['POST', 'GET'])
def prefin():
    transit = int(7)
    form = formSupplier()
    tora_red = request.args.get('name')
    req_id = request.args.get('id')
    date_request = request.args.get('date')
    customer_order_date=datetime.datetime.strptime(date_request, '%Y-%m-%d')
    supplier_name=request.args.get('supp')
    status_of_request = request.args.get('st')
    s_invoice_number = request.args.get('invoice_number')
    s_inv_amount =float(request.args.get('sinv_amount'))
    s_inv_vat = request.args.get('sinv_vat')
    c_inv_amount=int(request.args.get('cinv_amount'))
    supplier_id = Supplier.query.filter(Supplier.llc_name==supplier_name).first()
    pick_up_date = request.args.get('pick_up_date')
   
    unloading_date = request.args.get('unloading_date')
    s_inv_date = request.args.get('sinv_date')
    s_inv_currency = request.args.get('sinv_currency')
    s_inv_vat = request.args.get('sinv_vat')
    print('eto form.inv.date: ' +str(s_inv_currency) )
    if s_inv_vat=='НДС':
        cost_with_vat = round(s_inv_amount+(s_inv_amount*0.2),2)
    elif s_inv_vat=='БЕЗ НДС':
        cost_with_vat = round(s_inv_amount/0.93, 2)
    elif s_inv_vat=='НОЛЬ':
        cost_with_vat = s_inv_amount
        
    request_one=Request.query.get(req_id)
    direction = request_one.direction
    sale = request_one.user.name
    customer = request_one.customer.name
    buyer = request_one.users[0].name
    loading_place = request_one.org
    unloading_place  = request_one.dest
    
    s_inv_vat = s_inv_vat

    profit = cost_with_vat - c_inv_amount
    print('eto' + str(profit))

    try:
        if not Prefin.query.filter_by(req_id=req_id).first():
            print(tora_red + str(req_id) + ' ' + str(date_request)+''+str(supplier_name) + ''+ str(direction) + str(status_of_request))
            newFin = Prefin(tora_red=tora_red, 
                        req_id=req_id, 
                        request_id = req_id,
                        customer_order_date=customer_order_date,
                        direction=direction, 
                        sale=sale,
                        buyer = buyer,
                        customer_name=customer,
                        loading_place=loading_place,
                        unloading_place=unloading_place,
                        cargo_character = request_one.cargo_desciption,
                        supplier_name=supplier_id.llc_name,
                        status_of_request=status_of_request,
                        s_invoice_number=s_invoice_number,
                        s_inv_amount=s_inv_amount,
                        s_inv_vat = s_inv_vat,
                        c_inv_amount=int(c_inv_amount),
                        supplier_id = supplier_id.id,
                        loading_date = pick_up_date,
                        unloading_date = unloading_date,
                        s_inv_date = s_inv_date,
                        s_inv_currency = s_inv_currency,
                        cost_with_vat = cost_with_vat,
                        profit = c_inv_amount-cost_with_vat
                        
                        
                        )
            db.session.add(newFin)
            db.session.commit()
            newFin.supplier.append(supplier_id)
            supp_inv_draft = Supp_payment(s_inv_amount=s_inv_amount, supplier_id=supplier_id.id, fin_id=newFin.id)
            db.session.add(supp_inv_draft)
            

           
            request_one.complete_fin=1
            if request_one.zayvka.first():
                newFin.zayvka.append(request_one.zayvka.first())
                db.session.add(newFin)
                newFin.supplier.append(supplier_id)
                db.session.commit()
                
                return jsonify({'success':'данные успешно внесены в базу', 'req_id': newFin.id})
            else:
                db.session.add(newFin)
                db.session.commit()
                newFin.supplier.append(supplier_id)
                return jsonify({'success':'данные успешно внесены в базу но без заявки', 'req_id':  newFin.id})
              
           
        else:
            print('customer VGGFGF:' + customer)
            newFin=Prefin.query.filter_by(req_id=req_id).first()
            newFin.tora_red = tora_red,
            newFin.req_id=req_id,
            newFin.request_id = req_id,
            newFin.customer_order_date=customer_order_date,
            newFin.direction=direction, 
            newFin.sale=sale,
            newFin.buyer = buyer,
            newFin.customer_name=customer,
            newFin.cargo_character = request_one.cargo_desciption,
            
            newFin.supplier_name=supplier_id.llc_name,
            newFin.supplier_id = supplier_id.id,
            newFinloading_place=loading_place,
            newFin.unloading_place=unloading_place,
            newFin.status_of_request=status_of_request,
            newFin.s_invoice_number=s_invoice_number,
            newFin.s_inv_amount=s_inv_amount,
            newFin.s_inv_vat = s_inv_vat,
            newFin.c_inv_amount=int(c_inv_amount),
            
            newFin.loading_date = pick_up_date,
            newFin.unloading_date = unloading_date,
            newFin.s_inv_date = s_inv_date,
            newFin.s_inv_currency = s_inv_currency,
            newFin.cost_with_vat = cost_with_vat,
            newFin.profit = c_inv_amount- cost_with_vat
            if request_one.zayvka.first():
                newFin.zayvka.append(request_one.zayvka.first())
                newFin.supplier = []
                newFin.supplier.append(supplier_id)
                # newFin.supplier.first().supp_payment.append
                db.session.add(newFin)
                db.session.commit()
            else:
                newFin.supplier = []
                newFin.supplier.append(supplier_id)
                db.session.add(newFin)
                db.session.commit()
            db.session.commit()
            return jsonify({'success':'ок', 'req_id':  newFin.id})
    except exc.IntegrityError as e:
        return jsonify({'not':'в базе уже есть запись с таким ID', 'req_id':  newFin.id})
   
@supp.route('/prefin_change', methods=['POST', 'GET'])
def prefin_change():
    finance = Prefin.query.filter(Prefin.buyer==current_user.name).order_by(desc(Prefin.id)).all()
    finance_acc = Prefin.query.order_by(desc(Prefin.id)).all()
    finsales = Prefin.query.filter_by(sale=current_user.name).all()
    tn = Tn.query.all()
    return render_template('finance.html', finance=finance, form=formSupplier(), finsales=finsales, finance_acc=finance_acc)



#подгрузка счета подрядчика
@supp.route('/upload_invoice', methods=['POST', 'GET'])
def upload_invoice():
    if current_user.role=='buyer':
        target = os.path.join(APP_ROOT, 'invoice/')
        fin_id = request.args.get('find')
        print('ds' + str(session['fin_id']))
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            if file and allowed_file(file.filename):
                print(file)
                new_d = Invoicesup(fin_id=session['fin_id'])
                db.session.add(new_d)
                db.session.commit()
                filename=str('Счет поставщика') +' ' +  str(session['fin_id']) +' '  +  file.filename
                new_d.path=str(filename)
                db.session.commit()
                destination = "/".join([target, filename])
                print(destination)
                file.save(destination)
                return jsonify({'success':'файлы успешно сохранены'})
            else:
                return jsonify({'success':'файлы запрещен к загрузке'})
   

@supp.route('/download_s_inv_s/<path:filename>', methods=['GET'])
def download_s_inv_s(filename):
        return send_from_directory(os.path.join(APP_ROOT, 'invoice/'), filename, as_attachment=True)





@supp.route('/account', methods=['POST', 'GET'])
def account():
    finance = Prefin.query.all()
    return render_template('account.html', finance=finance)


#подгрузка счета для клиента
@supp.route('/upload_invoice_c', methods=['POST', 'GET'])
def upload_invoice_c():
        target = os.path.join(APP_ROOT, 'invoice_c/')
        fin_id = request.args.get('find')
        print('ds' + str(session['fin_id']))
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("file"):
            if file and allowed_file(file.filename):
                print(file)
                new_d = Invoicecust(fin_id=session['fin_id'])
                db.session.add(new_d)
                db.session.commit()
                filename=str('Счет ') +' ' +  str(session['fin_id']) +' '  +  file.filename
                new_d.path=str(filename)
                db.session.commit()

                destination = "/".join([target, filename])
                print(destination)
                file.save(destination)
                return jsonify({'success':'файлы успешно сохранены'})
            else:
                return jsonify({'success':'файлы запрещен к загрузке'})


#для подгрузки заявки продавцами
@supp.route('/zayavka_if_buyer', methods=['POST', 'GET'])
def zayavka_if_buyer():
    target = os.path.join(APP_ROOT, 'zayavka_if_buyer/')
    if not os.path.isdir(target):
         os.mkdir(target)
    if request.method == 'POST':
        f = request.files.get('file')
        f.filename = 'Заявка#' + str(session['id']) + ' ' + str(f.filename)
       
        
        t = Zayvka(req_id=session['id'], path = f.filename)
        db.session.add(t)
        req = Request.query.get(session['id'])
        print('eto req_id :' + str(req.id))
        t.req_id = req.id
        t.request_id = req.id
        db.session.commit()
        
        destination = "/".join([target, f.filename])
        print('eto dest: ' + str(destination))
        f.save(destination)
    return redirect (url_for('feedback', id=int(session['id'])))

@supp.route('/download_z_if_b/<path:filename>', methods=['GET'])
def download_z_if_b(filename):
        return send_from_directory(os.path.join(APP_ROOT, 'zayavka_if_buyer/'),
                                filename, as_attachment=True)







@supp.route('/upload_tn', methods=['POST', 'GET'])
def upload_tn():
    target = os.path.join(APP_ROOT, 'TN/')
    if not os.path.isdir(target):
         os.mkdir(target)
    if request.method == 'POST':
        f = request.files.get('file')
        f.filename = 'ТН#' + str(session['fin_id']) + ' ' + str(f.filename)
       
        
        t = Tn(prefin_id=session['fin_id'], path = f.filename)
        db.session.add(t)
        fin = Prefin.query.get(t.prefin_id)
        t.req_id = fin.req_id
        db.session.commit()
        print(session['fin_id'])
        destination = "/".join([target, f.filename])
        print('eto dest: ' + str(destination))
        f.save(destination)
    return redirect (url_for('supp.prefin_change_id_test', id=int(session['fin_id'])))

#маршрут для заугрзки доков от поставщика (документы, договора)
@supp.route('/upload_s_docs', methods=['POST', 'GET'])
def upload_s_docs():
    target = os.path.join(APP_ROOT, 's_docs/')
    if not os.path.isdir(target):
         os.mkdir(target)
    if request.method == 'POST':
        f = request.files.get('file')
        f.filename = 'документ#' + str(session['fin_id']) + ' ' + str(f.filename)
        docs = Documents(prefin_id=session['fin_id'], path = f.filename)
        db.session.add(docs)
        fin = Prefin.query.get(docs.prefin_id)
        docs.req_id = fin.req_id
        db.session.commit()
        print(session['fin_id'])
        destination = "/".join([target, f.filename])
        print('eto dest: ' + str(destination))
        f.save(destination)
    return redirect (url_for('supp.prefin_change_id_test', id=int(session['fin_id'])))


#маршрут для подгрузки счетов от поставщика
@supp.route('/upload_s_inv', methods=['POST', 'GET'])
def upload_s_inv():
    target = os.path.join(APP_ROOT, 's_invoice/')
    if not os.path.isdir(target):
         os.mkdir(target)
    if request.method == 'POST':

        f = request.files.get('file')
        f.filename = 'сч#' + str(session['fin_id']) + ' ' + str(f.filename)
        invs = Invoicesup(prefin_id=session['fin_id'], path = f.filename)
        db.session.add(invs)
        fin = Prefin.query.get(invs.prefin_id)
        invs.req_id = fin.req_id
        invs.supp_id = fin.supplier_id
        invs.fin_id = fin.id
        db.session.commit()
        invoice = Supp_payment.query.filter_by(fin_id=session['fin_id']).first()
        invoice.invoice_path.append(invs)
        db.session.commit()
        print(session['fin_id'])
        destination = "/".join([target, f.filename])
        print('eto dest: ' + str(destination))
        f.save(destination)
    return redirect (url_for('supp.prefin_change_id_test', id=int(session['fin_id'])))





@supp.route('/upload_с_invoice', methods=['POST', 'GET'])
def upload_с_invoice():
    target = os.path.join(APP_ROOT, 'c_inv/')
    if not os.path.isdir(target):
         os.mkdir(target)
    if request.method == 'POST':
        f = request.files.get('file')
        f.filename = 'документ#' + str(session['fin_id']) + ' ' + str(f.filename)
        invoice = Invoicecust(prefin_id=session['fin_id'], path = f.filename)
        db.session.add(invoice)
        fin = Prefin.query.get(invoice.prefin_id)
        invoice.req_id = fin.req_id
        db.session.commit()
        print(session['fin_id'])
        destination = "/".join([target, f.filename])
        print('eto dest: ' + str(destination))
        f.save(destination)
    return redirect (url_for('supp.prefin_change_id_test', id=int(session['fin_id'])))

@supp.route('/prefin_change_id_test/<int:id>', methods=['POST', 'GET'])
def prefin_change_id_test(id):
    form = formSupplier()
    form_n = UploadForm()
    formInvoice=FormInvoices()
    form.name.choices =[(g.id, g.llc_name) for g in Supplier.query.all()]
    print(form.name.choices)
   
    print(form)
    fin = Prefin.query.get(id)
    print(fin.c_inv_number)
    session['fin_id'] = fin.id
    print(session['fin_id'])

    fin_model = Prefin.query.get(session.get('fin_id'))
    fin_test = Prefin.query.get(105)
    
    #put all supplier name to list
    
    invoicec = Invoicecust.query.all()

    req = Request.query.filter_by(id=fin.req_id).first()
    cust = Customer.query.join(Request).filter(Request.id==req.id).first()
    
    
    docs = Documents.query.filter(Documents.req_id==req.id).all()
    invs = Invoicesup.query.filter(Invoicesup.req_id==req.id).all()
    tn = Documents.query.filter_by(req_id=req.id).all()
    ttn = Tn.query.filter(Tn.prefin_id==int(session['fin_id'])).all()
    zayavka = Zayvka.query.filter_by(req_id=req.id).all()

    print('pre fin' + str(req.id))

    print('session: ' + str(session['fin_id']))

    c_plan_day = req.customer.payment_day + 4


    
    
    print('forma: ' + str(form.s_invoice_number.data))

    
    user_me = User.query.filter(User.id==current_user.id).first()
    user_schema = UserSchema()
    print(user_schema.dump(user_me))
    p_chema = FinanceShema()
    x = Prefin.query.all()
    print (type(p_chema.dump(x[0])))
    invoiceCust = Invoicecust.query.filter(Invoicecust.prefin_id==session['fin_id']).all()
    print(invoiceCust)
    
    invCust_chema = InvoicecustShema(many=True)
    inv_dump = invCust_chema.dump(invoiceCust)
    print(inv_dump)
    
   

    return render_template('finance_change_test.html',
    inv_dump=inv_dump, u=user_schema.dump(user_me), f=p_chema.dump(x[1]),\
        formInvoice=formInvoice, supp=supp, fin=fin, form=form, req=req, tn=tn, docs=docs, form_n=form_n, ttn=ttn, zayavka=zayavka, invs=invs )


@supp.route('/download_file_s_tn/<path:filename>', methods=['GET'])
def download_file_s_tn(filename):
        return send_from_directory(os.path.join(APP_ROOT, 'TN/'),
                                filename, as_attachment=True)

@supp.route('/download_s_docs/<path:filename>', methods=['GET'])
def download_s_docs(filename):
        return send_from_directory(os.path.join(APP_ROOT, 's_docs/'),
                                filename, as_attachment=True)

@supp.route('/download_s_inv/<path:filename>', methods=['GET'])
def download_s_inv(filename):
        return send_from_directory(os.path.join(APP_ROOT, 's_invoice/'),
                                filename, as_attachment=True)


@supp.route('/download_c_inv/<path:filename>', methods=['GET'])
def download_c_inv(filename):
        return send_from_directory(os.path.join(APP_ROOT, 'c_inv/'),
                                filename, as_attachment=True)

#для выставлении счетов бухгалтерией
@supp.route('/need_inv', methods=['POST', 'GET'])
def need_inv():
    finance = Prefin.query.filter(Prefin.buyer==current_user.name).order_by(desc(Prefin.id)).all()
    finance_acc = Prefin.query.order_by(desc(Prefin.id)).all()   
    finsales = Prefin.query.filter_by(sale=current_user.name).all()
    tn = Tn.query.all()
    return render_template('need_inv.html', finance=finance, form=formSupplier(), finsales=finsales, finance_acc=finance_acc, tn=tn)

#для отправки счетов клиентам
@supp.route('/send_invc', methods=['POST', 'GET'])
def send_invc():
    finance = Prefin.query.filter(Prefin.buyer==current_user.name).order_by(desc(Prefin.id)).all()
    finance_acc = Prefin.query.order_by(desc(Prefin.id)).all()   
    finsales = Prefin.query.filter_by(sale=current_user.name).all()
    tn = Tn.query.all()
    return render_template('send_invc.html', finance=finance, form=formSupplier(), finsales=finsales, finance_acc=finance_acc, tn=tn)

import matplotlib.pyplot as plt
import pandas as pd


@supp.route('/suppliers', methods=['POST', 'GET'])
def suppliers():
    formName=formSupplierName()
    formINN = formSupplierInn()
    formInv = formSupplierInv()
    formTransit = FormTransit()
    formName.name.choices = [(g.llc_name, g.llc_name) for g in Supplier.query.all()]
    if formName.validate_on_submit():
        name =  formName.name.data
        supp = Supplier.query.filter_by(llc_name=name).first()
        session['gid'] = supp.id
        print('this is gid: ' + str(session.get('gid')))
    else:
        print('nnnn')

    formInv.our_company.choices = [(g.name, g.name) for g in Companies.query.all()]

    

    
   
    
    


    print('eto form' + str(formName.name.data))
    print('eto form INN' + str(formINN.check_inn.data))
   

    
    name = formName.name.data
    print('eto: ' + str(name))
    

    
    #### Доделать
    
    
    all = Supplier.query.all()
    
    formINN.check_inn.choices=[(g.inn, g.inn) for g in all]
    formTransit.name_tr.choices = [(g.name, g.name) for g in Transit.query.all() ]
    formInv.our_company.choices = [(g.inn, g.inn) for g in Companies.query.all()]
    
    

    supp=Supplier.query.get(1)
    supp = Supplier.query.filter(or_(Supplier.llc_name==formName.name.data, Supplier.inn==formINN.check_inn.data)).first()
    print('eto supp : ' + str(supp))
      #все счета
    
    try:
        invoices = Supp_payment.query.filter(Supp_payment.supplier_id==supp.id).order_by(Supp_payment.s_invoice_date.desc()).all()
       
    #все оплаты по счетам 
        invoice_payments = Invoice_payment_s.query.filter(Invoice_payment_s.supplier_id==supp.id).order_by(Invoice_payment_s.date_payment.desc()).all()
    except AttributeError:
        invoices = Supp_payment.query.order_by(Supp_payment.s_invoice_date).all()
        invoice_payments = Invoice_payment_s.query.order_by(Invoice_payment_s.date_payment).all()

    if request.method=='POST':
        try:
            formInv.supp_all_invoices.choices = [(g.id, g.s_inv_number) for g in Supp_payment.query.filter_by(supplier_id=supp.id).all()]
            formTransit.name_tr.choices = [(g.name, g.name) for g in Transit.query.all() ]
            session['supp_name'] = supp.llc_name
            formName.name.data = session['supp_name']
            number = request.args.get('supp_payment_id')
            print('number' + formInv.supp_all_invoices.data)
            print('data ' + formInv.choices.data)
            
            return render_template('suppliers.html', suppliers=suppliers, formName=formName, formINN=formINN,
            all=all, supplier=supplier, supp=supp, formInv=formInv, invoices=invoices, invoice_payments=invoice_payments,\
                formTransit=formTransit, day=datetime.datetime.today())
        
        except AttributeError:
            print('ttt' + str(formName.name.data))
            formInv.supp_all_invoices.choices = [(g.s_inv_number, g.s_inv_number) for g in Supp_payment.query.filter_by(supplier_id=session.get('gid')).all()]
    print('eto supp' + str(supp))

    return render_template('suppliers.html', formName=formName, formINN=formINN,
            all=all,  formInv=formInv, day=datetime.datetime.today(), supp=supp, formTransit=formTransit) 

#json to save paymentto suppliers
@supp.route('suppliers_payments_to_db', methods=['POST', 'GET'])
def suppliers_payments_to_db():
    form=formSupplierInv()
   
    summ_amount = request.args.get('summ_amount')
    supp_payment_id = request.args.get('supp_payment_id')
    print('eto supp_p_id: ' + str(supp_payment_id))
    transit_name = request.args.get('transit')
    print(transit_name)
    transit_model = Transit.query.filter_by(name=transit_name).first()
    print(transit_model)
   
    commision = request.args.get("commision")
    day = request.args.get('day')
    supplier_id = request.args.get('supplier')
    supp = Supplier.query.get(supplier_id)
    print('eto supplier: ' + str(supp))
    try:
        cost =int(summ_amount)/ (100-float(commision))
    except ValueError:
        print('no')

    
    supp_payment_s = Supp_payment.query.filter(Supp_payment.s_inv_number==supp_payment_id).first()
    print(supp_payment_s)
    

    print('day' + str(day))
    print('eto cost: '+str(cost))
    
    print(summ_amount)
    
    # su = Supp_payment.query.get(int(supp_payment_id))
    # print('eto supp_payment: ' + str(su))
    if supp_payment_id and transit_name !=None and day:
        if summ_amount !=0 or summ_amount !=None:
            
            new_payment = Invoice_payment_s(summ_pay=summ_amount, \
                supp_payment=supp_payment_s.id, \
                    date_payment=day, \
                        s_inv_number=int(supp_payment_id), 
                        supplier_id=int(supplier_id),\
                        )
            db.session.add(new_payment)
            
            new_payment.cost_for_us=cost
            
            
            supp.invoice_payment.append(new_payment)
            db.session.commit()

            supp_payment_s.invoice_payment.append(new_payment)
            db.session.commit()
            tr_db_p = Tr_payments(sum=new_payment.summ_pay, transit_id = transit_model.id, payment_id=new_payment.id, status='в процессе', transit_date_send=day )
            db.session.add(tr_db_p)
            db.session.commit()
            new_payment.tr_payment.append(tr_db_p)
            db.session.commit()
        
        
            return jsonify({'success': 'оплата зафиксирована'})

        else:
            return jsonify({'error': 'неудачно, проверьте все ли поля заполенны для разнесения оплаты'})


    
    else:
        
        return jsonify({'error': 'неудачно, проверьте все ли поля заполенны для разнесения оплаты'})




#using fetch API for suppliers route above
@supp.route('s_inv_number/<number>')
def s_inv_number(number):
    invoices = Supp_payment.query.filter_by(s_inv_number=number).all()
    
    invoicesArray = []

    for inv in invoices:
        invObj = {}
        invObj['id']=inv.id
        invObj['s_inv_number']=inv.s_inv_number
        invObj['s_inv_amount'] =inv.s_inv_amount
        invoicesArray.append(invObj)
   
    return jsonify({'invoices':invoicesArray})


@supp.route('all_suppliers', methods=['GET', 'POST'])
def all_suppliers():
    formName=formSupplierName()
    formINN = formSupplierInn()
    supps = Supplier.query.all()
    all = Supplier.query.all()
    formName.name.choices = [(g.llc_name, g.llc_name) for g in all]
    formINN.check_inn.choices=[(g.inn, g.inn) for g in all]

    return render_template('all_suppliers.html', supps=supps, formINN=formINN, formName=formName)


#удаление записи об оплате
@supp.route('/remove_payment/<int:id>', methods=['POST', 'GET'])
def remove_payment(id):
    id = request.args.get('id')
    if request.method=='GET':
        print('eto:' + str(id))
        payment = Invoice_payment_s.query.get(id)
        tr = Tr_payments.query.filter_by(payment_id=payment.id).first()
        
        
        if payment:
            db.session.delete(payment)
            db.session.delete(tr)
            
            db.session.commit()
            return jsonify({'success_remove': 'Запись удалена'})
        

#добавление транзита
@supp.route('/add_third_party', methods=['POST', 'GET'])
def add_third_party():
    
    inn = request.args.get('inn')
    print(inn)
    transit = Transit.query.filter_by(inn=inn).first()
   
    if transit:
        return jsonify({'error':'Данный агент уже есть в базе'})
    else:
        transit = Transit(inn=inn)
        db.session.add(transit)
        db.session.commit()
        return jsonify({'success':'Контрагент внесен'})

@supp.route('/s_payment_calendar', methods=['POST', 'GET'])
def s_payment_calendar():
    today = datetime.datetime.today()
    delta = timedelta(days=1)
    y = today - delta
    print(y)
   
    return render_template('s_payment_calendar.html', date=today)


@supp.route('/data')
def return_data():
    
   

    invoices = Supp_payment.query.all()
    
    invoicesArray = []

    for inv in invoices:
        invObj = {}
        invObj['id']=inv.id
        supplier = Supplier.query.get(inv.supplier_id)
        invObj['start']=inv.day_plan_pay.strftime("%Y-%m-%d")
        invObj['title'] = ( supplier.llc_name + ' ' + '[' + str(inv.s_inv_amount) + ']')
        invObj['s_inv_number']=inv.s_inv_number
        invObj['s_inv_amount'] =inv.s_inv_amount
        invoicesArray.append(invObj)
   
    return jsonify(invoicesArray)


@supp.route('/3rd_party_payments', methods=['POST', 'GET'])
def third_party_payments():
    all = Tr_payments.query.order_by(desc(Tr_payments.transit_date_send)).all()
    form=FormTransit() 
    form.status_tr.choices= [(i.id, i.status) for i in Tr_status.query.all()]
    print(form.status_tr.choices)
    form.process()
    return render_template('3rd_party.html',  form=form, all=all )
    
    

@supp.route('/3rd_party_payments_status', methods=['POST', 'GET'])
def third_party_payments_status():

    id = request.args.get('id')
    
    print('eto id: ' + str(id))
    
    
    status = request.args.get('status')
    print(status)
    transit = Tr_payments.query.get(id)
    transit.status=status
    db.session.commit()
    return jsonify({'success':'done'})


@supp.route('/upload_payment_doc_tr', methods=['POST', 'GET'])
def upload_payment_doc_tr():
    
    tr_payment = Tr_payments.query.get(session['tr_id_p'])
    target = os.path.join(APP_ROOT, 'payments_docs_tr/')
    if not os.path.isdir(target):
         os.mkdir(target)
    if request.method == 'POST':
        
        f = request.files.get('file')
        #подумать
        f.filename = 'платежка#' + str(tr_payment.id) + str(f.filename)
        print('this is tr : ' + str(tr_payment))
        destination = "/".join([target, f.filename])
        tr_payment.doc_path = f.filename
        tr_payment.transit_date_recieved=datetime.datetime.now()
        tr_payment.status = 'успешно'

        db.session.commit()

        
        print('eto dest: ' + str(destination))
        f.save(destination)


    return redirect (url_for('supp.third_party_payments'))

@supp.route('/get_tr_id', methods=['POST', 'GET'])
def get_tr_id():
    p_date = request.args.get('p_date')
    tr_id_p  = request.args.get('id')
    print('id is : ' + str(tr_id_p))
    session['tr_id_p'] = tr_id_p
    session['tr_p_date'] = p_date
    print(session['tr_id_p'])
    return jsonify({'id':session['tr_id_p'], 'p_date':session['tr_p_date'] })

@supp.route('/download_tr_doc_pay/<path:filename>', methods=['GET'])
def download_tr_doc_pay(filename):
    return send_from_directory(os.path.join(APP_ROOT, 'payments_docs_tr/'),
                                filename, as_attachment=True)


@supp.route('/tr_save_date', methods=['POST', 'GET'])
def tr_dave_date():
    id = request.args.get('id')
    st_date = request.args.get('p_date')
    t_date = datetime.datetime.strptime(st_date, "%Y-%m-%d").date()
    print(t_date)
    tr_payment = Tr_payments.query.get(id)
    tr_payment.transit_date_send = t_date
    print(type(tr_payment.transit_date_send))
    db.session.commit()
    return jsonify({'id':id, 'date_send':t_date})

@supp.route('/test')
def test():
    form = formSupplier()

    r = Tr_payments.query.all()
    return render_template('test.html', r=r, form=form)

@supp.route('/confirm_transit', methods=['POST', 'GET'])
def confirm_transit():
   
    id = request.args.get('node')
    sum = request.args.get('sum')
    tr = Tr_payments.query.get(id)
    if tr.confirm != 1:
        tr.sum = sum
        tr.payment.summ_pay=sum
        tr.confirm=1
        db.session.commit()

    return jsonify({'list_id':id, 'sum':sum})


#record ro db supp invoice amount in change_test_id route
@supp.route('/lets', methods=["POST", "GET"])
def lets():
    fin_id = request.args.get('id')
    print('this is id: ' + str(id))
    supp_id = request.args.get('supp_id')
    
    invoice_number = request.args.get('invoice_number')
    summ_invoice = request.args.get('summ_invoice')
    date_inv = request.args.get('date_inv')
    date_inv_pay = request.args.get('date_inv_pay')
    inv_currency = request.args.get('inv_currency')

    date_inv = datetime.datetime.strptime(date_inv, "%Y-%m-%d")
    date_inv_pay = datetime.datetime.strptime(date_inv_pay, "%Y-%m-%d")
   
    fin = Prefin.query.get(fin_id)
    supp = Supplier.query.get(supp_id)

    invoice = Supp_payment(s_inv_number=invoice_number,
                          s_invoice_date = date_inv,
                        s_inv_amount = summ_invoice, 
                        s_inv_currency = inv_currency,
                        s_inv_pay_day = date_inv_pay,
                        supplier_id = supp_id,
                        fin_id = fin.id)
    db.session.add(invoice)
    db.session.commit()
    supp.supp_payment.append(invoice)
    db.session.commit()
    


    return jsonify({'supp_id':supp_id, 
                    'fin_id':fin_id, 'invoice_number':invoice_number,
                     'date_inv':date_inv, 'date_inv_pay':date_inv_pay,
                     'summ_invoice':summ_invoice })

import json

#change supp in fin
@supp.route('/change_supp_fin', methods=["POST", "GET"])
def change_supp_fin():


    fin_id = request.args.get('id')
    print('assads' + str(fin_id))

    #search current supplier



 
    supp_id = request.args.get('supp_id')

    fin = Prefin.query.get(fin_id)


    
    new_supp = Supplier.query.get(supp_id)

    invoice_number = request.args.get('invoice_number')
    summ_invoice = request.args.get('summ_invoice')
    date_inv = request.args.get('date_inv')
    date_inv_pay = request.args.get('date_inv_pay')
    inv_currency = request.args.get('inv_currency')

    x = request.args.get('x')
    
    
    

    supp = Supplier.query.get(supp_id)
    
   

    # if fin.supplier:
    #     if fin in supp.prefin:
    #         supp.prefin.remove(fin)
    return jsonify({'supp_id':supp_id, 'fin':fin_id, 'x':x})


@supp.route('/add_supp_to_fin', methods=['POST', 'GET'])
def add_supp_to_fin():
    fin_id = request.args.get('fin_id')
    supp_id = request.args.get('supp_id')
    s_inv_number = request.args.get("s_inv_number")
    s_inv_amount = request.args.get("s_inv_amount")
    s_inv_date=request.args.get("s_inv_date")
    s_inv_deadline=request.args.get("s_inv_deadline")
    vat = request.args.get("vat")
    currency = request.args.get("currency")

    if s_inv_amount == 0:
        s_inv_amount == None

    
    try:
        s_inv_date = datetime.datetime.strptime(s_inv_date, '%Y-%m-%d')
    except ValueError:    
        s_inv_date=None
    try:
        s_inv_deadline = datetime.datetime.strptime(s_inv_deadline, '%Y-%m-%d')
    except ValueError:
        s_inv_deadline=None
        
    

    fin = Prefin.query.get(fin_id)
    supp = Supplier.query.get(supp_id)

    
    
    if  supp not in fin.supplier:
        fin.supplier.append(supp)
     
        new_inv = Supp_payment(s_inv_number=s_inv_number, s_inv_amount=s_inv_amount,\
                    s_invoice_date=s_inv_date, s_inv_currency=currency,\
                    s_inv_pay_day=s_inv_deadline, vat=vat, supp_payment=supp, fin_id=fin_id)
     
       
        db.session.add(new_inv)
        

        db.session.commit()


        return jsonify({'fin_id':fin_id, 'success':'поставщик был добавлен в работу'})
    else:
        return jsonify({ 'error':'неудачно, поставщик уже есть в работе'})

#доделать
@supp.route('/dell_supp_from_fin', methods=['POST', 'GET'])
def dell_supp_from_fin():
    supp_id = request.args.get('supp_id')
    supp = Supplier.query.get(supp_id)

    fin_id = request.args.get('fin_id')
    fin = Prefin.query.get(fin_id)

    invList=[i for i in supp.supp_payment if i.fin_id==fin.id]

    if len(invList)<1:

        fin.supplier.remove(supp)
        db.session.commit()
        return jsonify({'success':'поставщик удален'})
    else:
        return jsonify({'error':'у поставщика еще остались счета, удалите сначало их'})

    return jsonify({'supp': supp.llc_name})

@supp.route('/add_inv_to_supp', methods=['GET', 'POST'])
def add_inv_to_supp():
    supp_id = request.args.get('supp_id')
    supp = Supplier.query.get(supp_id)
    fin_id = request.args.get('fin_id')
    fin = Prefin.query.get(fin_id)
    invoice_id = request.args.get('invoice_id')
    s_inv_number = request.args.get('s_inv_number')
    s_inv_amount = request.args.get('s_inv_amount')
    s_inv_date = request.args.get('s_inv_date')
    s_inv_deadline = request.args.get('s_inv_deadline')
    vat = request.args.get('vat')
    currency = request.args.get('currency')
    print(invoice_id)

    current_inv = Supp_payment.query.get(invoice_id)
    print(current_inv)

    print(s_inv_date)

    if current_inv:
        current_inv.supplier_id = supp_id
        current_inv.fin_id=fin_id
        current_inv.s_inv_number=s_inv_number
        current_inv.s_inv_amount=s_inv_amount
        current_inv.s_invoice_date=s_inv_date or None
        current_inv.s_inv_pay_day=s_inv_deadline or None
        current_inv.s_inv_currency=currency
        current_inv.vat=vat

    
        
        db.session.commit()





    return jsonify({'inv_id':invoice_id, "fin_id": fin_id, 'sup_id': supp_id, 's_inv_number': s_inv_number,
    "s_inv_amount": s_inv_amount, "s_inv_date": s_inv_date, "s_inv_deadline": s_inv_deadline,
    "vat": vat, "currency": currency})


@supp.route('/del_inv_from_supp', methods=['GET', 'POST'])
def del_inv_from_supp():
    supp_id = request.args.get('supp_id')
    supp = Supplier.query.get(supp_id)
    fin_id = request.args.get('fin_id')
    fin = Prefin.query.get(fin_id)
    invoice_id = request.args.get('invoice_id')
    s_inv_number = request.args.get('s_inv_number')
    s_inv_amount = request.args.get('s_inv_amount')
    s_inv_date = request.args.get('s_inv_date')
    s_inv_deadline = request.args.get('s_inv_deadline')
    vat = request.args.get('vat')
    currency = request.args.get('currency')
    print(invoice_id)

    current_inv = Supp_payment.query.get(invoice_id)
    print(current_inv)

    print(s_inv_date)
    suppInvList=[i for i in fin.supp_payments if i.supplier_id==supp_id]
    print(suppInvList)
    print(len(suppInvList))

    if current_inv:
        db.session.delete(current_inv)        
        db.session.commit()
        return jsonify({'success': 'счет успешно был удален'})
   
                






    return jsonify({'inv_id':invoice_id, "fin_id": fin_id, 'sup_id': supp_id, 's_inv_number': s_inv_number,
    "s_inv_amount": s_inv_amount, "s_inv_date": s_inv_date, "s_inv_deadline": s_inv_deadline,
    "vat": vat, "currency": currency})


@supp.route('/add_inv_from_form', methods=['GET', 'POST'])
def add_inv_from_form():
    supp_id = request.args.get('supp_id')
    supp = Supplier.query.get(supp_id)
    fin_id = request.args.get('fin_id')
    fin = Prefin.query.get(fin_id)
   
    s_inv_number = request.args.get('s_inv_number')
    s_inv_amount = request.args.get('s_inv_amount')
    s_inv_date = request.args.get('s_inv_date')
    s_inv_deadline = request.args.get('s_inv_deadline')
    vat = request.args.get('vat')
    currency = request.args.get('currency')
    

    newInv=Supp_payment(
            supplier_id = supp_id,\
            fin_id=fin_id,\
            s_inv_number=s_inv_number,\
            s_inv_amount=s_inv_amount,\
            s_invoice_date=s_inv_date or None,\
            s_inv_pay_day=s_inv_deadline or None,\
            s_inv_currency=currency,\
            vat=vat
                )
    
    db.session.add(newInv)
    db.session.commit()





    return jsonify({"fin_id": fin_id, 'sup_id': supp_id, 's_inv_number': s_inv_number,
    "s_inv_amount": s_inv_amount, "s_inv_date": s_inv_date, "s_inv_deadline": s_inv_deadline,
    "vat": vat, "currency": currency})


@supp.route('/testVue', methods=['POST', 'GET'])
def testVue():
    count = request.args.get('count')
    description = request.args.get('description')
    quantity = request.args.get('quantity')
    unit=request.args.get('unit')
    amount = request.args.get('amount')
    price = request.args.get('price')
    total = request.args.get('total')
    total_w_vat = request.args.get('tt')
    vat = request.args.get('vat') 




    print(count, description, quantity, unit, amount, price, tt,  total, vat)
    return jsonify({'descripton':description})




    
    