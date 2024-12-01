# Imports
from flask import Blueprint, render_template, flash, redirect, url_for
from accounts.forms import RegistrationForm, LoginForm
from config import User, db

# Create instance of Blueprint
accounts_bp = Blueprint('accounts', __name__, template_folder='templates')

# Load webpages methods

@accounts_bp.route('/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    # If valid
    if form.validate_on_submit():
        # Check account doesn't already exist (same email)
        if User.query.filter_by(email=form.email.data).first():
            flash('An account with this email already exists.', category="danger")
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
        flash('Account Successfully Created', category='success')
        return redirect(url_for('accounts.login'))
    return render_template('accounts/registration.html', form=form)

@accounts_bp.route('/login', methods=['GET','POST'])
def login():
    # Create instance of LoginForm
    form = LoginForm()

    # Validate login form instance 
    if form.validate_on_submit():
        # Check account doesn't already exist (same email)
        user = User.query.filter_by(email=form.email.data).first()
        # Could merge into one......
        if not user:
            flash('Email credential incorrect.', category="danger")
            return redirect(url_for('accounts.login'))
        elif not user.verify_password(form.password.data):
            flash('Login credentials incorrect.', category="danger")
            return redirect(url_for('accounts.login'))
        elif user.verify_password(form.password.data):
            flash('Login successful.', category="success")
            return redirect(url_for('posts.posts'))

    return render_template('accounts/login.html', form=form)

@accounts_bp.route('/account')
def account():
    return render_template('accounts/account.html')