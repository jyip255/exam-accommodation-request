from flask import render_template, request, abort, redirect, url_for
from app import app, db
from time import localtime, strftime
from flask_cas import login_required
from werkzeug import secure_filename
import os
from . import cas
from pdf2image import convert_from_path
import os

from app.forms import StudentForm, AddForm, FileForm
from app.models import Users, Examrequest

# QR code additions
import pyqrcode
import png
from PIL import Image
import pyzbar.pyzbar as pyzbar

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS=set(['pdf','jpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick fix for uploading to show QR Code
from flask_uploads import UploadSet, configure_uploads, IMAGES
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required

def index():
    if Users.query.filter_by(net_id=cas.username).all()==[]:
        abort(403)
    # Get student name from form
    form = StudentForm(request.form)
    # Make sure form has valid inputs & is making POST request
    if form.validate_on_submit():
        # Display form input (see console)
        print(form.searchStudents.data)
        # Get all records in Examrequest table (can look up SQLAlchemy commands to filter results, uses Examrequest in models.py)
        students = Examrequest.query.all()
        # Initialize list that will contain students where name matches form input
        searchResults = []
        # For each student
        for student in students:
            # Display all info from DB (see console)
            print('ID:{}, STUDENT_ID:{}, STUDENT_NETID:{}, STUDENT_NAME:{}, COURSE_ID:{}, COURSE_NAME:{}, EXAM_TYPE:{}, EXAM_FORMAT:{}, EXAM_TIME:{}, EXAM_CSD_TIME:{}, CSD_CAMPUS:{}, CSD_BUILDING:{}, CSD_ROOM:{}, CSD_SEAT:{}, INSTRUCTOR_NETID:{}, INSTRUCTOR_NAME:{}, INSTRUCTOR_PHONE:{}, INSTRUCTOR_EMAIL:{}, MATERIAL:{}, ACCOMMODATIONS:{}, INSTRUCTOR_NOTES:{}>'
                .format(student.id, student.student_id, student.student_netid, student.student_name,  student.course_id, student.course_name, student.exam_type, student.exam_format, student.exam_time, student.exam_csd_time, student.csd_campus, student.csd_building, student.csd_room, student.csd_seat, student.instructor_netid, student.instructor_name, student.instructor_phone, student.instructor_email, student.material, student.accommodations, student.instructor_notes))
            # Check if student name matches form input
            if student.student_name == form.searchStudents.data:
                # If so, add student to search results
                searchResults.append(student)
            # Send information to index.html to be shown on screen
        return render_template('index.html', form=form, results=searchResults)
    # If form is not validated or is making GET request (not POST), return index.html without results
    return render_template('index.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
@app.route('/requestAdd', methods=['GET','POST'])
def add():
    # Get AddForm from forms.py
    form = AddForm(request.form)
    if form.validate_on_submit():
        # Add the new request to the database
        p = Examrequest(student_id=form.student_id.data,
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
    rows = Examrequest.query.all()
    return render_template('requestList.html', rows = rows)

@app.route('/print/<netid>', methods=['GET', 'POST'])
def print(netid):
    # May need to change to be based on request id instead of netid after adding primary key (request id) to db
    req = Examrequest.query.filter(Examrequest.student_netid==netid).first()
    currentTime = strftime("%m/%d/%Y %I:%M %p", localtime())
    filename = "./app/static/qrcodes/"+netid+".png"
    qr = pyqrcode.create("yourapp.uconn.edu/exam_requests/"+netid)
    qr.png(filename, scale=4)
    return render_template('print.html', req=req, currentTime = currentTime, filename="qrcodes/"+netid+".png")

# Quick fix for uploading to show QR Code
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        filename = 'app/static/uploads/'+filename
        decodedImg = pyzbar.decode(Image.open(filename))[0].data.decode("utf-8")
        return render_template('upload.html', msg="The QR code reads: "+decodedImg)
    return render_template('upload.html')

@app.route('/uploadPdf', methods=['GET', 'POST'])
def uploadPdf():
    target = os.path.join(APP_ROOT, 'static/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            notypename = filename[:-4]

            pages = convert_from_path(filename, 500)

            i = 1
            for page in pages:
                destination = "/".join([target, notypename + str(i) + ".jpg"])
                page.save(destination)
                i+=1

            return render_template('complete.html', image_name=notypename+str(1)+".jpg")

            #destination = "/".join([target, tojpg + ".jpg"])
            #file.save(destination)
        else:
            return render_template('uploadPdfError.html')
    return render_template('uploadPdf.html')

@app.route('/uploadSpecific/<netid>', methods=['GET', 'POST'])
def uploadSpecific(netid):
    target = os.path.join(APP_ROOT, 'images/')
    for file in request.files.getlist("file"):
        if allowed_file(file.filename):
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)
            updatedRequest = Examrequest.query.filter(Examrequest.student_netid==netid).first()
            updatedRequest.has_file="True"
            updatedRequest.file_path=filename
            db.session.commit()
            return render_template('uploadSuccess.html', filename=filename)
        else:
            return render_template('uploadPdfError.html')

@app.route('/requestListHasFile', methods=['GET', 'POST'])
def requestListHasFile():
    rows = Examrequest.query.filter(Examrequest.has_file=="True")
    return render_template('requestList.html', rows = rows)

@app.route('/requestListNoFile', methods=['GET', 'POST'])
def requestListNoFile():
    rows = Examrequest.query.filter(Examrequest.has_file == None)
    return render_template('requestList.html', rows = rows)
