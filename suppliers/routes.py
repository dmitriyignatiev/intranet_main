from flask import render_template, request, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g
from suppliers import supp
from .models import Supplier, Prefin, Documents
from app_main.models import *
from app_main import db, app
from .forms import *
from sqlalchemy import exc
from sqlalchemy import desc



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
    
    if form.validate_on_submit():
        choose_supp = form.name.data
        name = choose_supp.llc_name
    return render_template('add_supplier.html', form=form, req=req, date=date, docs=docs, fin=fin, z_doc=z_doc)

@supp.route('/add_supplier_to_db', methods=['POST', 'GET'])
def add_supplier_to_db():

    form=formSupplier()
    name = request.args.get('name')
    print(name)
    new_supp = Supplier.query.filter_by(llc_name=name).first()
    if new_supp:
         return jsonify({'error': 'поставщик уже есть в базе данных'})
    
    elif not new_supp:
        new_supp = Supplier(llc_name=name)
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
    customer_order_date=datetime.strptime(date_request, '%Y-%m-%d')
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
            db.session.add(newFin)
            db.session.commit()
            return jsonify({'success':'данные успешно внесены в базу'})
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
            db.session.commit()
            return jsonify({'success':'ок'})
    except exc.IntegrityError as e:
        return jsonify({'not':'в базе уже есть запись с таким ID'})
   
@supp.route('/prefin_change', methods=['POST', 'GET'])
def prefin_change():
    finance = Prefin.query.filter(Prefin.buyer==current_user.name).order_by(desc(Prefin.id)).all()
    finsales = Prefin.query.filter_by(sale=current_user.name).all()
    return render_template('finance.html', finance=finance, form=formSupplier(), finsales=finsales)

@supp.route('/prefin_change_id/<int:id>', methods=['POST', 'GET'])
def prefin_change_id(id):
    form = formSupplier()
    print(form)
    fin = Prefin.query.get(id)
    session['fin_id'] = fin.id
    invoices = Invoicesup.query.filter(Invoicesup.fin_id==fin.id).all()
    invoicec = Invoicecust.query.filter(Invoicecust.fin_id==fin.id).all()

    req = Request.query.filter_by(id=fin.req_id).first()
    tn = Documents.query.filter_by(req_id=req.id).all()
    print('pre fin' + str(req.id))

    print('session: ' + str(session['fin_id']))

    if request.method=='POST':
        fin.s_invoice_number =form.s_invoice_number.data
        fin.s_inv_date = form.s_inv_date.data
        fin.s_inv_date_to_pay = form.s_inv_das_inv_date_to_pay.data
        print(fin.s_invoice_number)
        db.session.commit()
        return redirect(request.url)
    return render_template('finance_change.html', fin=fin, form=form, invoices=invoices, req=req, invoicec=invoicec, tn=tn)

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
   

@supp.route('/download_s_inv/<path:filename>', methods=['GET'])
def download_file_s_inv(filename):
        return send_from_directory(os.path.join(APP_ROOT, 'invoice/'),
                                filename, as_attachment=True)

@supp.route('/download_c_inv/<path:filename>', methods=['GET'])
def download_file_c_inv(filename):
    return send_from_directory(os.path.join(APP_ROOT, 'invoice_c/'),
                                filename, as_attachment=True)
        



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












