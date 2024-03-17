from . import get_db_connection
from flask import Blueprint, request, render_template, redirect, url_for
from datetime import date, datetime
import re
import sqlite3

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
                pay = f"€ {round(wage * total_hours, 2)}"
            
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
    
    
@views.route("/undo/<int:id>", methods=["GET", "POST"])
def undo(id=None):
    if id is not None:
        # Get paid entry
        entry = db.execute("SELECT * FROM paid WHERE id = ?", (id, )).fetchone()
        # Move to entries
        db.execute("""
                    INSERT INTO entries (id, creation_date, start_time, end_time, duration, note, wage, pay)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (entry["id"], entry["creation_date"], entry["start_time"], entry["end_time"], entry["duration"], entry["note"], entry["wage"], entry["pay"]))
        
        # Delete from paid
        db.execute("DELETE FROM paid WHERE id = ?", (id, ))
        db.commit()

        return redirect(url_for("views.paid_view"))
    else:
        return redirect(url_for("views.home"))
    

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


@views.route("/bin_view", methods=["GET", "POST"])
def bin_view():
    if request.method == "GET":
        data = db.execute("SELECT * FROM bin").fetchall()
        bin_entries = []
        for row in data:
            bin_entries.append(
                {
                    "id": row["id"],
                    "creation_date": row["creation_date"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                    "duration": row["duration"],
                    "note": row["note"],
                    "wage": row["wage"],
                    "pay": row["pay"]
                }
            )

    return render_template("bin_view.html", bin_entries=bin_entries)

@views.route("/clear_bin", methods=["GET", "POST"])
def clear_bin():
    # Delete everything from bin
    db.execute("DELETE FROM bin")
    db.commit()

    return redirect(url_for("views.home"))

@views.route("/all_paid", methods=["GET", "POST"])
def all_paid():
    # Get all entries 
    entries = db.execute("SELECT * FROM entries").fetchall()
    # Insert every entry into paid table 
    for row in entries:
        db.execute("""
                   INSERT INTO paid (id, creation_date, start_time, end_time, duration, note, wage, pay)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   """, (row["id"], row["creation_date"], row["start_time"], row["end_time"], row["duration"], row["note"], row["wage"], row["pay"]))
        
    # Remove from entries table
    db.execute("DELETE FROM entries")
    db.commit()

    return redirect(url_for("views.home"))

@views.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id=None):
    if id is not None:
        if request.method == "GET":
            entry = db.execute("SELECT * FROM entries WHERE id = ?", (id, )).fetchone()

            return render_template("edit.html", creation_date=entry["creation_date"], starttime=entry["start_time"], endtime=entry["end_time"], worktime=entry["duration"], pay=entry["pay"], note=entry["note"], id=id)
        else:
            date = request.form.get("date")
            starttime = request.form.get("starttime")
            endtime = request.form.get("endtime")
            duration = request.form.get("worktime")
            note = request.form.get("note")
            wage = request.form.get("wage")
            pay = request.form.get("pay")

            db.execute("DELETE FROM entries WHERE id = ?", (id, ))
            db.execute("""
                        INSERT INTO entries (id, creation_date, start_time, end_time, duration, note, wage, pay)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """, (id, date, starttime, endtime, duration, note, wage, pay))
            db.commit()

            return redirect(url_for("views.home"))
    else:
        return redirect(url_for("views.home"))