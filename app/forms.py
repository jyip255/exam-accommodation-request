from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField, TextField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional
from wtforms.widgets import TextArea

EXAM_TYPE_CHOICES = [('','---'), ('Midterm', 'Midterm'), ('Final', 'Final')]
EXAM_FORMAT_CHOICES = [('','---'), ('Paper', 'Paper'), ('Online', 'Online')]
CSD_EXAM_CAMPUS = [('','---'), ('Storrs','Storrs'),('Avery Point','Avery Point'),('Hartford','Hartford'),('Waterbury','Waterbury'),('Stamford','Stamford'),('Torrington','Torrington'),('Health Center','Health Center'),('Law School','Law School')]

# Form example (see views.py for implementation)
class StudentForm(FlaskForm):
    searchStudents = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search Students by Name')

# Form for adding request to the database
class AddForm(FlaskForm):
    student_id = StringField(label='Student PeopleSoft ID', validators=[DataRequired(), Length(7,7,"PeopleSoft ID must be 7 digits long")])
    student_netid = StringField(label='Student Net ID', validators=[DataRequired(), Length(8,8,"Net ID must have 3 letters followed by 5 numbers (e.g. abc12345)")])
    student_name = StringField(label='Student Name', validators=[DataRequired()])
    course_id = StringField(label='Course ID', validators=[DataRequired()])    
    course_name = StringField(label='Course Name', validators=[DataRequired()])
    exam_type = SelectField(label='Exam Type', validators=[DataRequired()], choices=EXAM_TYPE_CHOICES)
    exam_format = SelectField(label='Exam Format', validators=[DataRequired()], choices=EXAM_FORMAT_CHOICES)
    exam_time = DateTimeField(label='Original Exam Time', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    exam_csd_time = DateTimeField(label='CSD Exam Time', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    csd_campus = SelectField(label='CSD Exam Campus', validators=[DataRequired()], choices=CSD_EXAM_CAMPUS)
    csd_building = StringField(label='CSD Exam Building', validators=[DataRequired()])
    csd_room = StringField(label='CSD Exam Room', validators=[DataRequired()])
    csd_seat = IntegerField(label='CSD Exam Seat', validators=[DataRequired()])
    instructor_netid = StringField(label='Instructor Net ID', validators=[DataRequired(), Length(8,8,"Net ID must have 3 letters followed by 5 numbers (e.g. abc12345)")])
    instructor_name = StringField(label='Instructor Name', validators=[DataRequired()])
    instructor_phone = StringField(label='Instructor Phone Number', validators=[Optional(), Length(10,10,"Phone number must be 10 digits long")])
    instructor_email = StringField(label='Instructor Email Address', validators=[Optional(), Email()])
    material = TextAreaField(label='Exam Material', widget=TextArea())
    accommodations = TextAreaField(label='Exam Accommodations', widget=TextArea(), validators=[DataRequired()])
    instructor_notes = TextAreaField(label='Instructor Notes', widget=TextArea())
    submit = SubmitField('Submit')