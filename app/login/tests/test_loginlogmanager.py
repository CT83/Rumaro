import datetime

from app.login.LoginLogManager import LoginLogManager
from app.login.models.LoginLog import LoginLog, LogEnum
from app.login.models.User import User
from app.login.utils import delete_logs

test_user_email = 'test@email.com'
test_user_password = "test@123"


def test_login_logs(client):
    """Make sure that when a user logs in it is recorded in db"""
    from app import db
    date_time = datetime.datetime.utcnow()
    user = User.query.filter_by(email=test_user_email).first()

    delete_logs(db)

    LoginLogManager(db=db, ip_address="0.0.0.0", user=user).log_logged_in(date_time=date_time)

    log = LoginLog.query.filter_by(user_id=user.id).first()

    assert log.date_time == date_time
    assert log.user_id is user.id
    assert log.action_type is LogEnum.login


def test_logout(client):
    """Make sure that when a user logs out in it is recorded in db"""
    from app import db
    date_time = datetime.datetime.utcnow()
    user = User.query.filter_by(email=test_user_email).first()

    delete_logs(db)

    LoginLogManager(db=db, ip_address="0.0.0.0", user=user).log_logged_out(date_time=date_time)

    log = LoginLog.query.filter_by(user_id=user.id).first()

    assert log.date_time == date_time
    assert log.user_id is user.id
    assert log.action_type is LogEnum.logout
