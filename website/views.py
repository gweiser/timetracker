from . import get_db_connection
from flask import Blueprint, request, render_template, redirect
from datetime import date, datetime

views = Blueprint('views', __name__) 

@views.route("/entry", methods=["GET", "POST"])
def entry():
    return render_template("entry.html")

@views.route("/start", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        current_date = date.today().strftime("%Y-%m-%d")
        print(current_date)
        starttime = datetime.now().strftime("%H:%M")
        print(starttime)

        return render_template("entry.html", current_date=current_date, starttime=starttime)