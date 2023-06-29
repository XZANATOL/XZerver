from XZerver.server_start import create_server
from XZerver import config

from sqlalchemy.sql import text

def test_login(client):
	res = client.post("/auth/login", data={
			"email": "admin@gmail.com",
			"password": "test"
		})
	assert res.status == "302 FOUND"


"""
Some Notes from flask-login docs for testing:

from flask_login import FlaskLoginClient
server.test_client_class = FlaskLoginClient

def test_request_with_logged_in_user():
    user = User.query.get(1)
    with app.test_client(user=user) as client:
        # This request has user 1 already logged in!
        client.get("/")
"""