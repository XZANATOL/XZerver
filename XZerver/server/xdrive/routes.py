from flask import (
	Blueprint, render_template, send_file, Response,
	request, flash,
)
from flask_login import current_user, login_required
from sqlalchemy.sql import text
from XZerver import config
from datetime import datetime
from shutil import disk_usage, rmtree
import os

xdrive = Blueprint(
	'xdrive', __name__, 
	url_prefix="/xdrive",
	static_folder='static',
	static_url_path='static/',
	template_folder="templates"
	)

def path_sanitizer(path) -> str:
	""" Sanitizing path before processing to avoid SQL Injection & Path Traversal. """
	try:
		path = path.replace("../", "").replace("..", "").split("/")
		path_from_db = int(path.pop(0))
		path = "/".join(path)

		absolute_path = config.db.session.execute(
				text(f"""
					SELECT shared_folder.path
					FROM shared_folder, json_each(shared_folder.permissions)
					WHERE json_each.key = '{current_user.id}'
						AND shared_folder.id = '{path_from_db}'
					LIMIT 1;
					""")
			).scalar()
		if absolute_path is None:
			directory = ""
		else:
			directory = os.path.join(f"{absolute_path}/{path}")
	except:
		directory = ""
	finally:
		return directory


def user_has_write_privilage(path) -> bool:
	""" Checking if user has write access to the provided path """
	try:
		path_from_db = int(path.replace("../", "").replace("..", "").split("/")[0])
		has_access = config.db.session.execute(
				text(f"""
					SELECT shared_folder.id
					FROM shared_folder, json_each(shared_folder.permissions)
					WHERE json_each.key LIKE '{current_user.id}'
						AND shared_folder.id = '{path_from_db}'
						AND json_each.value LIKE '%"write"%'
					LIMIT 1;
					""")
			).scalar()
		if has_access is None:
			return False
		return True
	except:
		return False

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
		],
		"stats": {
			"usedspace": int,
			"freespace": int
		},
		"write_acess": bool
	}
	"""
	res = {
		"status_code": 200,
		"directory": [],
		"stats": {
			"usedspace": 0,
			"freespace": 0
		},
		"write_access": False
	}
	if request.args.get("path") in ["", None]:
		records = config.db.session.execute(
				text(f"""
					SELECT shared_folder.id, shared_folder.name
					FROM shared_folder, json_each(shared_folder.permissions)
					WHERE json_each.key = '{current_user.id}';""")
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
		path = request.args.get("path")
		directory_abs_path = path_sanitizer(path)
		try:
			if os.path.isdir(directory_abs_path):
				directortyItems = next(os.walk(directory_abs_path))
			else:
				raise ValueError("Invalid Path")
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
					"dt_modified": datetime.fromtimestamp(os.path.getmtime(f"{directory_abs_path}/{folder}"))
					})

			# Files
			for file in directortyItems[2]:
				res["directory"].append({
					"name": file,
					"type": file.split(".")[-1],
					"path": file,
					"size": str(round(os.path.getsize(f"{directory_abs_path}/{file}")/1024, 2))+" KB",
					"dt_modified": datetime.fromtimestamp(os.path.getmtime(f"{directory_abs_path}/{file}"))
					})

			total_bytes, used_bytes, free_bytes = disk_usage(directory_abs_path)
			res["stats"] = {
				"usedspace": round(used_bytes / 1_000_000_000, 2), # for GB
				"freespace": round(free_bytes / 1_000_000_000, 2)
			}
			res["write_access"] = user_has_write_privilage(path)
	return res


@xdrive.route("/download", methods=["GET"])
@login_required
def xdrive_download():
	path = request.args.get("path")
	path = path_sanitizer(path)
	if os.path.isfile(path):
		return send_file(path)
	return Response("Not Found!", status=404)


@xdrive.route("/has_write_access", methods=["GET"])
@login_required
def has_write_access():
	""" 
	* This function was made for the SPA to
	check for write access before sending a file.
	* Same check will be done in the upload view
	to avoid malicious approaches to the API. 
	"""
	path = request.args.get("path")
	return {"access": user_has_write_privilage(path)}


@xdrive.route("/upload", methods=["POST"])
@login_required
@config.csrf.exempt
def xdrive_upload():
	path = request.args.get("path")
	if user_has_write_privilage(path):
		path = path_sanitizer(path)
		if os.path.isdir(path) and "file" in request.files:
			file = request.files.get("file")
			file.save(f"{path}{file.filename}")
			return Response("Success", status=200)
		return Response("Invalid Path", status=404)
	return Response("Not Allowed!", status=405)


@xdrive.route("/new", methods=["POST"])
@login_required
@config.csrf.exempt
def xdrive_new_folder():
	path = request.args.get("path")
	if user_has_write_privilage(path):
		path = path_sanitizer(path)
		if os.path.isdir(path) and request.get_json().get("folder_name"):
			folder_name = request.get_json().get("folder_name")
			os.mkdir(f"{path}{folder_name}")
			return Response("Success", status=200)
		return Response("Invalid Path", status=404)
	return Response("Not Allowed", status=405)


@xdrive.route("/delete", methods=["DELETE"])
@login_required
@config.csrf.exempt
def xdrive_delete():
	path = request.args.get("path")
	try:
		path_root_test = path.split("/")
		path_root_test.pop(0)
		if path_root_test[0] == "":
			raise ValueError("Invalid Path")
	except:
		return Response("Not Allowed!", status=405)
	else:
		if user_has_write_privilage(path):
			path = path_sanitizer(path)
			try:
				if os.path.isfile(path):
					os.remove(path)
				elif os.path.isdir(path):
					rmtree(path)
				return Response("Success", status=204)
			except Exception as e:
				print("Error:", e)
				return Response("Invalid Path", status=404)
		return Response("Not Allowed!", status=405)
