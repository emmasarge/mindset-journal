import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_journal")
def get_journal():
    journal = mongo.db.journal.find()
    return render_template("journal.html", journal=journal)


@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        journal = {
            "date": request.form.get("date"),
            "mood": request.form.get("mood"),
            "text": request.form.get("text")
        }
        mongo.db.journal.insert_one(journal)
        flash("Entry Successfully Added")
        return redirect(url_for("get_journal"))

    date = mongo.db.date.find().sort("date", 1)
    return render_template("add_entry.html", date=date)




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)