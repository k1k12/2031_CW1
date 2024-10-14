# Imports
from flask import Blueprint, render_template

# Create instance of Blueprint
security_bp = Blueprint('security', __name__, template_folder='templates')

# Load webpages methods

@security_bp.route('/security')
def registration():
    return render_template('security/security.html')
