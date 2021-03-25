from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    """Form for adding playlists."""

    username = StringField('Name', validators= [InputRequired()])
    email = StringField('Email', validators= [InputRequired()])
    password = PasswordField('Password', validators= [InputRequired()])
    
class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class HashtagForm(FlaskForm):
    """Hashtag form"""

    text = StringField('Hashtag Text', validators=[InputRequired()])