def test_home(client):
    with client.session_transaction(username="1") as session:
        session["us"]
    response = client.get("/index")
    assert b"<title>Redirecting...</title>" in response.data
    """ assert response.status_code == 200 """


""" def test_login(client):
    data = {
        "signin-username": "1", 
        "signin-password": "", 
    }
    response = client.post("/sign-in", data=data)
    print()
    print ("here")
    print (response.headers)
    print()
    assert response.status_code == 200 """

