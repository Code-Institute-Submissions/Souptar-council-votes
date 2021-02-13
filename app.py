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
@app.route("/get_motions")
def get_motions():
    motions = mongo.db.motions.find()
    return render_template("motions.html", motions=motions)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # username check
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # password match confirmation
        pass_check_1 = request.form.get("password")
        pass_check_2 = request.form.get("confirm_password")

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        elif pass_check_1 != pass_check_2:
            flash("Passwords do not match")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # updates session cookie with new user
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # username check
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # hashed pass match check
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username").capitalize()))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # password incorrext
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # get session user's username
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # logs user out by clearing session cookies
    flash("You have been logged out")
    session.clear()
    return redirect(url_for("login"))


@app.route("/submit_motion", methods=["GET", "POST"])
def submit_motion():
    if request.method == "POST":
        motion_pass = "on" if request.form.get("motion_pass") else "off"
        motion = {
            "motion_category": request.form.get("motion_category"),
            "motion_text": request.form.get("motion_text"),
            "motion_pass": motion_pass,
            "motion_date": request.form.get("motion_date"),
            "link": request.form.get("link"),
            "council_name": request.form.get("council_name"),
            "created_by": session["user"]
        }
        mongo.db.motions.insert_one(motion)
        flash("Motion Submitted")
        return redirect(url_for("get_motions"))

    return render_template("submit_motion.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
