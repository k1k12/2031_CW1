# Imports
from flask import Blueprint, render_template, flash, redirect, url_for, session
from accounts.forms import RegistrationForm, LoginForm
from config import User, db, limiter
from flask_login import login_required, login_user, logout_user, current_user
# Imports pt 10
from markupsafe import Markup

# Create instance of Blueprint
accounts_bp = Blueprint('accounts', __name__, template_folder='templates')

# Create constants
MAX_LOGIN_ATTEMPTS = 3
UNAUTHORISED_WARNING = 'You are not authorised to access this page.'

# Load webpages methods

@accounts_bp.route('/registration', methods=['GET','POST'])
def registration():
    # Prevent logged in users from accessing
    if current_user.is_authenticated:
        flash('Please logout to access registration page.', category='danger')
        return render_template('home/index.html')
                        
    form = RegistrationForm()
    # If user valid
    if form.validate_on_submit():
        # Check account doesn't already exist (same email)
        if User.query.filter_by(email=form.email.data).first():
            # TO DO: Add link to login page (in msg in html or markup)
            flash('An account with this email already exists.', category='danger')
            return render_template('accounts/login.html', form=form)
        
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

# Add limiter
@accounts_bp.route('/login', methods=['GET','POST'])
@limiter.limit('20 / minute')
def login():

    # Prevent logged in users from accessing
    if current_user.is_authenticated:
        flash('Please logout to access login page.', category='danger')
        return render_template('home/index.html')
     
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
        # Ugly fix this
        if not user or not user.verify_password(form.password.data) or not user.verify_mfa_pin(form.mfa_pin.data):
            # Check if have done MFA
            if user and user.verify_password(form.password.data):
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
                db.session.commit()
            # Login user
            login_user(user)
            flash('Login successful.', category='success')
            # Redirect based on user role
            if user.role == 'db_admin':
                return redirect(url_for('admin.index'))
            if user.role == 'sec_admin':
                return redirect(url_for('security.security'))
            else:
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
@login_required
def account():
    return render_template('accounts/account.html', user=current_user)

@accounts_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', category='success')
    return render_template('home/index.html')