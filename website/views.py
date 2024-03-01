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
        if request.form["submit_button"] == "Start/Stop":
            current_date = request.form.get("date")
            starttime = request.form.get("starttime")
            endtime = request.form.get("endtime")
            # If starttime is not specified
            if len(starttime) == 0:
                current_date = date.today().strftime("%Y-%m-%d")
                starttime = datetime.now().strftime("%H:%M")
                # Set other variables to 0, so that render_template works
                endtime = 0
                worktime = 0
            else:
                # If endtime is not specified
                if len(endtime) == 0:
                    # Set endtime to current time
                    endtime = datetime.now().strftime("%H:%M")

                t1 = datetime.strptime(starttime, "%H:%M")
                t2 = datetime.strptime(endtime, "%H:%M")

                timedelta = t2-t1
                seconds = timedelta.total_seconds()
                minutes = seconds / 60
                hours = minutes / 60

                worktime = 0

        return render_template("entry.html", current_date=current_date, starttime=starttime, endtime=endtime, worktime=worktime)
    