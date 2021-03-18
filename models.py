from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    # password =db.Column() Search about Bcrypt 



class Hashtag(db.Model):
    """Hashtag."""

    __tablename__= "hashtags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hashtag = db.Column(db.Text, nullable=False)

# *****************************
# OUTPUTS JSON
# *****************************
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'email': self.email,
    #     }

# *****************************

    # def __repr__(self):
    #     return f"<Hashtag{self.id} name={self.name} email={self.email}>"
