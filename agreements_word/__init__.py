from flask import Blueprint, current_app, render_template

agr = Blueprint('agreement', __name__, template_folder='templates', static_folder='static')

from agreements_word import routes