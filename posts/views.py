# Imports + pt 5
from flask import Blueprint, render_template, flash, url_for, redirect
from config import db, Post
from posts.forms import PostForm
from sqlalchemy import desc

# Create instance of Blueprint
posts_bp = Blueprint('posts', __name__, template_folder='templates')

# Load webpages methods

@posts_bp.route('/create', methods=('GET', 'POST'))
def create():
    # Create form instance
    form = PostForm()
    # Check valid
    if form.validate_on_submit():
        # New instance of post model created
        new_post = Post(title=form.title.data, body=form.body.data)
        # Add new post to db
        db.session.add(new_post)
        db.session.commit()
        # Show user success message
        flash('Post created', category='success')
        # Redirected to view posts
        return redirect(url_for('posts.posts'))
    # Render with appropriate message
    return render_template('posts/create.html', form=form)

@posts_bp.route('/posts')
def posts():
    # Posts retrieved from database 
    all_posts = Post.query.order_by(desc('id')).all()
    return render_template('posts/posts.html', posts=all_posts)

@posts_bp.route('/update')
def update():
    return render_template('posts/update.html')