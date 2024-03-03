from . import get_db_connection
from flask import Blueprint, request, render_template, redirect, url_for
from datetime import date, datetime
import re

views = Blueprint('views', __name__) 
db = get_db_connection()

@views.route("/", methods=["GET", "POST"])
def home():
    entries_row = db.execute("SELECT * FROM entries").fetchall()
    entries = []
    counter = 0
    for row in entries_row:
        entries.append(
            {"id": row["id"],
             "creation_date": row["creation_date"],
             "start_time": row["start_time"],
             "end_time": row["end_time"],
             "duration": row["duration"],
             "note": row["note"],
             "wage": row["wage"],
             "pay": row["pay"],
             "block_id": row["block_id"]
             }
        )
        counter += 1

    return render_template("index.html", entries=entries)

@views.route("/entry", methods=["GET", "POST"])
def entry():
    return render_template("entry.html")

@views.route("/startstop", methods=["GET", "POST"])
def startstop():
    if request.method == "POST":
        if request.form["submit_button"] == "Start/Stop":
            creation_date = request.form.get("date")
            starttime = request.form.get("starttime")
            endtime = request.form.get("endtime")

            # Calculate Time Worked
            # If starttime is not specified 
            if len(starttime) == 0:
                creation_date = date.today().strftime("%Y-%m-%d")
                starttime = datetime.now().strftime("%H:%M")
                # Set other variables to 0, so that render_template works
                endtime = 0
                worktime = 0
                pay = 0
            else:
                # If endtime is not specified
                if len(endtime) == 0:
                    # Set endtime to current time
                    endtime = datetime.now().strftime("%H:%M")

                t1 = datetime.strptime(starttime, "%H:%M")
                t2 = datetime.strptime(endtime, "%H:%M")
                
                # Difference between both times
                timedelta = t2-t1
                # use RegEx to filter out time from output
                filter = re.split("[:]", str(timedelta))

                # Get hours properly formatted
                hours_unfiltered = filter[0]
                hours = hours_unfiltered[-1].zfill(2)
                # Get minutes
                minutes = filter[1].zfill(2)

                worktime = f"{hours}:{minutes}"


                # Calculate Wage
                wage = int(request.form.get("wage"))
                total_hours = (timedelta.total_seconds() / 60) / 60
                pay = str(wage * total_hours)
            
        elif request.form["submit_button"] == "Submit":
            # If inputs are submitted
            creation_date = request.form.get("date")
            starttime = request.form.get("starttime")
            endtime = request.form.get("endtime")
            duration = request.form.get("worktime")
            wage = request.form.get("wage")
            pay = request.form.get("pay")
            note = request.form.get("note")

            db.execute("""
                       INSERT INTO entries (creation_date, start_time, end_time, duration, note, wage, pay, block_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """, (creation_date, starttime, endtime, duration, note, wage, pay, 1))
            db.commit()
            db.close()

            return redirect(url_for("views.entry"))
        return render_template("entry.html", creation_date=creation_date, starttime=starttime, endtime=endtime, worktime=worktime, pay=pay)
    else:      
        return render_template("entry.html", creation_date=creation_date, starttime=starttime, endtime=endtime, worktime=worktime, pay=pay)
    