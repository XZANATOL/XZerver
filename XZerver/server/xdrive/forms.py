from wtforms.validators import DataRequired
from wtforms import StringField

from XZerver.forms import CSRFSessionBaseForm, JSONField

class SharedFolderForm(CSRFSessionBaseForm):
	path = StringField(
			validators = [ DataRequired() ],
			render_kw = {"placeholder": "Absolute Path"}
		)
	permissions = JSONField(
			validators = [ DataRequired() ],
			render_kw = {"placeholder": """\{user_id\}: ["read", "write"]"""}
		)
