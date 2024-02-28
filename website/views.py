from . import get_db_connection
from flask import Blueprint, request, render_template, redirect
from datetime import date, datetime

views = Blueprint('views', __name__) 

@views.route("/entry", methods=["GET", "POST"])
def entry():
    return render_template("entry.html")

@views.route("/startstop", methods=["GET", "POST"])
def startstop():
    if request.method == "POST":
        current_date = request.form.get("date")
        starttime = request.form.get("starttime")
        # Start process
        if len(starttime) == 0:
            current_date = date.today().strftime("%Y-%m-%d")
            starttime = datetime.now().strftime("%H:%M")
            endtime = 0
            worktime = 0
        else:
            endtime = datetime.now().strftime("%H:%M")
            startime_split = starttime.split(":")
            startime_format = int(startime_split[0] + startime_split[1])
            endtime_split = endtime.split(":")
            endtime_format = int(endtime_split[0] + endtime_split[1])
            # Calculate difference, format it to have 4 digits
            difference = str(endtime_format - startime_format).zfill(4)
            # Convert to time format
            worktime = difference[:2] + ":" + difference[2:]
        return render_template("entry.html", current_date=current_date, starttime=starttime, endtime=endtime, worktime=worktime)
    