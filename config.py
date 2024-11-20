# Imports

from flask import Flask, url_for
from accounts.views import accounts_bp
from posts.views import posts_bp
from security.views import security_bp

# imports pt 4

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
import secrets

# Define app

app = Flask(__name__)
app.debug = True

# Create secret key for client server interaction

app.config['SECRET_KEY'] = secrets.token_hex(16)

# Create config attributes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csc2031blog.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Create metadata variable 

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

# Create database object

db = SQLAlchemy(app, metadata=metadata)

# Creaye Migrate object

migrate = Migrate(app, db)

# DB tables

class Post(db.Model):
    __tablename__ = 'posts'
    # Declare attributes of post
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    # Define constructor class
    def __init__(self, title, body):
        self.created = datetime.now()
        self.title = title
        self.body = body

# Db admin page template

class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for('index')       


# Override model view class with post view

class PostView(ModelView):
    column_display_pk = True  
    column_hide_backrefs = False
    column_list = ('id', 'created', 'title', 'body')

# Create admin instance
admin = Admin(app, name='DB Admin', template_mode='bootstrap4')

# Remove link to db admin home
admin._menu = admin._menu[1:] 

# Add link to blog home page
admin.add_link(MainIndexLink(name='Home Page'))

# To view data on posts table
admin.add_view(PostView(Post, db.session))

# Register blueprints

app.register_blueprint(accounts_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(security_bp)


