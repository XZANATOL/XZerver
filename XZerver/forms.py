from flask_wtf import FlaskForm
from flask import session
from wtforms.csrf.session import SessionCSRF
from os import urandom

class CSRFSessionBaseForm(FlaskForm):
	class meta:
		csrf = True
		csrf_class = SessionCSRF
		csrf_secret = urandom(16)

		@property
		def csrf_context(self):
			return session
		

