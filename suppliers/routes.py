from flask import render_template, request, jsonify
from suppliers import supp
from .models import Supplier
from app_main.models import *
from app_main import db
from .forms import *


@supp.route('/add_supplier/<int:id>', methods=['GET', 'POST'])
def add_supplier(id):
    req = Request.query.get(id)
    form=formSupplier()
    if form.validate_on_submit():
        choose_supp = form.name.data
        name = choose_supp.llc_name
        print(name)
    return render_template('add_supplier.html', form=form, req=req)

@supp.route('/add_supplier_to_db', methods=['POST', 'GET'])
def add_supplier_to_db():
    form=formSupplier()
    name = request.args.get('name')
    print(name)
    new_supp = Supplier.query.filter_by(llc_name=name).first()
    if new_supp:
         return render_template('section1.html', form=form)
    
    elif not new_supp:
        new_supp = Supplier(llc_name=name)
        db.session.add(new_supp)
        db.session.commit()
        return render_template('section.html', new_supp=new_supp, form=form)
    
    


    


