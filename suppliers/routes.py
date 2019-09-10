from flask import render_template, request, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g
from suppliers import supp
from .models import Supplier, Prefin, Documents, Tn, Supp_payment 
from app_main.models import *
from app_main import db, app
from .forms import *
from sqlalchemy import exc
from sqlalchemy import desc, or_, and_

import datetime





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
            request_one.complete_fin=1
            if request_one.zayvka.first():
                newFin.zayvka.append(request_one.zayvka.first())
                db.session.add(newFin)
                newFin.supplier.append(supplier_id)
                db.session.commit()
                
                return jsonify({'success':'данные успешно внесены в базу'})
            else:
                db.session.add(newFin)
                db.session.commit()
                newFin.supplier.append(supplier_id)
                return jsonify({'success':'данные успешно внесены в базу но без заявки'})
                
           
        else:
            print('customer:' + customer)
            newFin=Prefin.query.filter_by(req_id=req_id).first()
            newFin.tora_red = tora_red,
            newFin.req_id=req_id,
            newFin.customer_order_date=customer_order_date,
            newFin.direction=direction, 
            newFin.sale=sale,
            newFin.buyer = buyer,
            newFin.customer_name=customer,
            newFin.cargo_character = request_one.cargo_desciption,

            newFin.supplier_name=supplier_id.llc_name,
            newFinloading_place=loading_place,
            newFin.unloading_place=unloading_place,
            newFin.status_of_request=status_of_request,
            newFin.s_invoice_number=s_invoice_number,
            newFin.s_inv_amount=s_inv_amount,
            newFin.s_inv_vat = s_inv_vat,
            newFin.c_inv_amount=int(c_inv_amount),
            newFin.supplier_id = supplier_id.id,
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
                db.session.add(newFin)
                db.session.commit()
            db.session.commit()
            return jsonify({'success':'ок'})
    except exc.IntegrityError as e:
        return jsonify({'not':'в базе уже есть запись с таким ID'})
   
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
    # 
    
    print(form)
    fin = Prefin.query.get(id)
    print(fin.c_inv_number)
    session['fin_id'] = fin.id
    print(session['fin_id'])
    invoices = Invoicesup.query.filter(Invoicesup.fin_id==fin.id).all()
    invoicec = Invoicecust.query.all()

    req = Request.query.filter_by(id=fin.req_id).first()
    
    docs = Documents.query.filter(Documents.req_id==req.id).all()
    invs = Invoicesup.query.filter(Invoicesup.req_id==req.id).all()
    tn = Documents.query.filter_by(req_id=req.id).all()
    ttn = Tn.query.filter(Tn.prefin_id==int(session['fin_id'])).all()
    zayavka = Zayvka.query.filter_by(req_id=req.id).all()

    print('pre fin' + str(req.id))

    print('session: ' + str(session['fin_id']))

    c_plan_day = req.customer.payment_day
    
    
    print('forma: ' + str(form.s_invoice_number.data))
   
   
    ####Доделать
   
    

    
       
    
    
    if request.method=='POST':
        print('eto'+ str(fin.s_invoice_number))
        

        fin.s_invoice_number =form.s_invoice_number.data 
        
        
        fin.s_inv_date = form.s_inv_date.data
        fin.s_inv_date_to_pay = form.s_inv_das_inv_date_to_pay.data
        fin.c_inv_number=form.c_inv_number.data
        fin.c_invoice_date=form.c_invoice_date.data
        
        if fin.c_invoice_date:
            fin.c_inv_plan_pay = fin.c_invoice_date + datetime.timedelta(days=c_plan_day)
        else:
            fin.c_inv_plan_pay=form.c_inv_plan_pay.data

        print(fin.s_invoice_number)
        db.session.commit()
   

    supp_p = Supp_payment.query.filter(and_(Supp_payment.supplier_id==fin.supplier_id, 
                                            Supp_payment.fin_id==fin.id)).first()

    if supp_p:
        supp_p.s_inv_number=fin.s_invoice_number,
        supp_p.s_invoice_date=fin.s_inv_date,
        supp_p.s_inv_amount=fin.s_inv_amount,
        supp_p.day_plan_pay = fin.s_inv_date_to_pay,
        supp_p.fin_id = fin.id,
        supp_p.tora_red = fin.tora_red,
        db.session.commit()
    else:
        supp_p = Supp_payment(
                                    s_invoice_date=fin.s_inv_date,
                                    s_inv_amount=fin.s_inv_amount,
                                    day_plan_pay = form.s_inv_das_inv_date_to_pay.data,
                                    fin_id = fin.id,
        
       


                                    s_inv_pay_day=form.s_inv_das_inv_date_to_pay.data,
                                    supplier_id=fin.supplier_id,
                                    
                                    )
   
        db.session.add(supp_p)                            
        db.session.commit()

    
    return render_template('finance_change_test.html', supp_p=supp_p, fin=fin, form=form, invoices=invoices, req=req, invoicec=invoicec, tn=tn, docs=docs, form_n=form_n, ttn=ttn, zayavka=zayavka, invs=invs )


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
    


    print('eto form' + str(formName.name.data))
    print('eto form INN' + str(formINN.check_inn.data))
   

    
    name = formName.name.data
    print('eto: ' + str(name))
    

    suppliers = db.session.query(Prefin.supplier_name, Prefin.sale, db.func.sum(Prefin.s_inv_amount)).group_by(Prefin.supplier_name, Prefin.sale).all()

   
    
    supplier = db.session.query(Prefin.supplier_name, Prefin.sale, db.func.sum(Prefin.s_inv_amount)).group_by(Prefin.supplier_name, Prefin.sale).\
        filter_by(supplier_name=formName.name.data).all()
    
    #### Доделать
    
    
    all = Supplier.query.all()
    formName.name.choices = [(g.llc_name, g.llc_name) for g in all]
    formINN.check_inn.choices=[(g.inn, g.inn) for g in all]

    
    


    supp = Supplier.query.filter(or_(Supplier.llc_name==formName.name.data, Supplier.inn==formINN.check_inn.data)).first()
    
      #все счета
    try:
        invoices = Supp_payment.query.filter(Supp_payment.supplier_id==supp.id).order_by(Supp_payment.s_invoice_date.desc()).all()
       
    #все оплаты по счетам 
        invoice_payments = Invoice_payment_s.query.filter(Invoice_payment_s.supplier_id==supp.id).order_by(Invoice_payment_s.date_payment.desc()).all()
    except AttributeError:


        invoices = Supp_payment.query.order_by(Supp_payment.s_invoice_date).all()

        invoice_payments = Invoice_payment_s.query.order_by(Invoice_payment_s.date_payment).all()
    

    if supp:
        try:
            formInv.supp_all_invoices.choices = [(g.id, g.s_inv_number) for g in Supp_payment.query.filter_by(supplier_id=supp.id).all()]
            session['supp_name'] = supp.llc_name
            formName.name.data = session['supp_name']
            number = request.args.get('supp_payment_id')
            print('number' + formInv.supp_all_invoices.data)
           

           

        except AttributeError:
            formInv.supp_all_invoices.choices = [(g.s_inv_number, g.s_inv_number) for g in Supp_payment.query.all()]
    print('eto supp' + str(supp))

    return render_template('suppliers.html', suppliers=suppliers, formName=formName, formINN=formINN,
            all=all, supplier=supplier, supp=supp, formInv=formInv, invoices=invoices, invoice_payments=invoice_payments,\
                formTransit=formTransit) 

