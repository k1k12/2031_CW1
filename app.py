# Imports
from config import app, conditions
from flask import render_template, request
import re
# Load webpage 'index' into browser
@app.route('/')
def index():
    return render_template('home/index.html')

# Handle error 400 (bad request)
@app.errorhandler(400)
def error_handler(e):
    return render_template('errors/error400.html'), 400

# Handle error 403 (forbidden)
@app.errorhandler(403)
def error_handler(e):
    return render_template('errors/error403.html'), 403

# Handle error 404 (not found)
@app.errorhandler(404)
def error_handler(e):
    return render_template('errors/error404.html'), 404

# Handle error 429 (too many requests)
@app.errorhandler(429)
def error_handler(e):
    return render_template('errors/error429.html'), 429

# Handle error 500 (internal server)
@app.errorhandler(500)
def error_handler(e):
    return render_template('errors/error500.html'), 500

# Handle error 501 (not implemented)
@app.errorhandler(501)
def error_handler(e):
    return render_template('errors/error501.html'), 501

# Handle attempted attacks
@app.before_request
def attack_handler():
    for attack_type, attack_pattern in conditions.items():
        if attack_pattern.search(request.path) or attack_pattern.search(request.query_string.decode()):
            return render_template('errors/error_attack.html', label=attack_type)

# Main method
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))