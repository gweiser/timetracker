from . import get_db_connection
from flask import Blueprint, request, render_template

views = Blueprint('views', __name__) 

#views.route("/", methods=["GET", "POST"])

