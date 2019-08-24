import os

os.environ.setdefault('LC_TIME', 'en_GB')

SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
DEBUG = False
BABEL_DEFAULT_LOCALE = 'UTC'
SESSION_TYPE = 'filesystem'
WTF_CSRF_SECRET_KEY = "powerful secretkey"

SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

DATA_FOLDER = 'data'
TEMP_FOLDER = 'temp'

MAX_POSTS_TO_ANALYSE = 500
ENABLE_DEEP_FASHION = True

# Used for sending client messages
INSTAGRAM_USERNAME = os.environ.get('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.environ.get('INSTAGRAM_PASSWORD')

DEEPFASHION_API_KEY = os.environ.get('DEEPFASHION_API_KEY')

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_EMAIL = 'contact@example.com'

ON_PROD = False
ON_DEV = False
ON_TEST = False
