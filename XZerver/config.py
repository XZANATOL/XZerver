from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

def init():
	global db, admn_pnl_mdl_reg, csrf
	db = SQLAlchemy()
	csrf = CSRFProtect()
	admn_pnl_mdl_reg = {}