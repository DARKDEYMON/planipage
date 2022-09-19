from .models import *

class PaginasExistentes:
	def __init__(self, get_response):
		self.get_response = get_response
	def __call__(self, request):
		
		request.paginas = Pagina.objects.filter()

		response = self.get_response(request)
		return response
