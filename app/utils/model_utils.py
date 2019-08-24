def convert_id_to_name(id):
    from app.login.models.User import User
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
