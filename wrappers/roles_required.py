from functools import wraps
from flask_login import current_user
from flask import render_template

def roles_required(*roles):
    def inner_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # If current user not in roles
            if current_user.role not in roles:
                # Render error page
                return render_template('errors/error403.html')
            return f(*args, **kwargs)
        return wrapped
    return inner_decorator