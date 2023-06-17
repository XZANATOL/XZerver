from flask import Blueprint

xdrive = Blueprint('xdrive', __name__, url_prefix="/xdrive")

@xdrive.route("/")
def xdrive_root():
	return "xdrive"