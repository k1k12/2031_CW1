# Imports

from flask import Flask
from accounts.views import accounts_bp
from posts.views import posts_bp
from security.views import security_bp

# Define app

app = Flask(__name__)
app.debug = True

# Register blueprints

app.register_blueprint(accounts_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(security_bp)


