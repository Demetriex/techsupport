import os
# application configurations
SECRET_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#database for local = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#database for online = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'saltandpepper'

SECURITY_CONFIRMABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_REGISTERABLE = False
SEND_REGISTER_EMAIL = False

# TEMPLATE PATHS
SECURITY_LOGIN_USER_TEMPLATE = 'custom/login.html'
#SECURITY_REGISTER_USER_TEMPLATE = 'custom/register.html'

# FILE UPLOAD
UPLOAD_FOLDER = 'files/Attachment'

RECAPTCHA_PUBLIC_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
RECAPTCHA_PRIVATE_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#SET TO FALSE TO ENABLE RECAPTCHA
TESTING = False
