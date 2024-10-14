# Imports

from config import app
from flask import render_template

# Load webpage into browsr
@app.route('/')
def index():
    return render_template('index.html')

# Main method
if __name__ == '__main__':
    app.run()