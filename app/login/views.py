from functools import wraps

from flask import request, render_template, redirect, url_for, make_response, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import db, login_manager
from app.login import login_blueprint
from app.login.LoginLogManager import LoginLogManager
from app.login.forms.change_password_form import ChangePasswordForm
from .forms.login_form import LoginForm
from .forms.signup_form import SignupForm
from .models.User import User


def admin_login_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            if current_user.role >= 9:
                return fn(*args, **kwargs)
            else:
                return login_manager.unauthorized()

        return decorated_function
    return wrapper

@login_blueprint.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
    form = SignupForm()

    if request.method == 'GET':
        return render_template('login/signup.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                flash("Email address already exists")
                return redirect(url_for('Login.login'))
            else:
                newuser = User(email=form.email.data, password=form.password.data, name=form.name.data,
                               instagram_id=form.instagram_id.data)
                db.session.add(newuser)
                db.session.commit()

                flash("New user created successfully!")
                return redirect(url_for('Login.login'))
        else:
            flash("Form didn't validate")
            return redirect(url_for('Login.login'))


@login_blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if request.method == 'GET':
        return render_template('login/change_password.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            if current_user.validate_password(
                    form.existing_password.data) and form.new_password.data == form.confirm_new_password.data:
                current_user.change_password(str(form.new_password.data))
                db.session.commit()
                flash("Password Changed Successfully!")
                return redirect(url_for('Login.logout'))
            else:
                flash("Ensure that the Existing password is correct and the new passwords match!")
                return redirect(url_for('Login.change_password'))
        else:
            flash("Form didn't validate!")
            return redirect(url_for('Login.change_password'))


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@login_manager.unauthorized_handler
def unauth_handler():
    if request.is_xhr:
        return "True"
    else:
        return redirect(url_for('Login.login'))


def notify_log_login_error(msg="Error! Invalid Credentials."):
    log_manager = LoginLogManager(db, ip_address=request.remote_addr, user=current_user)
    log_manager.log_failed_attempt()
    flash(msg, category="error")


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'GET':
        return render_template('login/login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if user.validate_password(form.password.data):
                    login_user(user)

                    log_manager = LoginLogManager(db, ip_address=request.remote_addr, user=current_user)
                    log_manager.log_logged_in()

                    flash('You were successfully logged in!', category="success")
                    return redirect(url_for('main.index'))
                else:
                    notify_log_login_error()
                    return redirect(url_for('Login.login'))
            else:
                notify_log_login_error()
                return redirect(url_for('Login.login'))
        else:
            notify_log_login_error()
            return redirect(url_for('Login.login'))


@login_blueprint.route("/logout")
@login_required
def logout():
    log_manager = LoginLogManager(db, ip_address=request.remote_addr, user=current_user)
    log_manager.log_logged_out()
    logout_user()

    flash('You were successfully logged out!', category="warning")
    resp = make_response(redirect(url_for('main.index')))
    return resp

