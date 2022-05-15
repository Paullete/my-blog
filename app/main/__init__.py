from flask import Blueprint

# create blueprint
main = Blueprint('main', __name__)

from . import views