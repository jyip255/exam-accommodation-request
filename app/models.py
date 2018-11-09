from app import db

# Class/attributes should reflect table name and table attributes
class Demo3(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_netid = db.Column(db.String(120))
    student_name = db.Column(db.String(120))
    course_id = db.Column(db.String(120))
    course_name = db.Column(db.String(120))
    exam_type = db.Column(db.String(120))
    exam_format = db.Column(db.String(120))
    exam_time = db.Column(db.String(120))
    exam_csd_time = db.Column(db.String(120))
    csd_campus = db.Column(db.String(120))
    csd_building = db.Column(db.String(120))
    csd_room = db.Column(db.String(120))
    csd_seat = db.Column(db.String(120))
    instructor_netid = db.Column(db.String(120))
    instructor_name = db.Column(db.String(120))
    instructor_phone = db.Column(db.String(120))
    instructor_email = db.Column(db.String(120))
    material = db.Column(db.String(120))
    accommodations = db.Column(db.String(120))
    instructor_notes = db.Column(db.String(120))
    # Defines how the object prints in console
    def __repr__(self):
        return '<Record for {}>'.format(self.student_name)

class Users(db.Model):
    netid = db.Column(db.String(120), primary_key=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    psid = db.Column(db.String(120))
    def __repr__(self):
        return '<Record for {}>'.format(self.netid)
