from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, FileField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

class MemoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    story = TextAreaField('Story', validators=[DataRequired()])
    event_date = DateField('Date of Event', format='%Y-%m-%d', validators=[DataRequired()])
    
    # Use the correct file validators instead of Regexp
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Images only!')
    ])
    
    submit = SubmitField('Add Memory')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')