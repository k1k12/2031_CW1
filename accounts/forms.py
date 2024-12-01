# Imports pt 6
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

# Registration class
class RegistrationForm(FlaskForm):

    
    def __init__(self):
        return None
    