# Imports
from config import app
from flask import render_template

# Load webpage 'index' into browser
@app.route('/')
def index():
    return render_template('home/index.html')

# Handle error 429 (too many requests)
@app.errorhandler(429)
def error_handler(e):
    return render_template('errors/error429.html'), 429

# Handle error 429 (too many requests)
@app.errorhandler(403)
def error_handler(e):
    return render_template('errors/error403.html'), 403

# Main method
if __name__ == '__main__':
    app.run()