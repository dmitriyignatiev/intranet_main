from flask import Blueprint, current_app, render_template

cust = Blueprint('cust', __name__, template_folder='templates', static_folder='static')

from customers import routes