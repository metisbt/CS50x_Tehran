import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Add the user's entry into the database
        alrt = ""

        iname = request.form.get("name")
        imonth = request.form.get("month")
        iday = request.form.get("day")

        if not iname:
            alrt = "please enter name"
        elif not imonth:
            alrt = "please enter month"
        elif not iday:
            alrt = "please enter day"
        else:
            db.execute('''INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)''', iname, imonth, iday)

        date = db.execute('''SELECT * FROM birthdays''')

        return render_template("index.html", message = alrt, birthdays = date)

    else:

        # Display the entries in the database on index.html

        date = db.execute('''SELECT * FROM birthdays''')

        return render_template("index.html", birthdays = date)


