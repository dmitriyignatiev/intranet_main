import graphene
from graphene import relay, List, Argument, String, Int
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db, Supplier as SupplierModel, Prefin as PrefinModel
from customers.models import db, Invoicecust as InvoicecustModel
from app_main.models import User, Book, Author, Request



class RequestObject(SQLAlchemyObjectType):
    class Meta:
        model=Request
        interface=(relay.Node,)

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    
    node = relay.Node.Field()
    
    all_users = SQLAlchemyConnectionField(UserObject)
 
   
    
    user = relay.Node.Field(UserObject)
    
    users = List(UserObject)


    find_employee = graphene.Field(lambda: UserObject, id=graphene.Int(), name=graphene.String())
    
    hello = String(
		name = Argument(String, default_value = 'stranger'),
		age = Argument(Int, default_value = 14)
	)

    def resolve_find_employee(self,  info, **args):
        query = UserObject.get_query(info)
        name = args.get('name') 
        
        return query.filter(User.name == name).first()

    def resolve_users_test(self, info):
        return UserObject.get_query(info)

    def resolve_hello(self, info, name, age):
    		return 'Hi {} you are {} years old.'.format(name, age)




schema = graphene.Schema(query=Query, types=[UserObject, RequestObject])



    


   

    
    

    


