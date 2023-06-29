from dotenv import load_dotenv
import tempfile
import os

import pytest
from sqlalchemy.sql import text
from XZerver.server_start import create_server
from XZerver import config

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as file:
	_data_sql = file.read().decode("utf8").split(";")

load_dotenv()

@pytest.fixture
def server():
	db_fd, db_path = tempfile.mkstemp()

	server = create_server({
		# Only necessary config
		"SECRET_KEY": os.getenv("server_secret_key"),
		"TESTING": True,
		"WTF_CSRF_ENABLED": False,
		"SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
		})

	with server.app_context():
		for sql in _data_sql:
			config.db.session.execute(text(f"{sql};"))
		config.db.session.commit()

	yield server

	os.close(db_fd)
	os.unlink(db_path)


@pytest.fixture
def client(server):
	return server.test_client()


@pytest.fixture
def runner(server):
	return server.test_cli_runner()