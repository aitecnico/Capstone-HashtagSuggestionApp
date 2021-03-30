from flask import Flask, jsonify, render_template, request, flash, redirect, session
from secrets import API_SECRET_KEY
from forms import UserForm, LoginForm, HashtagForm
import requests
import random
from models import db, connect_db, Hashtag, User
from sqlalchemy.exc import IntegrityError

# *****************************
# PYTHON API REQUEST
# *****************************
# API_BASE_URL = "http://numbersapi.com/random?"

client_id = API_SECRET_KEY

API_BASE_URL = "https://api.ritekit.com/v1"

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashtag_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)


@ app.route("/")
def homepage():
    """Show homepage."""
    hashtags = Hashtag.query.all()
    return render_template("index.html", hashtags=hashtags)


def get_results(hashtag):
    res = requests.get(f"{API_BASE_URL}/stats/hashtag-suggestions?text=seo", 
                    params={'client_id': client_id,'text': hashtag})
    data = res.json()
    hash = data["data"][1]['hashtag']
    tweets = data["data"][1]['tweets']
    results = {'hash': hash, 'tweets' : tweets}
    return results
    


@app.route('/hashtagsuggestion')
def get_hashtag():
    hashtag = request.args["hashtag"]
    results = get_results(hashtag)
    return render_template("index.html", results=results)




@app.route('/register', methods=['GET', 'POST'])
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
            return render_template('register.html', form=form)

        session['user_id'] = new_user.id
        flash('Welcome! You Have Successfully Created Your Account!', "success")
        return redirect('/hashtags')

    return render_template('register.html', form=form)




@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            flash(f"Welcome Back, {user.username}!", "success")
            session ['user_id'] = user.id
            return redirect('hashtags')
        else:
            form.username.errors = ['Invalid username/password']
          
    return render_template('/login.html', form=form)


# Need to make it a post route
@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Visit us again!", "info")
    return redirect('/')



@app.route('/hashtags', methods=['GET', 'POST'])
def show_hashtags():
    if "user_id" not in session:
        flash('Please Login First!', "danger")
        return redirect('/')
    form = HashtagForm()
    all_hashtags = Hashtag.query.all()
    if form.validate_on_submit():
        text = form.text.data
        new_hashtag = Hashtag(text=text, user_id=session['user_id'])
        db.session.add(new_hashtag)
        db.session.commit()
        flash('Hashtag Created!' "success")
        return redirect('/hashtags')
    
    
    return render_template("hashtags.html", form=form, hashtags=all_hashtags)



@app.route('/hashtags/<int:id>', methods=["POST"])
def delete_hashtag(id):
        """Delete hashtag"""
        if "user_id" not in session:
            flash("Please login first!", "danger")
            return redirect('/login')
        hashtag = Hashtag.query.get_or_404(id)
        if hashtag.user_id == session ["user_id"]:
            db.session.delete(hashtag)
            db.session.commit()
            flash("Hashtag deleted", "info")
            return redirect('/hashtags')
        flash ("You don't have permission to do that!", "danger")
        return redirect('/hashtags')


    # text = request.args["min=1&max=100&json"]
    # ****res = requests.get(f"{API_BASE_URL}/min=1&max=100&json")


# *****************************
# TEST in TERMINAL IF JSON IS RESPONDING
# *****************************
    # import pdb
    # pdb.set_trace()
    # data = res.json()
    # # number = data["text"]
    # # print('*******************************')
    # # print(data)
    # answers = data
    # return render_template("index.html", answers=answers)


# *********************************************************
# RESTFUL LUCKYNUMBERS JSON API (GET LIST ALL Luckynumbers)
# **********************************************************
# @ app.route('/api/luckynumbers')
# def list_luckynumbers():
#     """Returns JSON w/ all todos"""
#     all_luckynumbers = [luckynumber.serialize()
#                         for luckynumber in Luckynumber.query.all()]
#     return jsonify(luckynumbers=all_luckynumbers)

@app.route('/api/hashtags')
def list_hashtags():
    all_hashtags = [hashtag.serialize() for hashtag in Hashtag.query.all()]
    return jsonify(hashtags=all_hashtags)



