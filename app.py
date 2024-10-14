# Imports

from config import app
from flask import render_template

# Load webpage 'index' into browser
@app.route('/')
def index():
    return render_template('home/index.html')

# Load webpage 'registration' into browser
@app.route('/registration')
def registration():
    return render_template('accounts/registration.html')

# Main method
if __name__ == '__main__':
    app.run()