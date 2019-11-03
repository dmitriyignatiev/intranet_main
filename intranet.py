

from app_main import  app
from datetime import datetime

day = datetime.today()
day=day.replace(hour=0)



from app_main.models import db, User, Request, Posts, Costs, Status, \
    Direction, Agreement, Agg_number, Who_number,\
    Truck_opt, Truck, Quantity, Ttn, Customer_base, subs, Finance, Paid, Zayvka, Customer
        
from suppliers.models import Supplier, newSup, Prefin, Documents, \
    Pochta, Invoicesup, Tn, Supp_payment, Invoice_payment_s, Transit, Tr_status, Companies, Bank, Tr_payments

from customers.models import   Invoicecust, Invoice_payment_c
from agreements_word.models import *






@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Request':Request,  'Posts':Posts, 'Costs':Costs, 'Status':Status,
            'Direction':Direction, 'Agreement':Agreement, 'Customer':Customer, 'Agg_number':Agg_number,
            'Who_number':Who_number, 'Truck':Truck, 'Quantity':Quantity, 'Truck_opt':Truck_opt, 'Ttn':Ttn,
            'Customer_base':Customer_base, 'db':db, 'subs':subs, 'day':day, 'Finance':Finance, 'Paid':Paid, 
            
            
            'Supplier':Supplier,
            'newSup': newSup,
            'Prefin': Prefin,
            'Documents': Documents,
            'Pochta': Pochta,
            
            'Invoicesup':Invoicesup,
            'Zayvka':Zayvka,
            'Tn':Tn,
            'Supp_payment':Supp_payment,
            'Invoice_payment_s':Invoice_payment_s,
            'Transit':Transit,
            'Invoicecust':Invoicecust,
            'Invoice_payment_c':Invoice_payment_c,
            'Agreements':Agreements,
            'Tr_status':Tr_status,
            'Companies':Companies,
            'Bank': Bank,
            'Tr_payments':Tr_payments,
                        }


if __name__=='__main__':
    db.create_all()
    app.run(debug=True, host='10.10.1.39', port='5000')
