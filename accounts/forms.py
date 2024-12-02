# Imports pt 6
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

# Registration class
class RegistrationForm(FlaskForm):

    # Validate fields 
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email Address',validators=[DataRequired()])
    phone = StringField('Phone Number',validators=[DataRequired()])
    # PART 7
    # Check password (p) is 7 < p < 16, checks contains min 1 uppercase char, 1 lowercase char, 1 digit and 1 special char
    password = PasswordField('Password',
                             validators=[
        DataRequired(), 
        Length(min=8, max=15, message ='Password must be between 8 and 15 characters.'),
        Regexp('(?=.*[A-Z])', message='Password must contain an uppercase character.'), 
        Regexp('(?=.*[a-z])', message='Password must contain a lowercase character.'), 
        Regexp('(?=.*\d)', message='Password must contain a digit.'), 
        Regexp('(?=.*\W)', message='Password must contain a special character.')])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField('submit')

# Login Form class / part 7
class LoginForm(FlaskForm):
    # Validate fields 
    email = StringField('Email Address',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    # Add reCAPTCHA for part 8 / 5 MARKS
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')
    
