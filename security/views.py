# Imports
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import desc
from config import User, logging
from wrappers.roles_required import roles_required
# Create instance of Blueprint
security_bp = Blueprint('security', __name__, template_folder='templates')

# Load webpages methods

@security_bp.route('/security')
@login_required
@roles_required('sec_admin')
def security():
    with open('security.log', 'r') as file:
        file = file.readlines()
    all_users = User.query.order_by(desc('id')).all()
    return render_template('security/security.html', users=all_users, loggers=file)
