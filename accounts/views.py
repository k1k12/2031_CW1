# Imports
from flask import Blueprint, render_template, flash, redirect, url_for, session
from accounts.forms import RegistrationForm, LoginForm
from config import User, db
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
    # If valid
    if form.validate_on_submit():
        # Check account doesn't already exist (same email)
        if User.query.filter_by(email=form.email.data).first():
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
        flash('Account successfully created', category='success')
        return redirect(url_for('accounts.login'))
    
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

    # Define var to represent attempts remaining
    # attempts_remaining = (3 - session.get('num_attempts'))

    # Validate login form instance 
    if form.validate_on_submit():
        # Define a var to represent finding user in db
        user = User.query.filter_by(email=form.email.data).first()
        # Check user exists and passwords match
        if not user or not user.verify_password(form.password.data):
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
        elif user.verify_password(form.password.data):
            # Reset session key
            session['num_attempts'] = 0
            # Success msg
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