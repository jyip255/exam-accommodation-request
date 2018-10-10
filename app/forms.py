from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Form example (see views.py for implementation)
class StudentForm(FlaskForm):
    searchStudents = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search Students by Name')