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
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
from app.models import *
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import login_manager
from app.forms import RegistrationForm
from app.auth_guard import auth_required, encode_auth_token, decode_auth_token

#csrf content
from flask_wtf.csrf import CSRFProtect
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
csrf = CSRFProtect(app)
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


"""register user with flask-wtf"""
@app.route('/api/v1/register', methods=['POST'])
def register():
    form = RegistrationForm()
    duplicate_errors = duplicate_field_check(['username', 'email'], form)
    if duplicate_errors:
        #return 409 if user already exists
        return jsonify({'errors': duplicate_errors}), 409
    photo = save_upload_file(form.profile_photo.data, app.config['UPLOAD_FOLDER'])
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            location=form.location.data,
            biography=form.biography.data,
            profile_photo=photo,
            joined_on=datetime.datetime.now()
        )
        
        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [str(e)]}), 500
    else:
        return jsonify({'errors': form_errors(form)}), 400

"""get csrf token"""
@app.route('/api/csrf_token', methods=['GET'])
def csrf_token():
    return jsonify({'csrf_token': generate_csrf()}), 200


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    # No longer checking for JSON content type; form data is expected
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'errors': ['Username and password fields are required']}), 400
    
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = encode_auth_token(user.id)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
    
"""Used for adding posts to the user's feed"""
@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
@login_required
def add_post(user_id):
    if not User.query.filter(User.id == user_id).first():
        return jsonify({"errors": ["User not found"]}) 
    
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
@login_required
def get_user_posts(user_id):
    if not User.query.filter(User.id == user_id).first():
        return jsonify({"errors": ["User not found"]}) 
    
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
@login_required
def get_all_posts():
    try:
        posts = Post.query.options(joinedload(Post.user)).order_by(Post.created_on.desc()).all()
        posts_data = [{
            'post_id': post.id,
            'caption': post.caption,
            'photo': post.photo,
            'created_on': post.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': post.user_id,
            'username': post.user.username  
        } for post in posts]
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({'errors': [f"Unable to fetch posts {str(e)}"]}), 500

"""like a post"""
@app.route('/api/v1/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    like_exists = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if like_exists:
        return jsonify({'message': 'User already liked this post'}), 409

    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({'message': 'Post liked successfully'}), 201

@app.route('/api/users/<int:user_id>/follow', methods=['POST'])
@login_required
def follow_user(user_id):
    if current_user.id == user_id:
        return jsonify({'message': 'You cannot follow yourself'}), 400

    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'message': 'Target user not found'}), 404

    existing_follow = Follow.query.filter_by(follower_id=current_user.id, user_id=user_id).first()
    if existing_follow:
        return jsonify({'message': 'Already following this user'}), 409

    new_follow = Follow(follower_id=current_user.id, user_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({'message': 'You are now following {}'.format(target_user.username)}), 201

###
# The functions below should be applicable to all Flask apps.
###
def duplicate_field_check(fields, form):
    errors = []
    for field in fields:
        if User.query.filter_by(**{field: getattr(form, field).data}).first():
            errors.append(f"{field.capitalize()} '{getattr(form, field).data}' already exists")
    return errors

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

