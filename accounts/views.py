# Imports
from flask import Blueprint, render_template, flash, redirect, url_for, session
from accounts.forms import RegistrationForm, LoginForm
from config import User, db, app
# Imports pt 10
from markupsafe import Markup

# Create instance of Blueprint
accounts_bp = Blueprint('accounts', __name__, template_folder='templates')

# Create constant for login attempts
MAX_LOGIN_ATTEMPTS = 3


# Load webpages methods

@accounts_bp.route('/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    # If user valid
    if form.validate_on_submit():
        # Check account doesn't already exist (same email)
        if User.query.filter_by(email=form.email.data).first():
            # TO DO: Add link to login page (in msg in html or markup)
            flash('An account with this email already exists.', category='danger')
            return render_template('accounts/registration.html', form=form)
        
        # If user isn't taken in db, create new instance to add to db
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        )
        
        # Add new user to db
        db.session.add(new_user)
        db.session.commit()

        # Display success message
        flash('Account successfully created. Please now set up MFA.', category='success')
        return render_template('accounts/mfa.html', key=new_user.mfa_key, qr=new_user.uri)

    return render_template('accounts/registration.html', form=form)

# PART 7 and PART 10
from config import limiter 
# Add limiter for testing
@accounts_bp.route('/login', methods=['GET','POST'])
@limiter.limit('20 / minute')
def login():
    # PART 10 / 5 MARKS
    # Define session key if not already defined
    if not session.get('num_attempts'):
        session['num_attempts'] = 0

    # Create instance of LoginForm
    form = LoginForm()

    # Validate login form instance 
    if form.validate_on_submit():
        # Define a var to represent finding user in db
        user = User.query.filter_by(email=form.email.data).first()
        # Check user exists and passwords match
        if not user or not user.verify_password(form.password.data) or not user.verify_mfa_pin(form.mfa_pin.data):
            # Check if have done MFA
            if not user.mfa_enabled:
                # If not redirect to MFA set up page
                flash('You must set up MFA before you can access your account.', category='danger')
                return render_template('accounts/mfa.html', key=user.mfa_key, qr=user.uri)
            
            # Increment session key by 1
            session['num_attempts'] += 1
            # If max attempts exceeded
            if session['num_attempts'] >= MAX_LOGIN_ATTEMPTS:
                flash(Markup('Maximum number of login attempts exceeded, account locked. <br></br> <a href="/unlock">Click here to unlock account.</a>'))
                # Redirect to login page and hide login form
                return render_template('accounts/login.html')
            # Display warning message if authentication attempts not exceeded
            flash('Login credentials incorrect, {} attempts remaining.'.format((3 - session.get('num_attempts'))), category='danger')
            return redirect(url_for('accounts.login'))
        elif user.verify_password(form.password.data) and user.verify_mfa_pin(form.mfa_pin.data):
            # Reset session key
            session['num_attempts'] = 0
            # Check if user has set up MFA
            if not user.mfa_enabled:
                user.mfa_enabled = True
            flash('Login successful.', category='success')
            return redirect(url_for('posts.posts'))

    return render_template('accounts/login.html', form=form)

# Unlock function that resets key to 0 and redirects to login with form
@accounts_bp.route('/unlock', methods=['GET'])
def unlock():
    # Destroy session key
    session.pop('num_attempts')
    # Rerender page with form
    return redirect(url_for('accounts.login'))

@accounts_bp.route('/account')
def account():
    return render_template('accounts/account.html')
