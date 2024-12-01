# Imports pt 6
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

# Registration class
class RegistrationForm(FlaskForm):

    # Validate fields 
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email Address',validators=[DataRequired()])
    phone = StringField('Phone Number',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField('submit')
    

# Login Form class
class LoginForm(FlaskForm):

    # Validate fields 
    email = StringField('Email Address',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('submit')
    
