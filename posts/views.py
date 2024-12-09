# Imports
from flask import Blueprint, render_template, flash, url_for, redirect
from config import db, Post, logger
from posts.forms import PostForm
from sqlalchemy import desc
from flask_login import current_user, login_required
from wrappers.roles_required import roles_required

# Create instance of Blueprint
posts_bp = Blueprint('posts', __name__, template_folder='templates')

# Load webpages methods

@posts_bp.route('/create', methods=('GET', 'POST'))
@login_required
@roles_required('end_user')
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
        # Log event
        logger.warning('User: {}, Role: {}, Post ID: {}, IP Address: {}, MSG: Post successfully created.'.format(current_user.email, current_user.role, new_post.id, current_user.log.latest_ip))
        # Show user success message
        flash('Post created', category='success')
        # Redirected to view posts
        return redirect(url_for('posts.posts'))
    # Render with appropriate message
    return render_template('posts/create.html', form=form)

@posts_bp.route('/posts')
@login_required
@roles_required('end_user')
def posts():
    # Posts retrieved from database 
    all_posts = Post.query.order_by(desc('id')).all()
    return render_template('posts/posts.html', posts=all_posts)

# Including ID value (int) and allow handling of GET and POST requests
@posts_bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
@roles_required('end_user')
def update(id):
    # Post queried from db Post table
    post_to_update = Post.query.filter_by(id=id).first()

    # If does not exist
    if not post_to_update:
        return redirect(url_for('posts.posts'))
    
    # Prevent non author users updating post
    if current_user.id != post_to_update.userid:
        flash('You can only update your own posts.', category='danger')
        return redirect(url_for('posts.posts'))
 
    # Initialise form
    form = PostForm()

    # Check valid
    if form.validate_on_submit():
        post_to_update.update(title=form.title.data, body=form.body.data)
        
        # Log event
        logger.warning('User: {}, Role: {}, Post ID: {}, Post Author: {}, IP Address: {}, MSG: Post successfully updated.'.format(current_user.email, current_user.role, post_to_update.id, post_to_update.user.email, current_user.log.latest_ip))

        # Show success message
        flash('Post updated', category='success')
        return redirect(url_for('posts.posts'))

    # Pass to update
    form.title.data = post_to_update.title
    form.body.data = post_to_update.body
    return render_template('posts/update.html', form=form)

# Add delete route
@posts_bp.route('/<int:id>/delete')
@login_required
@roles_required('end_user')
def delete(id):
    # Identify post to delete
    post_to_delete = Post.query.filter_by(id=id).first()

    # Prevent non author users deleting post
    if current_user.id != post_to_delete.userid:
        flash('You can only delete your own posts.', category='danger')
        return redirect(url_for('posts.posts'))

    # Log event
    logger.warning('User: {}, Role: {}, Post ID: {}, Post Author: {}, IP Address: {}, MSG: Post successfully deleted.'.format(current_user.email, current_user.role, post_to_delete.id, post_to_delete.user.email, current_user.log.latest_ip))

    Post.query.filter_by(id=id).delete()
    db.session.commit()
    
    flash('Post deleted', category='success')
    
    return redirect(url_for('posts.posts'))