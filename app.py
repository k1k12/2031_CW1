# Imports

from config import app
from flask import render_template

# Load webpage 'index' into browser
@app.route('/')
def index():
    return render_template('home/index.html')

# Main method
if __name__ == '__main__':
    app.run()