from flask_login import UserMixin
from XZerver.filters import JinjaFilers
from XZerver import config

class User(UserMixin, JinjaFilers, config.db.Model):
	id = config.db.Column(config.db.Integer, primary_key=True)
	email = config.db.Column(config.db.String(100), unique=True, nullable=False)
	password = config.db.Column(config.db.String(105), nullable=False)
	name = config.db.Column(config.db.String(100), nullable=False)
	is_active = config.db.Column(config.db.BOOLEAN(), nullable=False)
	is_admin = config.db.Column(config.db.BOOLEAN(), nullable=False)