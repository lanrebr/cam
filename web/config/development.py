import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../data-dev.sqlite')

DEBUG = False
TESTING = False
IGNORE_AUTH = False
DROP_DB = False
SECRET_KEY = 'secret'
SERVER_NAME = 'localhost:5000'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + db_path
SQLALCHEMY_TRACK_MODIFICATIONS=False
MAX_CONTENT_LENGTH = 4*1024*1024*1024
ALLOWED_EXTENSIONS = {'docx'}