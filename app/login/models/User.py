from flask_login import UserMixin
from passlib.hash import bcrypt
from sqlalchemy.orm import backref

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(300), nullable=False)
    name = db.Column(db.Text)
    role = db.Column(db.Integer, default=1)  # Admin is level 10
    logs = db.relationship("LoginLog", backref='user', lazy=True)

    payment = db.Column(db.Boolean, default=False)
    analyzed = db.Column(db.Boolean, default=False)
    instagram_id = db.Column(db.String(100))

    instagram_user_id = db.Column(db.Integer, db.ForeignKey('instagram_user.id'))
    instagram_user = db.relationship("InstagramUser", backref=backref("user", uselist=False))

    def __init__(self, email, password, name, role=1, instagram_id=""):
        self.instagram_id = instagram_id
        self.email = email
        self.password = bcrypt.encrypt(password)
        self.name = name
        self.role = role

    def __repr__(self):
        return '<User {} {} {} {} {} {}>'.format(self.id, self.email, self.password, self.name,
                                                 self.role, self.logs)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)

    def change_password(self, password):
        self.password = bcrypt.encrypt(password)
        return self.password

    def promote_to_admin(self):
        self.role = 10

    def is_admin(self):
        if self.role is not None:
            return self.role >= 10
        else:
            return False
