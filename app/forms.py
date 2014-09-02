from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length, ValidationError, Email
from app.models import User
from app import db


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
   
