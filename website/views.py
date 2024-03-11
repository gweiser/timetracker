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
    for row in entries_row:
        entries.append(
            {"id": row["id"],
             "creation_date": row["creation_date"],
             "start_time": row["start_time"],
             "end_time": row["end_time"],
             "duration": row["duration"],
             "note": row["note"],
             "wage": row["wage"],
             "pay": row["pay"]
             }
        )
    total = 0
    for entry in entries:
        total += float(entry["pay"].split("€")[1])


    return render_template("index.html", entries=entries, total=f"€ {str(total)}")

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
                # todo: Insert starttime into temp

                # Set other variables to 0, so that render_template works
                endtime = 0
                worktime = 0
                pay = 0
            else:
                # If endtime is not specified
                if len(endtime) == 0:
                    # Set endtime to current time
                    endtime = datetime.now().strftime("%H:%M")
                # todo: Insert endtime into temp
                    
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
                # todo: Insert worktime into temp


                # Calculate Wage
                wage = int(request.form.get("wage"))
                total_hours = (timedelta.total_seconds() / 60) / 60
                pay = f"€ {round(wage * total_hours, 2)}"
                # todo: Insert wage and pay into temp
            
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
                       INSERT INTO entries (creation_date, start_time, end_time, duration, note, wage, pay)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       """, (creation_date, starttime, endtime, duration, note, wage, pay))
            db.commit()

            return redirect(url_for("views.home"))
        return render_template("entry.html", creation_date=creation_date, starttime=starttime, endtime=endtime, worktime=worktime, pay=pay)
    else:      
        return render_template("entry.html", creation_date=creation_date, starttime=starttime, endtime=endtime, worktime=worktime, pay=pay)
    

@views.route("/paid/<int:id>", methods=["GET", "POST"])
def paid(id=None):
    if id is not None:
        # Get data
        data = db.execute("SELECT * FROM entries WHERE id = ?", (id, )).fetchone()
        # Insert data into paid table
        db.execute("""
                   INSERT INTO paid (id, creation_date, start_time, end_time, duration, note, wage, pay)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
                   """, (data["id"], data["creation_date"], data["start_time"], data["end_time"], data["duration"], data["note"], data["wage"], data["pay"]))
        # Delete from home view
        db.execute("DELETE FROM entries WHERE id = ?", (id, ))
        db.commit()

        return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.home"))
    
@views.route("/paid_view", methods=["GET", "POST"])
def paid_view():
    if request.method == "GET":
        data_row = db.execute("SELECT * FROM paid").fetchall()
        data = []

        for row in data_row:
            data.append(
                    {"id": row["id"],
                    "creation_date": row["creation_date"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                    "duration": row["duration"],
                    "note": row["note"],
                    "wage": row["wage"],
                    "pay": row["pay"]}
            )
        
        return render_template("paid_view.html", data=data)
    

@views.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id=None):
    if id is not None:
        # Get entry
        data = db.execute("SELECT * FROM entries WHERE id = ?", (id, )).fetchone()
        # Insert into bin
        db.execute("""
                   INSERT INTO bin (id, creation_date, start_time, end_time, duration, note, wage, pay)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)

                   """, (data["id"], data["creation_date"], data["start_time"], data["end_time"], data["duration"], data["note"], data["wage"], data["pay"]))
        # Delete from entries
        db.execute("DELETE FROM entries WHERE id = ?", (id, ))
        db.commit()

        return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.home"))