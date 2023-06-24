from flask import (
	Blueprint, render_template,
	request, flash
)
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from XZerver import config
from datetime import datetime
import os

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
				"size": str, 		# None in case of dir
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
	else:
		# Sanitizing path before processing to avoid SQL Injection.
		path = request.args.get("path")
		path = path.replace("../", "").replace("..", "").split("/")
		try:
			path_from_db = int(path.pop(0))
			path = "/".join(path)

			absolute_path = config.db.session.execute(
					text(f"""
						SELECT shared_folder.path
						FROM shared_folder, json_each(shared_folder.permissions)
						WHERE json_each.key LIKE '{current_user.id}' AND shared_folder.id = '{path_from_db}';
						""")
				).scalar()
			directory = os.path.join(f"{absolute_path}/{path}")

			directortyItems = next(os.walk(directory))
		except Exception as e:
			print("error:", e)
			res["status_code"] = 404
		else:
			# If try block was successfull
			# Parent Directory
			res["directory"].append({
				"name": "..",
				"type": "dir",
				"path": "..",
				"size": None,
				"dt_modified": None
				})

			# Folders
			for folder in directortyItems[1]:
				res["directory"].append({
					"name": folder,
					"type": "dir",
					"path": folder,
					"size": None,
					"dt_modified": datetime.fromtimestamp(os.path.getmtime(f"{directory}/{folder}"))
					})

			# Files
			for file in directortyItems[2]:
				res["directory"].append({
					"name": file,
					"type": file.split(".")[-1],
					"path": file,
					"size": str(round(os.path.getsize(f"{directory}/{file}")/1024, 2))+" KB",
					"dt_modified": datetime.fromtimestamp(os.path.getmtime(f"{directory}/{file}"))
					})
	return res