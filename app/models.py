from app import db

# Class/attributes should reflect table name and table attributes
class Demo3(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(120))
    netid = db.Column(db.String(120))
    cid = db.Column(db.String(120), primary_key=True)
    cname = db.Column(db.String(120))
    # Defines how the object prints in console
    def __repr__(self):
        return '<Record for {}>'.format(self.sname)