# *****************************
# RESTFUL LUCKYNUMBERS JSON API (GET 1 ID of Luckynumbers)
# *****************************


# @ app.route('/api/luckynumbers/<int:id>')
# def get_luckynumber(id):
#     luckynumber = Luckynumber.query.get_or_404(id)
#     return jsonify(luckynumber=luckynumber.serialize())

@app.route('/api/hashtags/<int:id>')
def get_onehashtag(id):
    hashtag = Hashtag.query.get_or_404(id)
    return jsonify(hashtag=hashtag.serialize())




# *****************************
# RESTFUL LUCKYNUMBERS JSON API (POST CREATE Luckynumbers)
# *****************************
# @ app.route('/api/luckynumbers', methods=["POST"])
# def create_luckynumber():
#     new_luckynumber = Luckynumber(
#         name=request.json["name"], email=request.json["email"], year=request.json["year"], color=request.json["color"])
#     db.session.add(new_luckynumber)
#     db.session.commit()
#     response_json = jsonify(luckynumber=new_luckynumber.serialize())
#     return (response_json, 201)

@app.route('/api/hashtags', methods=["POST"])
def create_hashtag():
    new_hashtag = Hashtag(text=request.json["text"])
    db.session.add(new_hashtag)
    db.session.commit()
    response_json = jsonify(hashtag=new_hashtag.serialize())
    return (response_json, 201)


#*********************************
#RESTFUL HASHTAG JSON API (PATCH)
#*********************************
@app.route('/api/hashtags/<int:id>', methods=["PATCH"])
def update_hashtag(id):
    hashtag = Hashtag.query.get_or_404(id)
    hashtag.text = request.json.get('text', hashtag.text)
    db.session.commit()
    return jsonify(hashtag=hashtag.serialize())


#*********************************
#RESTFUL HASHTAG JSON API (DELETE)
#*********************************
@app.route('/api/hashtags/<int:id>', methods=["DELETE"])
def delete_apihashtag(id):
    hashtag = Hashtag.query.get_or_404(id)
    db.session.delete(hashtag)
    db.session.commit()
    return jsonify(message="deleted")






# # *****************************
# # JSON body with the following information
# # If the user failed to provide valid data
# # It's own API
# # *****************************
# @ app.route('/api/get-lucky-num', methods=["POST"])
# def create_lucknum():
#     return_value = {"error": {}, "mydata": request.json}
#     print(request.json)
#     error = {"error": {}}

#     # ******************************************************
#     # Individual Error if specific JSON is not recieved
#     # ******************************************************

#     # ********************************************************
#     # Name field is required
#     # *******************************************************
#     if "name" not in request.json or request.json["name"] == "":
#         error["error"]["name"] = "Name field is required"

#     # ********************************************************
#     # Email field is required
#     # *******************************************************
#     if "email" not in request.json or request.json["email"] == "":
#         error["error"]["email"] = "Email field is required"

#     # *************************************************************
#     # Invalid value, Year must be between 1900 and 2000, inclusive.
#     # *************************************************************
#     if "year" not in request.json or request.json["year"] == "":
#         error["error"]["year"] = "The year field is required."
#     elif int(request.json["year"]) < 1900 or int(request.json["year"]) > 2000:
#         error["error"]["year"] = "Year must be between 1900 and 2000, inclusive"

#     # ********************************************************
#     # Invalid value, must be one of: red, green, orange, blue!
#     # *******************************************************
#     color_list = ["red", "blue", "green", "orange"]

#     if "color" not in request.json or request.json["color"] == "":
#         error["error"]["color"] = "The color field is required."
#     elif request.json["color"].lower() not in color_list:
#         error["error"]["color"] = "Invalid value, must be one of: red, green, orange, blue"

#     if len(error["error"]) != 0:
#         return jsonify(error)

#     year = request.json["year"]
#     rand_num = random.randint(1, 100)

#     res_num = requests.get(f"http://numbersapi.com/{rand_num}/year")
#     res_year = requests.get(f"http://numbersapi.com/{year}/year")

#     return {
#         "num": {
#             "fact": f"{res_num.text}",
#             "num": rand_num
#         },
#         "year": {
#             "fact": f"{res_year.text}",
#             "year": year
#         }}
