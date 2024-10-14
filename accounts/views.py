# Imports
from flask import Blueprint, render_template

# Create instance of Blueprint
accounts_bp = Blueprint('accounts', __name__, template_folder='templates')

# Load webpages methods

@accounts_bp.route('/registration')
def registration():
    return render_template('accounts/registration.html')

@accounts_bp.route('/login')
def login():
    return render_template('accounts/login.html')

@accounts_bp.route('/account')
def account():
    return render_template('accounts/account.html')