from flask import Blueprint, current_app, render_template

supp = Blueprint('supp', __name__, template_folder='templates', static_folder='static')

from suppliers import routes