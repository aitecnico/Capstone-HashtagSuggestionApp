
from flask import Flask
from secrets import API_SECRET_KEY
import requests

client_id = '8a385f6168ea69789bee55e54a14ef4fbd19bb662ece'

API_BASE_URL = "https://api.ritekit.com/v1/stats/hashtag-suggestions?text=seo"

app = Flask(__name__)


@app.route('/hashtagform')
def show_hashtag_form():
    return render_template("hashtag_form.html")




#*******************************
#GET Hashtag Suggestion for Text
#*******************************
# res = requests.get("https://api.ritekit.com/v1/stats/hashtag-suggestions?text=seo", 
#                 params={'client_id': client_id, 'text': 'Apple', 'limit': 5})


# app = flask(__name__)

# @app.route('/')
# def show_hashtag_form():
#     return render_template("hashtag_form.html")

# data = res.json()

# for data in data['data']:
#     print(data['tag'])
#     print(data['tweets'])



#*****************
#GET Auto-Hashtag
#*****************
# res = requests.get("https://api.ritekit.com/v1/stats/auto-hashtag?post=Is%20artificial%20intelligence%20the%20future%20of%20customer%20service%3F&maxHashtags=2&hashtagPosition=auto", 
#                 params={'client_id': client_id, 'post': 'Music', 'maxHashtags': '2', 'HashtagPosition': 'auto'})

# print(response.json())

#******************
#GET Hashtag Stats
#******************
# response = requests.get("https://api.ritekit.com/v1/stats/multiple-hashtags?tags=jobs%2CChello", 
#                 params={'client_id': client_id, 'tags': 'jobs%2CChello'})












