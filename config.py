# Imports
from flask import Flask, redirect, url_for, flash, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
import secrets
import logging

# imports pt 4

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime

# Imports pt 11
import pyotp
from flask_qrcode import QRcode

# Imports pt 12
from flask_login import LoginManager, UserMixin, current_user

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

# Login manager 

# Define login manager
login_manager = LoginManager()

# Initialise application
login_manager.login_view = 'accounts.login'
login_manager.login_message = 'Please login to access CSC2031 blog.'
login_manager.login_message_category = 'info'

login_manager.init_app(app)

# Logger set up

# Define logger 
logger = logging.getLogger('security_logger')
handler = logging.FileHandler('security.log', 'w')
# Set logging level to DEBUG
handler.setLevel(logging.WARNING)
# Create formatter
formatter = logging.Formatter('%(asctime)s --> %(message)s', '%d/%m/%Y %I:%M:%S %p')
# Set formatter
handler.setFormatter(formatter)
# Pass handler to logger
logger.addHandler(handler)

# Create database object

db = SQLAlchemy(app, metadata=metadata)

# Create Migrate object

migrate = Migrate(app, db)

# Define QR code
qrcode = QRcode(app)

# User loader function
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# DB tables

class Post(db.Model):
    __tablename__ = 'posts'

    # set CRUD operations
    can_create = False
    can_edit = False
    can_delete = False
    
    # Declare attributes of post
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    user = db.relationship("User", back_populates="posts")

    # Define constructor class
    def __init__(self, title, body, userid, user):
        self.created = datetime.now()
        self.title = title
        self.body = body
        self.userid = userid
        self.user = user

    def update(self, title, body):
        self.created = datetime.now()
        self.title = title
        self.body = body
        db.session.commit()

# PT 11 / add MFA key
# PT 12 / add user authorisation

# Users table 
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # set CRUD operations
    can_create = False
    can_edit = False
    can_delete = False
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # User role
    role = db.Column(db.String(100), nullable=False, default='end_user')

    # Store MFA key and whether enabled
    mfa_key = db.Column(db.String(100), nullable=True)
    mfa_enabled = db.Column(db.Boolean(), nullable=False, default=False)

    # Store whether a user is active
    active = db.Column(db.Boolean(), nullable=False, default=False)

    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

    # Define relationships
    posts = db.relationship("Post", order_by=Post.id, back_populates="user")
    log = db.relationship("Log", uselist=False, back_populates="user")
    
    # Constructor method
    def __init__(self, email, firstname, lastname, phone, password):
        # CRUD operations
        # self.can_create = False

        # User details
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = password
        # Store MFA key and whether enabled
        self.mfa_key = pyotp.random_base32()
        self.mfa_enabled = False
        self.uri = str(pyotp.totp.TOTP(self.mfa_key).provisioning_uri(self.email, "csc2031"))
        # User role
        self.role = 'end_user'

    # Check if login password = submitted password
    def verify_password(self, submitted_password):
        return self.password == submitted_password

    # Check if login pin = submitted pin
    def verify_mfa_pin(self, submitted_pin):
        return pyotp.TOTP(self.mfa_key).verify(submitted_pin)

    # Generate user log
    def generate_log(self):
        log = Log(self.id, self)
        db.session.add(log)
        db.session.commit()

# Users table 
class Log(db.Model):
    __tablename__ = 'logs'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    # User details
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Account creation details
    reg_time = db.Column(db.DateTime, nullable=False)
    latest_login = db.Column(db.DateTime, nullable=True)
    previous_login = db.Column(db.DateTime, nullable=True)
    # IP details
    latest_ip = db.Column(db.String(100), nullable=True)
    previous_ip = db.Column(db.String(100), nullable=True)
    # Define relationship
    user = db.relationship("User", back_populates="log")

    # Constructor for log
    def __init__(self, userid, user):
        self.userid = userid
        self.user = user
        self.reg_time = datetime.now()
        # self.latest_login = datetime.now()
        # self.latest_ip = request.remote_addr
        # self.previous_ip = request.remote_addr

    def update(self):
        self.previous_login = self.latest_login
        self.latest_login = datetime.now()
        self.previous_ip = self.latest_ip
        self.latest_ip = request.remote_addr
        db.session.commit()

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

    # Ensure user is authenticated
    def is_accessible(self):
        return current_user.get_id() and (current_user.role == 'db_admin')

    # Ensure user is authenticated
    def inacessible_callback(self, name, *kwargs):
        if current_user.get_id():
            return redirect('errors/error403.html')
        flash('Please login before attempting to access this page.')
        return redirect(url_for('accounts.login'))

# Create UserView class
class UserView(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'email', 'password', 'firstname', 'lastname', 'phone', 'mfa key', 'mfa enabled', 'posts')
    
    # Ensure user is authenticated
    def is_accessible(self):
        return current_user.get_id() and (current_user.role == 'db_admin')

    # Ensure user is authenticated
    def inacessible_callback(self, name, *kwargs):
        if current_user.get_id():
            return redirect('errors/error403.html')
        flash('Please login before attempting to access this page.')
        return redirect(url_for('accounts.login'))

# Create LogView class
class LogView(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'userid', 'registered on', 'latest login', 'previous login', 'latest ip', 'previous ip', 'user')
    
    # Ensure user is authenticated
    def is_accessible(self):
        # Change back!
        return current_user.get_id() and (current_user.role == 'db_admin')

    # Ensure user is authenticated
    def inacessible_callback(self, name, *kwargs):
        if current_user.get_id():
            return redirect('errors/error403.html')
        flash('Please login before attempting to access this page.')
        return redirect(url_for('accounts.login'))

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
# To view data on logs table
admin.add_view(LogView(Log, db.session))

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


