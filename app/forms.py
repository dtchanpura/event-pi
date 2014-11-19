from flask.ext.wtf import Form #, RecaptchaField
from wtforms import TextField, BooleanField, TextAreaField, PasswordField, DateTimeField, IntegerField, FileField
from wtforms.validators import Required, Length, ValidationError, Email
from wtforms.widgets import html_params
from app.models import User, Events
from app import db
import hashlib
from datetime import datetime, timedelta

###
class RegistrationForm(Form):
   #username = TextField(validators = [Required()])
   first_name = TextField()
   last_name = TextField()
   email = TextField(validators = [Email()])

   college_name = TextField('College/Organization')
   #password = fields.PasswordField(validators=[validators.required()])

   def validate_on_submit(self):
      rv = Form.validate(self)
      if not rv:
         return False
      #if db.session.query(User).filter_by(username = self.username.data).count() > 0:
      #   self.username.errors.append('Duplicate username')
      #   return False
      if db.session.query(User).filter_by(email = self.email.data).count() > 0:
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

class NewEventForm(Form):
  event_name = TextField(validators=[Required()])
  address = TextAreaField()
  start_date = DateTimeField(default=datetime.today(), format='%d-%m-%y %H:%M')
  end_date = DateTimeField(default=datetime.today() + timedelta(days = 1), format='%d-%m-%y %H:%M')
  fees = IntegerField()

  def validate_on_submit(self):
    if not Form.validate(self):
      return False
    if self.start_date.data == self.end_date.data and self.start_time.data > self.end_time.data:
      self.fees.errors.append('Start Time is later then End Time')
      return False
    elif self.start_date.data > self.end_date.data:
      self.fees.errors.append('Start Time is later then End Time')
      return False
    else:
      return True

class UserData(Form):
  filehandle = FileField()
  def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
