# Imports
from flask import Flask, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
import secrets

# imports pt 4

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime

# Imports pt 11
import pyotp
from flask_qrcode import QRcode

# Imports pt 12
from flask_login import LoginManager, UserMixin

# Define app

app = Flask(__name__)
app.debug = True

# Create secret key for client server interaction

app.config['SECRET_KEY'] = secrets.token_hex(16)

# Widen DB admin page view / PT 11
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

# Create config attributes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csc2031blog.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create reCAPTCHA keys

app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lcefo8qAAAAAJ3mwVv8jeehCR67ZQCFmwL9Oe-0'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lcefo8qAAAAAME-BjaTPB0X_nUO5snj8yfOdAmb'

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

# Create Migrate object

migrate = Migrate(app, db)

# Define QR code
qrcode = QRcode(app)

########## Login manager ##########

# Define login manager
login_manager = LoginManager()

# Initialise application
login_manager.init_app(app)
login_manager.login_view = 'accounts.login'
login_manager.login_message = 'Please login to acess CSC2031 blog.'
login_manager.login_message_category = 'info'

# User loader function
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# DB tables

class Post(db.Model):
    __tablename__ = 'posts'
    # Declare attributes of post
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    user = db.relationship("User", back_populates="posts")

    # Define constructor class
    def __init__(self, title, body):
        self.created = datetime.now()
        self.title = title
        self.body = body
        # self.current_user = current_user

    def update(self, title, body):
        self.created = datetime.now()
        self.title = title
        self.body = body
        # self.current_user = current_user
        db.session.commit()

# PT 11 / add MFA key
# PT 12 / ass user authentication

# Users table 
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # Store MFA key and whether enabled
    mfa_key = db.Column(db.String(100), unique=True)
    uri = db.Column(db.String(100), unique=True)
    mfa_enabled = db.Column(db.Boolean(), nullable=False, default=False)

    # Store whether a user is active
    active = db.Column(db.Boolean(), nullable=False, default=False)

    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

    # User posts
    posts = db.relationship("Post", order_by=Post.id, back_populates="user")

    # Constructor method / pt 11 add mfa details
    def __init__(self, email, firstname, lastname, phone, password, mfa_key, mfa_enabled):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = password
        # Store MFA key and whether enabled
        self.mfa_key = mfa_key
        self.mfa_enabled = mfa_enabled
        self.uri = str(pyotp.totp.TOTP(mfa_key).provisioning_uri(self.email, "csc2031"))
        self.active = False

    # Check if login password = submitted password / part 7
    def verify_password(self, submitted_password):
        return self.password == submitted_password

    # Check if login password = submitted password / part 7
    def verify_mfa_pin(self, submitted_pin):
        return pyotp.TOTP(self.mfa_key).verify(submitted_pin)

    # Returns the users idd
    def get_id(self):
        return self.id

    # Returns whether a user is currently active
    @property
    def is_active(self):
        return self.active

# Db admin page template

class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for('index')       

# Override model view class with post view

class PostView(ModelView):
    column_display_pk = True  
    column_hide_backrefs = False
    column_list = ('id', 'userid', 'created', 'title', 'body', 'user')

    # Update creation
    def update(self, title, body):
        self.created = datetime.now()
        self.title = title
        self.body = body
        db.session.commit()

# Create UserView class
class UserView(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'email', 'password', 'firstname', 'lastname', 'phone', 'mfa key', 'mfa enabled', 'posts')

# Create admin instance
admin = Admin(app, name='DB Admin', template_mode='bootstrap4')

# Remove link to db admin home
admin._menu = admin._menu[1:] 

# Add link to blog home page
admin.add_link(MainIndexLink(name='Home Page'))

# To view data on posts table
admin.add_view(PostView(Post, db.session))

# To view data on users table
admin.add_view(UserView(User, db.session))

## Implement rate limiter PT 10

# Imports for rate limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create default limiter
limiter = Limiter(
    app=app,
    # key_func is set to local host
    key_func=get_remote_address,
    # 500 calls per day limit
    default_limits=["500 / day"]
)

# Imports for blueprints
from accounts.views import accounts_bp
from posts.views import posts_bp
from security.views import security_bp

# Register blueprints

app.register_blueprint(accounts_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(security_bp)


