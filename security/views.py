# Imports
from flask import Blueprint, render_template
from flask_login import current_user

# Create instance of Blueprint
security_bp = Blueprint('security', __name__, template_folder='templates')

# Load webpages methods

@security_bp.route('/security')
def security():
    return render_template('security/security.html', user=current_user)
