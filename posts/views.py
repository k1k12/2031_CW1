# Imports + pt 5
from flask import Blueprint, render_template, flash, url_for, redirect
# import flask_login
from config import db, Post
from posts.forms import PostForm
from sqlalchemy import desc
# Pt 12
from flask_login import current_user

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
        new_post = Post(user=current_user, userid=current_user.get_id(), title=form.title.data, body=form.body.data)
        # Add new post to db
        db.session.add(new_post)
        db.session.commit()
        # Show user success message
        flash('Post created', category='success')
        # Redirected to view posts
        return redirect(url_for('posts.posts'))
    # Render with appropriate message
    return render_template('posts/create.html', form=form, user=current_user)

@posts_bp.route('/posts')
def posts():
    # Posts retrieved from database 
    all_posts = Post.query.order_by(desc('id')).all()
    return render_template('posts/posts.html', posts=all_posts, user=current_user)

# Including ID value (int) and allow handling of GET and POST requests
@posts_bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    # Post queried from db Post table
    post_to_update = Post.query.filter_by(id=id).first()

    # If does not exist
    if not post_to_update:
        return redirect(url_for('posts.posts'))

    # Initialise form
    form = PostForm()

    # Check valid
    if form.validate_on_submit():
        post_to_update.update(title=form.title.data, body=form.body.data)
        # Show success message
        flash('Post updated', category='success')
        return redirect(url_for('posts.posts'))

    # Pass to update
    form.title.data = post_to_update.title
    form.body.data = post_to_update.body
    return render_template('posts/update.html', form=form, user=current_user)

# Add delete route
@posts_bp.route('/<int:id>/delete')
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    flash('Post deleted', category='success')
    return redirect(url_for('posts.posts'))