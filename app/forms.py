# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])    
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    profile_photo = FileField('Profile Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])

class PostForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    caption = TextAreaField('Caption', validators=[InputRequired()])