from flask import request, make_response
from functools import wraps

# Authentication configuration
USERNAME = "admin"
PASSWORD = "password123"

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
        return f(*args, **kwargs)
    return decorated
