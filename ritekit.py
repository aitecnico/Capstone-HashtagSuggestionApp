import requests

client_id = '8a385f6168ea69789bee55e54a14ef4fbd19bb662ece'


#*****************
#GET Auto-Hashtag
#*****************
response = requests.get("https://api.ritekit.com/v1/stats/auto-hashtag?post=Is%20artificial%20intelligence%20the%20future%20of%20customer%20service%3F&maxHashtags=2&hashtagPosition=auto", 
                params={'client_id': client_id, 'post': 'Yoga', 'maxHashtags': '2', 'HashtagPosition': 'auto'})


#******************
#GET Hashtag Stats
#******************
# response = requests.get("https://api.ritekit.com/v1/stats/multiple-hashtags?tags=jobs%2CChello", 
#                 params={'client_id': client_id, 'tags': 'jobs%2CChello'})


#*******************************
#GET Hashtag Suggestion for Text
#*******************************
# response = requests.get("https://api.ritekit.com/v1/stats/hashtag-suggestions?text=seo", 
#                 params={'client_id': client_id, 'text': 'DJ'})









