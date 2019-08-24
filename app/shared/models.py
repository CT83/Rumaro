from flask_assets import Environment
from flask_caching import Cache
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from webassets import Bundle

assets = Environment()
js = Bundle('js/*.js', output='gen/packed.js')
db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()
cache = Cache(config={'CACHE_TYPE': 'simple'})
