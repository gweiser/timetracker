from . import get_db_connection
from flask import Blueprint, request, render_template, redirect
from datetime import date, datetime
import re

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
                
                # Difference between both times
                timedelta = str(t2-t1)
                print(timedelta)
                # use RegEx to filter out time from output
                filter = re.split("[:]", timedelta)

                # Get hours properly formatted
                hours_unfiltered = filter[0]
                hours = hours_unfiltered[-1].zfill(2)
                # Get minutes
                minutes = filter[1].zfill(2)

                worktime = f"{hours}:{minutes}"
 

        return render_template("entry.html", current_date=current_date, starttime=starttime, endtime=endtime, worktime=worktime)
    