#json to save paymentto suppliers
@supp.route('suppliers_payments_to_db', methods=['POST', 'GET'])
def suppliers_payments_to_db():
    form=formSupplierInv()
    summ_amount = request.args.get('summ_amount')
    supp_payment_id = request.args.get('supp_payment_id')
    transit = request.args.get('transit')

    

    commision = float(request.args.get("commision"))
    day = request.args.get('day')
    supplier_id = request.args.get('supplier')
    supp = Supplier.query.get(int(supplier_id))
    cost =int(summ_amount)/ (100-commision)

    print('day' + str(day))
    print('eto cost: '+str(cost))
    
    
    

    print(summ_amount)
    
    su = Supp_payment.query.get(int(supp_payment_id))
    if su and summ_amount and transit and day:
        invoice_number = su.s_inv_number
        new_payment = Invoice_payment_s(summ_pay=summ_amount, \
            supp_payment=supp_payment_id, \
                transit=transit, date_payment=day, \
                    s_inv_number=invoice_number, supplier_id=int(supplier_id),\
                        commision=commision)
        db.session.add(new_payment)
        new_payment.cost_for_us=cost
        
        
        supp.invoice_payment.append(new_payment)
        
        db.session.commit()

        
        return jsonify({'success': 'оплата зафиксирована'})
    
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
        if payment:
            db.session.delete(payment)
            db.session.commit()
            return jsonify({'success_remove': 'Запись удалена'})
        

#добавление транзита
@supp.route('/add_third_party', methods=['POST', 'GET'])
def add_third_party():
    form=FormTransit()
    new = request.form['inn']
    print(new)
    if request.method=='POST':
        print('inn :' + str(new))
        return jsonify({'inn':new})