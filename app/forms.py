from flask.ext.wtf import Form #, RecaptchaField
from wtforms import TextField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import Required, Length, ValidationError, Email
from app.models import User, Logs
from app import db
import hashlib
import datetime


class RegistrationForm(Form):
   username = TextField(validators = [Required()])
   email = TextField(validators = [Email()])
   first_name = TextField()
   last_name = TextField()
   enrollment = TextField()
   college_name = TextField()
   #password = fields.PasswordField(validators=[validators.required()])

   def validate_on_submit(self):
      rv = Form.validate(self)
      if not rv:
         return False
      if db.session.query(User).filter_by(username = self.username.data).count() > 0:
         self.username.errors.append('Duplicate username')
         return False
      elif db.session.query(User).filter_by(email = self.email.data).count() > 0:
         self.email.errors.append('Duplicate Email')
         return False
      else:
         return True
class AdminLogin(Form):
   username = TextField(validators = [Required()])
   password = PasswordField(validators = [Required()])
   '''def validate_on_submit(self):
      if not db.session.query(User).filter_by(username = self.username.data).count():
         return False
      else:
         return True'''
   def validate_on_submit(self):
      #Form.Validate()
      return hashlib.sha1(self.password.data).hexdigest()=='a9ee4a53fb4f12777beb4b85792b871fb5c43df0'

   def getMetaData(self):
      return db.session.query(User, Logs).\
         filter(Logs.timestamp > datetime.timedelta(days = 1),
               Logs.timestamp <= datetime.datetime.today()).\
               join(Logs).all()


class ResendMail(Form):
   email = TextField(validators = [Email()])
   #recapt = RecaptchaField()
   def validate_on_submit(self):
      if not db.session.query(User).filter_by(email = self.email.data).count():
         self.email.errors.append('Email not Registered. Check it again...')
         return False
      else:
         return True
