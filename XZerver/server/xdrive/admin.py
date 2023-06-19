from sqlalchemy import desc
from XZerver import config

def xdrive_admin():
	columns = ["path"]
	folders = config.db.session.execute(
			config.db.select(config.admn_pnl_mdl_reg["xdrive"]["model"])
					.order_by(desc(
						config.admn_pnl_mdl_reg["xdrive"]["model"].id)
					)
		).scalars()
	context = {
		"title": "XDrive",
		"model_columns": columns,
		"records": folders
	}
	return context