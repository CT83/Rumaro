from flask import Blueprint

login_blueprint = Blueprint('Login', __name__, template_folder='templates')
from . import views
