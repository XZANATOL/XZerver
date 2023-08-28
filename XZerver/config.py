from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO

def init(server):
	global db, admn_pnl_mdl_reg, csrf
	global socketio

	db = SQLAlchemy()
	csrf = CSRFProtect()
	socketio = SocketIO()
	admn_pnl_mdl_reg = {}

	db.init_app(server)
	csrf.init_app(server)
	socketio.init_app(server)		
