from flask import (
	Blueprint, render_template,
	request, flash
)
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from XZerver import config

xdrive = Blueprint(
	'xdrive', __name__, 
	url_prefix="/xdrive",
	static_folder='static',
	static_url_path='static/',
	template_folder="templates"
	)

@xdrive.route("/", methods=["GET"])
@login_required
def xdrive_root():
	return render_template("app.html")


@xdrive.route("/path", methods=["GET"])
@login_required
def file_explorer():
	"""
	returns directory structure
	{
		"status_code": int,
		"directory": [
			{
				"name": str,
				"type": str,
				"path": str,
				"size": int, 		# None in case of dir
				"dt_modified": str
			}
		]
	}
	"""
	res = {
		"status_code": 200,
		"directory": []
	}
	if request.args.get("path") in ["", None]:
		records = config.db.session.execute(
				text(f"""
					SELECT shared_folder.id, shared_folder.name
					FROM shared_folder, json_each(shared_folder.permissions)
					WHERE json_each.key LIKE '{current_user.id}';""")
			)
		for folder_id, name in records:
			res["directory"].append({
				"name": name,
				"type": "dir",
				"path": folder_id,
				"size": None,
				"dt_modified": "-"
				})

	return res