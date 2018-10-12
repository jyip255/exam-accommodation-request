from flask import render_template, request
from app import app, db

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
            print('<SID:{}, SNAME:{}, NETID:{}, CID:{}, CNAME:{}>'.format(student.sid, student.sname, student.netid, student.cid, student.cname))
            # Check if student name matches form input
            if student.sname == form.searchStudents.data:
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
        p = Demo3(sid=form.sid.data, sname=form.sname.data, netid=form.netid.data, cid=form.cid.data, cname=form.cname.data)
        db.session.add(p)
        db.session.commit()
        return render_template('requestAdd.html', form=form, msg="Exam request added!")
    return render_template('requestAdd.html', form=form)

@app.route('/requestList')
def requestList():
    # Get all records in Demo3 table (can look up SQLAlchemy commands to filter results, uses Demo3 in models.py)
    students = Demo3.query.all()
    # For each student
    for student in students:
        # Display all info from DB (see console)
        print('<SID:{}, SNAME:{}, NETID:{}, CID:{}, CNAME:{}>'.format(student.sid, student.sname, student.netid, student.cid, student.cname))
    # Send information to requestList.html to be shown on screen
    return render_template('requestList.html', rows = students)

