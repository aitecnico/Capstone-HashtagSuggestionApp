from models import db, connect_db, Hashtag
from app import app

db.drop_all()
db.create_all()

Hashtag.query.delete()

users = [
    User(name="William Fayette", email="afflatus@gmail.com", hashtags="hashtagtest")
]
db.session.add_all(hashtags)
db.session.commit()
