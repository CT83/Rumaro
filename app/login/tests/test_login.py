from app.login.tests.helper_functions import login, signup, change_password, logout

test_user_email = 'test@email.com'
test_user_password = "test@123"


def test_routes(client):
    res = client.get('/login')
    assert res.status_code is 200

    res = client.get('/logout', follow_redirects=True)
    assert res.status_code is 200


def test_login(client):
    """Make sure login works."""

    rv = login(client, email="wrong@email.com", password=test_user_password)
    assert 'Error! Invalid Credentials.' in str(rv.data)

    rv = login(client, email=test_user_email, password="wrong_password")
    assert 'Error! Invalid Credentials.' in str(rv.data)

    rv = login(client, email=test_user_email, password=test_user_password)
    assert 'You were successfully logged in!' in str(rv.data)

    rv = login(client, email="wrong@email.com", password="wrong_password")
    assert 'Error! Invalid Credentials.' in str(rv.data)


def test_logout(client):
    """Make sure login and logout works."""

    rv = login(client, email=test_user_email, password=test_user_password)
    assert 'You were successfully logged in!' in str(rv.data)

    rv = logout(client)
    assert 'You were successfully logged out!' in str(rv.data)


def test_signup_and_login(client):
    """Make sure signup and login works."""

    new_test_user_name = 'Test User 2'
    new_test_user_email = 'test2@email.com'
    new_test_user_password = "test2@123"

    rv = login(client, email=test_user_email, password=test_user_password)
    assert 'You were successfully logged in!' in str(rv.data)

    rv = signup(client, name=new_test_user_name, email=new_test_user_email, password=new_test_user_password)
    assert 'New user created successfully!' in str(rv.data)

    rv = logout(client)
    assert 'You were successfully logged out!' in str(rv.data)

    rv = login(client, email=new_test_user_email, password=new_test_user_password)
    assert 'You were successfully logged in!' in str(rv.data)

    rv = logout(client)
    assert 'You were successfully logged out!' in str(rv.data)

    # Test with existing email

    rv = login(client, email=test_user_email, password=test_user_password)
    assert 'You were successfully logged in!' in str(rv.data)

    rv = signup(client, name=new_test_user_name, email=test_user_email, password=new_test_user_password)
    assert 'Email address already exists' in str(rv.data)

    rv = logout(client)
    assert 'You were successfully logged out!' in str(rv.data)


def test_simple_change_password(client):
    """Make sure signup and login works."""
    new_password = "new_test_password"
    confirm_new_password = "new_test_password"

    # Test if simple password changing works

    rv = login(client, email=test_user_email, password=test_user_password)
    assert 'You were successfully logged in!' in str(rv.data)

    rv = change_password(client, test_user_password, new_password, confirm_new_password)
    assert 'Password Changed Successfully!' in str(rv.data)

    # Try to login with old password, ensure if fails

    rv = login(client, email=test_user_email, password=test_user_password)
    assert 'Error! Invalid Credentials' in str(rv.data)

    # Try to login with new password

    rv = login(client, email=test_user_email, password=new_password)
    assert 'You were successfully logged in!' in str(rv.data)


def test_change_password_confirm_password(client):
    """Make sure signup and login works."""
    new_password = "new_test_password"
    confirm_new_password = "new_test_password"

    # Test if password changing works, when confirmation passwords are different

    rv = login(client, email=test_user_email, password=test_user_password)
    assert 'You were successfully logged in!' in str(rv.data)

    rv = change_password(client, "wrong_password", new_password, confirm_new_password)
    assert 'Ensure that the Existing password is correct and the new passwords match!' in str(rv.data)

    rv = change_password(client, test_user_password, "wrong_password", confirm_new_password)
    assert 'Ensure that the Existing password is correct and the new passwords match!' in str(rv.data)

    rv = change_password(client, test_user_password, new_password, "wrong_password")
    assert 'Ensure that the Existing password is correct and the new passwords match!' in str(rv.data)

    rv = change_password(client, test_user_password, new_password, confirm_new_password)
    assert 'Password Changed Successfully!' in str(rv.data)
