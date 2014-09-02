from app import db


class User(db.Model):
   __tablename__ = 'user'
   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(100))
   last_name = db.Column(db.String(100))
   username = db.Column(db.String(80), unique=True)
   email = db.Column(db.String(120), unique=True)
   enrollment = db.Column(db.String(15))     # 00000 for not having enrollment number
   college_name = db.Column(db.String(80))  # College or Organization name
   qr_data = db.Column(db.String(64))
   log = db.relationship("Logs", backref='user')
   # Flask-Login integration
   def get_id(self):
      return self.id

   # Required for administrative interface
   def __unicode__(self):
      return self.username

class Logs(db.Model):
   __tablename__ = 'logs'
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   timestamp = db.Column(db.DateTime)
