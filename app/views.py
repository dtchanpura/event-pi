from flask import render_template, redirect, url_for, request, flash
from app import app, db, mail
from flask.ext.mail import Message
from forms import RegistrationForm, ResendMail
from app.models import User, Logs
from qrcode import QRCode, ERROR_CORRECT_H, ERROR_CORRECT_L
from hashlib import sha1



@app.route('/')
@app.route('/index')
def index():
   return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
   form = RegistrationForm(request.form)
   if request.method == 'POST' and form.validate_on_submit():
      #user = User(form.first_name.data, form.last_name.data, form.username.data,
      #            form.username.data, form.email.data, form.enrollment.data,
      #            form.college_name.data)
      user = User()
      form.populate_obj(user)
      #user.password = generate_password_hash(user.password)
      user.qr_data = sha1(user.email).hexdigest()

      qr = QRCode(version=10, error_correction=ERROR_CORRECT_H)
      qr.add_data(user.qr_data)
      qr.make() # Generate the QRCode itself
      #im contains a PIL.Image.Image object
      im = qr.make_image()
      # To save it
      im.save("qr.png")
      #db_session.add(user)
      sendmail(user.email)
      db.session.add(user)
      db.session.commit()

      return render_template('register.html',isreg=True)
   return render_template('register.html', form=form, isreg=False)


def sendmail(mail_id):
   msg = Message("Your Attendance QR-Code.",
            recipients=[mail_id],
            sender='cic3@gtu.ac.in',
            html="<p>&nbsp;&nbsp;&nbsp;QR code has been generated please display it near the system while coming. This QR-Code is secret any violation will subject invalidation.</p>"
            )
   with app.open_resource("../qr.png") as fp:
      msg.attach("qr.png", "image/png", fp.read())
   mail.send(msg)

@app.route('/resendmail',methods=['GET','POST'])
def resendmail():
   form = ResendMail(request.form)
   if request.method == 'POST' and form.validate() and form.validate_on_submit():
      qr = QRCode(version=10)
      qr_data = sha1(form.email.data).hexdigest()
      qr.add_data(qr_data)
      qr.make() # Generate the QRCode itself
      #im contains a PIL.Image.Image object
      im = qr.make_image()
      # To save it
      im.save("qr_temp.png")
      msg = Message("Your Attendance QR-Code.",
               recipients=[form.email.data],
               sender='cic3@gtu.ac.in',
               html="<p>&nbsp;&nbsp;&nbsp;QR code has been re-generated please display it near the system while coming.<br><br> If you didn't requested for the new QR-Code please report it to CIC3 </p>"
               )
      with app.open_resource("../qr_temp.png") as fp:
         msg.attach("qr_temp.png", "image/png", fp.read())
      mail.send(msg)
      return render_template('resend.html',issent=True)
   return render_template('resend.html', form=form, issent=False)

@app.route('/adminpanel')
def adminpanel():
   logs=Logs.query.\
      filter(timestamp > datetime.timedelta(days = 2),
         models.Logs.timestamp <= datetime.datetime.today()
         ).all()

   return render_template('admin.html',logs=logs)
