import jwt
from datetime import datetime, timedelta
from flask import jsonify, g, request
from functools import wraps
from app.config import Config
from app import app

# Configuration
SECRET_KEY = app.config['SECRET_KEY']
ALGORITHM = 'HS256'
TOKEN_EXPIRATION_DAYS = 1

def encode_auth_token(token_payload):
    try:
      
        payload = {
            'exp': datetime.now() + timedelta(days=TOKEN_EXPIRATION_DAYS),
            'iat': datetime.now(),
            'sub': token_payload["id"],
            'firstname': token_payload["firstname"],
            'lastname': token_payload["lastname"],
            'location': token_payload["location"],
            'biography': token_payload["biography"],
            'profile_photo': token_payload["profile_photo"],
            'joined_on': token_payload["joined_on"]
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        return str(e)

def decode_auth_token(auth_token):
    try:
        token = auth_token.split(" ")[1] if auth_token.startswith('Bearer ') else auth_token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError as e:
        return 'Invalid token. Please log in again.'

def auth_required(func):
    """Decorator to protect routes."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing.'}), 403
        
        user_id = decode_auth_token(token)  
        if isinstance(user_id, str):  
            return jsonify({'message': user_id}), 401
        
        g.user_id = user_id  # Store user_id in Flask's g object, accessible throughout the request
        return func(*args, **kwargs)
    
    return decorated_function
