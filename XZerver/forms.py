from flask_wtf import FlaskForm
from flask import session
from wtforms.csrf.session import SessionCSRF
from wtforms.fields import TextAreaField

from os import urandom
import json

class CSRFSessionBaseForm(FlaskForm):
	class meta:
		csrf = True
		csrf_class = SessionCSRF
		csrf_secret = urandom(16)

		@property
		def csrf_context(self):
			return session
		

class JSONField(TextAreaField):
	# Modified version of https://gist.github.com/dukebody/dcc371bf286534d546e9
	def _value(self):
		return json.dumps(self.data) if self.data else ""

	def process_formdata(self, valuelist):
		try:
			self.data = json.loads(valuelist[0])
		except ValueError:
			raise ValueError("Invalid JSON")

	def pre_validate(self, form):
		super().pre_validate(form)
		try:
			json.dumps(self.data)
		except TypeError:
			raise ValueError("Invalid JSON")