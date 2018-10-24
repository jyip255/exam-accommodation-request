from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

# Form example (see views.py for implementation)
class StudentForm(FlaskForm):
    searchStudents = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search Students by Name')

# Form for adding request to the database
class AddForm(FlaskForm):
    student_id = StringField('', validators=[DataRequired()])
    student_name = StringField('', validators=[DataRequired()])
    student_netid = StringField('', validators=[DataRequired()])
    course_id = StringField('', validators=[DataRequired()])
    course_name = StringField('', validators=[DataRequired()])
    exam_type = StringField('', validators=[DataRequired()])
    exam_format = StringField('', validators=[DataRequired()])
    exam_time = StringField('', validators=[DataRequired()])
    exam_csd_time = StringField('', validators=[DataRequired()])
    csd_campus = StringField('', validators=[DataRequired()])
    csd_building = StringField('', validators=[DataRequired()])
    csd_room = StringField('', validators=[DataRequired()])
    csd_seat = StringField('', validators=[DataRequired()])
    instructor_netid = StringField('', validators=[DataRequired()])
    instructor_name = StringField('', validators=[DataRequired()])
    instructor_phone = StringField('')
    instructor_email = StringField('')
    material = StringField('')
    accommodations = StringField('', validators=[DataRequired()])
    instructor_notes = StringField('')
    submit = SubmitField('Submit')