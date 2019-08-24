from app.login.models.User import User


def convert_id_to_name(id):
    try:
        user = User.query.filter_by(id=id).first()
        return user.name
    except AttributeError as ae:
        return "-"


def convert_action_type_to_str(enum_value):
    if str(enum_value) in 'LogEnum.logout':
        return "Logout"
    elif str(enum_value) in 'LogEnum.login':
        return "Login"
    elif str(enum_value) in 'LogEnum.invalid_credentials':
        return "Failed"
    else:
        return "Undefined"


def delete_users(db):
    User.query.delete()
    db.session.commit()


def delete_logs(db):
    from app.login.models.LoginLog import LoginLog
    LoginLog.query.delete()
    db.session.commit()


def create_admin(db):
    user = User(email='rohansawantct83@gmail.com', password="roh@ns@w@nt",
                name="Rohan Sawant", role=10)
    db.session.add(user)
    db.session.commit()

    print(User.query.all())

