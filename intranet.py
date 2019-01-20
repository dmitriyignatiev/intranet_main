from app_main import app

from app_main.models import db, User, Request, Posts, Costs, Status, \
    Direction, Agreement, Customer, Agg_number, Who_number, Truck_opt, Truck, Quantity, Ttn, Customer_base

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Request':Request,  'Posts':Posts, 'Costs':Costs, 'Status':Status,
            'Direction':Direction, 'Agreement':Agreement, 'Customer':Customer, 'Agg_number':Agg_number,
            'Who_number':Who_number, 'Truck':Truck, 'Quantity':Quantity, 'Truck_opt':Truck_opt, 'Ttn':Ttn,
            'Customer_base':Customer_base
            }

