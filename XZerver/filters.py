class JinjaFilers():
	""" Class used to add custom jinja filters """
	def attr(self, prop):
		if hasattr(self, str(prop)):
			return getattr(self, prop)
		return False