import graphene
from graphene import relay, List, Argument, String, Int
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db, Supplier as SupplierModel, Prefin as PrefinModel
from customers.models import db, Invoicecust as InvoicecustModel
from app_main.models import User, Book, Author, Request
from suppliers.models import Prefin, Invoicesup, Supplier
from customers.models import Invoicecust



class RequestObject(SQLAlchemyObjectType):
    class Meta:
        model=Request
        interface=(relay.Node,)

class RequestConnection(relay.Connection):
    class Meta:
        node=RequestObject



class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        id = graphene.Field(graphene.Int())
        interfaces = (relay.Node, )

class UserConnection(relay.Connection):
    class Meta:
        node=UserObject




class SupplierObject(SQLAlchemyObjectType):
    class Meta:
        model=Prefin

class SupplierConnection(relay.Connection):
    class Meta:
        node=SupplierObject




class Query(graphene.ObjectType):
    all_users = SQLAlchemyConnectionField(UserConnection)
    all_requests = SQLAlchemyConnectionField(RequestConnection)
    all_suppliers = SQLAlchemyConnectionField(SupplierConnection)

    user = relay.Node.Field(UserObject)

    find_user = graphene.Field(UserObject, uid = graphene.Int(), name=graphene.String())

    def resolve_find_user(self, info, **args):
        query = UserObject.get_query(info)
        uid = args.get('uid')
        name = args.get('name')
        if uid:
            return query.filter(User.uid==uid).first()
        elif name:
            return query.filter(User.name==name).first()

    
   
    


   



schema = graphene.Schema(query=Query)



    


   

    
    

    


