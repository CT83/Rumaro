import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap

from app.shared.models import assets, js, login_manager, db, sess
from app.utils.file_utils import create_uploads_folder, create_dir_if_not_exists


def create_app(testing=False, prod_testing=False, dev=False):
    # App
    app = Flask('DemoApp', static_folder='app/static', template_folder='app/templates')
    app.secret_key = '@!#$!@%$!@#$!@DSA'

    if testing or "ON_TEST" in os.environ:
        app.config.from_pyfile('app/config/test.py')
    elif "ON_DEV" in os.environ or dev:
        print("Running on Dev Environment")
        app.config.from_pyfile('app/config/dev.py')
    else:
        print("Running on Production Environment")
        app.config.from_pyfile('app/config/production.py')

    app.config.from_envvar('APP_CONFIG', silent=True)

    # Assets
    assets.init_app(app)

    # Javascript
    assets.register('js', js)

    create_dir_if_not_exists(app.config['DATA_FOLDER'])
    create_dir_if_not_exists(app.config['TEMP_FOLDER'])
    db.app = app
    db.init_app(app)
    db.create_all()

    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    sess.init_app(app)

    from app.main.deep_learning.models import Photo
    from app.main.deep_learning.models import InstagramUser

    from app.login.views import login_blueprint
    app.register_blueprint(login_blueprint)
    from app.main import main_blueprint
    app.register_blueprint(main_blueprint)

    # Configuring Logging
    logHandler = RotatingFileHandler('info.log',
                                     maxBytes=1000000, backupCount=5)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    logHandler.setFormatter(formatter)
    logHandler.setLevel(logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logHandler)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(logHandler)

    app.logger.info('App Started!')

    print("Loaded App Config:", app.config)
    return app
