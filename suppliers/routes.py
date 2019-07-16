from flask import render_template, request, \
    jsonify, redirect, flash, \
        send_from_directory, url_for, send_file, session, make_response, g
from suppliers import supp
from .models import Supplier, preFin, Documents
from app_main.models import *
from app_main import db, app
from .forms import *
from sqlalchemy import exc



@supp.route('/index')
def index():
    return render_template('app_main.base.html')

@supp.route('/add_supplier/<int:id>', methods=['GET', 'POST'])
def add_supplier(id):
    
    req = Request.query.get(id)
    session['id']=req.id
    fin = preFin.query.filter(preFin.req_id==session['id']).first()
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
  
    tora_red = request.args.get('name')
    req_id = request.args.get('id')
    date_request = request.args.get('date')
    customer_order_date=datetime.strptime(date_request, '%Y-%m-%d')
    supplier_name=request.args.get('supp')
    status_of_request = request.args.get('st')
    s_invoice_number = request.args.get('invoice_number')
    s_inv_amount = request.args.get('sinv_amount')
    s_inv_vat = request.args.get('sinv_vat')
    c_inv_amount=request.args.get('cinv_amount')
    supplier_id = Supplier.query.filter(Supplier.llc_name==supplier_name).first()
    pick_up_date = request.args.get('pick_up_date')
    unloading_date = request.args.get('unloading_date')
    print('eto supp_id: ' + str(pick_up_date))
    
    request_one=Request.query.get(req_id)
    direction = request_one.direction
    sale = request_one.user.name
    customer = request_one.customer.name
    s_inv_vat = s_inv_vat
    print('eto' +str(s_inv_vat))

    try:
        if not preFin.query.filter_by(req_id=req_id).first():
            print(tora_red + str(req_id) + ' ' + str(date_request)+''+str(supplier_name) + ''+ str(direction) + str(status_of_request))
            newFin = preFin(tora_red=tora_red, req_id=req_id, 
                        customer_order_date=customer_order_date,
                        direction=direction, sale=sale,
                        status_of_request=status_of_request,
                        s_invoice_number=s_invoice_number,
                        s_inv_amount=s_inv_amount,
                        s_inv_vat = s_inv_vat,
                        c_inv_amount=c_inv_amount,
                        supplier_id = supplier_id.id,
                        loading_date = pick_up_date,
                        unloading_date =unloading_date,
                        )
            request_one.complete_fin=1
            db.session.add(newFin)
            db.session.commit()
            return jsonify({'success':'данные успешно внесены в базу'})
        else:
            print(date_request)
            return jsonify({'not':'в базе уже есть запись с таким ID'})
    except exc.IntegrityError as e:
        return jsonify({'not':'в базе уже есть запись с таким ID'})
   

@supp.route('/prefin_change', methods=['POST', 'GET'])
def prefin_change():
    print(request.args)
    lls = request.args.get('name')
    req_id = request.args.get('id')
    date_request = request.args.get('date')
    date_request=datetime.strptime(date_request, '%Y-%m-%d')
    request_one=Request.query.get(req_id)
    newFin=preFin.query.filter_by(req_id=req_id).first()
    
    try:
        if  newFin:
            print(lls + str(req_id) + ' ' + str(date_request))
            newFin.date_request = date_request
            db.session.commit()
            return jsonify({'success':'данные успешно изменены'})
        else:
            print(date_request)
            return jsonify({'not':'не удалось изменить данные'})
    except exc.IntegrityError:
        return jsonify({'not':'не удалось изменить данные'})


    


