from werkzeug.wrappers import Request, Response, ResponseStream

class IsAdmin():

	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		request = Request(environ)
		print(request)

		return self.app(environ, start_response)