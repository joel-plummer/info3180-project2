"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import datetime
from app import app
from flask import render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload
from app.models import *


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'email', 'password', 'firstname', 'lastname']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing data'}), 400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'User already exists'}), 409

    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        firstname=data['firstname'],
        lastname=data['lastname'],
        location=data.get('location', ''),
        biography=data.get('biography', ''),
        profile_photo=data.get('profile_photo', ''),
        joined_on=datetime.datetime.now()
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

"""Used for adding posts to the user's feed"""
@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
def add_post(user_id):
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo part'}), 400
    photo = request.files['photo']
    
    caption = request.form.get('caption')
    if not caption:
        return jsonify({'error': 'No caption provided'}), 400

    photo_path, error = save_upload_file(photo, app.config['UPLOAD_FOLDER'])
    if error:
        return jsonify({'error': error}), 400

    new_post = create_post(caption, photo_path, user_id)
    return jsonify({
        'message': 'Post created successfully',
        'post': {
            'id': new_post.id,
            'caption': new_post.caption,
            'photo': new_post.photo,
            'created_on': new_post.created_on.isoformat()
        }
    }), 201
    
"""return a user's posts"""
@app.route('/api/v1/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    if request.method == 'GET':
        get_current_user(user_id)
        posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_on.desc()).all()
        posts_data = [{
            'id': post.id,
            'caption': post.caption,
            'photo': post.photo,
            'created_on': post.created_on.strftime('%Y-%m-%d %H:%M:%S')
        } for post in posts]
        if posts_data == []:
            return jsonify({'message': 'No posts found'}), 404
        return jsonify(posts_data), 200

"""return all posts for all users"""
@app.route('/api/v1/posts', methods=['GET'])
def get_all_posts():
    try:
        posts = Post.query.options(joinedload(Post.user)).order_by(Post.created_on.desc()).all()
        posts_data = [{
            'post_id': post.id,
            'caption': post.caption,
            'photo_url': post.photo,
            'created_on': post.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': post.user_id,
            'username': post.user.username  
        } for post in posts]
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({'error': 'Unable to fetch posts', 'message': str(e)}), 500

###
# The functions below should be applicable to all Flask apps.
###
def save_upload_file(file, upload_folder):
    if file.filename == '':
        return None, 'No selected photo'
    if not allowed_file(file.filename):
        return None, 'File type not allowed'
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filepath, None

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_post(caption, photo_path, user_id):
    new_post = Post(
        caption=caption,
        photo=photo_path,
        user_id=user_id,
        created_on=datetime.datetime.utcnow()
    )
    db.session.add(new_post)
    db.session.commit()
    return new_post

def get_current_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return user

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404