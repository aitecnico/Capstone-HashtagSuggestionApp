from flask import Flask, jsonify, render_template, request, flash, redirect, session
from secrets import API_SECRET_KEY
from forms import UserForm, LoginForm, HashtagForm
import requests
import random
from models import db, connect_db, Hashtag, User
from sqlalchemy.exc import IntegrityError
import os

# from flask_debugtoolbar import DebugToolbarExtension

# *****************************
# PYTHON API REQUEST
# *****************************
client_id = API_SECRET_KEY

API_BASE_URL = "https://api.ritekit.com/v1"

app = Flask(__name__)
# app.debug = True


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///hashtag_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "hellosecret1")
# toolbar = DebugToolbarExtension(app)


# *******************
# Connect to Database
# *******************
connect_db(app)


# ********************
# Home Directory Route
# ********************
@app.route("/")
def homepage():
    """Show homepage."""

    # Keep a count of how many times page is visited
    session["count"] = session.get("count", 0) + 1

    hashtags = Hashtag.query.all()
    return render_template("index.html", hashtags=hashtags)


# ************************************************************
# Find Users hashtag results
# GET The Hashtag currently trending on Twitter
# and the number of times tweeted JSON through the Ritekit API
# ************************************************************
def get_results(hashtag):
    res = requests.get(
        f"{API_BASE_URL}/stats/hashtag-suggestions?text=seo",
        params={"client_id": client_id, "text": hashtag},
    )
    data = res.json()
    hash = data["data"][1]["hashtag"]
    tweets = data["data"][1]["tweets"]
    results = {"hash": hash, "tweets": tweets}
    return results


# *******************************
# DISPLAYS Users hashtag result
# *******************************
@app.route("/hashtagsuggestion")
def get_hashtag():
    hashtag = request.args["hashtag"]
    results = get_results(hashtag)
    return render_template("index.html", results=results)


# **************************************
# REGISTER User and add them to database
# **************************************
@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User.register(username, email, password)
        # Do some error handeling HERE

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Please choose another.")
            return render_template("register.html", form=form)

        session["user_id"] = new_user.id
        flash("Welcome! You Have Successfully Created Your Account!", "success")
        return redirect("/hashtags")

    return render_template("register.html", form=form)


# **********************************************
# LOGIN User Authenticate Username and Password
# **********************************************
@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            flash(f"Welcome Back, {user.username}!", "success")
            session["user_id"] = user.id
            return redirect("hashtags")
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("/login.html", form=form)


# ********************************************************
# LOGOUT and clear user selection and redirect to homepage
# ********************************************************
@app.route("/logout")
def logout_user():
    session.pop("user_id")
    flash("Visit us again!", "info")
    return redirect("/")


@app.route("/hashtags", methods=["GET", "POST"])
def show_hashtags():
    if "user_id" not in session:
        flash("Please Login First!", "danger")
        return redirect("/")
    form = HashtagForm()
    all_hashtags = Hashtag.query.all()
    if form.validate_on_submit():
        text = form.text.data
        new_hashtag = Hashtag(text=text, user_id=session["user_id"])
        db.session.add(new_hashtag)
        db.session.commit()
        flash("Hashtag Created!" "success")
        return redirect("/hashtags")

    return render_template("hashtags.html", form=form, hashtags=all_hashtags)


# *********************************
# DELETE Hashtag that user created
# *********************************
@app.route("/hashtags/<int:id>", methods=["POST"])
def delete_hashtag(id):
    """Delete hashtag"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect("/login")
    hashtag = Hashtag.query.get_or_404(id)
    if hashtag.user_id == session["user_id"]:
        db.session.delete(hashtag)
        db.session.commit()
        flash("Hashtag deleted", "info")
        return redirect("/hashtags")
    flash("You don't have permission to do that!", "danger")
    return redirect("/hashtags")
