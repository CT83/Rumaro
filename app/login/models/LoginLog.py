import datetime
import enum

from sqlalchemy import Integer, DateTime

from app import db


class LogEnum(enum.Enum):
    login = "Login"
    logout = "Logout"
    invalid_credentials = "Invalid Credentials"


class LoginLog(db.Model):
    __tablename__ = 'login_log'
    id = db.Column(Integer, primary_key=True)
    date_time = db.Column(DateTime, default=datetime.datetime.utcnow)
    action_type = db.Column('value', db.Enum(LogEnum))
    ip_address = db.Column(db.Text, nullable=False, default="0.0.0.0")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=True)

    def __repr__(self):
        return "{} {} {} {} ".format(self.id, self.date_time, self.action_type, self.user_id)
