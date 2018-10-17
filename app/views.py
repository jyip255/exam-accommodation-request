from flask import render_template, request
from app import app, db
from time import localtime, strftime

from app.forms import StudentForm, AddForm
from app.models import Demo3

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # Get student name from form
    form = StudentForm(request.form)
    # Make sure form has valid inputs & is making POST request
    if form.validate_on_submit():
        # Display form input (see console)
        print(form.searchStudents.data)
        # Get all records in Demo3 table (can look up SQLAlchemy commands to filter results, uses Demo3 in models.py)
        students = Demo3.query.all()
        # Initialize list that will contain students where name matches form input
        searchResults = []
        # For each student
        for student in students:
            # Display all info from DB (see console)
            print('<STUDENT_ID:{}, STUDENT_NETID:{}, STUDENT_NAME:{}, COURSE_ID:{}, COURSE_NAME:{}, EXAM_TYPE:{}, EXAM_FORMAT:{}, EXAM_TIME:{}, EXAM_CSD_TIME:{}, CSD_CAMPUS:{}, CSD_BUILDING:{}, CSD_ROOM:{}, CSD_SEAT:{}, INSTRUCTOR_NETID:{}, INSTRUCTOR_NAME:{}, INSTRUCTOR_PHONE:{}, INSTRUCTOR_EMAIL:{}, MATERIAL:{}, ACCOMMODATIONS:{}, INSTRUCTOR_NOTES:{}>'
                .format(student.student_id, student.student_netid, student.student_name,  student.course_id, student.course_name, student.exam_type, student.exam_format, student.exam_time, student.exam_csd_time, student.csd_campus, student.csd_building, student.csd_room, student.csd_seat, student.instructor_netid, student.instructor_name, student.instructor_phone, student.instructor_email, student.material, student.accommodations, student.instructor_notes))
            # Check if student name matches form input
            if student.student_name == form.searchStudents.data:
                # If so, add student to search results
                searchResults.append(student)
            # Send information to index.html to be shown on screen
        return render_template('index.html', form=form, results=searchResults)
    # If form is not validated or is making GET request (not POST), return index.html without results
    return render_template('index.html', form=form)

@app.route('/requestAdd', methods=['GET','POST'])
def add():
    # Get AddForm from forms.py
    form = AddForm(request.form)
    if form.validate_on_submit():
        # Add the new request to the database
        p = Demo3(student_id=form.student_id.data,
            student_netid=form.student_netid.data,
            student_name=form.student_name.data, 
            course_id=form.course_id.data, 
            course_name=form.course_name.data,
            exam_type=form.exam_type.data,
            exam_format=form.exam_format.data,
            exam_time=form.exam_time.data,
            exam_csd_time=form.exam_csd_time.data,
            csd_campus=form.csd_campus.data,
            csd_building=form.csd_building.data,
            csd_room=form.csd_room.data,
            csd_seat=form.csd_seat.data,
            instructor_netid=form.instructor_netid.data,
            instructor_name=form.instructor_name.data,
            instructor_phone=form.instructor_phone.data,
            instructor_email=form.instructor_email.data,
            material=form.material.data,
            accommodations=form.accommodations.data,
            instructor_notes=form.instructor_notes.data)
        db.session.add(p)
        db.session.commit()
        return render_template('requestAdd.html', form=form, msg="Exam request added!")
    return render_template('requestAdd.html', form=form)

@app.route('/requestList', methods=['GET', 'POST'])
def requestList():
    rows = Demo3.query.all()
    return render_template('requestList.html', rows = rows)

@app.route('/print/<netid>', methods=['GET', 'POST'])
def print(netid):
    # May need to change to be based on request id instead of netid after adding primary key (request id) to db
    req = Demo3.query.filter(Demo3.student_netid==netid).first()
    currentTime = strftime("%m/%d/%Y %I:%M %p", localtime())
    return render_template('print.html', req=req, currentTime = currentTime)

