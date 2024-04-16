"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import datetime
from app import app
from flask import render_template, request, jsonify, send_file,send_from_directory
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
from app.models import *
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import login_manager
from app.forms import RegisterForm, LoginForm, PostForm
from flask_wtf.csrf import generate_csrf
import jwt
from functools import wraps


###
# Routing for your application.
###

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

"""register user"""

@app.route('/api/v1/register', methods=['POST'])
def register():
    form=RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        location = form.location.data
        biography = form.biography.data
        profile_photo = form.profile_photo.data
        filename=secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        possible_duplicate_fields = ['username', 'email']
        duplicate_fields = []
        
        for user in User.query.all():
            for field in possible_duplicate_fields:
                if getattr(user, field) == locals()[field]:
                    duplicate_fields.append(f"That {field} already exists")
        
        if len(duplicate_fields) > 0:
            return jsonify({'errors': duplicate_fields})
        
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            firstname=firstname,
            lastname=lastname,
            location=location,
            biography=biography,
            profile_photo=filename,
        )
        db.session.add(new_user)
        db.session.commit()
        joined_on= new_user.joined_on
        return jsonify({
            'message': 'User registered successfully',
            'username': username,
            'email': email,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
            'location': location,
            'biography': biography,
            'profile_photo': filename,
            'joined_on': joined_on
        })
    return jsonify({'errors': form_errors(form)})

    # data = request.get_json()
    
    # possible_missing_fields = ['username', 'password', 'firstname', 'lastname', 'email', 'location', 'biography', 'profile_photo']
    # missing_fields = [f"The {field} field is missing" for field in possible_missing_fields if not data.get(field)]

    # if len(missing_fields) > 0:
    #     return jsonify({'errors': missing_fields}), 400
    

    # new_user = User(
    #     username=data['username'],
    #     email=data['email'],
    #     password=generate_password_hash(data['password']),
    #     firstname=data['firstname'],
    #     lastname=data['lastname'],
    #     location=data.get('location', ''),
    #     biography=data.get('biography', ''),
    #     profile_photo=data.get('profile_photo', ''),
    #     joined_on=datetime.datetime.now()
    # )

    # db.session.add(new_user)

    # try:
    #     db.session.commit()
    #     return jsonify({'message': 'User registered successfully'}), 201
    # except Exception as e:
    #     db.session.rollback()
    #     return jsonify({'errors': [str(e)]}), 500

"""login user"""
@app.route('/api/v1/auth/login', methods=['POST'])
def login():

    # data = request.get_json()
    
    # possible_missing_fields = ['username', 'password']
    # missing_fields = [f"The {field} field is missing" for field in possible_missing_fields if not data.get(field)]

    # if len(missing_fields) > 0:
    #     return jsonify({'errors': missing_fields}), 400
    
    # username = data.get('username')
    # password = data.get('password')
    form=LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

    # if user and check_password_hash(user.password, password):
    #     login_user(user)
    #     return jsonify({'message': 'Logged in successfully'}), 200
    # else:
    #     return jsonify({'error': 'Invalid username or password'}), 401
        errors=[]

        if(not user):
            errors.append("User not found")
            return jsonify({'errors': errors})
        if(not(check_password_hash(user.password, password))):
            errors.append("Invalid password")
            return jsonify({'errors': errors})
        data = {}
        data['id'] = user.id
        data['username'] = user.username
        token = jwt.encode(data, app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({
            "message": "User successfully logged in",
            "token": token
        })

@app.route('/api/v1/users/', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'firstname': current_user.firstname,
        'lastname': current_user.lastname,
        'location': current_user.location,
        'biography': current_user.biography,
        'profile_photo': current_user.profile_photo,
        'joined_on': current_user.joined_on
    })


@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

"""Used to get current user's info"""
@app.route("/api/v1/users/<userId>", methods=["GET"])
def get_user(userId):
    print(userId)
    if (userId == "id"):
        print("booo" + userId)
        token = request.headers["Authorization"].split(" ")[1]
        user = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        userId = user['id']
    user = User.query.filter_by(id=userId).first()
    if (not user):
        return jsonify({
            "error": "user not found"
        }), 404
    return jsonify({
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "location": user.location,
            "biography": user.biography,
            "profile_photo": "/api/v1/photo/" + user.profile_photo,
            "joined_on": user.joined_on
        }), 200

"""To get an image"""
@app.route("/api/v1/photo/<filename>", methods=['GET'])
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

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


"""Used for adding posts to the user's feed"""
@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@login_required
def add_post(user_id):
    form=PostForm()
    user=User.query.filter_by(id=user_id).first()
    errors=[]
    if not user:
        errors.append("User not found")
        return jsonify({'errors': errors})
    if request.method == 'POST' and form.validate_on_submit():
        photo = form.photo.data
        caption = form.caption.data
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_post = Post(
            caption=caption,
            photo=filename,
            user=user,
            created_on=datetime.datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({
            'message': 'Post created successfully',
            'post': {
                'id': new_post.id,
                'caption': new_post.caption,
                'photo': new_post.photo,
                'created_on': new_post.created_on.isoformat()
            }
        })
    return jsonify({'errors': form_errors(form)})
    # if 'photo' not in request.files:
    #     return jsonify({'error': 'No photo part'}), 400
    # photo = request.files['photo']
    
    # caption = request.form.get('caption')
    # if not caption:
    #     return jsonify({'error': 'No caption provided'}), 400

    # photo_path, error = save_upload_file(photo, app.config['UPLOAD_FOLDER'])
    # if error:
    #     return jsonify({'error': error}), 400

    # new_post = create_post(caption, photo_path, user_id)
    # return jsonify({
    #     'message': 'Post created successfully',
    #     'post': {
    #         'id': new_post.id,
    #         'caption': new_post.caption,
    #         'photo': new_post.photo,
    #         'created_on': new_post.created_on.isoformat()
    #     }
    # }), 201
    
"""return a user's posts"""
@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
@login_required
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
@login_required
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

    # Check if the current user is already following the target user
    existing_follow = Follow.query.filter_by(follower_id=current_user.id, user_id=user_id).first()
    if existing_follow:
        return jsonify({'message': 'Already following this user'}), 409

    # Create a new follow relationship
    new_follow = Follow(follower_id=current_user.id, user_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({'message': 'You are now following {}'.format(target_user.username)}), 201

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

