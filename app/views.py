from flask import Flask, Response, render_template, request, abort, redirect, url_for
from app import app, db
from time import localtime, strftime
from flask_cas import login_required
from werkzeug import secure_filename
import os
from . import cas
from pdf2image import convert_from_path
import os
import wand.image

from app.forms import StudentForm, AddForm, FileForm
from app.models import Users, Examrequest

# QR code additions
import pyqrcode
import png
from PIL import Image
import pyzbar.pyzbar as pyzbar
import logging

# Date/time additions
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

datepicker(app)

ALLOWED_EXTENSIONS=set(['pdf','jpg'])
DOMAIN_NAME = "https://b8700398.ngrok.io"

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if Users.query.filter_by(net_id=cas.username).all()==[]:
        abort(403)
    form = StudentForm(request.form)
    if form.validate_on_submit():
        print(form.searchStudents.data)
        students = Examrequest.query.all()
        searchResults = []
        for student in students:
            print('ID:{}, STUDENT_ID:{}, STUDENT_NETID:{}, STUDENT_NAME:{}, COURSE_ID:{}, COURSE_NAME:{}, EXAM_TYPE:{}, EXAM_FORMAT:{}, EXAM_TIME:{}, EXAM_CSD_TIME:{}, CSD_CAMPUS:{}, CSD_BUILDING:{}, CSD_ROOM:{}, CSD_SEAT:{}, INSTRUCTOR_NETID:{}, INSTRUCTOR_NAME:{}, INSTRUCTOR_PHONE:{}, INSTRUCTOR_EMAIL:{}, MATERIAL:{}, ACCOMMODATIONS:{}, INSTRUCTOR_NOTES:{}>'
                .format(student.id, student.student_id, student.student_netid, student.student_name,  student.course_id, student.course_name, student.exam_type, student.exam_format, student.exam_time, student.exam_csd_time, student.csd_campus, student.csd_building, student.csd_room, student.csd_seat, student.instructor_netid, student.instructor_name, student.instructor_phone, student.instructor_email, student.material, student.accommodations, student.instructor_notes))
            if student.student_name == form.searchStudents.data:
                searchResults.append(student)
        return render_template('index.html', form=form, results=searchResults)
    return render_template('index.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
@app.route('/requestAdd', methods=['GET','POST'])
@login_required
def add():
    form = AddForm(request.form)
    if form.validate_on_submit():
        p = Examrequest(student_id=form.student_id.data,
            student_netid=form.student_netid.data,
            student_name=form.student_name.data, 
            course_id=form.course_id.data, 
            course_name=form.course_name.data,
            exam_type=form.exam_type.data,
            exam_format=form.exam_format.data,
            date=form.date.data,
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
@login_required
def requestList():
    rows = Examrequest.query.all()
    filterby = 'id'
    return render_template('requestList.html', rows = rows, filterby = filterby)

@app.route('/print/<reqid>', methods=['GET', 'POST'])
def print(reqid):
    req = Examrequest.query.filter(Examrequest.id==reqid).first()
    currentTime = strftime("%m/%d/%Y %I:%M %p", localtime())
    filename = "./app/static/qrcodes/"+reqid+".png"
    qr = pyqrcode.create(DOMAIN_NAME+"/print/"+reqid)
    qr.png(filename, scale=4)
    return render_template('print.html', req=req, currentTime = currentTime, filename="qrcodes/"+reqid+".png")

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    for file in request.files.getlist("file"):
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            notypename = filename[:-4]
            filename = "app/static/uploads/"+filename
            file.save(filename)
            if filename.endswith('.jpg') or filename.endswith('.jpeg'):
                imgfilename = filename
                with wand.image.Image(filename=filename) as img:
                    with img.convert('pdf') as converted:
                        converted.save(filename='app/static/uploads/'+notypename+".pdf")
            if filename.endswith('.pdf'):
                with wand.image.Image(filename=filename) as img:
                    with img.convert('jpg') as converted:
                        converted.save(filename='app/static/uploads/'+notypename+".jpg")
                        imgfilename = 'app/static/uploads/'+notypename+".jpg"
            if pyzbar.decode(Image.open(imgfilename)) != []:
                decodedImg = pyzbar.decode(Image.open(imgfilename))[0].data.decode("utf-8")
                app.logger.warning(decodedImg)
                reqId = decodedImg.split('/')[-1]
            else:
                reqId = "nullexamreq"
            updatedRequest = Examrequest.query.filter(Examrequest.id==reqId).first()
            if reqId == "nullexamreq":
                msg = "QR code not found on image."
                os.remove('app/static/uploads/'+notypename+".pdf")
                os.remove('app/static/uploads/'+notypename+".jpg")
            elif updatedRequest is None:
                msg = "QR code does not match any request ID."
                os.remove('app/static/uploads/'+notypename+".pdf")
                os.remove('app/static/uploads/'+notypename+".jpg")
            else:
                updatedRequest.has_file="True"
                if filename.endswith('.jpg'):
                    filename = 'app/static/uploads/'+notypename+".pdf"
                os.remove('app/static/uploads/'+notypename+".jpg")
                updatedRequest.file_path=filename
                db.session.commit()
                msg = "Added to request "+reqId+" successfully!"
            return render_template('upload.html', msg=msg)
        else:
            return render_template('upload.html', msg="File format not accepted.")
    return render_template('upload.html')

@app.route('/bulkUpload', methods=['GET', 'POST'])
@login_required
def bulkUpload():
    for file in request.files.getlist("file"):
        filepath = "../shared/check/"+file.filename
        file.save(filepath)
    if len(request.files.getlist("file")) > 0:
        return render_template('bulkUpload.html',msg="Upload complete! Changes may take time to load.")
    return render_template('bulkUpload.html')

@app.route('/uploadSpecific/<reqid>', methods=['GET', 'POST'])
@login_required
def uploadSpecific(reqid):
    for file in request.files.getlist("file"):
        if allowed_file(file.filename):
            filename = file.filename
            destination = "app/static/uploads/"+filename
            file.save(destination)
            updatedRequest = Examrequest.query.filter(Examrequest.id==reqid).first()
            updatedRequest.has_file="True"
            updatedRequest.file_path=destination
            db.session.commit()
            return render_template('uploadSuccess.html', filename=filename)
        else:
            return render_template('uploadPdfError.html')

@app.route('/requestListHasFile', methods=['GET', 'POST'])
@login_required
def requestListHasFile():
    rows = Examrequest.query.filter(Examrequest.has_file=="True")
    filterby = 'id'
    return render_template('requestList.html', rows = rows, filterby = filterby)

@app.route('/requestListNoFile', methods=['GET', 'POST'])
@login_required
def requestListNoFile():
    rows = Examrequest.query.filter(Examrequest.has_file == None)
    filterby = 'id'
    return render_template('requestList.html', rows = rows, filterby = filterby)

@app.route('/requestListRequestID', methods=['GET', 'POST'])
@login_required
def requestListRequestID():
    rows = Examrequest.query.all()
    filterby = 'student_name'
    return render_template('requestList.html', rows = rows, filterby = filterby)

@app.route('/requestListPeoplesoftID', methods=['GET', 'POST'])
@login_required
def requestListPeoplesoftID():
    rows = Examrequest.query.all()
    filterby = 'student_id'
    return render_template('requestList.html', rows = rows, filterby = filterby)

@app.route('/requestListStudentNetID', methods=['GET', 'POST'])
@login_required
def requestListStudentNetID():
    rows = Examrequest.query.all()
    filterby = 'student_netid'
    return render_template('requestList.html', rows = rows, filterby = filterby)

@app.route('/requestListStudentName', methods=['GET', 'POST'])
@login_required
def requestListStudentName():
    rows = Examrequest.query.all()
    filterby = 'student_name'
    return render_template('requestList.html', rows = rows, filterby = filterby)

@app.route('/requestListCourseID', methods=['GET', 'POST'])
@login_required
def requestListStudentCourseID():
    rows = Examrequest.query.all()
    filterby = 'course_id'
    return render_template('requestList.html', rows = rows, filterby = filterby)

@app.route('/dateTest', methods=['GET', 'POST'])
@login_required
def dateTest():
    return render_template('dateTest.html')

@app.route('/attach', methods=['POST'])
def addToReqId():
    data = request.get_json()
    filepath = data['filepath']
    reqId = data['reqid']
    updatedRequest = Examrequest.query.filter(Examrequest.id==reqId).first()
    if updatedRequest is None:
        msg = "QR code does not match any request ID."
        return Response(msg, status=404);
    else:
        updatedRequest.has_file="True"
        updatedRequest.file_path=filepath
        db.session.commit()
        msg = "Added to request "+reqId+" successfully!"
        return Response(msg, status=200);
