
from flask import Blueprint, jsonify, request, session
from app_main import db, app
from suppliers.models import Supplier, Prefin, Supp_payment
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_marshmallow import Marshmallow

import flask_restless
from flask_restless import APIManager





api = Blueprint('api', __name__)
ma = Marshmallow()

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Supplier, include_columns=['id', 'llc_name', 'prefin', 'prefin.id'], methods=['GET', 'POST'])
manager.create_api(Prefin, include_columns=['id'], methods=['GET'])




# class PrefinSchema(ma.ModelSchema):
#     class Meta:
#         model=Prefin
#         sqla_session = db.session

# class SupplierSchema(ma.ModelSchema):
#     class Meta:
#         model=Supplier
#         sqla_session = db.session
  
    

# supplier_schema=SupplierSchema()

@api.route('/suppliers', methods=['GET'])
def index():
   name = request.args.get('name')
   if name:
       name = request.args.get('name')
       supplier = Supplier.query.filter_by(llc_name=name).first()
   else:
       name='t001'
       supplier = Supplier.query.filter_by(llc_name=name).first()
   if session.get('fin_id'):
        fin_id = session.get('fin_id')
   else:
       fin_id=1

    
#    result = supplier_schema.dump(supplier)


    

   


   return jsonify([{'result':'result', 
   'test':'api', 'name': name, 'finid':session.get('fin_id'),
                    
                    }])