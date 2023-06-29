from XZerver.server_start import create_server

def test_config():
	server = create_server()
	assert not server.testing
	server.config.update(TESTING=True)
	assert server.testing


def test_home(client):
	res = client.get("/")
	assert res.status == "200 OK"
