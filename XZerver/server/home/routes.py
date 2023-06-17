from flask import (
	Blueprint,
	render_template, url_for
)
from flask_login import current_user


home = Blueprint(
	"home", __name__,
	url_prefix="/",
	static_folder="static",
	static_url_path="static/",
	template_folder="templates"
)

@home.route("/", methods=["GET"])
def home_page():
	return render_template("home.html")