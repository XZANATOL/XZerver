from wtforms.validators import DataRequired, Optional, Email, Length, ValidationError
from wtforms import StringField, EmailField, PasswordField, BooleanField

from XZerver.forms import CSRFSessionBaseForm

class UserFrom(CSRFSessionBaseForm):
	name = StringField(
			validators = [ DataRequired(), Length(min=4, max=100, message="Must be > 4 & < 100.") ],
			render_kw = {"placeholder": "ex: oblivion69"}
		)
	email = EmailField(
			validators = [ DataRequired(), Email(), Length(max=100, message="Must be < 100.") ],
			render_kw = {"placeholder": "ex: oblivion69@gmail.com"}
		)
	password = PasswordField(
			validators = [ DataRequired(), Length(min=8, message="Minumum length is 8.") ],
			render_kw = {"placeholder": "********"}
		)
	is_active = BooleanField(label="is_active", default='checked')
	is_admin = BooleanField(label="is_admin")


class UserFromEdit(CSRFSessionBaseForm):
	name = StringField(
			validators = [ DataRequired(), Length(min=4, max=100, message="Must be > 4 & < 100.") ],
			render_kw = {"placeholder": "ex: oblivion69"}
		)
	email = EmailField(
			validators = [ DataRequired(), Email(), Length(max=100, message="Must be < 100.") ],
			render_kw = {"placeholder": "ex: oblivion69@gmail.com"}
		)
	password = PasswordField(
			validators = [ Length(min=8, message="Minumum length is 8.") ],
			render_kw = {"placeholder": "********"}
		)
	is_active = BooleanField(label="is_active", default='checked')
	is_admin = BooleanField(label="is_admin")
