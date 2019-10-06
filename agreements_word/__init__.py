from flask import Blueprint, current_app, render_template

agr = Blueprint('agr', __name__, template_folder='templates', static_folder='static')

from agreements_word import routes