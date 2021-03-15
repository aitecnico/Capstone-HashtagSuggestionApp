from wtforms import StringField, FloatField
from flask_wtf import FlaskForm 
import wtforms.validators import InputRequired,


class LuckynumberForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField('Name', validators= InputRequired()])
    email = StringField('Email', validators= InputRequired()]))
    year = StringField('Year', validators= InputRequired()])))
    color = StringField('Color', validators= InputRequired()])))
