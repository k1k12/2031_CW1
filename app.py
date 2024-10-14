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

# Load webpage 'login' into browser
@app.route('/login')
def login():
    return render_template('accounts/login.html')

# Load webpage 'account' into browser
@app.route('/account')
def account():
    return render_template('accounts/account.html')

# Load webpage 'posts' into browser
@app.route('/posts')
def posts():
    return render_template('posts/posts.html')

# Load webpage 'create' into browser
@app.route('/create')
def create():
    return render_template('posts/create.html')

# Load webpage 'update' into browser
@app.route('/update')
def update():
    return render_template('posts/update.html')

# Load webpage 'security' into browser
@app.route('/security')
def security():
    return render_template('security/security.html')

# Main method
if __name__ == '__main__':
    app.run()