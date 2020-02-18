from flask import Blueprint, current_app, render_template

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')

from api import routes