from XZerver.server_start import create_server
server = create_server()

from werkzeug.security import generate_password_hash
from XZerver.server.auth.models import User
from XZerver import config

from dotenv import load_dotenv
from os import getenv

load_dotenv()

def make_db(server) -> None:
	with server.app_context():
		config.db.create_all()
		print("[+] Database established.")

def add_admin(server) -> None:
	with server.app_context():
		admin = User(
			name=getenv("db_seed_name"), 
			email=getenv("db_seed_email"), 
			password=generate_password_hash(getenv("db_seed_password")),
			is_active=True,
			is_admin=True
			)
		config.db.session.add(admin)
		config.db.session.commit()

		admin = config.db.get_or_404(User, 1)
		print(f"[+] Admin {admin.name} added.")

make_db(server)
add_admin(server)
