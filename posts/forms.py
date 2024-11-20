# Imports pt 5

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# Class PostForm

class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired()]) # Title of post, single string line
    body = TextAreaField(validators=[DataRequired()]) # Multi line area field for body text
    submit = SubmitField() # Form submit button

