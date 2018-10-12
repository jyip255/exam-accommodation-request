from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Form example (see views.py for implementation)
class StudentForm(FlaskForm):
    searchStudents = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search Students by Name')

# Form for adding request to the database
class AddForm(FlaskForm):
    sname = StringField('', validators=[DataRequired()])
    sid = StringField('', validators=[DataRequired()])
    netid = StringField('', validators=[DataRequired()])
    cid = StringField('', validators=[DataRequired()])
    cname = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')