# Imports

from flask import Flask
from accounts.views import accounts_bp
from posts.views import posts_bp
from security.views import security_bp

# imports pt 4

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime
from datetime import datetime

# Define app

app = Flask(__name__)
app.debug = True

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

# Register blueprints

app.register_blueprint(accounts_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(security_bp)


