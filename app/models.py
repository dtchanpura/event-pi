from app import db

class User(db.Model):
   __tablename__ = 'user'
   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(100))
   last_name = db.Column(db.String(100))
   #username = db.Column(db.String(80), unique=True)
   email = db.Column(db.String(120), unique=True)
   #enrollment = db.Column(db.String(15))     # 00000 for not having enrollment number
   college_name = db.Column(db.String(80))  # College or Organization name
   qr_data = db.Column(db.String(64))
   #log = db.relationship("Logs", backref='user')
   #conn_table = db.relationship('Event-Users', secondary='connection')
   #rsvp = db.Column(db.Boolean)
   # Flask-Login integration
   events_data = db.relationship("EventUsers", backref='user')

   def get_id(self):
      return self.id

   # Required for administrative interface
   def __unicode__(self):
      return self.first_name



class Events(db.Model):
  __tablename__ = 'events'
  id = db.Column(db.Integer, primary_key=True)
  event_name = db.Column(db.String(100))
  address = db.Column(db.String(300))
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)
  # start_time = db.Column(db.Time)
  # end_time = db.Column(db.Time)
  fees = db.Column(db.Integer)
  users_data = db.relationship("EventUsers", backref='events')

  def __init__(self, event_name, address='Online', fees=0):
    self.event_name = event_name
    self.address = address
    self.fees = fees

  def __unicode__(self):
    return self.event_name
  def __str__(self):
    return self.event_name

class EventUsers(db.Model):
  __tablename__ = 'eventusers'
  id = db.Column(db.Integer, primary_key=True)
  event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __init__(self, event_id, user_id):
    self.event_id = event_id
    self.user_id = user_id
