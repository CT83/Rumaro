from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import Length, DataRequired


class ChangePasswordForm(FlaskForm):
    existing_password = PasswordField('Existing Password', validators=[DataRequired(), Length(max=150)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(max=150)])
    confirm_new_password = PasswordField('Re-enter New Password', validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Change Password")
