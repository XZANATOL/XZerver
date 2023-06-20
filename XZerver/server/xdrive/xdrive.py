from flask import Blueprint
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from XZerver import config

from .models import SharedFolder

xdrive = Blueprint(
	'xdrive', __name__, 
	url_prefix="/xdrive",
	static_folder='static',
	static_url_path='static/',
	template_folder="templates"
	)

@xdrive.route("/")
@login_required
def xdrive_root():
	records = config.db.session.execute(
			text(f"""
				SELECT shared_folder.permissions
				FROM shared_folder, json_each(shared_folder.permissions)
				WHERE json_each.key LIKE '{current_user.id}';""")
		).scalars()
	return "xdrive"