# noinspection PyUnresolvedReferences
from app.config.base import *

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
TESTING = True
WTF_CSRF_METHODS = []
WTF_CSRF_ENABLED = False

print("Test Settings Added!")

ON_TEST = True
