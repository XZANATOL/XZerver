from flask_login import UserMixin
from XZerver.filters import JinjaFilers
from XZerver import config

class SharedFolder(UserMixin, JinjaFilers, config.db.Model):
	id = config.db.Column(config.db.Integer, primary_key=True)
	name = config.db.Column(config.db.String(100), nullable=False)
	path = config.db.Column(config.db.String(100), nullable=False)
	permissions = config.db.Column(config.db.JSON())
