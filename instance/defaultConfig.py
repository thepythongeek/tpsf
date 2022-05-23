import os

SECRET_KEY = 'ghjbj'

UPLOADS = os.path.join('app/static', 'uploads')
DOCUMENTS = os.path.join('app/static/uploads', 'documents')
ALLOWED_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx', 'doc', 'mp4'}
CONFIRMATION_LINK_EXPIRATION_TIME = 300
MAX_CONTENT_LENGTH = 100 * 1000 * 1000

# sqlalchemy configuration parameters
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mkoani2021@localhost/tpsf"
SQLALCHEMY_ECHO = True