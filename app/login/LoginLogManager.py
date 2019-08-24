import datetime

from flask_login import current_user

from app.login.models.LoginLog import LoginLog, LogEnum


class LoginLogManager:

    def __init__(self, db, ip_address, user=current_user):
        self.ip_address = ip_address
        self.db = db
        self.user = user

    def log_logged_in(self, date_time=datetime.datetime.utcnow()):
        log = LoginLog(user_id=self.user.id, ip_address=self.ip_address,
                       date_time=date_time, action_type=LogEnum.login)
        self.db.session.add(log)
        self.db.session.commit()

    def log_logged_out(self, date_time=datetime.datetime.utcnow()):
        log = LoginLog(user_id=self.user.id, ip_address=self.ip_address,
                       date_time=date_time,
                       action_type=LogEnum.logout)
        self.db.session.add(log)
        self.db.session.commit()

    def log_failed_attempt(self, date_time=datetime.datetime.utcnow()):
        log = LoginLog(user_id=self.user.get_id(), ip_address=self.ip_address, date_time=date_time,
                       action_type=LogEnum.invalid_credentials)
        self.db.session.add(log)
        self.db.session.commit()
