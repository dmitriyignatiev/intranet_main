import graphene
from graphene import relay, List, Argument, String, Int
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db, Supplier as SupplierModel, Prefin as PrefinModel
from customers.models import db, Invoicecust as InvoicecustModel
from app_main.models import User, Book, Author, Request
from suppliers.models import Prefin, Invoicesup, Supplier, Supp_payment
from customers.models import Invoicecust



class RequestObject(SQLAlchemyObjectType):
    class Meta:
        model=Request
        

class RequestConnection(relay.Connection):
    class Meta:
        node=RequestObject



class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
      
class UserConnection(relay.Connection):
    class Meta:
        node=UserObject


class SupplierObject(SQLAlchemyObjectType):

    class Meta:
        model = Supplier
       

class SupplierConnection(relay.Connection):

    class Meta:
        node=SupplierObject

class SuppPaymentObject(SQLAlchemyObjectType):
    class Meta:
        model = Supp_payment
       

class SuppPaymentConnection(relay.Connection):
    class Meta:
        node = SuppPaymentObject


class PrefinObject(SQLAlchemyObjectType):
    class Meta:
        model = Prefin

class PrefinConnection(relay.Connection):
    class Meta:
        node = PrefinObject

#


class Query(graphene.ObjectType):
    node = relay.Node.Field()


    all_users = SQLAlchemyConnectionField(UserConnection)
    all_requests = SQLAlchemyConnectionField(RequestConnection)
    all_suppliers = SQLAlchemyConnectionField(SupplierConnection)
    all_supppayments = SQLAlchemyConnectionField(SuppPaymentConnection)
    all_prefin = SQLAlchemyConnectionField(PrefinConnection)

    user = relay.Node.Field(UserObject)

    find_user = graphene.Field(UserObject,  name=graphene.String())

    def resolve_find_user(self, info, **args):
       query = UserObject.get_query(info)
       name = args.get('name')
       return query.filter(User.name==name).first()

    find_supplier = graphene.Field(SupplierObject, llc_name = graphene.String())
    def resolve_find_supplier(self, info, **args):
        query = SupplierObject.get_query(info)
        llc_name = args.get('llc_name')
        return query.filter(Supplier.llc_name==llc_name).first()

    filter_supplier_prefin = graphene.List(
        SupplierObject, 
        llc_name = graphene.String(), 
        id = graphene.Int()
    )
    def resolve_filter_supplier_prefin(self, info, **args):
        query = SupplierObject.get_query(info)
        llc_name = args.get('llc_name')
        query = query.filter(Supplier.llc_name==llc_name)
        id = args.get('id')
        query = query.filter(Prefin.id==id)
        query = query.join(Supplier.prefin)
        objs = query.all()
        return objs

    filter_duo = graphene.List(
        SupplierObject,
        llc_name = graphene.String(), 
        id = graphene.Int()
    )

    def resolve_filter_duo(self, info, id, llc_name):
        query = SupplierObject.get_query(info=info)
        query = query.join(Supplier.prefin)
        query = query.filter(and_Supplier.llc_name==llc_name)





    
    

   
    
     


    #search prefin models which related to Supplier
    

schema = graphene.Schema(query=Query)





    


   

    
    

    


