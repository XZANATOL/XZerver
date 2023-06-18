from flask import (
	Blueprint,
	request, flash,
	render_template, redirect, url_for,
	session
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.datastructures import ImmutableMultiDict
from flask_login import login_user, current_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import desc
from XZerver import config

from .models import User
from .forms import UserFromEdit

auth = Blueprint(
	'auth', __name__,
	url_prefix="/auth",
	static_folder='static',
	static_url_path='static/',
	template_folder="templates"
	)
csrf = CSRFProtect()

def isAdmin():
	""" Middleware to check user is admin """
	def Redirect():
		flash("Not an admin user", "auth_error")
		return redirect(url_for("home.home_page"))
	if current_user.is_admin:
		return None # Don't redirect
	return Redirect # redirect


@auth.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("home.home_page"))

	if request.method == "POST":
		email = request.form.get("email")
		password = request.form.get("password")
		next_url = request.args.get("next")

		user = User.query.filter_by(email=email).first()

		if user and check_password_hash(user.password, password):
			login_user(user)
			if next_url:
				return redirect(next_url)
			return redirect(url_for("home.home_page"))
		else:
			flash("Please check your login credentials and try again.", "auth_error")

	return render_template("login.html")


@auth.route("/logout", methods=['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for("auth.login"))


@auth.route("/admin/", methods=['GET'])
@login_required
def admin():
	if isAdmin() is not None:
		return isAdmin()()
	return render_template("admin/admin_panel.html")


@auth.route("/admin/<string:app>/", methods=['GET'])
@login_required
def admin_app(app):
	if isAdmin() is not None:
		return isAdmin()()
	# I'm keeping a monolith structure for now till I'm sure \
	# everything is intact.
	# This section will be split up among other apps in an \
	# admin.py file where an app can has it's own configuration.
	if app == "accounts":
		columns = ["name", "email", "is_active", "is_admin"]
		users = config.db.session.execute(
					config.db.select(User).order_by(desc(User.id))
				).scalars()
		context = {
			"title": "User Accounts",
			"model_columns" : columns,
			"records": users
		}
		return render_template("admin/list_tables.html", **context)
	elif app == "xdrive":
		columns = ["path"]
		folders = config.db.session.execute(
					config.db.select(config.admn_pnl_mdl_reg[app]["model"])
			).scalars()
		context = {
			"title": "XDrive",
			"model_columns": columns,
			"records": folders
		}
		return render_template("admin/list_tables.html", **context)

	return redirect(url_for("auth.admin"))


@auth.route("/admin/<string:app>/create/", methods=['GET', 'POST'])
@login_required
def admin_app_create(app):
	if isAdmin() is not None:
		return isAdmin()()
	if not config.admn_pnl_mdl_reg.get(app):
		return redirect(url_for("auth.admin"))
	app_form = config.admn_pnl_mdl_reg[app]["form"]
	form = app_form(meta={'csrf_context': session})

	if request.method == "POST":
		post_form = request.form.to_dict(flat=False)	
		del post_form["csrf_token"]

		# In case of a user form
		if post_form.get("password"):
			post_form["password"] = [generate_password_hash(post_form["password"][0])]
		post_form = ImmutableMultiDict(post_form)

		form = app_form(post_form)
		if form.validate():
			record = config.admn_pnl_mdl_reg[app]["model"]()
			form.populate_obj(record)

		try:
			config.db.session.add(record)
			config.db.session.commit()
			flash("Record Added", category="success")
			return redirect(url_for("auth.admin_app", app=app))
		except Exception as e:
			flash(f"Couldn't Commit {e}", category="error")
			form = app_form(request.form, meta={'csrf_context': session})

	context = {
		"title": app,
		"form": form
		}

	return render_template("admin/list_form.html", **context)


@auth.route("/admin/<string:app>/<int:item_id>/delete", methods=['DELETE'])
@login_required
def admin_app_delete(app, item_id):
	if isAdmin() is not None:
		return isAdmin()()
	response = {
			"response": "Sucess",
			"status": 200,
			"mimetype": "application/json"
		}

	if not config.admn_pnl_mdl_reg.get(app):
		response["status"] = 404
		response["response"] = "App not found"
		return response

	record = config.admn_pnl_mdl_reg[app]["model"]()
	item = record.query.filter_by(id=item_id).first()

	if not item:
		response["status"] = 404
		response["response"] = "Item not found"
		return response

	config.db.session.delete(item)
	config.db.session.commit()
	return response


@auth.route("/admin/<string:app>/<int:item_id>/", methods=['GET', 'POST'])
@login_required
def admin_app_edit(app, item_id):
	if isAdmin() is not None:
		return isAdmin()()
	if not config.admn_pnl_mdl_reg.get(app):
		return redirect(url_for("auth.admin"))

	item = config.admn_pnl_mdl_reg[app]["model"]
	item = item.query.get_or_404(item_id)

	if app == "accounts":
		app_form = UserFromEdit
	else:
		app_form = config.admn_pnl_mdl_reg[app]["form"]

	form = app_form(obj=item, meta={'csrf_context': session})

	if request.method == "POST":
		post_form = request.form.to_dict(flat=False)	
		del post_form["csrf_token"]

		# In case of a user form
		if post_form.get("password"):
			if post_form["password"][0] == "":
				post_form["password"] = item.password
			else:
				post_form["password"] = [generate_password_hash(post_form["password"][0])]
		post_form = ImmutableMultiDict(post_form)

		form = app_form(post_form)
		if form.validate():
			form.populate_obj(item)

		try:
			config.db.session.add(item)
			config.db.session.commit()
			flash("Record Added", category="success")
			return redirect(url_for("auth.admin_app", app=app))
		except Exception as e:
			flash(f"Couldn't Commit: {e}", category="error")
			form = app_form(request.form, meta={'csrf_context': session})

	context = {
		"title": app,
		"form": form
		}

	return render_template("admin/list_form.html", **context)