from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, Regexp
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