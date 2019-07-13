from flask import render_template, request, \
    jsonify, redirect, flash, send_from_directory, url_for, send_file, session, make_response
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
    docs = Documents.query.filter(Documents.req_id==session['id'])
    id = req.id
    session['id']=id

    new_id = session['id']
    print(new_id)
    
    
    
    
    date = req.pick_up_date
    form=formSupplier()
    if form.validate_on_submit():
        choose_supp = form.name.data
        name = choose_supp.llc_name
    return render_template('add_supplier.html', form=form, req=req, date=date, docs=docs)

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
        print(file)
        new_d = Documents(req_id=session['id'])
        db.session.add(new_d)
        db.session.commit()
        filename=file.filename
        new_d.path=str(filename)
        db.session.commit()

        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return jsonify({'success':'файлы успешно сохранены'})
    # return render_template("complete.html")


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
    print(request.args)
    
    request_one=Request.query.get(req_id)
    direction = request_one.direction
    sale = request_one.user.name
    customer = request_one.customer.name


    try:
        if not preFin.query.filter_by(req_id=req_id).first():
            print(tora_red + str(req_id) + ' ' + str(date_request)+''+str(supplier_name) + ''+ str(direction) + str(status_of_request))
            newFin = preFin(tora_red=tora_red, req_id=req_id, 
                        customer_order_date=customer_order_date,
                        direction=direction, sale=sale,
                        status_of_request=status_of_request,
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


    


