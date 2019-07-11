from flask import render_template, request, \
    jsonify, redirect, flash, send_from_directory, url_for, send_file
from suppliers import supp
from .models import Supplier, preFin
from app_main.models import *
from app_main import db, app
from .forms import *
from sqlalchemy import exc


@supp.route('/index')
def index():
    return render_template('index.html')

@supp.route('/add_supplier/<int:id>', methods=['GET', 'POST'])
def add_supplier(id):
    req = Request.query.get(id)
    date = req.pick_up_date
    form=formSupplier()
    if form.validate_on_submit():
        choose_supp = form.name.data
        name = choose_supp.llc_name
    return render_template('add_supplier.html', form=form, req=req, date=date)

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

UPLOAD_FOLDER=r'C:\Users\Dmitriy\Desktop\int_1\intranet_main\TN'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pdf'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@supp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            return redirect(url_for('supp.download_file', filename=filename))
    return render_template('upload.html')
  

@supp.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

@supp.route('/prefin', methods=['POST', 'GET'])
def prefin():
    
    lls = request.args.get('name')
    req_id = request.args.get('id')
    date_request = request.args.get('date')
    date_request=datetime.strptime(date_request, '%Y-%m-%d')
    supp=request.args.get('supp')
    
    request_one=Request.query.get(req_id)
    dirr = request_one.direction
    sale = request_one.user.name
    



    try:
        if not preFin.query.filter_by(req_id=req_id).first():
            print(lls + str(req_id) + ' ' + str(date_request)+''+str(supp) + ''+ str(dir))
            newFin = preFin(llc=lls, req_id=req_id, date_request=date_request,
                        supplier=supp, direction=dirr, sale=sale,
                        status=form.status.data,
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


    


