# Imports
from config import app
from flask import render_template
from flask_login import current_user

# Load webpage 'index' into browser
@app.route('/')
def index():
    return render_template('home/index.html', user=current_user)

# Handle error 429 (too many requests)
@app.errorhandler(429)
def error_handler(e):
    return render_template('accounts/error429.html'), 429

# Main method
if __name__ == '__main__':
    app.run()