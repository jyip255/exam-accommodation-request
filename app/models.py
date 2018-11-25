from app import db
from datetime import datetime

# Class/attributes should reflect table name and table attributes
class Examrequest(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    student_id = db.Column(db.Integer, index=True)
    student_netid = db.Column(db.String(120), index=True)
    student_name = db.Column(db.String(120), index=True)
    course_id = db.Column(db.String(120), index=True)
    course_name = db.Column(db.String(120), index=True)
    exam_type = db.Column(db.String(120), index=True)
    exam_format = db.Column(db.String(120), index=True)
    exam_time = db.Column(db.DateTime(), index=True)
    exam_csd_time = db.Column(db.DateTime(), index=True)
    csd_campus = db.Column(db.String(120), index=True)
    csd_building = db.Column(db.String(120), index=True)
    csd_room = db.Column(db.String(120), index=True)
    csd_seat = db.Column(db.Integer, index=True)
    instructor_netid = db.Column(db.String(120), index=True)
    instructor_name = db.Column(db.String(120), index=True)
    instructor_phone = db.Column(db.Integer, index=True)
    instructor_email = db.Column(db.String(120), index=True)
    material = db.Column(db.String(120), index=True)
    accommodations = db.Column(db.String(120), index=True)
    instructor_notes = db.Column(db.String(120), index=True)
    # Defines how the object prints in console
    def __repr__(self):
        return '<Record for {}>'.format(self.student_name)

class Users(db.Model):
    net_id = db.Column(db.String(120), primary_key=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    psid = db.Column(db.String(120))
    def __repr__(self):
        return '<Record for {}>'.format(self.netid)
