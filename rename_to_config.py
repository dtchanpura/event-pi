import os
import app
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '123456790'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = False

MAIL_SERVER = 'smtp.example.com'
MAIL_PORT = 25
MAIL_USERNAME = 'you@example.com'
MAIL_PASSWORD = 'mysecretpassword'
DEFAULT_MAIL_SENDER = 'defaultsender@example.com'

#MAIL_SERVER = 'localhost'
#MAIL_PORT = 1025
#MAIL_USERNAME = 'rpi@local.com'
#MAIL_PASSWORD = ''

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['csv'])
