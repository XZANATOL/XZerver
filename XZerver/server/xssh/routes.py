from flask import (
	Blueprint, render_template,
	request
)
from flask_socketio import emit
from XZerver.config import socketio
from .socketio_ssh_rooms import socketio_rooms
from time import sleep

xssh = Blueprint(
	'xssh', __name__, 
	url_prefix="/ssh",
	static_folder='static',
	static_url_path='static/',
	template_folder="templates"
	)

@xssh.route("/", methods=["GET"])
def xssh_root():
	return render_template("ssh_client.html")

@socketio.on("connect", namespace="/ssh")
def connect_handler():
	socketio_rooms.create_room(request.sid)

@socketio.on("disconnect", namespace="/ssh")
def disconnect_handler():
	socketio_rooms.close_room(request.sid)

@socketio.on("ssh_connect", namespace="/ssh")
def ssh_connect(form_data):
	client = socketio_rooms.get_client(request.sid)
	shell = socketio_rooms.get_shell(request.sid)
	client.close()
	if shell:
		shell.close()
	try:
		stat = client.connect(
			form_data["hostname"],
			port=form_data["port"],
			username=form_data["username"],
			password=form_data["password"]
		)
		emit("connection_stat", True, to=request.sid)
		shell = client.invoke_shell()
		emit("ssh_response", shell.recv(5000), to=request.sid)
		socketio_rooms.invoke_shell(request.sid, shell)
	except Exception as err:
		print(err)
		emit("connection_stat", False, to=request.sid)

@socketio.on("ssh_command", namespace="/ssh")
def command_handler(command):
    shell = socketio_rooms.get_shell(request.sid)
    if shell.closed:
    	emit("connection_stat", False, to=request.sid)
    else:
	    shell.send(command)

@socketio.on("screen_updater", namespace="/ssh")
def ssh_updater():
	shell = socketio_rooms.get_shell(request.sid)
	out = shell.recv(10000)
	if shell:
		emit("ssh_response", out, to=request.sid)

@socketio.on_error("/ssh")
def error_handler(err):
	print(err)
