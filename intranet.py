

from app_main import  app
from datetime import datetime

day = datetime.today()
day=day.replace(hour=0)


from app_main.models import db, User, Request, Posts, Costs, Status, \
    Direction, Agreement, Customer, Agg_number, Who_number,\
    Truck_opt, Truck, Quantity, Ttn, Customer_base, subs, Finance, Paid, Zayvka
        
from suppliers.models import Supplier, newSup, Prefin, Documents, Pochta, Child, Parent, Invoicesup


fin = Finance.query.get(44)
pay = Paid.query.get(1)

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Request':Request,  'Posts':Posts, 'Costs':Costs, 'Status':Status,
            'Direction':Direction, 'Agreement':Agreement, 'Customer':Customer, 'Agg_number':Agg_number,
            'Who_number':Who_number, 'Truck':Truck, 'Quantity':Quantity, 'Truck_opt':Truck_opt, 'Ttn':Ttn,
            'Customer_base':Customer_base, 'db':db, 'subs':subs, 'day':day, 'Finance':Finance, 'Paid':Paid, 
            'fin':fin, 
            'pay':pay,
            'Supplier':Supplier,
            'newSup': newSup,
            'Prefin': Prefin,
            'Documents': Documents,
            'Pochta': Pochta,
            'Child': Child,
            'Parent': Parent,
            'Invoicesup':Invoicesup,
            'Zayvka':Zayvka
            }


if __name__=='__main__':
    app.run(debug=True, host='10.10.1.38')
