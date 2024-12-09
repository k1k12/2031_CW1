# Imports
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from wrappers.roles_required import roles_required
# Create instance of Blueprint
security_bp = Blueprint('security', __name__, template_folder='templates')

# Load webpages methods

@security_bp.route('/security')
@login_required
@roles_required('sec_admin')
def security():
    return render_template('security/security.html')
