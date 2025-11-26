from flask_limiter import Limiter
from flask import request, make_response
import uuid

def get_browser_key():
    token = request.cookies.get("client_token")
    if not token:
        token = str(uuid.uuid4())
    return token

rate_limiter = Limiter(key_func=get_browser_key)