import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("homepage.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    journal = list(mongo.db.journal.find({"$text": {"$search": query }}))
    return render_template("entry_collection.html", journal=journal)


@app.route("/entry_collection")
def entry_collection():
    journal = list(mongo.db.journal.find())
    return render_template("entry_collection.html", journal=journal)


# write journal entry
@app.route("/journal", methods=["GET", "POST"])
def journal():
    if request.method == "POST":
        journal = {
            "date": request.form.get("date"),
            "title": request.form.get("title"),
            "mood": request.form.get("mood"),
            "text": request.form.get("text")
            }
        mongo.db.journal.insert_one(journal)
        flash("Journal entry added")
        return redirect(url_for("entry_collection"))

    date = mongo.db.journal.find().sort("date", 1)
    return render_template("journal.html", date=date) 


# edit journal entry
@app.route("/edit_journal/<journal_id>", methods=["GET", "POST"])
def edit_journal(journal_id):
    if request.method == "POST":
        submit = {
            "date": request.form.get("date"),
            "title": request.form.get("title"),
            "mood": request.form.get("mood"),
            "text": request.form.get("text")
            }

        mongo.db.journal.update({"_id": ObjectId(journal_id)}, submit)
        flash("Your journal entry has been updated")
   
    journal = mongo.db.journal.find_one({"_id": ObjectId(journal_id)})
    title = mongo.db.title.find().sort("title", 1)
    return render_template("edit_journal.html", journal=journal, title=title)


# delete journal entry
@app.route("/delete_journal/<journal_id>")
def delete_journal(journal_id):
    mongo.db.journal.remove({"_id": ObjectId(journal_id)})
    flash("Your entry has been deleted")
    return redirect(url_for("entry_collection"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash(u"Username already exists")
            return redirect(url_for("register"))

        register = {	
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }

        mongo.db.users.insert_one(register)
        # Put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("homepage", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(existing_user["password"], request.form.get
            ("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                        request.form.get("username")))
                return redirect(url_for(
                        "homepage", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# user profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab session's username from mongodb
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session['user']:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


# logout
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)