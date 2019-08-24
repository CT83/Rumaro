# noinspection PyUnresolvedReferences
from app.config.base import *

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

DEBUG = False

print("Production Settings Added!")

ON_PROD = True
