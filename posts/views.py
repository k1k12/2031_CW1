# Imports
from flask import Blueprint, render_template

# Create instance of Blueprint
posts_bp = Blueprint('posts', __name__, template_folder='templates')

# Load webpages methods

@posts_bp.route('/create')
def registration():
    return render_template('posts/create.html')

@posts_bp.route('/posts')
def login():
    return render_template('posts/posts.html')

@posts_bp.route('/update')
def account():
    return render_template('posts/update.html')