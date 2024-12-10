# Imports pt 6
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp, Email

# Registration class
class RegistrationForm(FlaskForm):

    # Validate fields 
    firstname = StringField('First Name',
                            validators=
            [DataRequired(),
             Regexp('^[a-zA-Z-]*$', message='First name must only contain letters or hyphens.')
             ])
    lastname = StringField('Last Name',
                           validators=
            [DataRequired(),
             Regexp('^[a-zA-Z-]*$', message='Last name must only contain letters or hyphens.')
             ])
    email = StringField('Email Address',
                        validators=
            [DataRequired(),
            Email()
            ])
    phone = StringField('Phone Number',
                        validators=
            [DataRequired(),
            #  E.164 standard
             Regexp(r'(?:02\d-\d{8}|(?:011\d|01\d1)-\d{7}|01\d{3}-\d{5,6})', message='Invalid phone number: please adhere to E.164 standards.')
            
            ])
 
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
    submit = SubmitField('Submit')

# Login Form class / part 7
class LoginForm(FlaskForm):
    # Validate fields
    email = StringField('Email Address',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    # MFA pin / part 11
    mfa_pin = StringField('MFA Code',validators=[DataRequired()])
    # reCAPTCHA / part 8 
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
