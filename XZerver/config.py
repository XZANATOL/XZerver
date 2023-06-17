from flask_sqlalchemy import SQLAlchemy

def init():
	global db, admn_pnl_mdl_reg
	db = SQLAlchemy()
	admn_pnl_mdl_reg = {}