from functools import wraps
from flask_login import current_user
from flask import render_template

def roles_required(*roles):
    def inner_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # If current user not in roles
            if not roles[current_user.role]:
                # Render error page
                render_template('errors/error403.html')
                return f(*args, **kwargs)
        return wrapped
    return inner_decorator