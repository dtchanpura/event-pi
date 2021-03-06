from flask import render_template, redirect, url_for, request, flash
from app import app, db, mail
from flask.ext.mail import Message
from forms import RegistrationForm, ResendMail, AdminLogin, NewEventForm, UserData
from app.models import User, Events, EventUsers
from qrcode import QRCode, ERROR_CORRECT_H, ERROR_CORRECT_L,ERROR_CORRECT_Q
from hashlib import sha1
from csv import reader
from werkzeug import secure_filename
import os

def sendmail(mail_id):
   msg = Message("Your Attendance QR-Code.",
            recipients=[mail_id],
            sender='abc@123.com',#app.config['DEFAULT_SENDER'],#'cic3@gtu.ac.in',
            html="<p>&nbsp;&nbsp;&nbsp;QR code has been generated please display it near the system while coming. This QR-Code is secret any violation will subject invalidation.</p>"
            )
   with app.open_resource("../qr.png") as fp:
      msg.attach("qr.png", "image/png", fp.read())
   mail.send(msg)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/index')
def index():
   return redirect(url_for('cpanel'))

@app.route('/cpanel')
def cpanel():
  data = db.session.query(Events).all()
  return render_template('cpanel.html',data=data)



@app.route('/addevent', methods=['GET','POST'])
def addevent():
  form = NewEventForm(request.form)
  if request.method == 'POST' and form.validate_on_submit():
     #user = User(form.first_name.data, form.last_name.data, form.username.data,
     #            form.username.data, form.email.data, form.enrollment.data,
     #            form.college_name.data)
     event = Events(form.event_name.data, form.address.data, form.fees.data)
     event.start_date = form.start_date.data
     event.end_date = form.end_date.data

     db.session.add(event)
     db.session.commit()

     return render_template('addevent.html',isadded=True)
  return render_template('addevent.html',form=form, isadded=False)

@app.route('/event/<int:event_id>/')
def eventdetails(event_id=1):
  event = db.session.query(Events).filter_by(id = event_id).all()
  cnt = db.session.query(EventUsers).filter_by(event_id = event_id).count()
  return render_template('eventdetails.html', event_id=event_id, eventdata = event[0],cnt=cnt)

@app.route('/event/<int:event_id>/show_users/')
def show_users(event_id=1):
  #users_id = db.session.query(EventUsers).filter_by(event_id = event_id).all()
  users = db.session.query(EventUsers).filter_by(event_id=event_id).join(User.events_data).all()
  return render_template('show_users.html', event_id=event_id, users_data = users)

@app.route('/event/delete/<int:event_id>/')
def delete_event(event_id):
  event = db.session.query(Events).filter_by(id = event_id).all()
  db.session.delete(event[0])
  db.session.commit()
  return redirect(url_for('cpanel'))

@app.route('/adduser/<int:event_id>/', methods=['GET', 'POST'])
def adduser(event_id=1):
   form = RegistrationForm(request.form)
   eventdata = db.session.query(Events).filter_by(id = event_id).all()
   if request.method == 'POST' and form.validate_on_submit():
      #user = User(form.first_name.data, form.last_name.data, form.username.data,
      #            form.username.data, form.email.data, form.enrollment.data,
      #            form.college_name.data)
      user = User()

      form.populate_obj(user)
      #user.password = generate_password_hash(user.password)
      user.qr_data = sha1(user.email).hexdigest()

      #qr = QRCode(version=10, error_correction=ERROR_CORRECT_H)

      qr = QRCode(
         version=6,
         border=4,
         box_size=5,
         error_correction=ERROR_CORRECT_Q
         )

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
      eu = EventUsers(event_id,user.id)
      db.session.add(eu)
      db.session.commit()
      event_d = db.session.query(Events).filter_by(id = event_id).all()
      cnt = db.session.query(EventUsers).filter_by(event_id = event_id).count()
      return render_template('eventdetails.html', event_id=event_id, eventdata=event_d[0],cnt=cnt)
   return render_template('adduser.html', form=form, isreg=False,event_id=event_id, event=eventdata[0])



@app.route('/adduserdata/<int:event_id>/',methods=['GET','POST'])
def adduserdata(event_id=1):
  form = UserData(request.form)
  if request.method == 'POST':
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uploaded_at=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploaded_at)
        parse_add(uploaded_at,event_id)
        return redirect(url_for('eventdetails',event_id=event_id))
        #render_template('eventdetails.html',event_id=event_id)
        #return redirect(url_for('uploaded_file',
        #                        filename=filename))
  #file=request.files['file']
  #if request.method == 'POST':
  #  parse_add(file.filename,event_id)
  #  return render_template('eventdetails.html',event_id=event_id)
    #redirect(url_for('eventdetails(event_id)'))
  return render_template('adduserdata.html', form=form, event_id=event_id)

def parse_add(datafile, event_id):
  csvFile=open(datafile)
  fileData = reader(csvFile, delimiter=';', quotechar='|')
  for row in fileData:
    user = User()
    user.first_name=row[0]
    user.last_name=row[1]
    user.email=row[2]
    user.college_name=row[3]
    user.qr_data = sha1(user.email).hexdigest()
    #qr = QRCode(version=10, error_correction=ERROR_CORRECT_H)
    qr = QRCode(
       version=6,
       border=4,
       box_size=5,
       error_correction=ERROR_CORRECT_Q
       )

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
    eu = EventUsers(event_id,user.id)
    db.session.add(eu)
    db.session.commit()


@app.route('/adminpanel', methods=['GET','POST'])
def adminpanel():
   form = AdminLogin(request.form)
   if request.method == 'POST' and form.validate_on_submit():
      logs = form.getMetaData()
      return render_template('admin.html',isauth=True, logs=logs)
   return render_template('admin.html',form=form, isauth=False)

@app.route('/nothingsample')
def nothing():
  return render_template('sample.html')

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, format='%d-%m-%Y %H:%M'):
    # date = dateutil.parser.parse(date)
    # native = date.replace(tzinfo=None)
    return date.strftime(format)
