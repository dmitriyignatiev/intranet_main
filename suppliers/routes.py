from flask import render_template, request, jsonify
from suppliers import supp
from .models import Supplier
from app_main import db
from .forms import *


@supp.route('/add_supplier')
def add_supplier():
    form=formSupplier()
    return render_template('/add_supplier.html', form=form)

@supp.route('/add_supplier_to_db', methods=['POST', 'GET'])
def add_supplier_to_db():
    form=formSupplier()
    name = request.args.get('name')
    print(name)
    new_supp = Supplier.query.filter_by(llc_name=name).first()
    if new_supp:
         return render_template('section1.html', form=form)
    
    else:
        new_supp = Supplier(llc_name=name)
        db.session.add(new_supp)
        db.session.commit()
        return render_template('section.html', new_supp=new_supp, form=form)

    


