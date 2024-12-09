# Imports
from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Create instance of Blueprint
security_bp = Blueprint('security', __name__, template_folder='templates')

# Load webpages methods

@security_bp.route('/security')
@login_required
def security():

    # Prevent unauthorised users from accessing
    if current_user.role != 'sec_admin':
        return render_template('errors/error403.html')
     
    return render_template('security/security.html')
