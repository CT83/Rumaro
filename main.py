from flask_migrate import Migrate
from flask_sqlalchemy import Model

from app import create_app, db

app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Model=Model)


@app.cli.command()
def setup_default_users():
    """Create some default users"""
    from app.login.utils import create_admin
    create_admin(db)
