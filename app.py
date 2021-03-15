from flask import Flask, jsonify, render_template, request
import requests
import random

from models import db, connect_db, Hashtag

# *****************************
# PYTHON API REQUEST
# *****************************
# API_BASE_URL = "http://numbersapi.com/random?"


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashtag_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

# *****************************
# FLASK API CALL
# *****************************





@ app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")


@app.route('/lucky-form')
def get_luckform():
    # text = request.args["min=1&max=100&json"]
    res = requests.get(f"{API_BASE_URL}/min=1&max=100&json")


# *****************************
# TEST in TERMINAL IF JSON IS RESPONDING
# *****************************
    # import pdb
    # pdb.set_trace()
    data = res.json()
    # number = data["text"]
    # print('*******************************')
    # print(data)
    answers = data
    return render_template("index.html", answers=answers)


# *********************************************************
# RESTFUL LUCKYNUMBERS JSON API (GET LIST ALL Luckynumbers)
# **********************************************************
@ app.route('/api/luckynumbers')
def list_luckynumbers():
    """Returns JSON w/ all todos"""
    all_luckynumbers = [luckynumber.serialize()
                        for luckynumber in Luckynumber.query.all()]
    return jsonify(luckynumbers=all_luckynumbers)

# *****************************
# RESTFUL LUCKYNUMBERS JSON API (GET 1 ID of Luckynumbers)
# *****************************


@ app.route('/api/luckynumbers/<int:id>')
def get_luckynumber(id):
    luckynumber = Luckynumber.query.get_or_404(id)
    return jsonify(luckynumber=luckynumber.serialize())


# *****************************
# RESTFUL LUCKYNUMBERS JSON API (POST CREATE Luckynumbers)
# *****************************
@ app.route('/api/luckynumbers', methods=["POST"])
def create_luckynumber():
    new_luckynumber = Luckynumber(
        name=request.json["name"], email=request.json["email"], year=request.json["year"], color=request.json["color"])
    db.session.add(new_luckynumber)
    db.session.commit()
    response_json = jsonify(luckynumber=new_luckynumber.serialize())
    return (response_json, 201)


# *****************************
# JSON body with the following information
# If the user failed to provide valid data
# It's own API
# *****************************
@ app.route('/api/get-lucky-num', methods=["POST"])
def create_lucknum():
    return_value = {"error": {}, "mydata": request.json}
    print(request.json)
    error = {"error": {}}

    # ******************************************************
    # Individual Error if specific JSON is not recieved
    # ******************************************************

    # ********************************************************
    # Name field is required
    # *******************************************************
    if "name" not in request.json or request.json["name"] == "":
        error["error"]["name"] = "Name field is required"

    # ********************************************************
    # Email field is required
    # *******************************************************
    if "email" not in request.json or request.json["email"] == "":
        error["error"]["email"] = "Email field is required"

    # *************************************************************
    # Invalid value, Year must be between 1900 and 2000, inclusive.
    # *************************************************************
    if "year" not in request.json or request.json["year"] == "":
        error["error"]["year"] = "The year field is required."
    elif int(request.json["year"]) < 1900 or int(request.json["year"]) > 2000:
        error["error"]["year"] = "Year must be between 1900 and 2000, inclusive"

    # ********************************************************
    # Invalid value, must be one of: red, green, orange, blue!
    # *******************************************************
    color_list = ["red", "blue", "green", "orange"]

    if "color" not in request.json or request.json["color"] == "":
        error["error"]["color"] = "The color field is required."
    elif request.json["color"].lower() not in color_list:
        error["error"]["color"] = "Invalid value, must be one of: red, green, orange, blue"

    if len(error["error"]) != 0:
        return jsonify(error)

    year = request.json["year"]
    rand_num = random.randint(1, 100)

    res_num = requests.get(f"http://numbersapi.com/{rand_num}/year")
    res_year = requests.get(f"http://numbersapi.com/{year}/year")

    return {
        "num": {
            "fact": f"{res_num.text}",
            "num": rand_num
        },
        "year": {
            "fact": f"{res_year.text}",
            "year": year
        }}
