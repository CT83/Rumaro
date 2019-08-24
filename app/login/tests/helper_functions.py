def login(client, email, password):
    res = client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)
    return res


def signup(client, name, email, password):
    res = client.post('/signup', data=dict(
        name=name,
        email=email,
        password=password
    ), follow_redirects=True)
    return res


def change_password(client, existing_password, new_password, confirm_new_password):
    res = client.post('/change_password', data=dict(
        existing_password=existing_password,
        new_password=new_password,
        confirm_new_password=confirm_new_password
    ), follow_redirects=True)
    return res


def logout(client):
    return client.get('/logout', follow_redirects=True)