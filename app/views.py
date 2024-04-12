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

from app.models import *


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

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

    # Create and save the new post
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