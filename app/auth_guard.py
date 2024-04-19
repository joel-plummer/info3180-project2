import jwt
from datetime import datetime, timedelta
from flask import jsonify
from app.config import Config

# Configuration
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = 'HS256'
TOKEN_EXPIRATION_DAYS = 1

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=TOKEN_EXPIRATION_DAYS),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        return str(e)

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def auth_required(func):
    """Decorator to protect routes."""
    from functools import wraps
    from flask import request
    
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing.'}), 403
        else:
            response = decode_auth_token(token)
            if isinstance(response, str):
                return jsonify({'message': response}), 401
            # Pass user_id to the route if needed
            return func(*args, **kwargs, user_id=response)
    return decorated_function
