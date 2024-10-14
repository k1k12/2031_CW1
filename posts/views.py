# Imports
from flask import Blueprint, render_template

# Create instance of Blueprint
posts_bp = Blueprint('posts', __name__, template_folder='templates')

# Load webpages methods

@posts_bp.route('/create')
def create():
    return render_template('posts/create.html')

@posts_bp.route('/posts')
def posts():
    return render_template('posts/posts.html')

@posts_bp.route('/update')
def update():
    return render_template('posts/update.html')