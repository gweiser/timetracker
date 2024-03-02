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
                print(timedelta)
                seconds = timedelta.total_seconds()
                minutes = int(seconds / 60)

                if minutes < 60:
                    worktime = f"00:{(minutes)}"
                elif minutes > 59:
                    # Hours with comma
                    total = str(round((minutes / 60), 2))
                    # Just hours
                    hours = total.split(".")[0].zfill(2)
                    # Minutes to the hundredth
                    minutes_hundreds = int(total.split(".")[1]) / 100 
                    #Remaining minutes
                    minutes_full = int(round((minutes_hundreds * 60), 0))
                    # Minutes formatted
                    minutes = str(minutes_full).zfill(2)
                    worktime = f"{hours}:{minutes}"


        return render_template("entry.html", current_date=current_date, starttime=starttime, endtime=endtime, worktime=worktime)
    